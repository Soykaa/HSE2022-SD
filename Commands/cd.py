from typing import List, Tuple

import os
from os.path import expanduser

from Executor.context import Context
from Executor.executor import Executor


class Cd:
    """
    Change current directory.
    """

    def __init__(self, args: List[str]):
        """
        :param args: command arguments
        """
        self.args = args
        self.output = ""

    def __remove_suffix(self, string: str, suffix: str) -> str:
        if string.endswith(suffix):
            return string[:-len(suffix)]
        return string

    def execute(self, context: Context) -> Tuple[str, int]:
        """
        Change current directory
        :returns: Status code
        :rtype: int
        """
        if len(self.args) > 1:
            return f'cd: too many arguments', 1
        if not self.args:
            Executor.current_directory = expanduser("~")
            return self.output, 0
        if not self.args[0].startswith(os.path.sep):
            current_directory = os.path.abspath(Executor.current_directory + os.path.sep +
                                                self.__remove_suffix(self.args[0], os.path.sep))
        else:
            if self.args[0] == os.path.sep:
                current_directory = os.path.sep
            else:
                current_directory = os.path.abspath(self.__remove_suffix(self.args[0], os.path.sep))
        if not os.path.exists(current_directory):
            return f'cd: no such directory {current_directory}', 2
        if os.path.isfile(current_directory):
            return f'cd: directory is expected but file {current_directory} was provided', 3
        Executor.current_directory = current_directory
        return self.output, 0

    def __str__(self):
        return f'CD {self.args}'

    def __eq__(self, other):
        if isinstance(other, Cd):
            return self.args == other.args
        return False
