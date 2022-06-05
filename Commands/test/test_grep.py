import argparse
import os
import pytest
import tempfile
from argparse import Namespace

from Commands.grep import Grep, ArgumentParserError
from Executor.context import Context


def create_tmp_file(content):
    fd, path = tempfile.mkstemp(prefix=os.getcwd() + os.path.sep)
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return fd, path


def test_parse_arguments_without_files():
    args = ["str"]
    grep = Grep(args=args)
    result = Namespace(pattern="str", count=0, case_insensitive=False, words=False)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == []


def test_parse_arguments_with_one_file_and_no_flags():
    args = ["str", "file.txt"]
    result = Namespace(pattern="str", count=0, case_insensitive=False, words=False)
    grep = Grep(args=args)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]


def test_parse_arguments_with_files_and_no_flags():
    args = ["str", "file.txt", "file2.txt", "file3.txt"]
    result = Namespace(pattern="str", count=0, case_insensitive=False,
                       words=False)
    grep = Grep(args=args)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt", "file2.txt", "file3.txt"]


def test_parse_arguments_with_one_file_and_words_flag():
    args = ["-w", "str", "file.txt"]
    result = Namespace(pattern="str", count=0, case_insensitive=False, words=True)
    grep = Grep(args=args)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "-w", "file.txt"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "file.txt", "-w"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]


def test_parse_arguments_with_one_file_and_case_insensitive_flag():
    args = ["-i", "str", "file.txt"]
    result = Namespace(pattern="str", count=0, case_insensitive=True, words=False)
    grep = Grep(args=args)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "-i", "file.txt"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "file.txt", "-i"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]


def test_parse_arguments_with_one_file_and_count_flag():
    args = ["-A", "str", "file.txt"]
    grep = Grep(args=args)
    with pytest.raises(ArgumentParserError):
        grep.parse_arguments(args)
    args = ["-A", "0", "str", "file.txt"]
    result = Namespace(pattern="str", count=0, case_insensitive=False, words=False)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "file.txt", "-A", "0"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "-A", "0", "file.txt"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]
    args = ["str", "file.txt", "-A", "0"]
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]


def test_parse_arguments_with_all_flags():
    args = ["-A", "0", "-w", "-i", "str", "file.txt"]
    grep = Grep(args=args)
    result = Namespace(pattern="str", count=0, case_insensitive=True, words=True)
    output, files = grep.parse_arguments(args)
    assert output == result
    assert files == ["file.txt"]


def test_simple_string_execute():
    content = 'hello\nworld'
    context = Context()
    fd1, path1 = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)

    args = ["hello", path1[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f'{path1}: hello'
    os.remove(path1)


def test_or_string_execute():
    content = 'hello world\nbye\nhello bye\ngray'
    context = Context()
    fd1, path1 = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)

    args = ["hello|bye", path1[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f'{path1}: hello world\n{path1}: bye\n{path1}: hello bye'
    os.remove(path1)


def test_or_inside_string_execute():
    content = 'gray, grey\ngrey 1233\ngray 1244\nhello world\nend grey'
    context = Context()
    fd1, path1 = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)

    args = ["gr(a|e)y", path1[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f'{path1}: gray, grey\n{path1}: grey 1233\n{path1}: gray 1244\n{path1}: end grey'
    os.remove(path1)


def test_char_array_string_execute():
    content = "babble\nbebble\nbibble\nbobble\nbubble\nhello world\n babble hello\nno such grep"
    context = Context()
    fd1, path1 = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)

    args = ["b[aeiou]bble", path1[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == (f"{path1}: babble\n{path1}: bebble\n{path1}: bibble\n"
                      f"{path1}: bobble\n{path1}: bubble\n{path1}:  babble hello")
    os.remove(path1)


def test_simple_string_multiple_files():
    content1 = "hello world1\nhello1\nworld\nbye"
    content2 = "world\nbye\nhello world2\nhello2"
    context = Context()

    fd1, path1 = create_tmp_file(content1)
    fd2, path2 = create_tmp_file(content2)
    num = len(os.getcwd() + os.path.sep)

    args = ["hello", path1[num:], path2[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f"{path1}: hello world1\n{path1}: hello1\n" + f"{path2}: hello world2\n{path2}: hello2"
    os.remove(path1)
    os.remove(path2)


def test_ignore_case():
    content = "Hello IM PASHA\nhello IM KATYA"
    context = Context()

    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)

    args = ["Hello", path[num:], '-i']
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f'{path}: Hello IM PASHA\n{path}: hello IM KATYA'
    os.remove(path)


def test_ignore_case_two_files():
    content1 = "Hello World\n hello world"
    content2 = "Hello World1\n hello world"

    context = Context()
    fd1, path1 = create_tmp_file(content1)
    fd2, path2 = create_tmp_file(content2)
    num = len(os.getcwd() + os.path.sep)

    args = ["hello", "-i", path1[num:], path2[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)
    print(output)
    assert ret_code == 0
    assert output == f"{path1}: Hello World\n{path1}:  hello world\n" + f"{path2}: Hello World1\n{path2}:  hello world"
    os.remove(path1)
    os.remove(path2)


def test_search_like_word():
    content = "hello worldmy name id daniel\nhello world"
    context = Context()
    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    args = ["hello world", "-w", path[num:]]
    grep = Grep(args=args)
    output, ret_code = grep.execute(context)
    print(output)
    assert ret_code == 0
    assert output == f"{path}: hello world"
    os.remove(path)


def test_use_flag_a():
    content = "hello\nworld1\nworld2\nworld3\nworld4\nworld5"
    context = Context()
    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    args = ["hello", "-A", "5", path[num:]]

    grep = Grep(args=args)
    output, ret_code = grep.execute(context)
    print(output)
    assert ret_code == 0
    assert output == f"{path}: hello\n{path}: world1\n{path}: world2\n{path}: world3\n{path}: world4\n{path}: world5"
    os.remove(path)


def test_use_flag_a_double_find():
    content = "hello\nhello\nworld2\nworld3\nworld4\nworld5"
    context = Context()
    fd, path = create_tmp_file(content)
    num = len(os.getcwd() + os.path.sep)
    args = ["hello", "-A", "3", path[num:]]

    grep = Grep(args=args)
    output, ret_code = grep.execute(context)

    assert ret_code == 0
    assert output == f"{path}: hello\n{path}: hello\n{path}: world2\n{path}: world3\n{path}: world4"
    os.remove(path)
