from abc import ABC, abstractmethod
#figure out how to get working, need real time data even before executed
#invoker - game, reciever - character, command - update stat
#need a way to have a different command list for each character, and to have real time output
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod 
    def undo(self) -> None:
        pass

    @abstractmethod
    def redo(self) -> None:
        pass

class CharCommand(Command):
    def __init__(self, receiver, amount, stat):
        self._receiver = receiver
        self.amount = amount
        self.stat = stat
        self.character = character

    def execute(self) -> None:
        self._receiver.updateStat(self.amount, self.stat)

    def unExecute(self) -> None:
        self._receiver.undoStat(self.amount, self.stat)

class Invoker():
    def __init__(self):
        self._history_pivot = 0
        self._command_list = []

    def history(self):

    def undo(self):

    def redo(self):

