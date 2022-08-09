from web3 import Web3
import os

contract_address = '0x9083EA3756BDE6Ee6f27a6e996806FBD37F6F093'

class SpiritSwap:
    def __init__(self, provider):
        web3 = Web3(Web3.HTTPProvider(provider))
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpiritAbi.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=contract_address, abi=contract_abi)


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
