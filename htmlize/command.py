# -*- coding:utf-8 -*-
"""generate html from any formats

Usage: htmlize [-h, --help] file

options:
    -h show this message and exit

"""


import sys
import re
import os.path
import argparse
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from markdown import markdown
from docutils.examples import html_parts as restructured_text


class NotSupport(Exception):
    pass


class Converter(object):
    def __init__(self):
        self.mapping = set()

    def register(self, rx, fn):
        self.mapping.add((rx, fn))

    def as_converter(self, rx):
        def wrap(fn):
            self.register(rx, fn)
            return fn
        return wrap

    def __call__(self, name):
        for rx, fn in self.mapping:
            m = rx.search(name)
            if m is not None:
                return fn
        raise NotSupport(name)

c = Converter()

markdown_rx = re.compile(r"\.(?:md|markdown)$")
rest_rx = re.compile(r"\.(rst|rest)")


template = """\
<!doctype html>
<html>
<head>
<meta charset="{encoding}"/>
{theme}
</head>
<body>
{body}
</body>
</html>
"""


def get_resource_directory_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources",)


def emit_theme(body, theme, encoding="UTF-8"):
    if theme is None:
        return(template.format(encoding=encoding, body=body, theme=""))
    else:
        dirpath = get_resource_directory_path()
        path = os.path.join(dirpath, theme) + ".css"
        if not os.path.exists(path):
            logger.warn("%s is not found use default theme", path)
            path = os.path.join(dirpath, "default.css")
        with open(path) as rf:
            css = rf.read()
        theme = """<style type="text/css">{}</style>""".format(css)
        return(template.format(encoding=encoding, body=body, theme=theme))


@c.as_converter(markdown_rx)
def on_markdown(filename, theme=None):
    with open(filename) as rf:
        body = markdown(rf.read())
        return emit_theme(body, theme, encoding="UTF-8")


@c.as_converter(rest_rx)
def on_rest(filename, theme=None):
    with open(filename) as rf:
        parts = restructured_text(rf.read())
        return emit_theme(
            parts["html_body"],
            theme,
            encoding=parts["encoding"]
        )


def detect(filename, converter=c):
    name = filename.lower()
    return converter(name)


def list_theme():
    root = get_resource_directory_path()
    for filename in os.listdir(root):
        print(filename.replace(".css", "", 1))


def main(sys_args=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("file")
    parser.add_argument("-b", "--browse", action="store_true", default=False)
    parser.add_argument("-l", "--list", action="store_true", default=False)
    parser.add_argument("-t", "--theme", default=None)
    args = parser.parse_args(sys_args)
    if args.list:
        return list_theme()
    
    if not args.browse:
        print(detect(args.file)(args.file, args.theme))
    else:
        import tempfile
        import webbrowser

        _, tmpname = tempfile.mkstemp(suffix=".html")
        with open(tmpname, "w") as wf:
            wf.write(detect(args.file)(args.file, theme=args.theme))
        webbrowser.open_new_tab("file://{}".format(tmpname))


if "__main__" == __name__:
    main()
