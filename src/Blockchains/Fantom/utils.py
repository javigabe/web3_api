import requests
from web3 import Web3
import os.path

from keys import FTM_SCAN_API_KEY


def getContractAbiFTM(address: str) -> str or None:
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    filename = os.path.join(script_dir, 'abi/' + address)
    if (os.path.isfile(filename)):
        with open(filename, 'r') as f:
            abi = f.readline()
        return abi

    ABI_ENDPOINT = 'https://api.ftmscan.com/api?module=contract&action=getabi&address=' + address + '&apikey=' + FTM_SCAN_API_KEY
    response = requests.get(ABI_ENDPOINT)
    response_json = response.json()
    abi_json = response_json['result']

    with open(filename, 'w') as f:
        f.write(abi_json)
    
    return abi_json

def getProxyAbiFTM(web3: Web3, address: str, abi: str) -> str or None:
    contract = web3.eth.contract(address=address, abi=abi)
    proxy_contract = contract.functions.implementation().call()
    return getContractAbiFTM(proxy_contract)
