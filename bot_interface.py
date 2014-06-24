

import time 
import requests
from multisigtables import multisig,escrow_address,user_info

class Multisig_escrow():
    

    def __init__(self):
        import dogecoinrpc
        import praw
        self.d = dogecoinrpc.connect_to_local()
        self.r = praw.Reddit(user_agent="doge_multisig v0.1 by /u/Doomhammer458")
        
        #message templates
        self.Register_message = "You are now registered with the address: %s and can \
start using doge mulitsig escrow! \n \n For info on getting started please visit /r/DogeMultisigEscrow"

        self.Register_error = " Please provide a valid doge address \n\n \
use this link to try again: [+register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"

        self.escrow_start = "you have successfully started an escrow transaction \
        you will be notified when the buyer and arbitrator have agreed to the transaction"
        self.escrow_start_fail = "Unable to complete the request please make sure you have spelled \
the user names correctly and have included /u/ before the names\n \n Use this link to try again: [+escrow]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=escrow&message=%2Bescrow%20buyer%20%2Fu%2Fusername%20Arbitrator%20%2Fu%2Fusername)" 
        self.register_ask = "%s would like to start a escrow transaction with %s.  If you would like to proceed, follow this link to register an\
 address with doge multlisig escrow: \n \n"
        self.register_url="[+register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"
        self.arbitrator_ask1 = '%s has asked you to arbitrate a transaction with %s, to accept click on the following link: \n \n '
        self.arbitrator_ask2="[+acceptarb]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=escrow&message=\%2Bacceptarb\%20"
        self.arbitrator_auto_accept_link = "\n\n if you would like to automatically accept future \
arbitrator requests please follow the following link: \n \n [+autoarb](\
http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=autoarb&message=%2Bautoarb)  \
(you will still need to accept this request manually)"
        self.fund_info = "Your escrow transaction is ready!  Here is all the vital info, if any of it is \
incorrect **DO NOT** proceed with the transaction. \n \n Seller: %s \n\n Buyer: %s  \n\n Arbitrator:  %s \
\n\n Multi signature address: %s \n \n  If all the information is correct, send your payment to the address listed above.\
You will be notified when the payment has been recieved. Below is your personal private key and the address reedeem script \
in the event you need to author your own transaction. Do not share this information. \n\n Your personal private key %s  Redeem script  %s " 

        self.funded = " A deposit of %s doge has been recieved in the following transaction: \n \n \
Seller: %s \n\n Buyer: %s  \n\n Arbitrator:  %s \n\n Multi signature address: %s \n \n when the transaction is complete or has failed,\
use the links below to send the funds to the apopriate party.  If you are the arbitrator do not use the links until you have talked to both parties in an attempt to resolve a dispute"
        self.funded_seller_vote = "\n \n [send funds to seller](http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=vote&message=%2Bvote%20SELLER%20"
        self.funded_buyer_vote = "[send funds to buyer](http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=vote&message=%2Bvote%20BUYER%20" 
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
        address = split2[0]
        if self.d.validateaddress(address).isvalid == False:
            return -1
        print address

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
        print multiadd
        multi_instance = session.query(multisig).\
        filter(multisig.multiaddress==multiadd).first()
        
        redeemscript = multi_instance.redeemscript
        adddb = escrow_address(multi_address = multiadd, seller=seller.lower(), 
        buyer = buyer.lower(), arbitrator = arbitrator.lower(), redeem_script = redeemscript, 
        seller_private_key = multi_instance.privkey1, buyer_private_key = multi_instance.privkey2,
        arbitrator_private_key = multi_instance.privkey3, status = "new", complete=False)
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
        vote = split2[1]
        print split2
        role = self.find_role(user,add)
        if role == None:
            return -1
        session = self.create_session()
        search = session.query(escrow_address).\
        filter(escrow_address.multi_address == add).first()
        print role
        if role == "seller":
            search.seller_vote=vote
        elif role =="buyer":
            search.buyer_vote=vote
        elif role =="arbitrator":
            search.arbitrator_vote=vote
        session.commit()
        session.close()
        return 1
        
        
        
        
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
                mess.reply(bot.Register_error)
            else:
                mess.reply(bot.Register_message % (add))
            mess.mark_as_read()
        elif "+escrow" in mess.body:

            try:
                split = mess.body.split("/u/")
                buyer = split[1].split(" ")[0]
                arbitrator = split[2]
                seller = mess.author.name
                bot.r.get_redditor(buyer)
                bot.r.get_redditor(arbitrator)
            except:
                mess.reply(bot.escrow_start_fail)
                mess.mark_as_read()
                continue
                
            bot.New_escrow(seller,buyer,arbitrator)
            
            mess.reply(bot.escrow_start)
            mess.mark_as_read()
        elif "+acceptarb" in mess.body:
            split = mess.body.split("+acceptarb ")
            arbadd=escrow_session.query(escrow_address).\
            filter(escrow_address.multi_address == split[1]).first()
            arbadd.arbitrator_accept = True
            escrow_session.add(arbadd)
            mess.mark_as_read()
        elif "+autoarb" in mess.body:
            autoarb_add = escrow_session.query(user_info).\
            filter(user_info.user==mess.author.name.lower()).first()
            autoarb_add.auto_accept_arb = True
            escrow_session.add(autoarb_add)
            mess.mark_as_read()
        elif "+vote" in mess.body:
            bot.vote_parser(mess.author.name,mess.body)
            mess.mark_as_read()

    #database checker
    for instance in escrow_session.query(escrow_address).filter(escrow_address.complete == False).all():
        print instance
        #new status
        if instance.status == "new":
            print instance
            users = bot.get_users(instance.multi_address)
            if bot.is_registered(users[0])==True:
                instance.seller_registered = True
            else:
                bot.r.send_message(users[0],"new escrow" ,bot.register_ask % (users[0],users[1])+bot.register_url)
            if bot.is_registered(users[1])==True:
                instance.buyer_registered = True
            else:
                bot.r.send_message(users[1],"new escrow" ,bot.register_ask % (users[0],users[1])+bot.register_url)
            if bot.auto_accept(users[2]) == True:
                instance.arbitrator_accept = True
            else:
                bot.r.send_message(users[0],"new escrow" ,bot.arbitrator_ask1 % (users[0],users[1])+bot.arbitrator_ask2+\
                instance.multi_address+")"+bot.arbitrator_auto_accept_link)
            

            instance.status = "waiting on register"
        elif instance.status =="waiting on register":
            if instance.seller_registered == True and instance.buyer_registered == True\
            and instance.arbitrator_accept == True:
                users = bot.get_users(instance.multi_address)
                bot.r.send_message(users[0],"Escrow Address",bot.fund_info %\
                (users[0],users[1],users[2],instance.multi_address, instance.seller_private_key,\
                instance.redeem_script))
                bot.r.send_message(users[1],"Escrow Address",bot.fund_info %\
                (users[0],users[1],users[2],instance.multi_address, instance.buyer_private_key,\
                instance.redeem_script))
                bot.r.send_message(users[2],"Escrow Address",bot.fund_info %\
                (users[0],users[1],users[2],instance.multi_address, instance.arbitrator_private_key,\
                instance.redeem_script))
                instance.status = "waiting on funds"
        #waiting on funds status
        elif instance.status == "waiting on funds":
                url = "https://dogechain.info/api/v1/unspent/"+instance.multi_address
                resp = requests.get(url).json()
                unspent = resp["unspent_outputs"]
                if unspent != []:
                    coins = bot.get_value(unspent)
                    if coins == 0:
                        pass
                    else:
                        users= bot.get_users(instance.multi_address)
                        for user in users:
                            bot.r.send_message(user,"Escrow Deposit",bot.funded %\
                (str(coins),users[0],users[1],users[2],instance.multi_address)\
                +bot.funded_seller_vote + instance.multi_address+") :  "\
                +bot.funded_buyer_vote + instance.multi_address+")")
                
                        instance.status = "funded"
                    
        #funded status
        elif instance.status == "funded":
            pass
        
        
        
        
        escrow_session.add(instance)
        
            
    
    escrow_session.commit()
    escrow_session.close()
    time.sleep(1)
    time.sleep(10)
        