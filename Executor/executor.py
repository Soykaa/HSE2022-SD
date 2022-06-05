from typing import List

from optional import Optional
from Executor.file_manager import FileManager

from Executor.context import Context
from Environment.impl import environment


class Executor:
    """
    Sequentially executes the given commands.
    """

    def __init__(self):
        self.commands = []
        self.env = environment

    current_directory = FileManager.get_current_directory()
    is_shell_terminated = False

    def set_commands(self, commands: List):
        """
        Set the sequence of commands
        :param commands: list of commands
        """
        self.commands = commands

    def run(self):
        """
        Executes the sequence of commands
        """
        if not self.commands:
            return Optional.of(''), 0

        context = Context()
        output, ret_code = None, None
        for command in self.commands:
            output, ret_code = command.execute(context)
            context.state = Optional.of(output)
            if ret_code != 0:
                return context.state, ret_code
        return context.state, ret_code
