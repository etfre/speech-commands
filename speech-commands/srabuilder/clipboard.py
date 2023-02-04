import contextlib
from dragonfly.windows.clipboard import Clipboard

def get():
    clip = Clipboard(from_system=True)
    return clip.get_text()

def set(value):
    clip = Clipboard(text=value)
    clip.copy_to_system()

@contextlib.contextmanager
def save_current():
    original = Clipboard(from_system=True)
    try:
        yield
    except Exception as e:
        raise e
    finally:
        original.copy_to_system()
