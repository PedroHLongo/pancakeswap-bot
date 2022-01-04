from web3 import Web3

import config
import time

web3 = Web3(Web3.HTTPProvider(config.BSC))

print(web3.isConnected())

def buy_token(token):
    #pancakeswap router
    pan_router_contract_address = config.PANCAKE_ROUTER_ADDRESS

    balance = web3.eth.get_balance(config.WALLET_ADDRESS)
    #print(balance)
    
    human_readable = web3.fromWei(balance,'ether')
    #print(humanReadable)
    
    #Contract Address of Token to buy
    token_to_buy = web3.toChecksumAddress(token)
    spend = web3.toChecksumAddress(config.WBNB_ADDRESS)  #wbnb contract
    
    #Setup the PancakeSwap contract
    contract = web3.eth.contract(address=pan_router_contract_address, abi=config.PANCAKE_ABI)
    nonce = web3.eth.get_transaction_count(config.WALLET_ADDRESS)
    
    start = time.time()

    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    0, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals
    [spend,token_to_buy],
    config.WALLET_ADDRESS,
    (int(time.time()) + 10000)
    ).buildTransaction({
    'from': config.WALLET_ADDRESS,
    'value': web3.toWei(0.07,'ether'), #This is the Token(BNB) amount you want to Swap from
    'gas': 250000,
    'gasPrice': web3.toWei('5','gwei'),
    'nonce': nonce,
    })
        
    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.PRIVATE_KEY)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(web3.toHex(tx_token))