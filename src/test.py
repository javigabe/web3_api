import time
from web3 import Web3


from PriceCalculator import PriceCalculator
from Blockchains.Binance_Smart_Chain.PancakeSwap import PancakeSwapV1, PancakeSwapV2
from Blockchains.Fantom.SpookySwap import SpookySwapV2, SpookySwapV3
from Blockchains.Fantom.SpiritSwap import SpiritSwap
from model import *


start_time = time.time()

pancake = PancakeSwapV2('https://bsc-dataseed.binance.org/')
length = pancake.poolLength()

web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
price_calculator = PriceCalculator(web3, 'binance')

for i in range(0, length):
    if ((amount := pancake.userInfo(i, '0x13Be1cb3648874A2d741119810f7e24884197a2F')[0]) != 0):
        lptoken = pancake.lpToken(i)
        lpTokens = Web3.fromWei(amount, 'ether')
        try:
            print(i)
            print(float(lpTokens)*price_calculator.getLpInfo(lptoken).get_price())
        except Exception:
            print("Ha habido un error calculando el precio del LP")

print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()

spooky = SpookySwapV2('wss://fantom-mainnet.public.blastapi.io/')

poolLength = spooky.poolLength()
web3 = Web3(Web3.WebsocketProvider('wss://fantom-mainnet.public.blastapi.io/'))
price_calculator = PriceCalculator(web3, 'fantom')

for i in range(0, poolLength):
    if ((amount := spooky.userInfo(i, '0x3C6696a2347329517EC65b971e1dc5EF1bf2556e')[0]) != 0):
        lpToken = spooky.lpToken(i)
        lpTokens = Web3.fromWei(amount, 'ether')
        lpInfo = price_calculator.getLpInfo(lpToken)
        print("TIENES UN LP FORMADO DE:")
        print("Token 1: " + lpInfo.get_token0().getName())
        print("Token 2: " + lpInfo.get_token1().getName())
        print("Por un valor de: ", float(lpTokens)*lpInfo.get_price())


print("--- %s seconds ---" % (time.time() - start_time))