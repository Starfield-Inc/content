"""Run the tools by hand, with no model, to see what the agent will be allowed to do."""
from repo_tools import RepoTools

tools = RepoTools("sample_repo")

print("$ list_files")
print(tools.run("list_files", {}))
print()
print("$ search_text 'MAX_TITLE'")
print(tools.run("search_text", {"query": "MAX_TITLE"}))
print()
for path in ["README.md", "../private/notes.txt", "/etc/hosts", "shelf/../../private/notes.txt"]:
    first_line = tools.run("read_file", {"path": path}).splitlines()[0]
    print(f"$ read_file {path}\n  -> {first_line}")
