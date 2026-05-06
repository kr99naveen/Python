import time


def endpoint(route):
    print(f"handling route ${route}")
    time.sleep(1)
    print("response for route ${route}")


def server():
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=1",
        "POST /shipment",
        "DELETE /shipment?id=1",
    )

    for route in tests:
        endpoint(route)


server()
