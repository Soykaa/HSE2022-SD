import os

from Commands.cd import Cd
from Commands.ls import Ls
from Executor.context import Context
from Executor.executor import Executor


def test_cd_with_correct_arg():
    prev_directory = Executor.current_directory
    context = Context()
    if os.getcwd().__contains__('Commands'):
        cd = Cd(['../resources/one'])
    else:
        cd = Cd(['Commands/resources/one'])
    _, ret_code = cd.execute(context)
    ls = Ls([])
    output, _ = ls.execute(context)
    assert ret_code == 0
    assert output == '4.txt'
    Executor.current_directory = prev_directory


def test_cd_without_args():
    prev_directory = Executor.current_directory
    context = Context()
    if os.getcwd().__contains__('Commands'):
        cd = Cd(['../resources/two/three'])
    else:
        cd = Cd(['Commands/resources/two/three'])
    _, ret_code = cd.execute(context)
    ls = Ls([])
    output, _ = ls.execute(context)
    assert ret_code == 0
    assert output == '6.txt'
    cd = Cd([])
    _, ret_code = cd.execute(context)
    assert ret_code == 0
    assert Executor.current_directory == os.path.expanduser("~")
    Executor.current_directory = prev_directory


def test_cd_with_two_dots():
    prev_directory = Executor.current_directory
    context = Context()
    if os.getcwd().__contains__('Commands'):
        cd = Cd(['../resources/two/three'])
    else:
        cd = Cd(['Commands/resources/two/three'])
    _, ret_code = cd.execute(context)
    ls = Ls([])
    output, _ = ls.execute(context)
    assert ret_code == 0
    assert output == '6.txt'
    cd = Cd(['..'])
    _, ret_code = cd.execute(context)
    assert ret_code == 0
    output, _ = ls.execute(context)
    assert output == '5.txt' + os.linesep + 'three'
    Executor.current_directory = prev_directory


def test_cd_with_many_args():
    prev_directory = Executor.current_directory
    context = Context()
    cd = Cd(['../resources', 'odd arg'])
    output, ret_code = cd.execute(context)
    assert ret_code == 1
    assert output == 'cd: too many arguments'
    Executor.current_directory = prev_directory


def test_cd_no_such_dir():
    prev_directory = Executor.current_directory
    context = Context()
    cd = Cd(['../resources/fifteen'])
    output, ret_code = cd.execute(context)
    assert ret_code == 2
    assert output.__contains__('cd: no such directory')
    Executor.current_directory = prev_directory
