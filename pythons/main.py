import build
import check
import os
import sys
import asyncio
import log

async def main() :
    if len(sys.argv) != 2:
        sys.exit(1)
    if os.path.isfile("/var/ids/db.json"):
        await check.check(sys.argv[1])
    else:
        await build.build(sys.argv[1])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)