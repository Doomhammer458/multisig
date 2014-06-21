# -*- coding: utf-8 -*-

import dogecoinrpc as doge
doge = doge.connect_to_local()

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
