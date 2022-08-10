import token
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
    
    
    def getTokenAddress(self) -> str:
        # Returns FTM address. This is the staking and rewards token
        return '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'

    # ------------------  CONTRACT FUNCTIONS  --------------------- #

    def getStake(self, pid: int, address: str) -> int:
        # Returns amount of fantom staked in validator
        return self.contract_instance.functions.getStake(address, pid).call()

    def poolLength(self) -> int:
        # Returns number of nodes available to stake
        return self.contract_instance.functions.lastValidatorID().call()
    
    def pendingRewards(self, address: str, pid: int) -> int:
        # Pending rewards of a user in a node
        return self.contract_instance.functions.pendingRewards(address, pid).call()

