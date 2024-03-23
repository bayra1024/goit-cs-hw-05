import argparse
import asyncio
import aiofiles
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(src_path, dest_path):
    try:
        extension = src_path.suffix[1:]
        target_dir = dest_path / extension
        target_dir.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(src_path, "rb") as src_file:
            content = await src_file.read()

        target_file = target_dir / src_path.name
        async with aiofiles.open(target_file, "wb") as dest_file:
            await dest_file.write(content)
    except Exception as e:
        logging.error(f"Error copying file {src_path}: {e}")


async def read_dir(src_path, dest_path):
    for path in src_path.rglob("*.*"):
        if path.is_file():
            await copy_file(path, dest_path)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sort files by extension asynchronously."
    )
    parser.add_argument(
        "src_dir",
        type=str,
        nargs="?",
        default="./Lib",
        help="Шлях до вихідної директорії",
    )
    parser.add_argument(
        "dest_dir",
        type=str,
        nargs="?",
        default="./sorted_files",
        help="Шлях до директорії призначення",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    src_path = Path(args.src_dir)
    dest_path = Path(args.dest_dir)

    asyncio.run(read_dir(src_path, dest_path))


if __name__ == "__main__":
    main()
