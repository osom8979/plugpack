# -*- coding: utf-8 -*-

__version__ = "0.0.0"
__doc__ = "Documentation"


def on_open(*args, **kwargs) -> None:
    assert args
    assert kwargs


def on_close() -> None:
    pass


if __name__ == "__main__":
    raise NotImplementedError
