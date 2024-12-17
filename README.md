Automatically generate HTML redirect files for specified links. See
[`links.txt`](links.txt) for examples.

### How To Use
I would recommend reading the [main file](__main__.py) for best guidance. To run
the project, clone this repository then use [`uv`](https://docs.astral.sh/uv/):

```
uv run . --help
```

### Templates in `links.txt` File
You can use `{runpy{my_script.py}}` syntax in the [`links.txt`](links.txt) file
to run a python file to merge links from. It will look for `LNGENLINKS` variable
in global scope of the script after running it then merge it into the existing
parsed contents of the `links.txt`. The parsing is done in a line-by-line linear
fashion, so the order of script in that file does matter. The type of the
variable should be
[`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping).

### Command-line Arguments
```
usage: . [-h] [--link-dir LINK_DIR] [--link-file LINK_FILE]
         [--bg-color BG_COLOR] [--delay-sec DELAY_SEC]

options:
  -h, --help            show this help message and exit
  --link-dir LINK_DIR   Set the directory at where it will create the link
                        HTML files.
  --link-file LINK_FILE
                        The file from which to gather links. Can be - for
                        stdin.
  --bg-color BG_COLOR   Set background color of the HTML pages. Default:
                        #282828
  --delay-sec DELAY_SEC
                        Delay before it redirects in seconds. Default: 0
```
