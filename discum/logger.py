import colorama
colorama.init()

class LogLevel:
	SEND = colorama.Fore.MAGENTA
	RECEIVE = colorama.Fore.GREEN
	WARNING = colorama.Fore.YELLOW
	DEFAULT = colorama.Style.RESET_ALL

class Logger:
	@staticmethod
	def log(text, color=None, log={"console":True, "file":False, "encoding":"utf-8"}):
		if isinstance(log, bool):
			log = {"console":log, "file":False}
		if "encoding" not in log:
			log["encoding"] = "utf-8"
		if log["console"]:
			if color:
				string = color + text + '\033[m'
			else:
				string = text
			print(string)
		if log["file"]:
			with open(log["file"], 'a+', encoding=log["encoding"], errors="ignore") as f:
				try:
					f.write(text + '\n\n')
				except UnicodeEncodeError:
					print("Error: Failed to write unicode characters to log. You may need to change your log encoding to utf-8.")
				except Exception as e:
					print("Failed to write to log! Error: {} You may need to change your log encoding to utf-8.".format(e))
