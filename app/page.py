import yaml, flask, re
from app import exceptions

class Page:
    def __init__(self, page_file, **kwargs):
        try:
            self.data = yaml.load(open(page_file))
        except yaml.scanner.ScannerError:
            raise exceptions.CorruptFileException(page_file)
        self.data['name'] = page_file.split('/')[-1]
        self.body = self._format_body()

    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise AttributeError("'Page' object has no attribute '{0}'".format(key))

    def _format_body(self):
        body = self.data['body'].split('\n')
        body = '<br>\n'.join(body)
        body = re.sub(r'img:([\w.]*):(center|wrap)',
                r'<img src="/static/images/\1" class="pure-image post-image-\2">',
                body)
        return flask.Markup(body)

class Pages:
    def __init__(self):
        self.load_pages()

    def __getitem__(self, key):
        return self._pages[key]

    def load_pages(self):
        import glob, os, yaml
        page_paths = glob.glob(os.path.dirname(__file__) + '/../pages/*')
        page_objs = []
        for page in page_paths:
            try:
                page_objs.append(Page(page))
            except exceptions.CorruptFileException as e:
                print('Encountered a YAML syntax error while trying to load a page: '
                        + e.message)
        self._pages = {page.name: page for page in page_objs}

pages = Pages()
