"""Collect variable/parameter/function names used by each author, with roles and contexts."""
import ast, json, re, sys, collections, keyword, builtins
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from census import try_parse, looks_like_text

data = json.load(open('allcode.json'))
AUTH = ['灵茶山艾府', 'yiduobo']

def short(s, n=70):
    s = re.sub(r'\s+', ' ', s)
    return s if len(s) <= n else s[:n - 1] + '…'

def targets_names(t):
    if isinstance(t, ast.Name):
        yield t
    elif isinstance(t, (ast.Tuple, ast.List)):
        for e in t.elts:
            yield from targets_names(e)
    elif isinstance(t, ast.Starred):
        yield from targets_names(t.value)

class Collector:
    def __init__(self):
        self.uses = []   # (name, role, context_str, init_str)

    def run(self, tree):
        self.tree = tree
        for n in ast.walk(tree):
            for c in ast.iter_child_nodes(n):
                c._parent = n
        self.visit_body(tree.body, cls=None, depth=0)

    def classify_methods(self, cls):
        methods = [s for s in cls.body if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))]
        called = set()
        for n in ast.walk(cls):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) \
                    and n.func.value.id == 'self':
                called.add(n.func.attr)
        names = [m.name for m in methods]
        given = set()
        if len(methods) == 1:
            given = {methods[0].name}
        else:
            for m in methods:
                if m.name not in called or m.name.startswith('__'):
                    given.add(m.name)
            if not given and methods:
                given = {methods[0].name}
        # in Solution class, __init__ is author's own
        return given

    def visit_body(self, body, cls, depth):
        for s in body:
            self.visit_stmt(s, cls, depth)

    def add(self, name, role, ctx, init=None):
        if name in ('self', 'cls', '_'):
            if name == '_':
                self.uses.append(('_', role, ctx, init))
            return
        self.uses.append((name, role, ctx, init))

    def handle_func(self, f, cls, depth, given):
        if cls is not None and depth == 1:
            role_p = 'given_param' if given else 'param'
            if not given:
                self.add(f.name, 'func', short('def ' + f.name + '(' + ast.unparse(f.args) + ')'))
        else:
            role_p = 'param'
            self.add(f.name, 'func', short('def ' + f.name + '(' + ast.unparse(f.args) + ')'))
        a = f.args
        for x in a.posonlyargs + a.args + a.kwonlyargs + ([a.vararg] if a.vararg else []) + ([a.kwarg] if a.kwarg else []):
            self.add(x.arg, role_p, short('def ' + f.name + '(' + ast.unparse(f.args) + ')'))
        for d in a.defaults:
            self.visit_expr(d)
        self.visit_body(f.body, None, depth + 1)

    def visit_stmt(self, s, cls, depth):
        if isinstance(s, ast.ClassDef):
            if s.name != 'Solution':
                self.add(s.name, 'class', 'class ' + s.name)
            given = self.classify_methods(s)
            for b in s.body:
                if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    is_given = b.name in given and not (s.name == 'Solution' and b.name == '__init__')
                    self.handle_func(b, s, 1, is_given)
                else:
                    # class-level assignments
                    if isinstance(b, ast.Assign):
                        for t in b.targets:
                            for nm in targets_names(t):
                                self.add(nm.id, 'var', short(ast.unparse(b)), short(ast.unparse(b.value), 50))
                        self.visit_expr(b.value)
                    else:
                        self.visit_stmt(b, None, depth + 1)
            return
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.handle_func(s, cls, depth if cls is None else 1, False)
            return
        if isinstance(s, ast.Assign):
            for t in s.targets:
                self.store_target(t, s)
            self.visit_expr(s.value)
            return
        if isinstance(s, ast.AnnAssign):
            self.store_target(s.target, s)
            if s.value is not None:
                self.visit_expr(s.value)
            return
        if isinstance(s, ast.AugAssign):
            # not a new binding; record as 'aug' so we know how it's updated
            if isinstance(s.target, ast.Name):
                self.add(s.target.id, 'aug', short(ast.unparse(s)))
            self.visit_expr(s.value)
            return
        if isinstance(s, (ast.For, ast.AsyncFor)):
            hdr = short('for ' + ast.unparse(s.target) + ' in ' + ast.unparse(s.iter))
            for nm in targets_names(s.target):
                self.add(nm.id, 'for', hdr)
            self.store_attr(s.target, s)
            self.visit_expr(s.iter)
            self.visit_body(s.body, None, depth)
            self.visit_body(s.orelse, None, depth)
            return
        if isinstance(s, (ast.With, ast.AsyncWith)):
            for it in s.items:
                if it.optional_vars is not None:
                    for nm in targets_names(it.optional_vars):
                        self.add(nm.id, 'var', short(ast.unparse(it)))
            self.visit_body(s.body, None, depth)
            return
        if isinstance(s, ast.Try):
            self.visit_body(s.body, None, depth)
            for h in s.handlers:
                if h.name:
                    self.add(h.name, 'var', 'except ... as ' + h.name)
                self.visit_body(h.body, None, depth)
            self.visit_body(s.orelse, None, depth)
            self.visit_body(s.finalbody, None, depth)
            return
        if isinstance(s, (ast.Import, ast.ImportFrom)):
            return
        # generic: visit expressions and nested bodies
        for field, val in ast.iter_fields(s):
            if isinstance(val, list):
                if val and isinstance(val[0], ast.stmt):
                    self.visit_body(val, None, depth)
                else:
                    for v in val:
                        if isinstance(v, ast.expr):
                            self.visit_expr(v)
            elif isinstance(val, ast.expr):
                self.visit_expr(val)

    def store_target(self, t, stmt):
        ctx = short(ast.unparse(stmt))
        val = getattr(stmt, 'value', None)
        if isinstance(t, ast.Name):
            self.add(t.id, 'var', ctx, short(ast.unparse(val), 50) if val is not None else None)
        elif isinstance(t, (ast.Tuple, ast.List)):
            # tuple unpacking: try to pair init values
            vals = val.elts if isinstance(val, (ast.Tuple, ast.List)) and len(val.elts) == len(t.elts) else None
            for i, e in enumerate(t.elts):
                if isinstance(e, ast.Name):
                    iv = short(ast.unparse(vals[i]), 50) if vals else None
                    self.add(e.id, 'var', ctx, iv)
                else:
                    self.store_target(e, stmt) if not isinstance(e, ast.Starred) else [self.add(n.id, 'var', ctx) for n in targets_names(e)]
        self.store_attr(t, stmt)

    def store_attr(self, t, stmt):
        for n in ast.walk(t):
            if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id == 'self':
                val = getattr(stmt, 'value', None)
                self.add('self.' + n.attr, 'attr', short(ast.unparse(stmt)), short(ast.unparse(val), 50) if isinstance(t, ast.Attribute) and val is not None else None)

    def visit_expr(self, e):
        for n in ast.walk(e):
            if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
                for g in n.generators:
                    hdr = short('for ' + ast.unparse(g.target) + ' in ' + ast.unparse(g.iter))
                    for nm in targets_names(g.target):
                        self.add(nm.id, 'comp', hdr)
            elif isinstance(n, ast.Lambda):
                a = n.args
                for x in a.args:
                    self.add(x.arg, 'lambda', short(ast.unparse(n)))
            elif isinstance(n, ast.NamedExpr):
                self.add(n.target.id, 'var', short(ast.unparse(n)), short(ast.unparse(n.value), 50))

records = []   # one per file: author, num, title, uses
stat = collections.Counter()
for rec in data:
    uses = []
    ok = False
    for code in rec['code']:
        if looks_like_text(code):
            continue
        tree, st, fixed, err = try_parse(code)
        stat[st] += 1
        if tree is None:
            continue
        ok = True
        c = Collector()
        try:
            c.run(tree)
        except RecursionError:
            continue
        uses.extend(c.uses)
    if ok:
        records.append(dict(author=rec['author'], num=rec['num'], title=rec['title'], file=rec['file'], uses=uses))
print(stat, len(records), collections.Counter(r['author'] for r in records))
json.dump(records, open('uses.json', 'w'), ensure_ascii=False)
