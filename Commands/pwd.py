from typing import List, Tuple, Any

from Executor.context import Context
from Executor.executor import Executor


class Pwd:
    """
    Return the current directory.
    """

    def __init__(self, args: List[str]):
        """
        :param args: command arguments
        """
        self.args = args

    def execute(self, context: Context) -> Tuple[Any, int]:
        """
        Return working directory
        :returns: Status code
        :rtype: int
        """
        if len(self.args) > 0 or not context.state.is_empty():
            return "pwd: too many arguments", 1
        result = Executor.current_directory
        return result, 0

    def __str__(self):
        return f'PWD {self.args}'

    def __eq__(self, other):
        if isinstance(other, Pwd):
            return self.args == other.args
        return False
