from pathlib import Path
folder= Path("src")
for item in folder.iterdir():
    if item.is_dir():
        print("FOLDER:",item.name)
    else:
        print("FILE:",item.name)
