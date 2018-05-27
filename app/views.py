import yaml
from flask import render_template
from random import choice

from app import app, exceptions
from app.post import posts
from app.page import pages

@app.route('/')
@app.route('/index')
def index(autorefresh = False):
    autorefresh = True
    if autorefresh:
        posts.load_posts()
    return render_template('post_list.html',
            page_title = 'Recent posts',
            tagline = choice(taglines),
            categories = posts.categories,
            posts = posts.by_date(count=10))

@app.route('/all-posts')
def all_posts():
    return render_template('post_list.html',
            page_title = 'All posts',
            tagline = choice(taglines),
            categories = posts.categories,
            posts = posts.by_date())

@app.route('/tag/<string:tag>')
def posts_by_tag(tag):
    try:
        return render_template('post_list.html',
                page_title = 'Tag: ' + tag,
                tagline = choice(taglines),
                categories = posts.categories,
                posts = posts.by_tag(tag))
    except KeyError:
        return render_template('error_404.html',
                tagline = choice(taglines),
                categories = posts.categories,
                path = '/tag/' + tag)

@app.route('/category/<string:category>')
def posts_by_category(category):
    try:
        return render_template('post_list.html',
                page_title = 'Category: ' + category,
                tagline = choice(taglines),
                categories = posts.categories,
                posts = posts.by_category(category))
    except KeyError:
        return render_template('error_404.html',
                tagline = choice(taglines),
                categories = posts.categories,
                path = '/category/' + category)

@app.route('/<string:name>')
def page(name):
    try:
        return render_template('page.html',
                tagline = choice(taglines),
                categories = posts.categories,
                page = pages[name])
    except KeyError:
        return render_template('error_404.html',
                tagline = choice(taglines),
                categories = posts.categories,
                path = '/' + name)

@app.route('/post/<string:name>')
def post(name):
    try:
        return render_template('post.html',
                tagline = choice(taglines),
                categories = posts.categories,
                post = posts[name])
    except KeyError:
        return render_template('error_404.html',
                tagline = choice(taglines),
                categories = posts.categories,
                path = '/post/' + name)

taglines = yaml.load(open('taglines.yaml'))
