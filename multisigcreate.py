# -*- coding: utf-8 -*-

import multisigtables

def generate_mutltisig_address():
    from multisigtables import multisig
    import sqlalchemy as sql
    from sqlalchemy.ext.declarative import declarative_base

    from sqlalchemy.orm import sessionmaker
    Base = declarative_base()
    import dogecoinrpc as doge
    doge = doge.connect_to_local()
    engine = sql.create_engine("sqlite:///multisig.db")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    db_add = multisig()
    
    
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
    
    return multiadd
if __name__ == "__main__":
    print generate_mutltisig_address()
    
