import inspect

class LogLevel:
    INFO = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    DEFAULT = '\033[m'

class Logger:
    @staticmethod
    def LogMessage(msg, log_level=LogLevel.INFO):
        stack = inspect.stack()
        function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
        print('{} [+] {} {}'.format(log_level, function_name, msg))
        print(LogLevel.DEFAULT) # restore console color
