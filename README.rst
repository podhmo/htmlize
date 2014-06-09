htmlize
========================================

tiny utility command, generate html from any formats(e.g. .md, .rst)

support format

- markdown
- restructured text

how to use
----------------------------------------

target file(markdown)

.. code:: bash

    $ cat sample/hello.md
    hello
    ========================================

    hello

    ## subsection

    * マルチバイト文字
    * multi bytes string

output

.. code:: bash

    $ htmlize sample/hello.md

    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8"/>
    </head>
    <body>
    <h1>hello</h1>
    <p>hello</p>
    <h2>subsection</h2>
    <ul>
    <li>マルチバイト文字</li>
    <li>multi bytes string</li>
    </ul>
    </body>
    </html>

open by browser with -b option
----------------------------------------

when -b option is added, dump generated html to teporary file, and open via web browser

.. code:: bash

    htmlize -b sample/hello.md

memo(and thunks)
----------------------------------------

css is borrowed from these repositories.

- https://github.com/jasonm23/markdown-css-themes
- https://gist.github.com/andyferra/2554919
