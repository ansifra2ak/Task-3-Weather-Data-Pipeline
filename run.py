"""One-click setup and launch from VS Code or a local terminal."""
from pathlib import Path
import subprocess, sys, venv
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    if sys.version_info < (3,10): raise SystemExit('Python 3.10+ required.')
    env=ROOT/'.venv'; python=env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
    if not python.exists(): venv.EnvBuilder(with_pip=True).create(env)
    subprocess.run([str(python),'-m','pip','install','-r',str(ROOT/'requirements.txt')],check=True,cwd=ROOT)
    subprocess.run([str(python),str(ROOT/'main.py'),'start'],cwd=ROOT,check=True)
