# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mammoth
from PIL import Image


# def compose(f, g):
#     def composed(*args, **kwargs):
#         return f(g(*args, **kwargs))
    
#     return composed


def Main():
    style_map = """
    p[style-name='Heading 1 for Top of Page'] => h1:fresh
    p[style-name='Body Text'] => p
    p[style-name='Exhibit Title Bold'] => bold
    p[style-name='Source'] => src
    """
    with open("test.docx", "rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file,
            style_map=style_map
        )
        html = result.value # The generated HTML
        messages = result.messages # Any messages, such as warnings during conversion
        Html_file= open("output.html","w")
        Html_file.write((html).encode('utf-8'))
        Html_file.close()
        print(messages)


Main()
