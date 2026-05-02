# Media Year-Month Organizer

Organize photos, videos, and archives from a full folder/partition into:

- `YYYY/YYYY-MM/filename`

The script scans subfolders, moves supported files, skips same-size duplicates, renames conflicts (`_1`, `_2`), and removes empty leftover folders.

## Supported Types

- Photos: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.heic`
- Videos: `.mp4`, `.mov`, `.mkv`, `.avi`
- Archives: `.zip`, `.7z`
- Thumbnails: `.thumb`, `.thm`, `.thumbnail`

## Run

```bash
python3 organize_media_by_year_month.py /path/to/folder-or-partition
```

Example:

```bash
sudo python3 organize_media_by_year_month.py /run/media/raushan/2414BFCAA5574337/
```

## Notes

- On Linux, true creation time is not always available.
- For images, EXIF date is used first when available.
- Otherwise file birth time (if supported) or modified time is used.
- Install Pillow for better image date detection:

```bash
pip install pillow
```
