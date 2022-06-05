import argparse
import re
import os
from typing import List, Tuple, Optional

from Executor.context import Context
from Executor.file_manager import FileManager
from Executor.executor import Executor


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def search(*, data: str, pattern: str, ignore_case, file_name: Optional[str], append_number: int):
    s = set()
    split_data = data.split('\n')
    for i, line in enumerate(split_data):
        if re.search(pattern, line, ignore_case):
            s.add(i)
            s = s.union(set(range(i + 1, min(i + 1 + append_number, len(split_data)))))
    result = []
    for line_no in s:
        line = ''
        if file_name:
            line += f'{file_name}: '
        line += split_data[line_no]
        result.append(line)
    return result


class Grep:
    """
    TODO написать описание
    """

    def __init__(self, args: List[str]):
        """
        :param args: command arguments
        """
        self.args = args

    def parse_arguments(self, args):
        parser = ThrowingArgumentParser()
        parser.add_argument("-w", dest="words", action="store_true", default=False)
        parser.add_argument("-i", dest="case_insensitive", action="store_true", default=False)
        parser.add_argument("-A", dest="count", type=int, default=0)
        parser.add_argument("pattern")
        return parser.parse_known_args(args)

    def execute(self, context: Context) -> Tuple[str, int]:
        """
        TODO написать описание
        :returns: Status code
        :rtype: int
        """
        try:
            result_of_parsing, files = self.parse_arguments(self.args)
        except (ArgumentParserError, ThrowingArgumentParser, argparse.ArgumentError) as e:
            return e.__str__(), 1
        ignore_case = 0
        pattern = result_of_parsing.pattern
        if result_of_parsing.case_insensitive:
            ignore_case |= re.IGNORECASE
        if result_of_parsing.words:
            pattern = '([^A-Za-z0-9_]' + pattern + '[^A-Za-z0-9_]|' + \
                      '^' + pattern + '[^A-Za-z0-9_]|' +\
                      '^' + pattern + '$|' +\
                      '[^A-Za-z0-9_]' + pattern + '$)'
        result = []
        if not files:
            if not context.state:
                return "grep: empty input", 1
            result += search(data=context.state.get(), pattern=pattern,
                             ignore_case=ignore_case, file_name=None,
                             append_number=result_of_parsing.count)
        else:
            for file_name in files:
                if not file_name.startswith(os.path.sep):
                    file_name = Executor.current_directory + os.path.sep + file_name
                else:
                    file_name = Executor.current_directory + file_name
                if not FileManager.is_file(file_name):
                    return f'grep: no such file {file_name}', 2
                file_content = FileManager.get_file_content(file_name)
                result += search(data=file_content, pattern=pattern,
                                 ignore_case=ignore_case, file_name=file_name,
                                 append_number=result_of_parsing.count)
        return '\n'.join(result), 0

    def __str__(self):
        return f'GREP {self.args}'

    def __eq__(self, other):
        if isinstance(other, Grep):
            return self.args == other.args
        return False
