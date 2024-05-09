import aiohttp
import asyncio

from renault_api.renault_client import RenaultClient

import reverse_geocode

from dateutil import parser
from datetime import datetime
from dateutil import tz

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
        #print(f"Accounts: {await client.get_person()}") # List available accounts, make a note of kamereon account id

        account_id = os.getenv('account_id')
        account = await client.get_api_account(account_id)
        #print(f"Vehicles: {await account.get_vehicles()}") # List available vehicles, make a note of vehicle VIN

        vin = os.getenv('vin')
        vehicle = await account.get_api_vehicle(vin)
        cockpit_infos = await vehicle.get_cockpit()
        battery_status = await vehicle.get_battery_status()
        hvac = await vehicle.get_hvac_status()
        location = await vehicle.get_location()



        #from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Germany/Berlin')

        print(
            f"{bcolors.OKGREEN}Last updated: {parser.parse(battery_status.timestamp).astimezone(to_zone):%d.%m.%y, %H:%M}{bcolors.ENDC}"
        )

        print(
            f"{bcolors.OKGREEN}Kilometer total: {cockpit_infos.totalMileage}km{bcolors.ENDC}"
        )

        print(
            f"{bcolors.OKCYAN}Batterie: {battery_status.batteryLevel}%{bcolors.ENDC}"
        )
        print(
            f"{bcolors.OKGREEN}Lade-Status: {battery_status.get_charging_status()}{bcolors.ENDC}"
        )

        coordinates = (location.gpsLatitude, location.gpsLongitude),
        print(
            f"{bcolors.OKGREEN}Nähester Ort: {reverse_geocode.search(coordinates)[0]['city']}{bcolors.ENDC}"
        )
        print(
            f"{bcolors.OKGREEN}GPS last updated: {parser.parse(location.lastUpdateTime).astimezone(to_zone):%d.%m.%y, %H:%M}{bcolors.ENDC}"
        )

        print(
            f"{bcolors.OKGREEN}GPS: {location.gpsLatitude,location.gpsLongitude}{bcolors.ENDC}"
        )

        print(
            f"{bcolors.OKGREEN}Lüftung/Klima: {hvac.hvacStatus}{bcolors.ENDC}"
        )

print(f"{bcolors.OKBLUE}Warten auf Antwort ...{bcolors.ENDC}")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
