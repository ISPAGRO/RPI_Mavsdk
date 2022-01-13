#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyUSB0")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        latitude = terrain_info.latitude_deg
        longitude = terrain_info.longitude_deg
        break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off to 5 m and stay for 10 seconds")

    # To fly drone 10m above the ground plane serial:///dev/ttyUSB0 udp://:14540
    flying_alt = absolute_altitude + 5
    flying_alt_1 = flying_alt - 1.0
    flying_alt_2 = flying_alt_1 - 2.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(latitude, longitude, flying_alt, 90) 

    await asyncio.sleep(5)
    
    print("-- descend to 4 m and stay for 10 sec")
    await drone.action.goto_location(latitude, longitude, flying_alt_1, 90) 

    await asyncio.sleep(5)

    print("-- descend to 2 m and stay for 10 sec")
    await drone.action.goto_location(latitude, longitude, flying_alt_2, 90)

    await asyncio.sleep(5)

    print("-- land")
    await drone.action.land()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
