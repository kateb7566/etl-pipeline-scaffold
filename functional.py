import os
from pathlib import Path
import argparse

import config

def scaffold(base_path: str, structure: dict):
    for name, content in structure.items():
        if name == "__files__":
            for file_name in content:
                file_path = base_path / file_name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                if not file_path.exists():
                    with open(file_path, "w") as f:
                        f.write(config.TEMPLATE_FILES.get(file_name, ""))
        else:
            new_path = base_path / name
            new_path.mkdir(parents=True, exist_ok=True)
            scaffold(new_path, content)

def main():
    parser = argparse.ArgumentParser(description="Python ETL Data Pipeline project scaffolding tool.")
    parser.add_argument("--name", required=True, help="Project name / root directory")
    args = parser.parse_args()

    base_dir = Path(args.name)
    if base_dir.exists():
        print(f"❌ Directory '{args.name}' already exists.")
        return

    print(f"📁 Creating project: {args.name}")
    scaffold(base_dir, config.PROJECT_STRUCTURE)
    print("✅ Project scaffolded successfully!")