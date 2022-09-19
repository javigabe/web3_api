from web3 import Web3
import requests
import math

from .Fantom.utils import *
from .Binance_Smart_Chain.utils import *
from model.Token import Token
from model.LpInfo import LpInfo
from .Chains import Chains
from ..keys import MORALIS_API_KEY


class PriceCalculator:

    def __init__(self, web3: Web3, chain: str):
        # Web3 instance and chain name
        chains = [member.value for member in Chains]
        if (chain not in chains):
            raise Exception('Chain provided to PriceCalculator not supported')
        self.web3 = web3
        self.chain = chain

    def getLpInfo(self, lp_address: str) -> LpInfo:
        contract = self.web3.eth.contract(address=lp_address, abi=self._getContractAbi(lp_address))

        # Token0 contract
        token_0 = contract.functions.token0().call()
        # Token1 contract
        token_1 = contract.functions.token1().call()      

        # We obtain the supply of token0 and token1 in the lp
        reserves_token0, reserves_token1, *_ = contract.functions.getReserves().call()

        # We obtain the total supply of the lp token
        total_supply = Web3.fromWei(contract.functions.totalSupply().call(), 'ether')

        # Transform token contract addresses to checksum
        token0_address= Web3.toChecksumAddress(token_0)
        token1_address = Web3.toChecksumAddress(token_1)

        # We obtain the price of both tokens in USD
        token0_priceUSD = self._getTokenPrice(token0_address)
        token1_priceUSD = self._getTokenPrice(token1_address)

        # Supply of both tokens in the contract  
        total_supply_token_0 = self.getTokenAmount(token0_address, reserves_token0)
        total_supply_token_1 = self.getTokenAmount(token1_address, reserves_token1)

        lp_price = (token0_priceUSD * total_supply_token_0 + token1_priceUSD * total_supply_token_1)/float(total_supply)

        percentage_token0 = (token0_priceUSD * total_supply_token_0) / (float(total_supply) * lp_price)
        percentage_token1 = (token1_priceUSD * total_supply_token_1) / (float(total_supply) * lp_price)

        
        # TODO: Same thing happens with _getTokenSymbol than with getTokenAmount
        lp_info = LpInfo(lp_address, Token(token0_address, self._getTokenSymbol(token0_address), token0_priceUSD), Token(token1_address, self._getTokenSymbol(token1_address), token1_priceUSD))
        lp_info.setPrice(lp_price)
        lp_info.setPercentageToken0(percentage_token0)
        lp_info.setPercetangeToken1(percentage_token1)

        return lp_info


    def getTokenInfo(self, address: str) -> Token:
        address = Web3.toChecksumAddress(address)
        token_price = self._getTokenPrice(address)
        symbol = self._getTokenSymbol(address)
        return Token(address, symbol, token_price)

    def getTokenAmount(self, address: str, amount: int) -> float:
        # We obtain the decimals in each token to place the comma
        # TODO: These function may raise an exception (in a try catch block)
        # TODO: Because contract is in a proxy (e.g. 0xb86AbCb37C3A4B64f74f59301AFF131a1BEcC787)
        # TODO: So functions are not callable
        decimals = self._getTokenDecimals(address)
        return float(amount / math.pow(10, decimals))

    def _getTokenPrice(self, token_address: str) -> float:
        price_request = 'https://deep-index.moralis.io/api/v2/erc20/' + token_address + '/price?chain=' + self.chain
        headers = {
            'x-api-key': MORALIS_API_KEY
        }
        response = requests.get(price_request, headers=headers)
        resp = response.json()
        token_priceUSD = resp['usdPrice']
        return token_priceUSD

    def _getTokenDecimals(self, token_address) -> int or None:
        token_abi = self._getContractAbi(token_address)
        try:
            token_decimals = self.web3.eth.contract(address=token_address, abi=token_abi).functions.decimals().call()
            return token_decimals
        except Exception:
            # Contract may be readed as proxy
            ##token_decimals = self.web3.eth.contract(address=token_address, abi=self._getProxyAbi(token_address, token_abi)).functions.decimals().call()
            ##return token_decimals
            return None

    def _getContractAbi(self, address: str ) -> str:
        if self.chain == Chains.FANTOM.value:
            return getContractAbiFTM(address)
        elif self.chain == Chains.BINANCE.value:
            return getContractAbiBSC(address)

    def _getTokenSymbol(self, token_address: str) -> str:
        token_abi = self._getContractAbi(token_address)
        token_symbol = self.web3.eth.contract(address=token_address, abi=token_abi).functions.symbol().call()
        return token_symbol
    
    def _getProxyAbi(self, address: str, abi: str) -> str:
        if self.chain == Chains.FANTOM.value:
            return getProxyAbiFTM(self.web3, address, abi)
        elif self.chain == Chains.BINANCE.value:
            return getProxyAbiBSC(self.web3, address, abi)
