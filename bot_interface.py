

import time 

class Multisig_escrow():
    

    def __init__(self):
        import dogecoinrpc

        
        import praw
        self.d = dogecoinrpc.connect_to_local()
        self.r = praw.Reddit(user_agent="doge_multisig v0.1 by /u/Doomhammer458")
        self.Register_message = "You are now registered with the address: %s and can \
start using doge mulitsig escrow! \n \n For info on getting started please visit /r/DogeMultisigEscrow"

        self.Register_error = " please provide a valid doge address \n\n \
use this link to try again: [register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"
    
    def Register_user(self, User,message):
        from multisigtables import user_info
        import sqlalchemy as sql
        from sqlalchemy.orm import sessionmaker
        
        split = message.split("+register ")
        split2 = split[1].split(" ")
        address = split2[0]
        if self.d.validateaddress(address).isvalid == False:
            return -1
        print address
        engine = sql.create_engine("sqlite:///multisig.db")
        Session = sessionmaker(bind=engine)
        session = Session()
        dbadd= session.query(user_info).filter(user_info.user==User).first()
        if dbadd == None:
            dbadd = user_info(user = User, address = address, registered = True)
        else:
            dbadd.address = address
    
        session.add(dbadd)
        session.commit()
        session.close()
        
        return address
    def New_escrow(self,seller,buyer,arbitrator):

        """
        engine = sql.create_engine("sqlite:///multisig.db")
        Session = sessionmaker(bind=engine)
        session = Session()
        multiadd = generate_multi_sig_address()
        session.query(multisig)
        """
    

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

    time.sleep(1)
    time.sleep(10)
        