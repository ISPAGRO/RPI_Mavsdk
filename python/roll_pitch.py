#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)


async def run():
    """ Does Offboard control using attitude commands. """

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

    asyncio.ensure_future(print_drone_position(drone))

    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(5)

    print("-- Setting initial setpoint")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))

  #  async for flight_mode in drone.telemetry.flight_mode():
   #     print("FlightMode:", flight_mode)

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return


    print("-- takeoff")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.46))
    await asyncio.sleep(5)

    print("-- trying to find hover throttle")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.45))
    await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
              {error._result.result}")

    print("--Landing")
    await drone.action.land()
    await asyncio.sleep(10)   

async def print_drone_position(drone):

    async for angle in drone.telemetry.attitude_euler():
        print(f"pitch: {angle.pitch_deg},roll : {angle.roll_deg}, yaw: {angle.yaw_deg}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
