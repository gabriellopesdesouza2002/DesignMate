import os
import shutil
def cria_diretorio_no_local_do_projeto(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)