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


async def check(file_list_path):
    file_list = await stats.getFilesFromTxt(file_list_path)
    log.logger.info("Lecture des stats")
    jsonstr = open('/var/ids/db.json').read()
    check_dict = json.loads(jsonstr)
    await stats_compare(file_list, check_dict)
    
