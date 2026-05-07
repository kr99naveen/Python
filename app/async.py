import time
import asyncio


# def endpoint(route):
async def endpoint(route) -> str:
    print(f"handling route ${route}")
    # time.sleep(1)
    await asyncio.sleep(3)
    print(f"response for route ${route}")
    return f"{route} ::: success"


# def server():
async def server():
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=1",
        "POST /shipment",
        "DELETE /shipment?id=1",
    )

    begin = time.perf_counter()

    ###########################################directly calling with await(makes sync)
    # for route in tests:
    #     res = await endpoint(route)
    #     print(f"response for {route} :::: ", res)

    ###########################################calling using creating async tasks with asyncio
    # requests = [asyncio.create_task(endpoint(route)) for route in tests]

    # done, pending = await asyncio.wait(requests)

    # for task in done:
    #     print("Result task :: ", task.result())

    ###########################################calling by Taskgroup, managed through context
    async with asyncio.TaskGroup() as task_group:
        tasks = [task_group.create_task(endpoint(route)) for route in tests]
        for result in tasks:
            print(await result)

    end = time.perf_counter()

    print(f"time taken ::: {end - begin:.2f} seconds")


# server()
asyncio.run(server())
