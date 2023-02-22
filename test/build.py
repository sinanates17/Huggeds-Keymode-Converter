from subprocess import PIPE, run
import shutil
import os

MAIN_SCRIPT_NAME = 'Converter'
OUTPUT_NAME = 'Hugged\'s Keymode Converter'

run(['pyinstaller', '--onefile', f'{MAIN_SCRIPT_NAME}.py'], stdout=PIPE, stderr=PIPE, universal_newlines=True, timeout=20)

os.makedirs('build/zipper/Input', exist_ok=True)
os.makedirs('build/zipper/Output', exist_ok=True)
shutil.copy(f'dist/{MAIN_SCRIPT_NAME}.exe', 'build/zipper')
shutil.copy(f'config.ini', 'build/zipper')
shutil.make_archive(f'dist/{OUTPUT_NAME}', 'zip', 'build/zipper')