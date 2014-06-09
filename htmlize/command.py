# -*- coding:utf-8 -*-
"""generate html from any formats

Usage: htmlize [-h, --help] file

options:
    -h show this message and exit

"""


import sys
import re
import argparse
import logging
logger = logging.getLogger(__name__)

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
</head>
<body>
{body}
</body>
</html>
"""


@c.as_converter(markdown_rx)
def on_markdown(filename):
    with open(filename) as rf:
        return(template.format(encoding="UTF-8", body=markdown(rf.read())))


@c.as_converter(rest_rx)
def on_rest(filename):
    with open(filename) as rf:
        parts = restructured_text(rf.read())
        return(template.format(encoding=parts["encoding"], body=parts["html_body"]))


def detect(filename, converter=c):
    name = filename.lower()
    return converter(name)


def main(sys_args=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("file")
    parser.add_argument("-b", "--browse", action="store_true", default=False)
    args = parser.parse_args(sys_args)

    if not args.browse:
        print(detect(args.file)(args.file))
    else:
        import tempfile
        import webbrowser

        _, tmpname = tempfile.mkstemp(suffix=".html")
        with open(tmpname, "w") as wf:
            wf.write(detect(args.file)(args.file))
        webbrowser.open_new_tab("file://{}".format(tmpname))


if "__main__" == __name__:
    main()
