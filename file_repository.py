class FileRepository:
    def __init__(self, filepath, filetype, chunk_size):
        self.filepath = filepath
        self.filetype = filetype
        self.chunk_size = chunk_size

    def _get_filename(self, id):
        return f"{self.filepath}/{id}.{self.filetype}"

    def save_stream(self, id, read_stream):
        with open(self._get_filename(id), "wb") as file:
            while True:
                chunk = read_stream.read(self.chunk_size)
                if not chunk:  # Empty chunk means stream is closed/EOF
                    break
                file.write(chunk)

    def read_stream(self, id):
        return open(self._get_filename(id), "rb")


def testing():
    from io import BytesIO

    repository = FileRepository("recordings", "test", 1024)

    repository.save_stream("testing", BytesIO(b"Testing a stream!"))

    result = repository.read_stream("testing").read()

    print(result)


testing()
