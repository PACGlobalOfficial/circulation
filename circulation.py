#!/usr/bin/python3
# accurately determines total currency in circulation
# barrystyle 17122019
#
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json, time, os, sys

#config
rpcuser = ''
rpcpass = ''
rpchost = '127.0.0.1'
rpcport = 9998

#main
blocknum = 0
totalmoney = 0
rpccomms = AuthServiceProxy('http://%s:%s@%s:%s'%(rpcuser,rpcpass,rpchost,str(rpcport)))
totalblk = int(rpccomms.getblockcount())

while True:

   blocknum += 1
   if blocknum > totalblk:
      sys.exit()
   blockhash = rpccomms.getblockhash(blocknum)
   blockdata = rpccomms.getblock(blockhash)

   print ('block #'+str(blocknum)+' ('+str(blockhash)+')')

   #tx
   intotal = 0
   outtotal = 0
   for item in blockdata['tx']:

       txrawdata = rpccomms.getrawtransaction(item)
       txdata = rpccomms.decoderawtransaction(txrawdata)

       #ins
       if 'coinbase' in str(txdata):
           print ('input is coinbase')
       else:
           print ('input is vout')
           for vin in txdata['vin']:
               intxid = vin['txid']
               inn = vin['vout']
               txrawdata = rpccomms.getrawtransaction(intxid)
               txindata = rpccomms.decoderawtransaction(txrawdata)
               for specin in txindata['vout']:
                   if int(specin['n']) == int(inn):
                      valuein = specin['value']
                      intotal += valuein
       #outs
       for txout in txdata['vout']:
           valueout = txout['value']
           outtotal += valueout

   created = outtotal-intotal
   totalmoney += created

   print ('intotal is ' + str(intotal))
   print ('outtotal is ' + str(outtotal))
   print ('created in this block ' + str(created))
   print ('total money created ' + str(totalmoney))
   print (' ')
