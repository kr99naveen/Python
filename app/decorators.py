from typing import Callable, Any


def custom_fence(fence: str = "+"):
    def add_fence(fun):
        def wrapper(text: str):
            print(fence * (len(text) + 7))
            fun(text)
            print(fence * (len(text) + 7))

        return wrapper

    return add_fence


def fence(fun):
    def wrapper(text: str):
        print("-" * (len(text) + 7))
        fun(text)
        print("-" * (len(text) + 7))

    return wrapper


# decorator here is equivalent to
# log = fence(custom_fence("*")(log))
# decorator takes the function as arguemt and wrap it in some extra set of instructions
@fence  # this is pure decorator
@custom_fence(
    "*"
)  # this is not a decorator its kindoff function that returned a decorator
def log(text: str):
    print(f"{text} logged")


log("random string to print")

# simulate the route decorator

routes: dict[str, Callable[[Any], Any]] = {}


def route(path: str):
    def register_route(func):
        routes[path] = func
        return func

    return register_route


@route("/health")
def health():
    return {"health": 1, "status": "OK", "pod": "RUNNING"}


request: str = ""
while request != "quit":
    request = input(">>> ")
    if request in routes:
        response = routes[request]()
        print(response)
    elif request != "quit":
        print("Not Found")
