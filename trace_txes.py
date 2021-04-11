#!/usr/bin/env python
# coding: utf-8

# In[89]:


from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime


# In[71]:


rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))


# In[92]:


###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        tx_hash= tx['hash']
        n = tx['vout'][0]['n']
        amount = tx['vout'][0]['value']
        owner = tx['vout'][0]['scriptPubKey']['addresses'][0]
        time = datetime.fromtimestamp(tx['time'])
        self.inputs = []
        return cls(tx_hash = tx_hash, n=n, amount=amount, owner=owner, time = time)
        #YOUR CODE HERE

    def get_inputs(self,d=1):
        tx = rpc_connection.getrawtransaction(tx_hash,True)

        for i in tx['vin']:
            if 'txid' in i.keys() and 'vout' in i.keys():
                self.inputs.append(TXO.from_tx_hash(i['txid'],i['vout']))
        if d>0:
            for j in self.inputs:
                j.get_inputs(d-1)
        
        return self
        #YOUR CODE HERE


# In[72]:


tx_hash = "996b41652355960f49d919328d7779a05aac09ff95001de12349774c91970407"
tx = rpc_connection.getrawtransaction(tx_hash,True)
print(tx)


# In[80]:


t = tx['vout']
s = tx['vout'][0]['scriptPubKey']['addresses']
print(s)


# In[91]:


time = datetime.fromtimestamp(tx['time'])
print(time)


# In[ ]:




