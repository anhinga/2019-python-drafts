import trio
from trio_websocket import open_websocket_url


async def main():
    try:
        async with open_websocket_url('ws://127.0.0.1:8060/ws') as ws:
            await ws.send_message('hello world!')
            message = await ws.get_message()
            print('Received message: %s' % message)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose)

trio.run(main)
