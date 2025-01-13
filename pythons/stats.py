import aiofile
import os
import datetime as dt
import hashlib
import pwd
import grp
import sys
import asyncio

async def get_file_hash(file_path, hashCode) -> str:
    try:
        async with aiofile.async_open(file_path, 'rb') as file:
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

async def getFilesFromTxt(file_path) -> list:
    print(file_path)
    with await aiofile.async_open(file_path, 'r') as f:
        print(await f.readline())

async def get_files_from_directory(directory_path) -> list:
    try:
        files = []

        for entry in os.scandir(directory_path):
            if entry.is_file():
                files.append(entry.path)
            elif entry.is_dir():
                files.extend(await get_files_from_directory(entry.path))
            else:
                continue
        return files
    except FileNotFoundError:
        return {
            'error': f'Directory not found: {directory_path}'
        }
    except Exception as e:
        return {
            'error': str(e)
        }

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

async def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    await getFilesFromTxt(sys.argv[1])
    directory_path = sys.argv[1]
    files = await get_files_from_directory(directory_path)
    print(files)
    for file_path in files:
        stats_dict = await get_file_stats(file_path)
        print(stats_dict)
        if 'error' not in stats_dict:
            print(f'Stats for {file_path}:')
            print(stats_dict)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)