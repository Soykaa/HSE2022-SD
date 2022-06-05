from parser.yacc import yacc_parser, Node

from Commands.process import Process
from Commands.cat import Cat
from Commands.echo import Echo
from Commands.pwd import Pwd
from Commands.wc import Wc
from Commands.exit import Exit
from Commands.eq import Eq
from Commands.grep import Grep
from Commands.cd import Cd
from Commands.ls import Ls


# Парсит строку и возвращает очередь из комманд для исполнения
class Parser:
    def __init__(self):
        pass

    def __traverse_ast__(self, *, root: Node):
        if root.node_type == Node.NodeType.command:
            if root.value == '=':
                return [Eq(dest=root.children[0], src=root.children[1])]
            elif root.value == 'cat':
                return [Cat(args=root.children)]
            elif root.value == 'echo':
                return [Echo(args=root.children)]
            elif root.value == 'exit':
                return [Exit(args=root.children)]
            elif root.value == 'pwd':
                return [Pwd(args=root.children)]
            elif root.value == 'wc':
                return [Wc(args=root.children)]
            elif root.value == 'grep':
                return [Grep(args=root.children)]
            elif root.value == 'cd':
                return [Cd(args=root.children)]
            elif root.value == 'ls':
                return [Ls(args=root.children)]
            else:
                return [Process(name=root.value, args=root.children)]
        res = []
        for child in root.children:
            res += self.__traverse_ast__(root=child)
        return res

    # Строит AST, используя библиотеку ply, обходит его и формирует очередь комманд
    def parse(self, *, input_data: str):
        if not input_data:
            return []
        ast = yacc_parser.parse(input_data)
        command_list = self.__traverse_ast__(root=ast)
        return command_list
