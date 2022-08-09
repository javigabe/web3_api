from web3 import Web3
import os

farm_v2 = '0x18b4f774fdC7BF685daeeF66c2990b1dDd9ea6aD'
farm_v3 = '0x9C9C920E51778c4ABF727b8Bb223e78132F00aA4'

class SpookySwapV2:
    def __init__(self, provider):
        web3 = Web3(Web3.WebsocketProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpookyAbiV2.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v2, abi=contract_abi)


    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    
    def isLpToken(self, address: str) -> bool:
        return self.contract_instance.functions.isLpToken(address).call()

    def lpToken(self, pid: int) -> str:
        # address of lp Token staked in a farm
        return self.contract_instance.functions.lpToken(pid).call()

    def userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()


class SpookySwapV3:
    def __init__(self, provider):
        web3 = Web3(Web3.WebsocketProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpookyAbiV3.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v3, abi=contract_abi)

    
    # ------------------  CONTRACT FUNCTIONS  --------------------- #

    def isLpToken(self, address: str) -> bool:
        return self.contract_instance.functions.isLpToken(address).call()

    def lpToken(self, pid: int) -> str:
        # lp token address of pool
        return self.contract_instance.functions.lpToken(pid).call()

    def userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens), rewardDebt]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

