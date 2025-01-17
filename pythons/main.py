import build
import check
import os
import sys
import asyncio
import log

async def main() :
    log.logger.info("Initialisation")
    if len(sys.argv) != 2:
        sys.exit(1)
    if os.path.isfile("/var/ids/db.json"):
        log.logger.info("Check launch")
        await check.check(sys.argv[1])
    else:
        log.logger.info("Build launch")
        await build.build(sys.argv[1])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)