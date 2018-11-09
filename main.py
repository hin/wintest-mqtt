from aiowintest import WintestProtocol
import asyncio
import sys

import pprint

async def on_summary(summary):
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(summary)

async def on_gab(gab):
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(gab)

async def main(argv):
    loop = asyncio.get_event_loop()
    local_addr = ('0.0.0.0', 9871)
    broadcast_addr = ('192.168.11.255', 9000)
    wt = WintestProtocol(loop, local_addr, broadcast_addr)
    wt.add_handler('summary', on_summary)
    wt.add_handler('gab', on_gab)
    #await proto._connect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.run_forever()
    loop.close()
