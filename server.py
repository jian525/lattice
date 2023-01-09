# simple websockets brocaster
import asyncio
import websockets
clients = []  # to store all connected cleints

# handler for socket message activities


async def handler(websocket, path):
    # print(path) #path is not used currently
    if websocket not in clients:
        handle = [websocket, 'unknown']
        clients.append(handle)
        userName = 'unknown'
        # clients.append(websocket)  # append new cleint to the array

    else:
        userName = getClientName(websocket)
    async for message in websocket:
        print(message, 'received from client')  # print to console
        msg = message.split("###")
        if msg[0] == 'LOGIN':
            setClientName(websocket, msg[1])  # 當作特別的事
            print("set client name ", msg[1])
        else:
            brocast(message)  # send message to all clents


def getClientName(obj):
    for h in clients:
        if h[0] == obj:
            return h[1]
    return 'unkown'


def setClientName(sock, nickname):
    for h in clients:
        if h[0] == sock:
            h[1] = nickname
            return


async def brocast(msg):
    print(msg, ' brocasting')  # print to console

    # iterate the clients
    for websock in clients:
        try:
            await websock.send(msg)  # send message to each client
        except websockets.exceptions.ConnectionClosed:
            # remove the client when it disconnects
            print("Client disconnected.  Do cleanup")
            clients.remove(websock)
            # pass

# starts the service and run forever
loop = asyncio.new_event_loop()  # get an event loop
asyncio.set_event_loop(loop)  # set the event loop to asyncio

loop.run_until_complete(
    # setup the websocket service and handler
    websockets.serve(handler, 'localhost', 4040)
)  # hook to localhost:4545
loop.run_forever()  # keep it running
