class ExceptionTemplate(Exception):

    def __call__(self, *args):
        return self.__class__(*(self.args + args))

    def __str__(self):
        return ': '.join(self.args)


class RegisterError(ExceptionTemplate): pass


class ReceiveStonesError(ExceptionTemplate): pass


class MakeAMoveError(ExceptionTemplate): pass


class EndGameError(ExceptionTemplate): pass

