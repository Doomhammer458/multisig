import praw
import dogecoinrpc
doge = dogecoinrpc.connect_to_local()
import time 
import sqlalchemy as sql
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import sessionmaker
import requests

from multisigtables import *
    
Register_message = "You are now registered with the address: %s and can \
start using doge mulitsig escrow! \n \n For info on getting started please visit /r/DogeMultisigEscrow"

Register_error = " please provide a valid doge address \n\n \
use this link to try again: [register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"
    
r = praw.Reddit(user_agent="doge_multisig v0.1 by /u/Doomhammer458")

engine = sql.create_engine("sqlite:///multisig.db")
Base.metadata.create_all(engine)


def Register_user(User,message):
    import dogecoinrpc
    doge = dogecoinrpc.connect_to_local()
    
    split = message.split("+register ")
    split2 = split[1].split(" ")
    address = split2[0]
    if doge.validateaddress(address).isvalid == False:
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
def New_escrow(seller,buyer,arbitrator):
    pass
 
r.login()
    
while True:
    print "...."
    inbox = r.get_unread()
    for mess in inbox:
        if "+register" in mess.body :
            add = Register_user(mess.author.name,  mess.body)
            if add == -1:
                mess.reply(Register_error)
            else:
                mess.reply(Register_message % (add))
            mess.mark_as_read()

    time.sleep(1)
    time.sleep(10)
        