import asyncio
import aiofiles
import os
import json
import datetime as dt
import sys
import hashlib
import pwd
import grp

async def get_file_hash(file_path, hashCode) -> str:
    try:
        async with aiofiles.open(file_path, 'rb') as file:
            hash = None
            if hashCode == 'md5':
                hash = hashlib.md5()
            elif hashCode == 'sha512':
                hash = hashlib.sha512()
            elif hashCode == 'sha256':
                hash = hashlib.sha256()
            else:
                raise ValueError(f'Unsupported hash: {hash}')
            while True:
                data = await file.read(8192)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()
    except FileNotFoundError:
        return {
            'error': f'File not found: {file_path}'
        }
    except Exception as e:
        return {
            'error': str(e)
        }

async def format_datetime(date_time:dt) -> str:
    return date_time.strftime(f'%d/%m/%Y - %H:%M:%S')

async def get_file_stats(file_path) -> dict:
    try:
        async with aiofiles.open(file_path, 'r') as file:
            file_size = os.path.getsize(file_path)
            file_stats = os.stat(file_path)
            return {
                'md5_hash': await get_file_hash(file_path, 'md5'),
                'sha512_hash': await get_file_hash(file_path, 'sha512'),
                'sha256_hash': await get_file_hash(file_path, 'sha256'),
                'file_size': file_size,
                'creation_time': await format_datetime(dt.datetime.fromtimestamp(file_stats.st_ctime)),
                'modification_time': await format_datetime(dt.datetime.fromtimestamp(file_stats.st_mtime, tz = dt.timezone.utc)),
                'owner': pwd.getpwuid(file_stats.st_uid).pw_name,
                'owner_group': grp.getgrgid(file_stats.st_gid).gr_name,
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
        stats_dict[file_path] = await get_file_stats(file_path)
    for file_stats in stats_dict:
        print(f'Stats for {file_stats}:')
        print(stats_dict[file_stats])

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)