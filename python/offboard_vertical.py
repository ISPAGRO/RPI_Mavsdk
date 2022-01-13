
import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)



async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="serial:///dev/ttyUSB0")

    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(10)

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
    


    await drone.offboard.set_position_ned(PositionNedYaw(0.0,0.0,-5.0,0.0))
    await asyncio.sleep(10)
    


    
    
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
    await asyncio.sleep(10)
    
    print("--Landing")
    await drone.action.land()
    await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
