#how to import discum on repl.it

try:
    import discum
except:
    import os
    os.system("pip install git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum")
    import discum

'''
or, you can put this in your pyproject.toml file (ty dolfies for noting this):
discum = { git = "git@github.com:Merubokkusu/Discord-S.C.U.M.git", branch = "master" }
'''
