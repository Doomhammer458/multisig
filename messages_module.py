class Messages_module():
    def __init__(self):
        self.Register_message = "You are now registered with the address: %s and can \
start using doge mulitsig escrow! \n \n For info on getting started please visit /r/DogeMultisigEscrow"

        self.Register_error = " Please provide a valid doge address \n\n \
use this link to try again: [+register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"

        self.escrow_start = "you have successfully started an escrow transaction \
        you will be notified when the buyer and arbitrator have agreed to the transaction"
        self.escrow_start_fail = "Unable to complete the request. please make sure you have spelled \
the user names correctly, have three different users, and have included /u/ before the names\n \n Use this link to try again: [+escrow]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=escrow&message=%2Bescrow%20buyer%20%2Fu%2Fusername%20Arbitrator%20%2Fu%2Fusername)" 
        self.register_ask = "%s would like to start a escrow transaction with %s.  If you would like to proceed, follow this link to register an\
 address with doge multisig escrow: \n \n"
        self.register_url="[+register]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=register&message=%2Bregister%20ADDRESS)"
        self.arbitrator_ask1 = '%s has asked you to arbitrate a transaction with %s, to accept click on the following link: \n \n '
        self.arbitrator_ask2="[+acceptarb]\
(http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=escrow&message=\%2Bacceptarb\%20"
        self.arbitrator_auto_accept_link = "\n\n if you would like to accept this requests and automatically accept future \
arbitrator requests please follow the following link: \n \n [+autoarb](\
http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=autoarb&message=%2Bautoarb) "
        self.fund_info = "Your escrow transaction is ready!  Here is all the vital info, if any of it is \
incorrect **DO NOT** proceed with the transaction. \n \n Seller: %s \n\n Buyer: %s  \n\n Arbitrator:  %s \
\n\n Multi signature address: [%s](http://dogechain.info/address/%s) \n \n  If all the information is correct, send your payment to the address listed above.\
 You will be notified when the payment has been received.\n\n Below is your personal private key and the address redeem script \
in the event you need to author your own transaction. Do not share this information. \n\n Your personal private key %s  Redeem script  %s " 
        self.message_fail = "unable to proccess your request.  Please resend the message without modifying the content of the message body"
        self.funded = " A deposit of %s doge has been recieved in the following transaction: \n \n \
Seller: %s \n\n Buyer: %s  \n\n Arbitrator:  %s \n\n Multi signature address: [%s](http://dogechain.info/address/%s) \n \n When the transaction is complete or has failed,\
 use the links below to send the funds to the appropriate party.  If you are the arbitrator do not use the links until you have talked to both parties in an attempt to resolve a dispute."
        self.funded_seller_vote = "\n \n [send funds to seller](http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=vote&message=%2Bvote%20SELLER%20"
        self.funded_buyer_vote = "[send funds to buyer](http://www.reddit.com/message/compose?to=dogemultisigescrow&subject=vote&message=%2Bvote%20BUYER%20" 
        self.complete = "Your transaction is complete, the funds were sent to %s \n\n\
 your TX ID is [%s](http://dogechain.info/tx/%s)" 
        self.timeout_reg = "Your request has timed out.  Either the buyer did not register with Doge Multisig Escrow or the arbitrator did not agree to arbitrate the transaction\n\n \
 Contact the buyer and arbitrator and try again."