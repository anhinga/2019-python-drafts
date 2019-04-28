import trio
from trio_websocket import serve_websocket, ConnectionClosed

async def echo_server(request):
    print("ECHO SERVER")
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            print(message)
            await ws.send_message(message + " (sending back)")
        except ConnectionClosed:
            break

async def main():
    await serve_websocket(echo_server, '127.0.0.1', 8060, ssl_context=None)

trio.run(main)
