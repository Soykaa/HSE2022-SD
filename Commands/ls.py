from typing import List, Tuple

import os
import glob

from Executor.context import Context
from Executor.executor import Executor


class Ls:
    """
    Print directory contents.
    """

    def __init__(self, args: List[str]):
        """
        :param args: command arguments
        """
        self.args = args
        self.output = ""

    def __remove_prefix(self, s, prefix):
        return s[len(prefix):] if s.startswith(prefix) else s

    def __list_dir(self, path):
        return os.linesep.join(map(lambda x: self.__remove_prefix(x, path),
                                   glob.glob(os.path.join(path, '*'))))

    def execute(self, context: Context) -> Tuple[str, int]:
        """
        Prints directory contents
        :returns: Status code
        :rtype: int
        """
        if len(self.args) > 1:
            return f'ls: too many arguments', 1
        if not self.args:
            self.output = self.__list_dir(Executor.current_directory + os.path.sep)
            return self.output, 0
        if not self.args[0].startswith(os.path.sep):
            self.args[0] = os.path.sep + self.args[0]
        current_directory = Executor.current_directory + self.args[0]
        if not os.path.exists(current_directory):
            return f'ls: no such directory {current_directory}', 2
        self.output = self.__list_dir(current_directory + os.path.sep)
        return self.output, 0

    def __str__(self):
        return f'LS {self.args}'

    def __eq__(self, other):
        if isinstance(other, Ls):
            return self.args == other.args
        return False
