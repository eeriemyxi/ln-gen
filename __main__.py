import argparse
import pathlib
import re
import runpy
import shutil
import sys
import kisesi

from chameleon import PageTemplate

kisesi.basic_config(level=kisesi.DEBUG)
log = kisesi.get_logger(__name__)

SCRIPT_DIR = pathlib.Path(__file__).parent
LINK_DIR = SCRIPT_DIR / "ln"
LINK_FILE = open(SCRIPT_DIR / "links.txt")
DELAY_SEC = 0
BG_COLOR = "#282828"
RUNPY_RE = re.compile(r"^{runpy{(?P<path>.+)}}$")


def parse_links(text):
    links = {}

    for line in text.splitlines():
        if not (runpymatch := RUNPY_RE.match(line)):
            name, link = line.strip().split(maxsplit=1)
            links[name] = link
            continue

        runpy_path = pathlib.Path(runpymatch["path"]).resolve()
        log.info("Running '%s'", runpy_path)
        runpymatch_globals = runpy.run_path(runpy_path)

        if "LNGENLINKS" not in runpymatch_globals:
            log.error("Ran '%s' but couldn't find 'LNGENLINKS' in globals", runpy_path)
            exit(1)

        links |= dict(runpymatch_globals["LNGENLINKS"])

    log.info("Parsing links complete")
    return links


def main():
    global LINK_DIR, LINK_FILE, BG_COLOR, DELAY_SEC

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--link-dir",
        help="Set the directory at where it will create the link HTML files.",
        type=pathlib.Path,
        default=LINK_DIR,
    )
    parser.add_argument(
        "--link-file",
        type=argparse.FileType("r"),
        default=LINK_FILE,
        help="The file from which to gather links. Can be - for stdin.",
    )
    parser.add_argument(
        "--bg-color",
        help="Set background color of the HTML pages. Default: #282828",
        default=BG_COLOR,
    )
    parser.add_argument(
        "--delay-sec",
        help="Delay before it redirects in seconds. Default: 0",
        type=int,
        default=DELAY_SEC,
    )
    args = parser.parse_args()

    LINK_DIR = args.link_dir
    LINK_FILE = args.link_file
    BG_COLOR = args.bg_color
    DELAY_SEC = args.delay_sec

    log.info("Removing '%s'", LINK_DIR)
    shutil.rmtree(LINK_DIR, ignore_errors=True)
    log.info("Creating '%s'", LINK_DIR)
    LINK_DIR.mkdir()

    with open(SCRIPT_DIR / "templates" / "ln.pt") as lnhtml:
        links = parse_links(LINK_FILE.read())
        html = lnhtml.read()

    ln_template = PageTemplate(html)

    for name, link in links.items():
        filename = (LINK_DIR / name).with_suffix(".html")
        with open(filename, "w") as file:
            file.write(ln_template(DELAY_SEC=DELAY_SEC, URL=link, BG_COLOR=BG_COLOR))
            log.info(f"[{name}] -> {filename} @ [{link}]")


if __name__ == "__main__":
    main()
