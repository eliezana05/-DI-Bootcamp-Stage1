"""Execute every submitted notebook, preserving outputs for GitHub review."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parent
for path in sorted(ROOT.glob('day*/*.ipynb')):
    nb=nbformat.read(path,as_version=4)
    NotebookClient(nb,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(path.parent)}}).execute()
    nbformat.write(nb,path)
    print('PASS',path.relative_to(ROOT))
