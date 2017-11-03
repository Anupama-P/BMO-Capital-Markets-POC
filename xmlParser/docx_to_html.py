# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mammoth
from PIL import Image
import os
import shutil

# def compose(f, g):
#     def composed(*args, **kwargs):
#         return f(g(*args, **kwargs))
    
#     return composed

class ImageWriter(object):
    def __init__(self, output_dir):
        self._output_dir = output_dir
        self._image_number = 1

    def __call__(self, element):
        extension = element.content_type.partition("/")[2]
        image_filename = "{0}.{1}".format(self._image_number, extension)
        with open(os.path.join(self._output_dir, image_filename), "wb") as image_dest:
            with element.open() as image_source:
                shutil.copyfileobj(image_source, image_dest)

        self._image_number += 1

        new_name = str(image_filename.split('.')[0]) + '.emf'
        os.rename(image_filename, new_name)

        os.system('"inkscape "' + new_name + ' --export-png=' + new_name.split('.')[0] + '.png')

        return {"src": new_name.split('.')[0] + '.png'}

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
            style_map=style_map,
            convert_image=mammoth.images.inline(ImageWriter('D:\\Work7\\BMO-Capital-Markets-POC\\xmlParser'))
        )
        html = result.value # The generated HTML
        messages = result.messages # Any messages, such as warnings during conversion
        Html_file= open("output.html","w")
        Html_file.write((html).encode('utf-8'))
        Html_file.close()
        print(messages)


Main()
