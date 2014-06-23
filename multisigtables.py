


import sqlalchemy as sql


from sqlalchemy import Column, String,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
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
    auto_accept_arb = Boolean(False)
    
class escrow_address(Base):
    __tablename__ = "escrow"
    multi_address = Column(String,primary_key = True)
    seller = Column(String)
    buyer = Column(String)
    arbitrator = Column(String)
    seller_registered = Column(Boolean)
    buyer_registered = Column(Boolean)
    arbitrator_accept = Column(Boolean)
    seller_vote = Column(String)
    buyer_vote = Column(String)
    arbitrator_vote = Column(String)
    seller_private_key = Column(String)
    buyer_private_key = Column(String)
    arbitrator_private_key=Column(String)
    date_created = Column(String)
    redeem_script = Column(String)
    tx_id = Column(String)
    complete = Column(Boolean(False))
    status = Column(String) #"new" , "waiting on register" "waiting on funds" , "funded" , "complete","failed","timeout"
    def __repr__(self):
        return "add: %s status: %s" % (self.multi_address, self.status)
    
if __name__ == "__main__":

    
    engine = sql.create_engine("sqlite:///multisig.db")
    Base.metadata.create_all(engine) 

    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.add(multisig(multiaddress="*"))
    session.add(user_info(user = "*"))
    session.add(escrow_address(multi_address = "*"))
    session.commit()
    session.close()
    