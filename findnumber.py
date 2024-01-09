import websockets, asyncio, json

playerslist = [] 
roomslist = []
def PlayersList(action, username, current = None):
    if action == "View":
        return playerslist
    if action == "Add":
        if username in playerslist:
            return None
        playerslist.append(username)
        return playerslist
    if action == "Remove":
        playerslist.remove(username)
        return playerslist
    if action == "Change":
        playerslist.remove(current)
        playerslist.append(username)
        return playerslist


async def handler(websocket):
    async for message in websocket:
        message = json.loads(message)
        if(message["type"] == "player"):
            try:
                playerslist = PlayersList(message["action"], message["username"], message["current"])
            except:
                playerslist = PlayersList(message["action"], message["username"])
            if playerslist == None:
                await websocket.send("Username already taken")
            else:
                await websocket.send(json.dumps(playerslist))

        


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())