import os

from Commands.process import Process
from Environment.impl import environment
from Executor.context import Context


def test_print():
    if os.name == 'nt':
        return
    process = Process(name='echo', args=["Hello World!"])
    context = Context()
    output, ret_code = process.execute(context)
    assert ret_code == 0
    assert output == "Hello World!\n"


def test_env():
    if os.name == 'nt':
        return
    process = Process(name='echo', args=["$x"])
    environment.add_var(name='x', value='Hello World!')

    context = Context()
    output, ret_code = process.execute(context)
    assert output == "Hello World!\n"
    assert ret_code == 0


def test_process_with_error():
    if os.name == 'nt':
        return
    process = Process(name='ca', args=[])
    context = Context()
    output, ret_code = process.execute(context)
    assert ret_code != 0