
import asyncio
import numpy as np
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)



async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="serial:///dev/ttyUSB0")

    await drone.action.set_maximum_speed(0.5)

    asyncio.ensure_future(print_drone_position(drone))

    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(5)

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    #await asyncio.sleep(10)
    
    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    
    print("-- takeoff")

   
    await drone.offboard.set_position_ned(PositionNedYaw(0.0,0.0,-3.0,0.0))
    await asyncio.sleep(10)

    print("1.0,-1.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(1.0,-1.0,-3.0,30.0))
    await asyncio.sleep(5)
    print("1.0,-3.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(1.0,-3.0,-3.0,60.0))
    await asyncio.sleep(5)
    print("0.0,-4.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0,-4.0,-3.0,90.0))
    await asyncio.sleep(5)
    print("-3.0,-4.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(-3.0,-4.0,-3.0,120.0))
    await asyncio.sleep(5)
    print("-4.0,-3.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(-4.0,-3.0,-3.0,180.0))
    await asyncio.sleep(5)
    print("-4.0,-1.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(-4.0,-1.0,-3.0,210.0))
    await asyncio.sleep(5)
    print("-3.0,0.0,-3.0,0.0")
    await drone.offboard.set_position_ned(PositionNedYaw(-3.0,0.0,-3.0,0.0))
    await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
    await asyncio.sleep(5)
    
    print("--Landing")
    await drone.action.land()
    await asyncio.sleep(10)

async def print_drone_position(drone):

    async for angle in drone.telemetry.attitude_euler():
        print(f"pitch: {angle.pitch_deg},roll : {angle.roll_deg}, yaw: {angle.yaw_deg}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
