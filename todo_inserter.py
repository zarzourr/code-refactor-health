import ast, os


def is_empty_function(node):
    return (
        isinstance(node, ast.FunctionDef)
        and len(node.body) == 1
        and isinstance(node.body[0], ast.Pass)
    )


def insert_todos(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    tree = ast.parse("".join(lines))
    offset = 0
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and is_empty_function(node):
            lineno = node.lineno - 1 + offset
            lines.insert(lineno, "    # TODO: implement this function\n")
            offset += 1
    with open(file_path, "w") as f:
        f.writelines(lines)


def scan_directory(root="."):
    for dirpath, _, filenames in os.walk(root):
        if "venv" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".py"):
                insert_todos(os.path.join(dirpath, filename))


scan_directory()
