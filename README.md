# Suhian's image utils

## Features

- copy media (image & movie) files and group by date


## Usage

```text
usage: shnail.py [-h] -r SOURCE_PATH [-t TARGET_PATH] [-z SIZE] [-c CONFIG]
                 [-a ACTION] [-s START_DATE] [-v]
                 [-d | --dry_run | --no-dry_run]

options:
  -h, --help            show this help message and exit
  -r SOURCE_PATH, --source_path SOURCE_PATH
                        source directory
  -t TARGET_PATH, --target_path TARGET_PATH
                        target directory
  -z SIZE, --size SIZE  resolution size ("1024" or "s:200,m:600")
  -c CONFIG, --config CONFIG
                        config file for copy
  -a ACTION, --action ACTION
                        process action {copy|thumbnail}
  -s START_DATE, --start_date START_DATE
                        process start from
  -v, --verbose         verbose level. v...vvv
  -d, --dry_run, --no-dry_run
                        dry run
```
## TODO

- make thumbnails
