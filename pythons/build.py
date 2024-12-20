import asyncio
import aiofiles
import os
import json
import log
import sys

async def get_file_stats(file_path) -> dict:
    try:
        async with aiofiles.open(file_path, 'r') as file:
            file_size = os.path.getsize(file_path)
            file_stats = os.stat(file_path)
            return {
                'file_size': file_size,
                'creation_time': file_stats.st_ctime,
                'modification_time': file_stats.st_mtime,
                'owner': file_stats.st_uid,
                'owner_group': file_stats.st_gid,
            }
    except FileNotFoundError:
        return {
            'error': f'File not found: {file_path}'
        }
    except Exception as e:
        return {
            'error': str(e)
        }

async def statsToJson(stats_dict) -> None:
    try:
        os.makedirs('/var/ids', exist_ok=True)
        with open('/var/ids/db.json', 'w') as file:
            await file.write(json.dumps(stats_dict, indent=4))
    except Exception as e:
        print(f'Error writing to stats.json: {str(e)}')

async def main():
    if len(sys.argv) != 2:
        print('Usage: python check.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    stats = await get_file_stats(file_path)
    print(stats)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info('Interrupted by user')
        sys.exit(1)