

import time 
import requests
import datetime
import calendar
from multisigtables import multisig,escrow_address,user_info
from multisigredeem import redeem_funds
class Multisig_escrow():
    

    def __init__(self):

        
        import dogecoinrpc
        import praw
        from messages_module import Messages_module 
        self.d = dogecoinrpc.connect_to_local()
        self.r = praw.Reddit(user_agent="doge_multisig v0.2 by /u/Doomhammer458")
        self.m = Messages_module()
    def Timestamp(self,_datetime): 
        
        return calendar.timegm(_datetime.timetuple())

    def toTStamp(self,DATETIME):
        stamp = self.Timestamp(DATETIME)
        stamp = str(stamp)
        return stamp
    def fromTStamp(self,stamp):
        date = datetime.datetime.utcfromtimestamp(float(stamp))
        return date
    
    def create_session(self):
        import sqlalchemy as sql
        from sqlalchemy.orm import sessionmaker
        engine = sql.create_engine("sqlite:///multisig.db")
        Session = sessionmaker(bind=engine)
        session =Session()
        return session
        
    def add_user(self,User):
        session = self.create_session()
        dbadd= session.query(user_info).filter(user_info.user==User).first()
        if dbadd == None:
            dbadd = user_info(user = User.lower(), registered = False)
            session.add(dbadd)
        session.commit()
        session.close()
        
    def Register_user(self, User,message):
        split = message.split("+register ")
        split2 = split[1].split(" ")
        address = split2[0].strip()
        if self.d.validateaddress(address).isvalid == False:
            return -1
        print User, address 
        session = self.create_session()
        dbadd= session.query(user_info).filter(user_info.user==User).first()
        if dbadd == None:
            dbadd = user_info(user = User.lower(), address = address, registered = True)
        else:
            dbadd.address = address
            dbadd.registered = True
        session.add(dbadd)
        session.commit()
        session.close()
        return address
        
    def New_escrow(self,seller,buyer,arbitrator):
        from multisigcreate import generate_mutltisig_address
        session = self.create_session()
        multiadd = generate_mutltisig_address()["address"]
        self.d.sendtoaddress(multiadd,1)
        multi_instance = session.query(multisig).\
        filter(multisig.multiaddress==multiadd).first()
        redeemscript = multi_instance.redeemscript
        adddb = escrow_address(multi_address = multiadd, seller=seller.lower(), 
        buyer = buyer.lower().strip(), arbitrator = arbitrator.lower().strip(), redeem_script = redeemscript, 
        seller_private_key = multi_instance.privkey1, buyer_private_key = multi_instance.privkey2,
        arbitrator_private_key = multi_instance.privkey3, status = "new", \
        date_created = self.toTStamp(datetime.datetime.utcnow()) ,complete=False)
        session.close()
        session = self.create_session()
        session.add(adddb)
        session.commit()
        session.close()
        return [multiadd,redeemscript]
        
    def get_users(self, add):
        session = self.create_session()
        search = session.query(escrow_address).\
        filter(escrow_address.multi_address == add).first()
        session.close()
        return [ search.seller, search.buyer, search.arbitrator]
        
    def is_registered(self,user):
        session=self.create_session()
        search = session.query(user_info).\
        filter(user_info.user == user).first()
        session.close()
        if search != None:
            if search.registered == True:
                return True
            else:
                return False
        else:
            return False
            
    def duplicate_user_check(self, user1,user2,user3):
        u1 = user1.lower().strip()
        u2 = user2.lower().strip()
        u3 = user3.lower().strip()
        if u1 == u2:
            return True
        elif u1 == u3:
            return True
        elif u2 == u3:
            return True
        else:
            return False
        
    def find_role(self,user,address):
        u = user.lower()
        session = self.create_session()
        search = session.query(escrow_address).\
        filter(escrow_address.multi_address == address).first()
        session.close()
        if search == None:
            return None
        if search.seller == u:
            return "seller"
        elif search.buyer == u:
            return "buyer"
        elif search.arbitrator ==u:
            return "arbitrator"
        else:
            return None
        
    def vote_parser(self, user, message):
        u = user.lower()
        split = message.split("+vote ")
        split2 = split[1].split(" ")
        add = split2[1]
        vote = split2[0]
        role = self.find_role(u,add)
        if role == None:
            return -1
        session = self.create_session()
        search = session.query(escrow_address).\
        filter(escrow_address.multi_address == add).first()
        if role == "seller":
            search.seller_vote=vote
        elif role =="buyer":
            search.buyer_vote=vote
        elif role =="arbitrator":
            search.arbitrator_vote=vote
        session.commit()
        session.close()
        return 1
        
    def vote_address_picker(self, address):
        session = self.create_session()
        search = session.query(escrow_address).\
        filter(escrow_address.multi_address == address).first()
        votes = [search.seller_vote,search.buyer_vote,search.arbitrator_vote]
        if votes.count("BUYER")>=2:
            user = session.query(user_info).\
            filter(user_info.user == search.buyer).first()
            session.close()
            return [user.address,user.user]
        elif votes.count("SELLER")>=2:
            user = session.query(user_info).\
            filter(user_info.user == search.seller).first()
            session.close()
            return [user.address,user.user]
        else:
            session.close()
            return None
        
        
        
    def auto_accept(self,user): 
        session=self.create_session()
        search = session.query(user_info).\
        filter(user_info.user == user.lower()).first()
        session.close()
        if search != None:
            if search.auto_accept_arb==True:
                return True
            else:
                return False
        else:
            self.add_user(user)
            return False  
    def get_value(self,unspent):
        v=0.0
        for i in unspent:
            if int(i["confirmations"])<3:
                return 0
            v+=float(i["value"])*10**-8
        return v
    

