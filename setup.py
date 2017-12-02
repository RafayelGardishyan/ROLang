from cx_Freeze import setup, Executable

setup(name = "RO" ,
      version = "0.1" ,
      description = "The Cobra programming language" ,
      executables = [Executable("ro.py")])
