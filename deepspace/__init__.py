import os
from .errors import deepspaceError

DataFolder = os.getenv("DEEPSPACE")

if DataFolder is None:
    raise deepspaceError("DEEPSPACE environment variable not set.")
