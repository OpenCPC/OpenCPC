import websockets
import asyncio
import pickle
import ssl
import json
import functools
from frontend.sps_comms.websocket_server import submissionProcessingServer
from frontend.submission_dispatch import submissionDispatchFunc, submissionDispatchIntervalFunc
from frontend.client.websocket_server import client_server
from frontend.csql import ConstantSQL
from frontend.storage import Storage

if __name__ == "__main__":
    with open("hub_config.json") as hub_config:
        config = json.load(hub_config)

    # Set up SQL
    sql = ConstantSQL()
    asyncio.get_event_loop().run_until_complete(sql.connect(config["database"]))

    # Set up storage
    storage = Storage(sql)

    # Set up SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(
        "/etc/letsencrypt/live/mcsc.enrog.com/cert.pem",
        keyfile="/etc/letsencrypt/live/mcsc.enrog.com/privkey.pem"
    )

    # Set up servers & tasks
    submission_processing_server_receive = websockets.serve(
        functools.partial(submissionProcessingServer, storage=storage), '0.0.0.0', 35123
    )
    client_server_receive = websockets.serve(
        functools.partial(client_server, storage=storage), '0.0.0.0', 80, ssl=ssl_context
    )
    submission_dispatch = asyncio.ensure_future(
        submissionDispatchFunc(storage)
    )
    submission_dispatch_interval = asyncio.ensure_future(
        submissionDispatchIntervalFunc(storage)
    )

    # Run until everything completes
    asyncio.get_event_loop().run_until_complete(submission_processing_server_receive)
    asyncio.get_event_loop().run_until_complete(client_server_receive)
    asyncio.get_event_loop().run_until_complete(submission_dispatch)
    asyncio.get_event_loop().run_until_complete(submission_dispatch_interval)
