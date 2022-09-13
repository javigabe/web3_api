from typing import Dict
from web3 import Web3
import os

farm_v2 = '0x18b4f774fdC7BF685daeeF66c2990b1dDd9ea6aD'
farm_v3 = '0x9C9C920E51778c4ABF727b8Bb223e78132F00aA4'

class SpookySwapV2:
    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpookyAbiV2.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v2, abi=contract_abi)

    def getUserLiquidity(self, address: str) -> Dict:
        poolLength = self._poolLength()
        reward_token = self._rewardToken()

        user_liquidity = {'user_liquidity': []}
        for i in range(0, poolLength):
            amount, reward_debt = self._userInfo(i, address)
            if (amount != 0):
                lp_token = self._lpToken(i)
                #lpTokens = float(Web3.fromWei(user_info[0], 'ether'))
                pool = {
                    'is_lp': 'True',
                    'amount': amount,
                    'reward_debt': reward_debt,
                    'token_address': lp_token,
                    'reward_token': reward_token
                }
                user_liquidity['user_liquidity'].append(pool)
        
        return user_liquidity
        

    # ------------------  CONTRACT FUNCTIONS  --------------------- #
    
    def _isLpToken(self, address: str) -> bool:
        return self.contract_instance.functions.isLpToken(address).call()

    def _lpToken(self, pid: int) -> str:
        # address of lp Token staked in a farm
        return self.contract_instance.functions.lpToken(pid).call()

    def _userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens) uint256, rewardDebt uint256]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def _poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def _rewardToken(self) -> str:
        # Boo token address
        # HARD CODED TO SAVE ONE REQUEST
        return Web3.toChecksumAddress('0x841fad6eae12c286d1fd18d1d525dffa75c7effe')


class SpookySwapV3:
    def __init__(self, web3: Web3):
        # Check if connected correctly
        if (not web3.isConnected()):
            raise ConnectionError('Error connecting to fantom rpc')

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        abi_path = "abi/SpookyAbiV3.txt"
        with open(os.path.join(script_dir, abi_path), 'r') as f:
            contract_abi = f.readline()
        
        self.contract_instance = web3.eth.contract(address=farm_v3, abi=contract_abi)

    def getUserLiquidity(self, address: str) -> Dict:
        poolLength = self._poolLength()
        reward_token = self._rewardToken()
        
        user_liquidity = {'user_liquidity': []}
        for i in range(0, poolLength):
            amount, reward_debt = self._userInfo(i, address)
            if (amount != 0):
                lpToken = self._lpToken(i)
                #lpTokens = float(Web3.fromWei(user_info[0], 'ether'))
                pool = {
                    'is_lp': 'True',
                    'amount': amount,
                    'reward_debt': reward_debt,
                    'token_address': lpToken,
                    'reward_token': reward_token

                }
                user_liquidity['user_liquidity'].append(pool)
        
        return user_liquidity

    # ------------------  CONTRACT FUNCTIONS  --------------------- #

    def _isLpToken(self, address: str) -> bool:
        return self.contract_instance.functions.isLpToken(address).call()

    def _lpToken(self, pid: int) -> str:
        # lp token address of pool
        return self.contract_instance.functions.lpToken(pid).call()

    def _userInfo(self, pid: int, address: str) -> list:
        #  [amount (lpTokens), rewardDebt]
        return self.contract_instance.functions.userInfo(pid, address).call()

    def _poolLength(self) -> int:
        # Number of pools under this contract
        return self.contract_instance.functions.poolLength().call()

    def _rewardToken(self) -> str:
        # Boo token address
        # HARD CODED TO SAVE ONE REQUEST
        return Web3.toChecksumAddress('0x841fad6eae12c286d1fd18d1d525dffa75c7effe')
