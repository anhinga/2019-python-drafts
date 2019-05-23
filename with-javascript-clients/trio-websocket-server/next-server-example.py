import trio
from trio_websocket import serve_websocket, ConnectionClosed
import sys
import names

class SetOfNames:

    def __init__(self, server_name):
        self.server_name = server_name
        self.dict_of_names = {}

who_is_who = SetOfNames('Server Ben')
        
async def echo_server(request):
    print("ECHO SERVER")
    ws = await request.accept()
    while True:
        client_name = names.get_full_name()
        if client_name not in who_is_who.dict_of_names:
            who_is_who.set_of_names = who_is_who.dict_of_names[client_name] = ws
            print("KNOWN NAMES: ", set(who_is_who.dict_of_names.keys())) 
            print("PRESENT NAMES: ", [a for a in list(who_is_who.dict_of_names.keys()) if who_is_who.dict_of_names[a]])
            print("NEW CLIENT: ", client_name)
            break
    await ws.send_message("From " + who_is_who.server_name + ": Your name is " + client_name)
    while True:
        try:
            message = await ws.get_message()
            print(message + " (message from " + client_name + ")")
            await ws.send_message(message + " (" + who_is_who.server_name + " sending back to " + client_name + ")")
            if message == "Stop Server":
                for a in list(who_is_who.dict_of_names.keys()):
                    a_ws = who_is_who.dict_of_names[a]
                    if a_ws:                    
                        await a_ws.send_message("SERVER EXITING (by " + client_name + " request)")
                sys.exit()
        except ConnectionClosed:
            who_is_who.dict_of_names[client_name] = None
            break

async def main():
    await serve_websocket(echo_server, '127.0.0.1', 8060, ssl_context=None)

trio.run(main)
