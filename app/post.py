import yaml, datetime, flask, re
from app import exceptions

class Post(object):
    def __init__(self, post_file, **kwargs):
        super(Post, self).__init__()
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
