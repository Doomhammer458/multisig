






def redeem_funds(multi_address,to_address):
    import requests
    from multisigtables import multisig
    import sqlalchemy as sql

    from sqlalchemy.orm import sessionmaker
    
    import dogecoinrpc
    doge = dogecoinrpc.connect_to_local()
    engine = sql.create_engine("sqlite:///multisig.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    instance= session.query(multisig).\
    filter(multisig.multiaddress == multi_address).first()
    print instance
    url = "https://dogechain.info/api/v1/unspent/"+multi_address
    
    resp = requests.get(url).json()
    unspent = resp["unspent_outputs"]

    
    value = 0.0
    
    in_list=[]
    
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
        
        
    out_dict = {to_address:value}
    raw = doge.createrawtransaction(in_list,out_dict)
    
    sign1 = doge.signrawtransaction(raw,prev,[instance.privkey1,instance.privkey2])
    
    tx = doge.sendrawtransaction(sign1["hex"])
    return tx

if __name__ ==  "__main__":
    print redeem_funds("9ysiaB2hzqZykCMH59dnSKjhDN4APR3pnZ","D8WVhodPoAfY7zKbYB8RvTjst5BLm6v3me")
    pass


    
    
    

