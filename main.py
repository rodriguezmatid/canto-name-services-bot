from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import time
import tweepy

_dotenv.load_dotenv()
rpc = 'https://canto.gravitychain.io/' # mainnet
# rpc = 'https://eth.plexnode.wtf/' # testnet
web3 = Web3(Web3.HTTPProvider(rpc))

# Authenticate to Twitter
TW_API_KEY = os.environ["TWITTER_API_KEY"]
TW_API_SECRET = os.environ["TWITTER_API_SECRET"]
TW_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TW_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

# auth = tweepy.OAuthHandler(TW_API_KEY, TW_API_SECRET)
# auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_SECRET)

# api_twitter = tweepy.API(auth)

# try:
#     api_twitter.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

# Log to the blockchain
if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')
print()

# Contracts
ycnMainnetAddress = web3.toChecksumAddress('0xC53597C33d0dc3FFEC4Bcba31aEe6D01f18C197F')
ycnTestnetAddress = web3.toChecksumAddress('0x4cdc0251c8eb4fd96b8b9acdcf314b969b3af4d9')

# Abi
with open('./utils/ycn.json', 'r') as f:
  abi_contract_erc20 = json.load(f)

contract = web3.eth.contract(address=ycnTestnetAddress, abi=abi_contract_erc20)

def handle_event(event):
    print(event)
    # try:
    #     print("From: ", event['address'])
    #     # print("To: ", event['to'])
    #     print("From: ", event['topics'][1])
    #     print("To: ", event['topics'][2])
    #     print("Transaction Hash: ", event['transactionHash'])
    #     print("Block Number: ", event['blockNumber'])
    #     print("\n")
    # except KeyError:
    #     print("Could not find expected keys in event:", event)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = contract.events.Register.createFilter(fromBlock='latest')
log_loop(block_filter, 2)

# api_twitter.update_status("hola")