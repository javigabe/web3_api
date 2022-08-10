import math
from multiprocessing import pool
import time
from web3 import Web3


from PriceCalculator import PriceCalculator
from Blockchains.Binance_Smart_Chain.PancakeSwap import PancakeSwapV1, PancakeSwapV2
from Blockchains.Fantom.SpookySwap import SpookySwapV2, SpookySwapV3
from Blockchains.Fantom.SpiritSwap import SpiritSwap
from Blockchains.Fantom.FantomWallet import FantomWallet
from model.LpInfo import LpInfo
from model.Token import Token


start_time = time.time()

pancake = PancakeSwapV2('https://bsc-dataseed.binance.org/')
length = pancake.poolLength()

web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
price_calculator = PriceCalculator(web3, 'binance')

"""for i in range(0, length):
    if ((amount := pancake.userInfo(i, '0x13Be1cb3648874A2d741119810f7e24884197a2F')[0]) != 0):
        lptoken = pancake.lpToken(i)
        lpTokens = Web3.fromWei(amount, 'ether')
        try:
            print(i)
            print(float(lpTokens)*price_calculator.getLpInfo(lptoken).get_price())
        except Exception:
            print("Ha habido un error calculando el precio del LP")

print("--- %s seconds ---" % (time.time() - start_time))
"""

"""start_time = time.time()

spooky = SpookySwapV2('wss://fantom-mainnet.public.blastapi.io/')

poolLength = spooky.poolLength()
web3 = Web3(Web3.WebsocketProvider('wss://fantom-mainnet.public.blastapi.io/'))
price_calculator = PriceCalculator(web3, 'fantom')

for i in range(0, poolLength):
    if ((amount := spooky.userInfo(i, '0x3C6696a2347329517EC65b971e1dc5EF1bf2556e')[0]) != 0):
        lpToken = spooky.lpToken(i)
        lpTokens = float(Web3.fromWei(amount, 'ether'))
        lpInfo = price_calculator.getLpInfo(lpToken)

        lpInfo.setAmountToken0(lpInfo.getPrice()/(2*lpInfo.getToken0().getPrice())*lpTokens)
        lpInfo.setAmountToken1(lpInfo.getPrice()/(2*lpInfo.getToken1().getPrice())*lpTokens)

        print("TIENES UN LP FORMADO DE:")
        print("Token 1: " + lpInfo.getToken0().getName() + "\tAMOUNT: " , lpInfo.getAmountToken0())
        print("Token 2: " + lpInfo.getToken1().getName() + "\tAMOUNT: " , lpInfo.getAmountToken1())
        print("Por un valor de: ", lpTokens*lpInfo.getPrice())


print("--- %s seconds ---" % (time.time() - start_time))
"""

start_time = time.time()

fantom = FantomWallet('wss://fantom-mainnet.public.blastapi.io/')

poolLength = fantom.poolLength()
web3 = Web3(Web3.WebsocketProvider('wss://fantom-mainnet.public.blastapi.io/'))
price_calculator = PriceCalculator(web3, 'fantom')

fantom_token = Token(fantom.getTokenAddress(), 'WFTM', price_calculator.getTokenPrice(fantom.getTokenAddress()))
fantom_decimals = price_calculator.getTokenDecimals(fantom_token.getTokenAddress())
dollars = 0
for i in range(0, poolLength):
    if ((amount := fantom.getStake(i, '0x3C6696a2347329517EC65b971e1dc5EF1bf2556e')) != 0):
        print("Staked in node: ", i)
        tokens = amount / math.pow(10, fantom_decimals)
        print("Amount: ", tokens)
        print("Value in dollars: ", tokens*fantom_token.getPrice())
        print("\n\n\n")
        dollars += tokens*fantom_token.getPrice()
print("Total amount in dollars: ", dollars)
print("--- %s seconds ---" % (time.time() - start_time))
