from glob import glob
from pathlib import Path
import shutil

from constants import N, STATS_PATH, ENCODING

def move_fs(source_path, dest_dir):
  Path(dest_dir).mkdir(parents=True, exist_ok=True)
  shutil.move(f"{source_path}/Fconst", f"{dest_dir}/Fconst")

  for fhd_dir_path in glob(f"{source_path}/FHD*"):
    shutil.move(fhd_dir_path, f"{dest_dir}/{fhd_dir_path.split('/').pop()}")

def move_fxs(source_path, dest_dir):
  Path(dest_dir).mkdir(parents=True, exist_ok=True)
  for fx_dir_path in glob(f"{source_path}/*x*"):
    shutil.move(fx_dir_path, f"{dest_dir}/{fx_dir_path.split('/').pop()}")

def move_xlsx(source_path, dest_dir):
  Path(dest_dir).mkdir(parents=True, exist_ok=True)
  for xlsx_path in list(Path(source_path).rglob("*.xlsx")):
    shutil.move(xlsx_path, f"{dest_dir}/")

def main():
  dest_dir = "archives"
  Path(dest_dir).mkdir(parents=True, exist_ok=True)

  if ENCODING == 'binary':
    move_xlsx(STATS_PATH,  f"{dest_dir}/charts")
    move_fs(STATS_PATH, f"{dest_dir}/binary_chains")

  move_fxs(STATS_PATH, f"{dest_dir}/{ENCODING}")


# move_xlsx(STATS_PATH,  f"archives/{ENCODING}/{N}/charts")

main()
