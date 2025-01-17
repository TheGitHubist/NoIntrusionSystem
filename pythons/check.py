import asyncio
import aiofile
import os
import log
import build
import stats
import sys
import json


async def stats_compare(files : list, check_dict : dict):
    stat_dict = {}
    compteur = 0
    pfile = []
    log.logger.info("Comparaison des stats")
    for file_name in files:       
        stat_dict[file_name] = await stats.get_file_stats(file_name)
        if stat_dict[file_name] == check_dict[file_name]:
            continue
        else :
            log.logger.CRITICAL("probleme")
            compteur += 1
            pfile.append(file_name)
            
    if compteur != 0:
        log.logger.CRITICAL(f"this files have problem : {pfile}")
    else:
        log.logger.info("pas de probleme")


async def main():

    if len(sys.argv) != 2:
        sys.exit(1)
    file_list_path = sys.argv[1]
    file_list = []
    log.logger.info("Lecture des stats")
    await build.build(sys.argv[1])
    with open(file_list_path, 'r') as file:
        file_list = [line.strip() for line in file.readlines()]
    jsonstr = open('/var/ids/db.json').read()
    check_dict = json.loads(jsonstr)
    await stats_compare(file_list, check_dict)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)