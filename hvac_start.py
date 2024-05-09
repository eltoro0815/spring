import aiohttp
import asyncio

from renault_api.renault_client import RenaultClient

import logging
import os

from dotenv import load_dotenv

load_dotenv()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# better logging
#class LoggingClientSession(aiohttp.ClientSession):
#    async def _request(self, method, url, **kwargs):
        # print('Starting request: ', method, url, kwargs)
#        return await super()._request(method, url, **kwargs)


async def main():

    #async with LoggingClientSession() as websession:
    async with aiohttp.ClientSession() as websession:
        client = RenaultClient(websession=websession, locale="de_DE")
        await client.session.login(os.getenv('user'), os.getenv('password'))

        account_id = os.getenv('account_id')
        account = await client.get_api_account(account_id)

        vin = os.getenv('vin')
        vehicle = await account.get_api_vehicle(vin)

        response = await vehicle.set_ac_start(temperature=21)
        print(response)



print(f"{bcolors.OKBLUE}Warten auf Antwort ...{bcolors.ENDC}")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
