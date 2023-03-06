from abc import ABC, abstractmethod
#invoker - game, reciever - character, command - update stat
#need a way to have a different command list for each character, and to have real time output
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod 
    def unExecute(self) -> None:
        pass

class CharCommand(Command):
    def __init__(self, receiver, amount, stat):
        self._receiver = receiver
        self.amount = amount
        self.stat = stat

    def execute(self) -> None:
        self._receiver.updateStat(self.amount, self.stat)

    def unExecute(self) -> None:
        self._receiver.undoStat(self.amount, self.stat)


