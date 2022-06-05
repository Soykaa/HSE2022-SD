from typing import List, Tuple

import os

from Executor.context import Context
from Executor.file_manager import FileManager
from Executor.executor import Executor


class Wc:
    """
    Count the number of lines, words and bytes in given files.
    """

    def __init__(self, args: List[str]):
        """
        :param args: command arguments
        """
        self.args = args

    def execute(self, context: Context) -> Tuple[str, int]:
        """
        Print number of lines, words, and bytes for each FILE in args.
        For pipe read previous command output
        :returns: Status code
        :rtype: int
        """
        paths = []
        for arg in self.args:
            if arg.startswith(os.path.sep):
                paths.append(Executor.current_directory + arg)
            else:
                paths.append(Executor.current_directory + os.path.sep + arg)
        self.args = paths
        if len(self.args) > 0:
            for arg in self.args:
                if not FileManager.is_file(arg):
                    return f'wc: no such file {arg}', 2

        if len(self.args) > 0:
            args = zip([FileManager.get_file_content(arg) for arg in self.args], self.args)
        else:
            if context.state.is_empty():
                return "wc: empty input", 1
            args = zip([''.join(context.state.get()) + '\n'], [''])
        final_result = []
        for arg, file_name in args:
            result = []
            # Count the number of lines as the number of newline characters
            lines = arg.count('\n')
            result.append(str(lines))

            # Count the number of words
            words = len(arg.split())
            result.append(str(words))

            # Transform the contents of the file into bytes and count their number
            num_bytes = len(arg.encode())
            result.append(str(num_bytes))

            result.append(file_name)
            final_result.append(' '.join(result))
        return '\n'.join(final_result), 0

    def __str__(self):
        return f'WC {self.args}'

    def __eq__(self, other):
        if isinstance(other, Wc):
            return self.args == other.args
        return False
