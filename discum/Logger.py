import inspect

class LogLevel:
    INFO = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    DEFAULT = '\033[m'

class Logger:
    @staticmethod
    def LogMessage(msg, hex_data='', to_file=False, to_console=True, log_level=LogLevel.INFO): #to_file was acting a bit buggy so I decided to remove it altogether for now
        stack = inspect.stack()
        function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
        if to_console is True:
            if hex_data is not '':
                print('{} {}'.format(log_level, " ".join([h.encode('hex') for h in hex_data])))
            else:
                print('{} [+] {} {}'.format(log_level, function_name, msg))
            print(LogLevel.DEFAULT) # restore console color
