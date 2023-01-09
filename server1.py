# simple websockets brocaster
import asyncio
import websockets
clients = []  # to store all connected cleints
lockSign = 0
owner = None

# handler for socket message activities


async def handler(websocket, path):
    global lockSign, owner
    # print(path) #path is not used currently
    userName = 'unknown'
    if websocket not in clients:
        clients.append(websocket)  # append new cleint to the array

    async for message in websocket:
        print(message, 'received from client')  # print to console
        msg = message.split("###")
        if msg[0] == 'LOGIN':
            userName = msg[1]
            print("set client name,", msg[1])
        elif message == 'GET':  # 想搶答
            print("GET", lockSign)
            if lockSign > 0:  # 被別人搶走
                await websocket.send('No')
            else:
                lockSign = 1
                owner = websocket  # 我是擁有者
                await websocket.send('YES')
        elif message == "DROP":
            if websocket == owner:  # 是否為搶到的人
                lockSign = 0
                await websocket.send('RELEASED')
            else:
                await websocket.send('You can not do that')
        else:  # 一般訊息，廣播出去
            await brocast(userName+"###"+message)


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
    websockets.serve(handler, 'localhost', 4545)
)  # hook to localhost:4545
loop.run_forever()  # keep it running
