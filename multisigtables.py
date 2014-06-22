


import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,Float, Boolean

Base = declarative_base()
class multisig(Base):
    __tablename__ = "multisig"
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    privkey1 = Column(String)
    privkey2 = Column(String)
    privkey3 = Column(String)
    multiaddress = Column(String, primary_key=True)
    redeemscript = Column(String)
    status = Column(String)
    
class user_info(Base):
    __tablename__ = "user_info"
    user = Column(String, primary_key = True)
    address = Column(String)
    registered = Column(Boolean)
    banned = Column(Boolean(False))
    txs = Column(String)
class escrow_address(Base):
    __tablename__ = "escrow"
    multi_address = Column(String,primary_key = True)
    seller = Column(String)
    buyer = Column(String)
    arbitrator = Column(String)
    seller_registered = Column(Boolean)
    buyer_registered = Column(Boolean)
    Arbitrator_accept = Column(Boolean)
    seller_vote = Column(String)
    buyer_vote = Column(String)
    arbitrator_vote = Column(String)
    seller_private_key = Column(String)
    buyer_private_key = Column(String)
    arbitrator_private_key=Column(String)
    date_created = Column(String)
    redeem_script = Column(String)
    status = Column(String) #"new" , "waiting on funds" , "funded" , "complete","failed","timeout"