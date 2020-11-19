import json
import asyncio
import websockets
import importlib
import serverparsers
from websockets.protocol import WebSocketCommonProtocol

parser = serverparsers.WebParser("data.db")

async def handle(websocket:WebSocketCommonProtocol, path):

    print(f"Received from {path}")
    importlib.reload(serverparsers)

    try:

        #Get the data from the webpage
        data = await websocket.recv()
        parsed_data = json.loads(data)
        result = parser.parse(parsed_data)
        await websocket.send(result)

    except (websockets.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
        print(f"Disconnected {path}")

if __name__ == "__main__":
    start_server = websockets.serve(handle, "localhost", 8080)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
