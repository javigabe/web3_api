from multiprocessing import Process, Queue
from typing import Dict, List, Tuple
import time

from .FantomWallet import *
from .SpookySwap import *
from .SpiritSwap import *
from ..WebProviders import get_provider
from ..Chains import Chains

def get_user_info(address: str, blockchain_queue: Queue) -> Dict:
    start_time = time.time()
    print("empieza fantom")

    FANTOM_PROVIDER = get_provider(Chains.FANTOM.value)

    platform_queue = Queue()
    available_platforms = [('fantom_wallet', FantomWallet(FANTOM_PROVIDER)), ('spooky_v2', SpookySwapV2(FANTOM_PROVIDER)),
                            ('spooky_v3', SpookySwapV3(FANTOM_PROVIDER)), ('spirit', SpiritSwap(FANTOM_PROVIDER))]

    processes = _run_platforms(address, available_platforms, platform_queue)
    
    platforms_info = {}
    for platform, process in processes:
        platform_info = platform_queue.get()
        process.join()
        platforms_info[platform] = platform_info


    print("--- FANTOM TOOK %s seconds ---" % (time.time() - start_time))

    blockchain_queue.put(
        {
            Chains.FANTOM.value: {
                platforms_info
            }
        }
    )

def _run_platforms(address: str, available_platforms: List[Tuple[str, object]], queue: Queue) -> List[Tuple[str, object]]:
    platform_process = []

    for platform_name, platform_object in available_platforms:
        print(platform_name)
        print(platform_object.getUserLiquidity)
        process = Process(target=platform_object.getUserLiquidity, args=(address, queue,))
        process.start()
        platform_process.append((platform_name, process))

    return platform_process


if __name__ == '__main__':
    print(get_user_info('0x3C6696a2347329517EC65b971e1dc5EF1bf2556e'))

