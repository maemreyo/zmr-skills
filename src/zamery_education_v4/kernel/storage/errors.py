class StorageError(RuntimeError):
    pass


class ContentHashMismatch(StorageError):
    pass


class RecordNotFound(StorageError):
    pass
