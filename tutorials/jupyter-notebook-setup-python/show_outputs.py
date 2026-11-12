"""Print the text output of each code cell in an executed notebook."""
import sys

import nbformat

nb = nbformat.read(sys.argv[1], as_version=4)
for number, cell in enumerate((c for c in nb.cells if c.cell_type == "code"), 1):
    print(f"--- cell {number} ---")
    for out in cell.outputs:
        if out.output_type == "stream":
            print(out.text.rstrip())
        elif out.output_type == "display_data" and "image/png" in out.data:
            print("[chart image, PNG]")
        elif out.output_type == "error":
            print("ERROR:", out.ename, "-", out.evalue)
