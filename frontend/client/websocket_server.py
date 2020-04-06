import websockets
import json
from .handle_function import handle_function
from .user_object import UserObject


async def client_server_handle_message(uobj, msg):
    """Unpackages a new message and sends it to the handler.

    Args:
        uobj: The client's UserObject
        msg: The new message (as a string)
    """
    params = json.loads(msg)
    func = params["func"]
    await handle_function(func, params, uobj)


async def client_server_new_message(uobj):
    """Read client messages.

    Args:
        uobj: The client's UserObject
    """
    while True:
        msg = await uobj.ws.recv()
        await client_server_handle_message(uobj, msg)


async def client_server(ws, path, storage):
    """Handle a new client connection.

    Args:
        ws: A websocket
        path: The websocket's connection path (unused)
        storage: A Storage
    """
    allCL = storage.all_cl
    checkCode = await ws.recv()

    if checkCode != "Hi, I'm a valid client.":
        ws.send("Invalid client check code.")
        print("Invalid client check code received.")
        return

    allCLL = UserObject(ws, storage.get_new_unique_clid(), storage)
    allCL.append(allCLL)

    print("New client. Total clients:", len(allCL))

    try:
        await client_server_new_message(allCLL)
    except websockets.exceptions.ConnectionClosed:
        print("WS ConnClosed")
    finally:
        allCL.remove(allCLL)
        print("Lost client. Clients remaining:", len(allCL))
