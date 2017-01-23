class CorruptFileException(Exception):
    def __init__(self, filename, *args, **kwargs):
        super(CorruptFileException, self).__init__()
        self.message = "Encountered a corrupted file: " + filename
