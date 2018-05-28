# YAML-Blog 
This minimal Python blog is designed to be portable, self-contained, easy to self-host, and to allow you to publish without ever touching a browser.

Posts are written as very simple YAML documents in the blog's source tree. Indexes and pages are generated automatically based on the available YAML documents. The blog has zero backend dependencies, being entirely stateless. It also has minimal browser dependencies, being entirely javascript-less.

This is basically a pet project, but it may appeal to people who want the most basic of soapboxes that operate with a minimum of fuss, or to those who, like me, dislike how web development tends to mean wrestling with a half dozen frameworks, guarding a very wide security attack surface, or just dealing with integrations for third-party services and other humans. Other sysadmins may find this model to their liking.

You can download this project, create a virtualenv, write a post, and be hosting the server in a few minutes (assuming you're familiar with similar processes). Then, when your friends ask why your blog is so web 1.0, just tell them "so you can't @ me".

## Features

- Publishing posts
- Easy image embedding
- Indexing by category and tag
- Being pretty damn simple

### Feature wishlist

- Actual error pages for HTTP 400's, 500's, and other kinds of errors that might show up.

### Features not invited to this party

- Syndication
- "share" buttons
- HTTPS (this is a flask app, you should terminate SSL with something more secure)
- Logins of any kind (for you or your readers)



## Setup and use
You'll need to clone the project first, obviously.

This project depends on very few libraries. You can install these manually if you like, or use the provided `requirements.txt` to let `pip` do it for you.

For testing you can just call `run.py` in the project root, which should get you a working blog with no posts hosted on `localhost:5000`. You'll probably want to reverse proxy incoming connections from nginx or apache if you want to host this publicly. Here's a tutorial on how to set this up: https://github.com/mking/flask-uwsgi

### Publishing
To publish a blog post, just create a new file in `posts/`. The name of the file becomes the post slug (i.e. a file named `my_first_post` becomes available at the URL `your.server.name/posts/my_first_post`). File extensions are *not* stripped off, so you may want to omit them. I guess I didn't consider windows users. Sorry, guys.

The post's display title, tags, categories, and body text are all defined within the document. You may optionally also declare a post date (this is just a string, it isn't parsed, so the format is freeform). If you do not write a date, the server will write a date back into the file the first time it reads it, corresponding to the date of the first time it reads the document.

Once you've go the server going, you may also want to edit the `about` and `contact` YAML documents in `pages/`. You can add additional documents to this directory if you want, which will become available at `your.server.com/docname`, bit will not be automatically indexed anywhere. You'll need to modify the HTML templates if you want these to show up.

To embed images in your pages and posts, drop the images in `images/`, and then tag them inline like this: `img:cats_with_bananas.jpg:align` (where `align` is either: `wrap` or `center`). Or just plug in an HTML tag to format it as you choose.

For further details, see the example post document `/example-post`.

### Gotchas
The server reads the `/posts` and `/pages` directory on demand, reads all YAML files there, and loads them into memory. New posts and pages will not be picked up until the server does another directory sweep. By default, this occurs every time the route `/` or `/index` is requested, but this may need to be disabled if this becomes a significant drain on system resources.

In this case, you'll need to devise a new way to publish pages. Since the server reads both directories once on startup, this could be as simple as restarting the server when you publish, or with a cron job at midnight.

## Dependencies
I've done essentially zero version testing to determine which versions this supports. Here's what I have installed in my dev environment:

- `python 3.5`
- `flask 1.0.2`
- `pyyaml 3.12`

## Credits
I wrote all of this code, with the notable exceptions of the following parts:

- Flask, which I really like. http://flask.pocoo.org/
- PyYAML, which has terrible documentation. http://pyyaml.org/
- Pure CSS, which I'm using for graphical layout. I don't understand it super well, but it's pretty cool. https://purecss.io/
