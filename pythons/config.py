import asyncio
import os
import json
import sys
import log

async def build_conf(file_path, log_level):
    conf_dict = {}
    conf_dict[file_path] = log_level
    try:
        os.makedirs('/etc/ids', exist_ok=True)
        with open('/etc/ids/config.json', 'a') as file:
            file.write(json.dumps(conf_dict, indent=4))
    except Exception as e:
        log.logger.error(f'Error writing to stats.json: {str(e)}')