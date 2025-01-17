import asyncio
import os
import json
import sys
import stats

async def statsToJson(stats_dict) -> None:
    try:
        os.makedirs('/var/ids', exist_ok=True)
        with open('/var/ids/db.json', 'w') as file:
            file.write(json.dumps(stats_dict, indent=4))
    except Exception as e:
        print(f'Error writing to stats.json: {str(e)}')

async def build(file_path_act):
    file_list = await stats.getFilesFromTxt(file_path_act)
    stats_dict = {}
    for file_path in file_list:
        stats_dict[file_path] = await stats.get_file_stats(file_path)
    for file_stats in stats_dict:
        print(f'Stats for {file_stats}:')
        print(stats_dict[file_stats])
    await statsToJson(stats_dict)