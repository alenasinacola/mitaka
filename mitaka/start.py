#!/usr/bin/env python

import os
import glob

from PIL import Image

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<name>.html') # keep .html for stylistic reasons
def rootpage(name):
    return render_template("%s.html"%name)

@app.route('/stories/<name>/<pgid>')
def story(name, pgid):
    return render_template("stories/%s.html"%name, pgid=int(pgid))

@app.route('/gallery/<name>.html')
def gallery(name):
    gpath = os.path.join(app.static_folder, 'images', 'gallery', name)
    if not os.path.exists(gpath):
        os.mkdir(gpath)
    if not os.path.exists(os.path.join(gpath, 'thumbs')):
        os.mkdir(os.path.join(gpath, 'thumbs'))
    gimages = glob.glob(os.path.join(gpath, '*.jpg'))
    for image in gimages:
        bn = os.path.basename(image)
        thumb = os.path.join(gpath, 'thumbs', bn)
        if not os.path.exists(thumb):
            size = (160, 160)
            im = Image.open(image)
            width, height = im.size
            if width > height:
                left = (width - height) / 2
                right = left + height
                top = 0
                bottom = height
            else:
                left = 0
                right = width
                top = (height - width) / 2
                bottom = width + top
            tim = im.crop((left, top, right, bottom))
            tim.thumbnail(size, Image.ANTIALIAS)
            tim.save(thumb, 'JPEG')
    return render_template("gallery.html", name=name,
                                           images=[os.path.basename(x) for x in gimages])

if __name__ == '__main__':
    app.debug = True
    app.run()