#begin program
bot = Multisig_escrow()
bot.r.login()

while True:    
    print "...."
    #inbox checker
    inbox = bot.r.get_unread()
    escrow_session = bot.create_session()
    for mess in inbox:
        if "+register" in mess.body :
            add = bot.Register_user(mess.author.name,  mess.body)
            if add == -1:
                mess.reply(bot.m.Register_error)
            else:
                mess.reply(bot.m.Register_message % (add))
            mess.mark_as_read()
        elif "+escrow" in mess.body:

            try:
                split = mess.body.split("/u/")
                buyer = split[1].split(" ")[0].strip()
                arbitrator = split[2].strip()
                seller = mess.author.name
                bot.r.get_redditor(buyer)
                bot.r.get_redditor(arbitrator)
            except:
                mess.reply(bot.m.escrow_start_fail)
                mess.mark_as_read()
                continue
            if bot.duplicate_user_check(seller,buyer,arbitrator):
                mess.reply(bot.m.escrow_start_fail)
            else:
                bot.New_escrow(seller,buyer,arbitrator)
            
                mess.reply(bot.m.escrow_start)
            mess.mark_as_read()
            
        elif "+acceptarb" in mess.body:
            try:
                split = mess.body.split("+acceptarb ")
                arbadd=escrow_session.query(escrow_address).\
                filter(escrow_address.multi_address == split[1]).first()
                arbadd.arbitrator_accept = True
                escrow_session.add(arbadd)
            except:
                mess.reply(bot.m.message_fail)
            mess.mark_as_read()
        elif "+autoarb" in mess.body:
            try:
                autoarb_add = escrow_session.query(user_info).\
                filter(user_info.user==mess.author.name.lower()).first()
                autoarb_add.auto_accept_arb = True
                escrow_session.add(autoarb_add)
            except:
                mess.reply(bot.m.message_fail)
            mess.mark_as_read()
        elif "+vote" in mess.body:
            try:
                vote_result = bot.vote_parser(mess.author.name,mess.body)
                if vote_result == -1:
                    mess.reply(bot.m.message_fail)
            except:
                mess.reply(bot.m.message_fail)
            mess.mark_as_read()

    #database checker
    for instance in escrow_session.query(escrow_address).filter(escrow_address.complete == False).all():
        print instance
        #new status
        if instance.status == "new":
           
            users = bot.get_users(instance.multi_address)
            if bot.is_registered(users[0])==True:
                instance.seller_registered = True
            else:
                bot.r.send_message(users[0],"new escrow" ,bot.m.register_ask % (users[0],users[1])+bot.m.register_url)
            if bot.is_registered(users[1])==True:
                instance.buyer_registered = True
            else:
                bot.r.send_message(users[1],"new escrow" ,bot.m.register_ask % (users[0],users[1])+bot.m.register_url)
            if bot.auto_accept(users[2]) == True:
                instance.arbitrator_accept = True
            else:
                bot.r.send_message(users[2],"new escrow" ,bot.m.arbitrator_ask1 % (users[0],users[1])+bot.m.arbitrator_ask2+\
                instance.multi_address+")"+bot.m.arbitrator_auto_accept_link)
            

            instance.status = "waiting on register"
         #Waiting on register    
        elif instance.status =="waiting on register":
            print instance.seller_registered, instance.buyer_registered, instance.arbitrator_accept
            if instance.seller_registered == True and instance.buyer_registered == True\
            and instance.arbitrator_accept == True:
                users = bot.get_users(instance.multi_address)
                bot.r.send_message(users[0],"Escrow Address",bot.m.fund_info %\
                (users[0],users[1],users[2],instance.multi_address,instance.multi_address, instance.seller_private_key,\
                instance.redeem_script))
                bot.r.send_message(users[1],"Escrow Address",bot.m.fund_info %\
                (users[0],users[1],users[2],instance.multi_address,instance.multi_address, instance.buyer_private_key,\
                instance.redeem_script))
                bot.r.send_message(users[2],"Escrow Address",bot.m.fund_info %\
                (users[0],users[1],users[2],instance.multi_address,instance.multi_address, instance.arbitrator_private_key,\
                instance.redeem_script))
                instance.status = "waiting on funds"
            
            #check for new sign ups
            reg = escrow_session.query(user_info).\
            filter(user_info.user == instance.buyer).first()
            if reg !=None:
                if reg.registered == True:
                    instance.buyer_registered=True
                
            reg = escrow_session.query(user_info).\
            filter(user_info.user == instance.seller).first()
            if reg !=None:
                if reg.registered == True:
                    instance.seller_registered=True
            reg = escrow_session.query(user_info).\
            filter(user_info.user == instance.arbitrator).first()
            if reg != None:
                if reg.auto_accept_arb == True:
                    instance.arbitrator_accept = True
            
        #waiting on funds status
        elif instance.status == "waiting on funds":
                url = "https://dogechain.info/api/v1/unspent/"+instance.multi_address
                resp = requests.get(url).json()
                unspent = resp["unspent_outputs"]
                if unspent != []:
                    coins = bot.get_value(unspent)
                    if coins <2:
                        pass
                    else:
                        users= bot.get_users(instance.multi_address)
                        for user in users:
                            bot.r.send_message(user,"Escrow Deposit",bot.m.funded %\
                (str(coins-1),users[0],users[1],users[2],instance.multi_address,instance.multi_address)\
                +bot.m.funded_seller_vote + instance.multi_address+") :  "\
                +bot.m.funded_buyer_vote + instance.multi_address+")")
                
                        instance.status = "funded"
                    
        #funded status
        elif instance.status == "funded":
            print instance.seller_vote, instance.buyer_vote, instance.arbitrator_vote 
            to_user = bot.vote_address_picker(instance.multi_address)
            if to_user == None:
                pass
            else:
                
                instance.tx_id = redeem_funds(instance.multi_address,to_user[0])

                seller,buyer = bot.get_users(instance.multi_address)[0],bot.get_users(instance.multi_address)[1]
                for rec in [seller,buyer]:
                    bot.r.send_message(rec,"escrow complete",bot.m.complete % (to_user[1],instance.tx_id,instance.tx_id))                
                instance.status = "complete"
                instance.complete = True
        
        
        
        escrow_session.add(instance)
        
            
    
    escrow_session.commit()
    escrow_session.close()
    time.sleep(1)
    time.sleep(5)
        