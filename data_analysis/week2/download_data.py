"""Download assignment datasets and verify the archives against SOURCES.json."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent

def main():
    sources=json.loads((ROOT/'SOURCES.json').read_text())
    with tempfile.TemporaryDirectory() as temporary:
        for name,source in sources.items():
            archive=Path(temporary)/(name+'.zip')
            subprocess.run(['curl','-L','--fail','--silent','--show-error','--max-time','120',source['url'],'-o',str(archive)],check=True)
            digest=hashlib.sha256(archive.read_bytes()).hexdigest()
            if digest!=source['archive_sha256']:
                raise ValueError(f'{name}: upstream archive changed; inspect before updating the recorded hash')
            destination=ROOT/'data'/name
            destination.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(archive) as z:
                for member in z.infolist():
                    if member.filename.startswith('__MACOSX/'):
                        continue
                    target=(destination/member.filename).resolve()
                    if not target.is_relative_to(destination.resolve()):
                        raise ValueError('Unsafe archive path')
                    z.extract(member,destination)
            for filename,expected in source['files'].items():
                if hashlib.sha256((destination/filename).read_bytes()).hexdigest()!=expected:
                    raise ValueError(f'{name}/{filename}: content hash mismatch')
            print('Verified',name)

if __name__=='__main__':
    main()
