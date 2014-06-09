# -*- coding:utf-8 -*-
import logging
import re
logger = logging.getLogger(__name__)


class NotSupport(Exception):
    pass


markdown_rx = re.compile(r"\.(?:md|markdown)$")
rest_rx = re.compile(r"\.(rst|rest)")


def on_markdown(filename):
    pass


def on_rest(filename):
    pass


mapping = [(markdown_rx, on_markdown),
           (rest_rx, on_rest)]


def detect(filename):
    name = filename.lower()
    for rx, fn in mapping:
        m = rx.search(name)
        if m is not None:
            return fn
    raise NotSupport(filename)


def main():
    print("hello")
