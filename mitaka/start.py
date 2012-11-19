#!/usr/bin/env python

import os
import re
import glob
import datetime

from PIL import Image

from flask import Flask, render_template

app = Flask(__name__)

@app.template_filter('prettydate')
def pretty_date(udate):
    try:
        dt = datetime.datetime.strptime(udate, "%Y-%m-%d")
    except:
        return "Unknown Date"
    return dt.strftime("%d %B %Y")

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/what.html')
def weekwhat():
    wpath = os.path.join(app.static_folder, 'images', 'what')
    if not os.path.exists(wpath):
        return render_template('what.html', dates=[])
    rex = re.compile("\d{4}-\d{2}-\d{2}")
    opts = os.listdir(wpath)
    dates = [x for x in opts if rex.match(x)]
    return render_template('what.html', dates=sorted(dates, reverse=True))

@app.route('/<name>.html') # keep .html for stylistic reasons
def rootpage(name):
    return render_template("%s.html"%name)

@app.route('/what/<date>')
def what(date):
    wpath = os.path.join(app.static_folder, 'images', 'what', date)
    if not os.path.exists(wpath):
        return weekwhat()
    whats = sorted([os.path.basename(x) for x in glob.glob(os.path.join(wpath, 'what*.jpg'))]) # blech
    title = None
    tfile = os.path.join(wpath, 'title.txt')
    if os.path.exists(tfile):
        with open(tfile) as tf:
            title = tf.read().strip()
    return render_template('what/index.html', d=date, whats=whats, title=title)

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
    gimages += glob.glob(os.path.join(gpath, '*.png'))
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
                                           images=sorted([os.path.basename(x) for x in gimages]))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
