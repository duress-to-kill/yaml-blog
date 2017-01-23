import yaml
from flask import render_template
from random import choice

from app import app, exceptions
from app.post import Post

@app.route('/')
@app.route('/index')
def index(autorefresh = False):
    autorefresh = True
    if autorefresh:
        global posts
        posts = read_posts()
    return render_template('index.html',
            tagline = choice(taglines),
            posts = posts[0:10])

@app.route('/all-posts')
def all_posts():
    return render_template('index.html',
            tagline = choice(taglines),
            posts = posts)

@app.route('/about-me')
def about_me():
    return render_template('aboutme.html',
            tagline = choice(taglines))

@app.route('/contact')
def contact():
    return render_template('contact.html',
            tagline = choice(taglines))

@app.route('/post/<string:name>')
def post(name):
    try:
        for post in posts:
            if post.name == name:
                return render_template('post.html',
                        tagline = choice(taglines),
                        post = post)
    except AttributeError:
        pass
    return render_template('error_404.html',
            path = 'posts/' + title)

def read_posts():
    import glob, os, yaml
    post_paths = glob.glob(os.path.dirname(__file__) + '/../posts/*')
    post_objs = []
    for post in post_paths:
        try:
            post_objs.append(Post(post))
        except exceptions.CorruptFileException as e:
            print('Encountered a YAML syntax error while trying to load a post: ' + e.message)
    post_objs.sort(key=lambda x: x.date, reverse=True)
    return post_objs

taglines = yaml.load(open('taglines.yaml'))
posts = read_posts()
