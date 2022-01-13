
import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)



async def run():
    """ Does Offboard control using position NED coordinates. """

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


    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    #await asyncio.sleep(10)
    
    print("-- Starting offboard")
    try:
        await drone.offboard.start()
        await asyncio.sleep(10)
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    

    print("-- go up 5m")

    await drone.offboard.set_position_ned(PositionNedYaw(0.0,0.0,-5.0,0.0))
    await asyncio.sleep(10)   


    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
    await asyncio.sleep(5)
    
    print("--Landing")
    await drone.action.land()
    await asyncio.sleep(10)

    print("-- DisArming")
    await drone.action.disarm()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
