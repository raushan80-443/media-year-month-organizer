from pathlib import Path
from datetime import datetime
import shutil
import sys


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".heic",
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".zip",
    ".7z",
    ".thumb",
    ".thm",
    ".thumbnail",
}

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    Image = None


def get_exif_date(path: Path):
    if Image is None:
        return None

    try:
        with Image.open(path) as img:
            exif = img.getexif()
            if not exif:
                return None

            exif_data = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

            for key in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
                if key in exif_data:
                    return datetime.strptime(exif_data[key], "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None

    return None


def get_file_date(path: Path):
    exif_date = get_exif_date(path)
    if exif_date:
        return exif_date

    stat = path.stat()

    if hasattr(stat, "st_birthtime"):
        return datetime.fromtimestamp(stat.st_birthtime)

    return datetime.fromtimestamp(stat.st_mtime)


def organize_by_month(folder_path: str):
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print(f"Folder not found: {folder}")
        return

    files = [item for item in folder.rglob("*") if item.is_file()]

    for item in files:
        if not item.is_file() or item.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            file_date = get_file_date(item)
            year_folder = folder / file_date.strftime("%Y")
            year_folder.mkdir(exist_ok=True)

            month_folder = year_folder / file_date.strftime("%Y-%m")
            month_folder.mkdir(exist_ok=True)

            target = month_folder / item.name

            if target.resolve() == item.resolve():
                continue

            if target.exists():
                if target.stat().st_size == item.stat().st_size:
                    item.unlink()
                    print(f"Deleted duplicate: {item.name}")
                    continue

                stem = item.stem
                suffix = item.suffix
                counter = 1
                while target.exists():
                    target = month_folder / f"{stem}_{counter}{suffix}"
                    counter += 1

            shutil.move(str(item), str(target))
            print(f"Moved {item.name} -> {month_folder.name}/")
        except Exception as e:
            print(f"Skipped {item.name}: {e}")

    empty_dirs = sorted(
        [path for path in folder.rglob("*") if path.is_dir()],
        key=lambda path: len(path.parts),
        reverse=True,
    )

    for directory in empty_dirs:
        if directory == folder:
            continue

        if directory.parent == folder and directory.name.isdigit() and len(directory.name) == 4:
            continue

        try:
            directory.rmdir()
            print(f"Removed empty folder: {directory}")
        except OSError:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organize_media_by_year_month.py /path/to/folder")
        sys.exit(1)

    organize_by_month(sys.argv[1])