import os
from Commands.ls import Ls
from Executor.context import Context
from Executor.executor import Executor


def test_ls_without_args():
    context = Context()
    ls = Ls([])
    output, ret_code = ls.execute(context)
    if Executor.current_directory.__contains__('Commands'):
        expected_output_list = ['__init__.py', '__pycache__', 'test_cat.py',
                                'test_cd.py', 'test_echo.py', 'test_grep.py',
                                'test_ls.py', 'test_process.py', 'test_pwd.py',
                                'test_wc.py']
    else:
        expected_output_list = ['App', 'Architecture', 'cliArch.png',
                                'Commands', 'Environment', 'Executor',
                                'main.py', 'parser', 'README.md',
                                'requirements.txt', 'Review', 'Substitution',
                                'venv']
    actual_output_list = output.split(os.linesep)
    assert ret_code == 0
    assert len(expected_output_list) >= len(actual_output_list)
    for file in actual_output_list:
        assert expected_output_list.__contains__(file)


def test_ls_with_many_args():
    context = Context()
    ls = Ls(['../resources', 'odd arg'])
    output, ret_code = ls.execute(context)
    assert ret_code == 1
    assert output == 'ls: too many arguments'


def test_ls_no_such_dir():
    context = Context()
    ls = Ls(['../resources/fifteen'])
    output, ret_code = ls.execute(context)
    assert ret_code == 2
    assert output.__contains__('ls: no such directory')
