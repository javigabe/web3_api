from web3 import Web3
import requests
import math

from Blockchains.Fantom.utils import getContractAbiFTM, getProxyAbiFTM
from Blockchains.Binance_Smart_Chain.utils import getContractAbiBSC, getProxyAbiBSC
from model.LpInfo import LpInfo
from model.Token import Token


# TODO: REMOVE KEY FROM HERE
MORALIS_API_KEY = 'SNXINaRtMzipLwPc4pPYUhfmY3CeiPv8K03UbHTqqhzWTUIXnJsbKGUKtXX4jHOT'

class PriceCalculator:

    def __init__(self, web3: Web3, chain: str):
        # Web3 instance and chain name
        self.web3 = web3
        self.chain = chain

    def getLpInfo(self, lp_address: str) -> LpInfo:
        contract = self.web3.eth.contract(address=lp_address, abi=self._getContractAbi(lp_address))

        # Token0 contract
        token_0 = contract.functions.token0().call()
        # Token 1 contract
        token_1 = contract.functions.token1().call()      

        # We obtain the supply of token0 and token1 in the lp
        reserves = contract.functions.getReserves().call()

        # We obtain the total supply of the lp token
        total_supply = Web3.fromWei(contract.functions.totalSupply().call(), 'ether')

        # Transform token contract addresses to checksum
        token0_address = Web3.toChecksumAddress(token_0)
        token1_address = Web3.toChecksumAddress(token_1)

        # We obtain the decimals in each token to place the comma
        # TODO: These function may raise an exception (in a try catch block)
        # TODO: Because contract is in a proxy (e.g. 0xb86AbCb37C3A4B64f74f59301AFF131a1BEcC787)
        # TODO: So functions are not callable
        token0_decimals = self._getTokenDecimals(token0_address)
        token1_decimals = self._getTokenDecimals(token1_address)
       
        # We obtain the price of both tokens in USD
        token0_priceUSD = self._getTokenPrice(token0_address)
        token1_priceUSD = self._getTokenPrice(token1_address)

        total_supply_token_0 = reserves[0] / math.pow(10, token0_decimals)
        total_supply_token_1 = reserves[1] / math.pow(10, token1_decimals)

        lp_price = (token0_priceUSD * float(total_supply_token_0) + token1_priceUSD * float(total_supply_token_1))/float(total_supply)
        
        # TODO: Same thing happens with _getTokenSymbol than explained before
        lp_info = LpInfo(lp_address, Token(token0_address, self._getTokenSymbol(token0_address)), Token(token1_address, self._getTokenSymbol(token1_address)))
        lp_info.set_price(lp_price)
        lp_info.setAmountToken0(total_supply_token_0)
        lp_info.setAmountToken1(total_supply_token_1)

        return lp_info


    def getTokenPrice(self, token_address: str) -> float:
        price_request = 'https://deep-index.moralis.io/api/v2/erc20/' + token_address + '/price?chain=' + self.chain
        headers = {
            'x-api-key': MORALIS_API_KEY
        }
        response = requests.get(price_request, headers=headers)
        resp = response.json()
        token_priceUSD = resp['usdPrice']
        return token_priceUSD

    def _getContractAbi(self, address: str ) -> str:
        if self.chain == 'fantom':
            return getContractAbiFTM(address)
        elif self.chain == 'binance':
            return getContractAbiBSC(address)

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

    def _getProxyAbi(self, address: str, abi: str) -> str:
        if self.chain == 'fantom':
            return getProxyAbiFTM(self.web3, address, abi)
        elif self.chain == 'binance':
            return getProxyAbiBSC(self.web3, address, abi)

    def _getTokenSymbol(self, token_address: str) -> str:
        token_abi = self._getContractAbi(token_address)
        token_symbol = self.web3.eth.contract(address=token_address, abi=token_abi).functions.symbol().call()
        return token_symbol
