#https://earthly.dev/blog/python-ast/
import json
import ast
try:
    from graphviz import Digraph
except Exception:
    Digraph = None

class DependencyGenerator:
    def _safe_parse(self, content):
        try:
            return ast.parse(content)
        except Exception:
            return None
    
    def generateGraph(self, content) -> None:
        if Digraph is None:
            print("graphviz not available; skipping graph generation")
            return None

        tree = self._safe_parse(content)
        if tree is None:
            return None

        dot = Digraph()

        def add_node(node, parent=None):
            node_name = str(node.__class__.__name__)
            dot.node(str(id(node)), node_name)
            if parent:
                dot.edge(str(id(parent)), str(id(node)))
            for child in ast.iter_child_nodes(node):
                add_node(child, node)

        add_node(tree)

        dot.format = 'png'
        dot.render('my_ast', view=True)

    def extract_imports(self, content) -> list:
        tree = self._safe_parse(content)
        if tree is None:
            return []
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias.name}")

        return imports

    def extract_functions(self, content) -> list:       
        tree = self._safe_parse(content)
        if tree is None:
            return []
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                returns = None
                try:
                    if node.returns is not None:
                        returns = ast.unparse(node.returns)
                except Exception:
                    returns = None
                functions.append({
                    'name': node.name,
                    'args': args,
                    'returns': returns,
                    'docstring': ast.get_docstring(node)
                })

        return functions

    def extract_classes(self, content) -> list:
        """Return classes with bases, methods and docstring.

        Returns list of dicts: {name, bases, methods, docstring}
        """
        tree = self._safe_parse(content)
        if tree is None:
            return []
        classes = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                bases = []
                for b in node.bases:
                    try:
                        bases.append(ast.unparse(b))
                    except Exception:
                        bases.append(getattr(b, 'id', str(type(b))))

                methods = []
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        methods.append(child.name)

                classes.append({
                    'name': node.name,
                    'bases': bases,
                    'methods': methods,
                    'docstring': ast.get_docstring(node)
                })

        return classes

    def extract_docstrings(self, content) -> dict:
        """Return module docstring and per-symbol docstrings."""
        tree = self._safe_parse(content)
        if tree is None:
            return {'module': None, 'functions': {}, 'classes': {}}
        module_doc = ast.get_docstring(tree)
        functions = self.extract_functions(content)
        classes = self.extract_classes(content)
        return {
            'module': module_doc,
            'functions': {f['name']: f['docstring'] for f in functions},
            'classes': {c['name']: c['docstring'] for c in classes}
        }

    def extract_type_hints(self, content):
        """Extract simple type hints from top-level functions.

        Returns dict mapping function name to {'args': {arg: annotation}, 'returns': annotation}
        """
        tree = self._safe_parse(content)
        if tree is None:
            return {}
        hints = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                arg_hints = {}
                for arg in node.args.args:
                    ann = None
                    if arg.annotation is not None:
                        try:
                            ann = ast.unparse(arg.annotation)
                        except Exception:
                            ann = None
                    arg_hints[arg.arg] = ann
                ret = None
                if node.returns is not None:
                    try:
                        ret = ast.unparse(node.returns)
                    except Exception:
                        ret = None
                hints[node.name] = {'args': arg_hints, 'returns': ret}
        return hints

    def extract_top_level_constants(self, content):
        """Return module-level simple constants (NAME = Constant).

        Returns list of dicts: {name, value_repr}
        """
        tree = self._safe_parse(content)
        if tree is None:
            return []
        consts = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                # only simple name targets
                names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                if not names:
                    continue
                # try to evaluate constant-ish values
                if isinstance(node.value, (ast.Constant, ast.Num, ast.Str, ast.Bytes)):
                    val = node.value.value if isinstance(node.value, ast.Constant) else None
                    for n in names:
                        consts.append({'name': n, 'value': repr(val)})
        return consts

    def extract_todos(self, content):
        """Return list of comment TODO/FIXME lines with line numbers."""
        todos = []
        for i, line in enumerate(content.splitlines(), start=1):
            idx = line.lower().find('todo')
            fix = line.lower().find('fixme')
            if idx != -1 or fix != -1:
                todos.append({'line': i, 'text': line.strip()})
        return todos

    def summarize_file(self, content):
        """Return a combined summary dict for a file using the various extractors."""
        return {
            'imports': self.extract_imports(content),
            'functions': self.extract_functions(content),
            'classes': self.extract_classes(content),
            'docstrings': self.extract_docstrings(content),
            'type_hints': self.extract_type_hints(content),
            'constants': self.extract_top_level_constants(content),
            #'todos': self.extract_todos(content)
        }
    def __init__(self) -> None:
        pass


