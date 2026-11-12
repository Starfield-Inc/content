"""Assemble first_notebook.ipynb from the files in cells/, one code cell per file."""
from pathlib import Path

import nbformat

nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_markdown_cell("# Label sentences with a model, then chart them"))
for path in sorted(Path("cells").glob("*.py")):
    nb.cells.append(nbformat.v4.new_code_cell(path.read_text().rstrip()))
nbformat.write(nb, "first_notebook.ipynb")
print(f"Wrote first_notebook.ipynb with {len(nb.cells)} cells")
