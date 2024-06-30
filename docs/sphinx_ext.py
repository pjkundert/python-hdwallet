def setup(app):
    app.connect('autodoc-process-docstring', update_docstring)

def update_docstring(app, what, name, obj, options, lines):
    if what == 'class':
        idx = 1
    else:
        idx = 2

    module_path = ".".join(name.split(".")[:-idx])
    class_name = name.split(".")[-idx]
    for i, line in enumerate(lines):
        lines[i] = line\
                    .replace("{class_name}", class_name)\
                    .replace("{module_path}", module_path)

