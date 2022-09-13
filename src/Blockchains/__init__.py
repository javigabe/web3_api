from typing import Callable, Dict, List
from web3 import Web3
from multiprocessing import Process, Queue


from .config import Config as _
from .Fantom import get_user_info as fantom_info
from .Binance_Smart_Chain import get_user_info as binance_info
from .WebProviders import get_provider
from .PriceCalculator import PriceCalculator
from model.LpInfo import LpInfo
from model.Token import Token



def get_all_liquidity_by_user(address: str) -> Dict:
    queue = Queue()
    available_blockchains = [fantom_info, binance_info]
    processes = _run_blockchains(address, available_blockchains, queue)

    user_blockchains_info = {}
    for process in processes:
        chain_info = queue.get()
        
        for chain in chain_info:
            user_blockchains_info[chain] = _get_balances(chain_info[chain], chain)
        process.join()

    return {'blockchains': user_blockchains_info}

def _run_blockchains(address: str, available_blockchains: List[Callable], queue: Queue) -> List[Process]:
    processes = []

    for blockchain in available_blockchains:
        process = Process(target=blockchain, args=(address, queue,))
        process.start()
        processes.append(process)

    return processes

def _get_balances(chain_user_info: Dict, chain: str) -> Dict:
    price_calculator = PriceCalculator(get_provider(chain), chain)
    for platform in chain_user_info.keys():
        platform_user_info = chain_user_info[platform]['user_liquidity']
        
        for index, token in enumerate(platform_user_info):
            if token['is_lp'] == 'True':
                lp_tokens = float(Web3.fromWei(token['amount'], 'ether'))
                reward_debt = price_calculator.getTokenAmount(token['token_address'], token['reward_debt'])
                lp_info: LpInfo = price_calculator.getLpInfo(token['token_address'])

                # We update the value of amount and reward debt with readable values
                chain_user_info[platform]['user_liquidity'][index]['amount'] = lp_tokens
                chain_user_info[platform]['user_liquidity'][index]['reward_debt'] = reward_debt

                chain_user_info[platform]['user_liquidity'][index]['dollar_value'] = lp_info.getPrice() * lp_tokens
                
                # We merge the token Dict with the lp info Dict
                chain_user_info[platform]['user_liquidity'][index].update(lp_info.toJson(lp_tokens))
            else:
                token_info: Token = price_calculator.getTokenInfo(token['token_address'])
                token_amount = price_calculator.getTokenAmount(token['token_address'], token['amount'])
                reward_debt = price_calculator.getTokenAmount(token['token_address'], token['reward_debt'])

                # We update the value of amount and reward debt with readable value
                chain_user_info[platform]['user_liquidity'][index]['amount'] = token_amount
                chain_user_info[platform]['user_liquidity'][index]['reward_debt'] = reward_debt

                chain_user_info[platform]['user_liquidity'][index]['dollar_value'] = token_info.getPrice() * token_amount
                chain_user_info[platform]['user_liquidity'][index]['symbol'] = token_info.getName()

    return chain_user_info