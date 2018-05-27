import yaml, datetime, flask, re, glob, os
from app import exceptions

class Post:
    def __init__(self, post_file, **kwargs):
        try:
            self.data = yaml.load(open(post_file))
        except yaml.scanner.ScannerError:
            raise exceptions.CorruptFileException(post_file)
        if 'date' not in self.data.keys():
            now = datetime.datetime.now()
            with open(post_file, 'r') as file:
                content = file.read()
            content += 'date: ' + now.strftime('%c')
            with open(post_file, 'w') as file:
                file.write(content + '\n')
            self.data = yaml.load(open(post_file))
        try:
            self.data['tags'] = self.data['tags'].split(',')
        except AttributeError as e:
            if "'list' object has no attribute 'split'" not in str(e):
                raise
            # else, tags doesn't need to be split because it's already a list. do nothing.
        self.data['name'] = post_file.split('/')[-1]
        self.body = self._format_body()

    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise AttributeError("'Post' object has no attribute '{0}'".format(key))

    def _format_body(self):
        body = self.data['body'].split('\n')
        body = '<br>\n'.join(body)
        body = re.sub(r'img:([\w.]*):(center|wrap)',
                r'<img src="/static/images/\1" class="pure-image post-image-\2">',
                body)
        return flask.Markup(body)

class Posts:
    def __init__(self):
        self.load_posts()

    def __getitem__(self, key):
        """ Return a single Post object whose `name` attribute matches the
        supplied key.
        Expects: A single string, the name of a post.
        Returns: A single Post object.
        Throws: KeyError
        """
        return self._posts_by_name[key]

    def _build_indices(self):
        tag_set = {tag for post in self._posts for tag in post.tags}
        cat_set = {post.category for post in self._posts}
        self._posts_by_tag = {tag: list(filter(lambda x: tag in x.tags, self._posts)) for tag in tag_set}
        self._posts_by_category = {cat: list(filter(lambda x: cat == x.category, self._posts)) for cat in cat_set}
        self._posts_by_name = {post.name: post for post in self._posts}

    def load_posts(self):
        global categories
        post_paths = glob.glob(os.path.dirname(__file__) + '/../posts/*')
        post_objs = []
        for post in post_paths:
            try:
                post_objs.append(Post(post))
            except exceptions.CorruptFileException as e:
                print('Encountered a YAML syntax error while trying to load a post: '
                        + e.message)
        post_objs.sort(key=lambda x: x.date, reverse=True)
        tag_set = {tag for post in post_objs for tag in post.tags}
        cat_set = {post.category for post in post_objs}
        self._posts_by_tag = {tag: list(filter(lambda x: tag in x.tags, post_objs)) for tag in tag_set}
        self._posts_by_category = {cat: list(filter(lambda x: cat == x.category, post_objs)) for cat in cat_set}
        self._posts_by_name = {post.name: post for post in post_objs}
        self._posts = post_objs
        self.categories = cat_set

    def by_date(self, count=None, offset=0):
        """ Return a list of 0 or more Post objects, sorted by their `date`
        attributes, sorted most-recent-first.
        If the `count` argument is supplied, limit the returned list to at most
        `count` items. If `offset` is supplied, the first `offset` posts will be
        skipped.
        Expects: Nothing.
        Returns: A list of Post objects.
        """
        return self._posts[offset:count+offset if type(count) == int else None]

    def by_category(self, category, count=None, offset=0):
        """ Return a list of 1 or more Post object with a `category` attribute
        matching the provided argument.
        If the `count` argument is supplied, limit the returned list to at most
        `count` items. If `offset` is supplied, the first `offset` posts will be
        skipped.
        Expects: A single string, the name of a category.
        Returns: A non-empty list of Post objects.
        Throws: KeyError
        """
        return self._posts_by_category[category][offset:count+offset if type(count) == int else None]

    def by_tag(self, tag, count=None, offset=0):
        """ Return a list of 1 or more Post object with a `tag` attribute
        matching the provided argument.
        If the `count` argument is supplied, limit the returned list to at most
        `count` items. If `offset` is supplied, the first `offset` posts will be
        skipped.
        Expects: A single string, the name of a tag.
        Returns: A non-empty list of Post objects.
        Throws: KeyError
        """
        return self._posts_by_tag[tag][offset:count+offset if type(count) == int else None]

posts = Posts()
