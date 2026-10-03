from pathlib import Path
from rscbench.freeze import freeze

root = Path(__file__).resolve().parents[1]
manifest = freeze(root)
print("Prompts frozen.")
print(manifest)
