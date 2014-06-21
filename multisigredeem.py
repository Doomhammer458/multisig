import dogecoinrpc as doge
doge = doge.connect_to_local()

import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import sessionmaker
import requests
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
Session = sessionmaker(bind=engine)
session = Session()
instance= session.query(multisig).\
filter(multisig.status == None).first()

url = "https://dogechain.info/api/v1/unspent/"+instance.multiaddress
resp = requests.get(url).json()
unspent = resp["unspent_outputs"]

tx_id = unspent[0]["tx_hash"]
txn = unspent[0]["tx_output_n"]
value = float(unspent[0]["value"])*10**-8
decodetx = doge.getrawtransaction(tx_id,True).vout
scriptpubkey = decodetx[txn]["scriptPubKey"]["hex"]
in_list = [{"txid":tx_id,"vout":txn}]
out_dict = {"DFhGfJxZ2xzJc78ih4JaoKh8wYounJvvNs":value}
prev = [{'txid': tx_id,
'vout': txn, "scriptPubKey": scriptpubkey, 'redeemScript': instance.redeemscript}]
raw = doge.createrawtransaction(in_list,out_dict)
sign1 = doge.signrawtransaction(raw,prev,[instance.privkey1,instance.privkey3])
tx = doge.sendrawtransaction(sign1["hex"])
print tx
instance.status="complete"
session.add(instance)
session.commit()
session.close()






