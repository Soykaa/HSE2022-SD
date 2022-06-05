from typing import Tuple

import os

from Executor.context import Context
from Executor.file_manager import FileManager
from Executor.executor import Executor


class Cat:
    """
    Get file contents.
    """

    def __init__(self, args):
        """
        :param args: command arguments
        """
        self.args = args

    def execute(self, context: Context) -> Tuple[str, int]:
        """
        Check that arguments are paths to existing files.
        Return the contents of these files
        :returns: Status code
        :rtype: int
        """
        paths = []
        for arg in self.args:
            if not arg.startswith(os.path.sep):
                paths.append(Executor.current_directory + os.path.sep + arg)
        for path_to_file in paths:
            if not FileManager.is_file(path_to_file):
                return f'cat: no such file {path_to_file}', 2
        if len(self.args) > 0:
            result = ''.join([FileManager.get_file_content(path_to_file)
                              for path_to_file in paths])
        else:
            if context.state.is_empty():
                return "cat: empty input", 1
            result = ''.join(context.state.get())
        return result, 0

    def __str__(self):
        return f'CAT {self.args}'

    def __eq__(self, other):
        if isinstance(other, Cat):
            return self.args == other.args
        return False
