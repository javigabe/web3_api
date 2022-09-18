from typing import Dict
from web3 import Web3
import os

contract_address = '0x9083EA3756BDE6Ee6f27a6e996806FBD37F6F093'

class SpiritSwap:
    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpiritAbi.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=contract_address, abi=contract_abi)


    def getUserLiquidity(self, address: str) -> Dict:
        poolLength = self._poolLength()
        reward_token = self._rewardToken()

        user_liquidity = {'user_liquidity': []}
        for i in range(0, poolLength):
            amount, reward_debt = self._userInfo(i, address)
            if (amount != 0):
                lp_token = self._poolInfo(i)[0]
                #lpTokens = float(Web3.fromWei(amount, 'ether'))
                pool = {
                    'is_lp': 1,
                    'amount': amount,
                    'reward_debt': reward_debt,
                    'token_address': lp_token,
                    'reward_token': reward_token
                }
                user_liquidity['user_liquidity'].append(pool)
        
        return user_liquidity


    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    def _poolInfo(self, pid: int) -> list:
        # [lpToken address, allocPoint uint256, lastRewardBlock uint256, accSpiritPerShare uint256, depositFeeBP uint16]
        return self.contract_instance.functions.poolInfo(pid).call()

    def _userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def _poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def _rewardToken(self) -> str:
        # Spirit token address
        # HARD CODED TO SAVE ONE REQUEST
        return Web3.toChecksumAddress('0x5cc61a78f164885776aa610fb0fe1257df78e59b')
