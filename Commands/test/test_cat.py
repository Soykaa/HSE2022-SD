import os
import tempfile

from Commands.cat import Cat
from Executor.context import Context


def create_tmp_file(content):
    fd, path = tempfile.mkstemp(prefix=os.getcwd() + os.path.sep)
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return fd, path


def test_empty_file():
    content = ''
    context = Context()
    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    try:
        cat = Cat([path[num:]])
        output, ret_code = cat.execute(context)
        assert ret_code == 0
        assert not output
    finally:
        os.remove(path)


def test_not_empty_file():
    content = 'helloworld\n'
    context = Context()
    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    try:
        cat = Cat([path[num:]])
        output, ret_code = cat.execute(context)
        assert ret_code == 0
        assert content == output
    finally:
        os.remove(path)


def test_with_error():
    error = 'cat: no such file ' + os.getcwd() + os.path.sep + 'f'
    context = Context()
    cat = Cat(['f'])
    output, ret_code = cat.execute(context)
    assert ret_code == 2
    assert output == error


def test_with_files():
    content = 'helloworld\n'
    context = Context()
    fd1, path1 = create_tmp_file(content)
    fd2, path2 = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    try:
        cat = Cat([path1[num:], path2[num:]])
        output, ret_code = cat.execute(context)
        assert ret_code == 0
        assert output == 'helloworld\nhelloworld\n'
    finally:
        os.remove(path1)
        os.remove(path2)
