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

async def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    file_list_path = sys.argv[1]
    file_list = []
    try:
        with open(file_list_path, 'r') as file:
            file_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f'File not found: {file_list_path}')
        sys.exit(1)
    except Exception as e:
        print(f'Error reading file: {str(e)}')
        sys.exit(1)
    stats_dict = {}
    for file_path in file_list:
        stats_dict[file_path] = await stats.get_file_stats(file_path)
    for file_stats in stats_dict:
        print(f'Stats for {file_stats}:')
        print(stats_dict[file_stats])
    await statsToJson(stats_dict)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)