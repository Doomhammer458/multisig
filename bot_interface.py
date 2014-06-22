

import time 
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
    
    def create_session(self):
        import sqlalchemy as sql
        from sqlalchemy.orm import sessionmaker
        engine = sql.create_engine("sqlite:///multisig.db")
        Session = sessionmaker(bind=engine)
        session =Session()
        return session
        
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
        arbitrator_private_key = multi_instance.privkey3, status = "new")
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
        
            
    def auto_accept(self,user): 
        session=self.create_session()
        search = session.query(user_info).\
        filter(user_info.user == user).first()
        session.close()
        if search != None:
            if search.auto_accept_arb==True:
                return True
            else:
                return False
        else:
            return False  

bot = Multisig_escrow()
bot.r.login()
while True:
    print "...."
    inbox = bot.r.get_unread()
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
        
            

    escrow_session = bot.create_session()
    for instance in escrow_session.query(escrow_address).filter(escrow_address.status != "complete"):
        print instance
        #new status
        if instance.status == "new":
            users = bot.get_users(instance.multi_address)
            if bot.is_registered(users[0])==True:
                instance.seller_registered = True
            if bot.is_registered(users[1])==True:
                instance.buyer_registered = True
            if bot.auto_accept(users[2]) == True:
                instance.arbitrator_accept = True
            print instance.buyer_registered
            print instance.seller_registered
            
        
        
        
        
        escrow_session.add(instance)
        
            
    
    escrow_session.commit()
    escrow_session.close()
    time.sleep(1)
    time.sleep(10)
        