# -*- coding: utf-8 -*-
from bitcoin import *
import dogecoinrpc as doge
doge = doge.connect_to_local()
import random
import re
import sqlalchemy as sql
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,Float, Boolean
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
class multisig(Base):
    __tablename__ = "multisig"
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    privkey1 = Column(String)
    privkey2 = Column(String)
    privkey3 = Column(String)
    multiaddress = Column(String)
    ID = Column(String, primary_key=True)
    redeemscript = Column(String)
    status = Column(String)
    
    
    


engine = sql.create_engine("sqlite:///multisig.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
db_add = multisig(ID = str(uuid.uuid4()))


aone = doge.getnewaddress()
db_add.address1=aone
atwo = doge.getnewaddress()
db_add.address2=atwo
athree = doge.getnewaddress()
db_add.address3=aone



pone = doge.dumpprivkey(aone)
db_add.privkey1 = pone
ptwo = doge.dumpprivkey(atwo)
db_add.privkey2 = ptwo
pthree =doge.dumpprivkey(athree)
db_add.privkey3 = pthree

multi = [aone,atwo,athree] 

multiadd = doge.createmultisig(2,multi)

db_add.redeemscript=multiadd["redeemScript"]
db_add.multiaddress=multiadd["address"]
session.add(db_add)
session.commit()
session.close()
print multiadd

"""


prev = {'txid': "26b108226eab9bb9a98274eb7f8de784b7490d1cb6eb1b2e06c5a7494067837d",
'vout': 0, "scriptPubKey": "a914be126e4e1a93b35787236eb979116da63e3fa29187", 'redeemScript': redeemscript}

in_list=[{"txid":"26b108226eab9bb9a98274eb7f8de784b7490d1cb6eb1b2e06c5a7494067837d","vout":0}]
out_dict = {"DFhGfJxZ2xzJc78ih4JaoKh8wYounJvvNs":1}
"""