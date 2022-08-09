from web3 import Web3
import os

address = '0xFC00FACE00000000000000000000000000000000'

class FantomWallet:

    def __init__(self, provider):
        web3 = Web3(Web3.WebsocketProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/FantomWalletAbi.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=address, abi=contract_abi)
    
    
    # ------------------  CONTRACT FUNCTIONS  --------------------- #

    def getStake(self, pid: int, address: str) -> int:
        # Returns amount of fantom staked in validator
        return self.contract_instance.getStake(address, pid).call()

    def poolLength(self) -> int:
        return self.contract_instance.lastValidatorID().call()
    
    def pendingRewards(self, address: str, pid: int) -> int:
        return self.contract_instance.pendingRewards(address, pid).call()

