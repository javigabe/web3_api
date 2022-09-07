from .PancakeSwap import *
import time

try:
    BSC_PROVIDER = os.environ['BSC_PROVIDER']
except:
    BSC_PROVIDER = 'https://bsc-dataseed.binance.org/'


def get_user_info(address: str) -> Dict:
    start_time = time.time()

    pancake_v1 = PancakeSwapV1(BSC_PROVIDER).getUserLiquidity(address)
    pancake_v2 = PancakeSwapV2(BSC_PROVIDER).getUserLiquidity(address)

    print("--- BSC TOOK %s seconds ---" % (time.time() - start_time))

    return {
        'fantom': {
            'pancake_v1': pancake_v1,
            'pancake_v2': pancake_v2,
        }
    }

if __name__ == '__main__':
    print(get_user_info('0x3C6696a2347329517EC65b971e1dc5EF1bf2556e'))