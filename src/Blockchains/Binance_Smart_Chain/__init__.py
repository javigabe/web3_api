import time
from multiprocessing import Queue

from .PancakeSwap import *
from ..Chains import Chains
from ..WebProviders import get_provider

def get_user_info(address: str, queue: Queue) -> Dict:
    start_time = time.time()
    print("empieza binance")

    BINANCE_PROVIDER = get_provider(Chains.BINANCE.value)

    pancake_v1 = PancakeSwapV1(BINANCE_PROVIDER).getUserLiquidity(address)
    pancake_v2 = PancakeSwapV2(BINANCE_PROVIDER).getUserLiquidity(address)

    print("--- BSC TOOK %s seconds ---" % (time.time() - start_time))

    return queue.put(
        { 
            Chains.BINANCE.value: {
                'pancake_v2': pancake_v2,
                'pancake_v1': pancake_v1,
            }
        }
    )

if __name__ == '__main__':
    print(get_user_info('0x3C6696a2347329517EC65b971e1dc5EF1bf2556e'))