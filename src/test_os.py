import os
import shutil
print(os.path.exists("public"))
print(os.listdir("static"))
print(os.path.isfile("src/block.py"))
shutil.rmtree("public")
