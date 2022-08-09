from web3 import Web3
import os

# MIGRATION DATA:  https://docs.pancakeswap.finance/code/migration/masterchef-v2
# THIS DATA INCLUDES LIST OF FARMS WITH ITS PID IN FARM V1 AND FARM V2.
# NOT SURE IF FUNDS ARE ALREADY IN FARM V2 CONTRACT OR STILL IN FARM V1 

farm_v1 = '0x73feaa1eE314F8c655E354234017bE2193C9E24E'
farm_v2 = '0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652'

class PancakeSwapV1:
                #  -------------      POOLS START AT PID 251      ------------ #
    def __init__(self, provider):
        web3 = Web3(Web3.HTTPProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to binance smart chain rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/PancakeAbiV1.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v1, abi=contract_abi)


    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    def poolInfo(self, pid: int) -> list:
        # [lpToken address, allocPoint uint256, lastRewardBlock uint256, accSpiritPerShare uint256, depositFeeBP uint16]
        return self.contract_instance.functions.poolInfo(pid).call()

    def userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def pendingRewards(self, pid: int, address: str) -> int:
        # Pending cake rewards for a user in a pool
        return self.contract_instance.functions.pendingCake(pid, address).call()


class PancakeSwapV2:
    def __init__(self, provider):
        web3 = Web3(Web3.HTTPProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to binance smart chain rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/PancakeAbiV2.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v2, abi=contract_abi)


    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    def userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def pendingRewards(self, pid: int, address: str) -> int:
        # Pending cake rewards for a user in a pool
        return self.contract_instance.functions.pendingCake(pid, address).call()

    def lpToken(self, pid: int) -> str:
        # lp token address of a pool
        return self.contract_instance.functions.lpToken(pid).call()
