import os
from .Fantom import get_user_info
from .Binance_Smart_Chain import get_user_info
from model import Token, LpInfo

def run_config():
    os.environ['FANTOM_PROVIDER'] = 'wss://fantom-mainnet.public.blastapi.io/'
    os.environ['BSC_PROVIDER'] = 'https://bsc-dataseed.binance.org/'

if __name__ == '__main__':
    run_config()
