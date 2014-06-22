import praw
import dogecoinrpc as doge
doge = doge.connect_to_local()
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

    
    
r = praw.Reddit(user_agent="doge_multisig v0.1 by /u/Doomhammer458")

engine = sql.create_engine("sqlite:///multisig.db")
Base.metadata.create_all(engine)


def Register_new_user(User,message):
    split = message.split("+register ")
    split2 = split[1].split(" ")
    address = split2[0]
    print address
    dbadd = user_info(user = User, address = address, registered = True)
    engine = sql.create_engine("sqlite:///multisig.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(dbadd)
    session.commit()
    session.close()
    
    return address
    
r.login()
    
while True:
    print "...."
    inbox = r.get_unread()
    for mess in inbox:
        if "+register" in mess.body :
            add = Register_new_user(mess.author.name,  mess.body)
            print mess.reply(Register_message % (add))
            mess.mark_as_read()

    time.sleep(1)
    time.sleep(10)
        