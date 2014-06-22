import dogecoinrpc 
doge = dogecoinrpc.connect_to_local()

import sqlalchemy as sql
import sys
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
import requests
Base = declarative_base()
from multisigtables import *
doge = dogecoinrpc.connect_to_local()
engine = sql.create_engine("sqlite:///multisig.db")
Session = sessionmaker(bind=engine)
session = Session()
instance= session.query(multisig).\
filter(multisig.status == None).first()
print instance.multiaddress
if instance == None:
    print "no pending addresses"
    sys.exit()
url = "https://dogechain.info/api/v1/unspent/"+instance.multiaddress
resp = requests.get(url).json()
unspent = resp["unspent_outputs"]

if unspent ==[]:
    print "no unspent transactions"
    sys.exit()
    

value = 0.0

in_list=[]
scriptpk_list = []
in_list=[]
prev=[]


for i in range(len(unspent)):
    tx_id = unspent[i]["tx_hash"]
    txn = unspent[i]["tx_output_n"]
    value += float(unspent[i]["value"])*10**-8
    decodetx = doge.getrawtransaction(tx_id,True).vout
    scriptpubkey = decodetx[txn]["scriptPubKey"]["hex"]
    in_list.append({"txid":tx_id,"vout":txn})

    prev.append({'txid': tx_id,'vout': txn,
    "scriptPubKey": scriptpubkey, 'redeemScript': instance.redeemscript})
    
    
out_dict = {"DFhGfJxZ2xzJc78ih4JaoKh8wYounJvvNs":value}
raw = doge.createrawtransaction(in_list,out_dict)

sign1 = doge.signrawtransaction(raw,prev,[instance.privkey1,instance.privkey3])

tx = doge.sendrawtransaction(sign1["hex"])
print tx

instance.status="complete"

session.add(instance)
session.commit()
session.close()





