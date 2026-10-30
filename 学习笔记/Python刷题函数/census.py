"""Census of Python functions / methods / stdlib / syntax used by 灵茶山艾府 and yiduobo."""
import ast, builtins, json, re, sys, textwrap, warnings, collections
warnings.filterwarnings('ignore')

SRC = '/home/claude/pyfuncs/allcode.json'
AUTHORS = ['灵茶山艾府', 'yiduobo']

# ---------------- name tables ----------------
BARE = {}  # bare name -> module.name  (LeetCode auto star-imports these)
for mod, names in {
    'heapq': ('heappush heappop heapify heapreplace heappushpop nlargest nsmallest merge '
              'heappush_max heappop_max heapify_max heapreplace_max heappushpop_max'),
    'bisect': 'bisect_left bisect_right bisect insort insort_left insort_right',
    'collections': 'Counter defaultdict deque OrderedDict namedtuple ChainMap',
    'itertools': ('accumulate pairwise permutations combinations combinations_with_replacement product groupby '
                  'chain count cycle repeat islice starmap zip_longest compress takewhile dropwhile batched tee filterfalse izip'),
    'functools': 'cache lru_cache reduce cmp_to_key partial total_ordering cached_property',
    'math': ('inf gcd lcm comb perm isqrt sqrt log log2 log10 floor ceil factorial pi hypot prod isclose fsum '
             'trunc exp nan atan2 sin cos tau cbrt degrees acos'),
    'operator': 'add mul sub xor or_ and_ itemgetter attrgetter neg floordiv truediv mod iand ior ixor setitem',
    'string': 'ascii_lowercase ascii_uppercase ascii_letters',
    'sortedcontainers': 'SortedList SortedDict SortedSet',
    'random': 'randint shuffle randrange',
    'copy': 'deepcopy',
}.items():
    for n in names.split():
        BARE[n] = f'{mod}.{n}'
# py2 builtin reduce == functools.reduce
BARE['reduce'] = 'functools.reduce'
BARE['izip'] = 'itertools.izip'

KNOWN_MODULES = {'heapq', 'bisect', 'collections', 'itertools', 'functools', 'math', 'operator', 'string',
                 'sortedcontainers', 'random', 'copy', 'sys', 're', 'typing', 'queue', 'Queue', 'array', 'cmath',
                 'decimal', 'fractions', 'statistics', 'numpy', 'np', 'threading', 'time', 'datetime', 'json',
                 'os', 'struct', 'types', 'enum', 'dataclasses', 'contextlib', 'abc', 'weakref', 'gc'}

PY2_BUILTINS = {'xrange', 'cmp', 'unicode', 'long', 'raw_input', 'basestring', 'unichr', 'apply', 'execfile', 'file',
                'intern', 'buffer', 'coerce'}
BUILTIN_FUNCS = {n for n in dir(builtins)
                 if not n.startswith('_') and n[0].islower() and callable(getattr(builtins, n))} | PY2_BUILTINS
BUILTIN_FUNCS -= {'copyright', 'credits', 'license', 'exit', 'quit', 'help', 'aiter', 'anext', 'breakpoint'}

# methods we recognise (receiver type) — used for labelling only
METHOD_TYPES = {
    'list': 'append pop sort extend insert reverse index count remove clear copy',
    'str': ('join split strip lstrip rstrip lower upper isdigit isalpha isalnum islower isupper isspace startswith '
            'endswith find rfind replace format zfill ljust rjust center swapcase title capitalize partition rsplit '
            'encode decode splitlines isnumeric isdecimal translate maketrans rindex expandtabs casefold'),
    'dict': 'get setdefault items keys values update popitem fromkeys iteritems itervalues iterkeys has_key viewitems',
    'set': ('add discard union intersection difference symmetric_difference issubset issuperset isdisjoint '
            'intersection_update difference_update'),
    'deque': 'popleft appendleft extendleft rotate',
    'int': 'bit_count bit_length to_bytes as_integer_ratio conjugate',
    'Counter': 'most_common elements subtract total',
    'OrderedDict': 'move_to_end',
    'SortedList': 'bisect_left bisect_right irange islice peekitem',
    'float': 'is_integer',
}
METHOD_LABEL = {}
for t, ms in METHOD_TYPES.items():
    for m in ms.split():
        METHOD_LABEL.setdefault(m, t)
for m in ('pop', 'remove', 'clear', 'copy', 'update', 'count', 'index'):
    METHOD_LABEL[m] = 'list/dict/set' if m in ('pop', 'clear', 'copy') else METHOD_LABEL[m]
METHOD_LABEL['pop'] = 'list/dict/set'
METHOD_LABEL['remove'] = 'list/set'
METHOD_LABEL['update'] = 'dict/set/Counter'
METHOD_LABEL['count'] = 'list/str'
METHOD_LABEL['index'] = 'list/str'
METHOD_LABEL['bisect_left'] = 'SortedList'
METHOD_LABEL['add'] = 'set/SortedList'
METHOD_LABEL.update({'cache_clear': '@cache 函数', 'cache_info': '@cache 函数', 'acquire': 'threading', 'release': 'threading',
                     'put': 'Queue', 'matrix_power': 'numpy', 'wait': 'threading', 'notify': 'threading',
                     'notify_all': 'threading', 'set': 'threading', 'reshape': 'numpy', 'dot': 'numpy', 'tolist': 'numpy',
                     'astype': 'numpy'})


# ---------------- parsing with light fixes ----------------
CJK_PUNCT = re.compile(r'[：，。“”（）＊]')


def looks_like_text(code):
    s = code.strip()
    return (s.startswith('输入') or s.startswith('输出') or s.startswith('解释')) or (
        len(CJK_PUNCT.findall(s)) > 2 and 'def ' not in s and 'class ' not in s)


def fix_py2(code):
    lines = []
    for l in code.splitlines():
        l = re.sub(r'^(\s*)print\s*$', r'\1print()', l)
        m = re.match(r'^(\s*)print(?![\w(])\s*(.*?),?\s*$', l)
        if m and not m.group(2).startswith('('):
            l = f'{m.group(1)}print({m.group(2)})'
        l = re.sub(r'except\s+([\w.]+)\s*,\s*(\w+)\s*:', r'except \1 as \2:', l)
        l = l.replace('<>', '!=')
        l = re.sub(r'\b(\d+)[lL]\b', r'\1', l)
        lines.append(l)
    return '\n'.join(lines)


def try_parse(code):
    """returns (tree or None, status, fixed_code)"""
    c = code
    if c.lstrip().startswith('>'):
        c = '\n'.join(re.sub(r'^\s*>\s?', '', l) for l in c.splitlines())
    c = textwrap.dedent(c)
    for stage, fn in (('ok', lambda s: s), ('fixed', fix_py2), ('fixed', lambda s: fix_py2(s).expandtabs(8))):
        s = fn(c)
        try:
            return ast.parse(s), stage, s, None
        except SyntaxError as e:
            err = e
    # last resort: blank out offending lines (keep indentation) a few times
    s = fix_py2(c).expandtabs(8)
    L = s.splitlines()
    for _ in range(6):
        try:
            return ast.parse('\n'.join(L)), 'partial', '\n'.join(L), None
        except SyntaxError as e:
            if not e.lineno or e.lineno > len(L):
                break
            bad = L[e.lineno - 1]
            L[e.lineno - 1] = re.match(r'\s*', bad).group(0) + 'pass'
    return None, 'failed', c, err


# ---------------- AST census ----------------
class Census(ast.NodeVisitor):
    def __init__(self, tree):
        self.c = collections.Counter()  # key -> count
        self.kw = collections.Counter()  # (func, kw) -> count
        self.alias = {}  # local alias -> module
        self.from_names = {}  # local name -> module.name
        self.bound = set()  # names bound locally (vars, defs, args)
        self.defined_methods = set()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.bound.add(n.name)
                self.defined_methods.add(n.name)
                a = n.args
                for x in a.args + a.kwonlyargs + a.posonlyargs + ([a.vararg] if a.vararg else []) + (
                        [a.kwarg] if a.kwarg else []):
                    self.bound.add(x.arg)
            elif isinstance(n, ast.ClassDef):
                self.bound.add(n.name)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                self.bound.add(n.id)
            elif isinstance(n, ast.Lambda):
                for x in n.args.args:
                    self.bound.add(x.arg)
            elif isinstance(n, ast.Import):
                for a in n.names:
                    self.alias[(a.asname or a.name).split('.')[0]] = a.name.split('.')[0]
            elif isinstance(n, ast.ImportFrom) and n.module:
                for a in n.names:
                    if a.name != '*':
                        self.from_names[a.asname or a.name] = f'{n.module.split(".")[0]}.{a.name}'
        self.tree = tree

    def add(self, k, n=1):
        self.c[k] += n

    # skip annotations entirely
    def visit_arg(self, node):
        pass

    def visit_AnnAssign(self, node):
        self.add('syn:类型注解')
        self.visit(node.target)
        if node.value:
            self.visit(node.value)

    def visit_FunctionDef(self, node):
        if node.returns is not None or any(a.annotation for a in node.args.args):
            self.add('syn:类型注解')
        for d in node.decorator_list:
            base = d.func if isinstance(d, ast.Call) else d
            name = ast.unparse(base).split('.')[-1]
            if isinstance(d, ast.Call):
                args = ', '.join(ast.unparse(a) for a in d.args) + ', '.join(
                    f'{k.arg}={ast.unparse(k.value)}' for k in d.keywords)
                self.add(f'deco:@{name}({args})')
            else:
                self.add(f'deco:@{name}')
        if node.name.startswith('__') and node.name.endswith('__') and node.name != '__init__':
            self.add(f'syn:魔术方法 {node.name}')
        for d in node.decorator_list:
            self.visit(d)
        for x in node.args.defaults + node.args.kw_defaults:
            if x is not None:
                self.visit(x)
        for s in node.body:
            self.visit(s)
        if self._inside_func(node):
            self.add('syn:嵌套函数(闭包)')

    visit_AsyncFunctionDef = visit_FunctionDef

    def _inside_func(self, node):
        return getattr(node, '_nested', False)

    def visit_ClassDef(self, node):
        if node.name not in ('Solution',):
            self.add('syn:自定义类')
        for s in node.body:
            self.visit(s)
        for k in node.keywords:
            self.visit(k)

    # ---- names
    def resolve_name(self, nid):
        if nid in self.from_names:
            return 'mod', self.from_names[nid]
        if nid in self.bound:
            return None, None
        if nid in BARE:
            return 'mod', BARE[nid]
        if nid in BUILTIN_FUNCS:
            return 'builtin', nid
        return None, None

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            kind, key = self.resolve_name(node.id)
            if kind == 'mod':
                self.add('mod:' + key)
            elif kind == 'builtin':
                self.add('builtin:' + node.id)

    def visit_Attribute(self, node):
        v = node.value
        if isinstance(v, ast.Name) and v.id not in self.bound and (v.id in self.alias or v.id in KNOWN_MODULES):
            mod = self.alias.get(v.id, v.id)
            if mod == 'np':
                mod = 'numpy'
            if mod != 'typing':
                self.add(f'mod:{mod}.{node.attr}')
            return
        self.generic_visit(node)

    def visit_Call(self, node):
        f = node.func
        fname = None
        if isinstance(f, ast.Name):
            fname = self.resolve_name(f.id)[1]
            if f.id == 'float' and node.args and isinstance(node.args[0], ast.Constant) and \
                    str(node.args[0].value).strip().lstrip('+-').lower() in ('inf', 'infinity'):
                self.add("syn:float('inf')")
            if f.id == 'print':
                self.add('syn:print 调用(调试残留)')
        elif isinstance(f, ast.Attribute):
            v = f.value
            is_mod = isinstance(v, ast.Name) and v.id not in self.bound and (
                v.id in self.alias or v.id in KNOWN_MODULES)
            if is_mod:
                fname = f'{self.alias.get(v.id, v.id)}.{f.attr}'
            elif isinstance(v, ast.Name) and v.id in ('self', 'cls'):
                pass
            elif isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == 'super':
                pass
            elif f.attr in self.defined_methods and f.attr not in METHOD_LABEL:
                pass
            elif f.attr in self.defined_methods and not isinstance(v, (ast.Constant, ast.List, ast.Dict)):
                pass  # user-defined method with same name as a builtin method (e.g. UnionFind.find)
            else:
                self.add('method:.' + f.attr)
                fname = '.' + f.attr
                if isinstance(v, ast.Constant) and isinstance(v.value, str) and f.attr == 'join':
                    self.add("syn:''.join 拼接")
        if fname:
            for k in node.keywords:
                if k.arg:
                    self.kw[(fname, k.arg)] += 1
            if fname in ('sorted', '.sort', 'max', 'min', 'heapq.nlargest') and any(
                    k.arg == 'key' and isinstance(k.value, ast.Lambda) for k in node.keywords):
                self.add('syn:key=lambda')
            if any(k.arg == 'cmp' for k in node.keywords):
                self.add('py2:sort/sorted 的 cmp= 参数')
        if any(isinstance(a, ast.Starred) for a in node.args) or any(k.arg is None for k in node.keywords):
            self.add('syn:调用时解包 *args/**kw')
        self.generic_visit(node)

    # ---- syntax features
    def visit_ListComp(self, n):
        self.add('syn:列表推导式'); self._comp(n)

    def visit_SetComp(self, n):
        self.add('syn:集合推导式'); self._comp(n)

    def visit_DictComp(self, n):
        self.add('syn:字典推导式'); self._comp(n)

    def visit_GeneratorExp(self, n):
        self.add('syn:生成器表达式'); self._comp(n)

    def _comp(self, n):
        if len(n.generators) > 1:
            self.add('syn:多重 for 推导式')
        if any(g.ifs for g in n.generators):
            self.add('syn:推导式带 if 过滤')
        self.generic_visit(n)

    def visit_Subscript(self, n):
        s = n.slice
        if isinstance(s, ast.Slice):
            self.add('syn:切片 a[i:j]')
            st = s.step
            if st is not None and ast.unparse(st) == '-1':
                self.add('syn:切片反转 [::-1]')
            elif st is not None:
                self.add('syn:切片步长 a[::k]')
            if (s.lower is not None and ast.unparse(s.lower).startswith('-')) or (
                    s.upper is not None and ast.unparse(s.upper).startswith('-')):
                self.add('syn:负数切片 a[-k:]')
        elif isinstance(s, ast.UnaryOp) and isinstance(s.op, ast.USub):
            self.add('syn:负下标 a[-1]')
        elif isinstance(s, ast.Tuple) and any(isinstance(e, ast.Slice) for e in s.elts):
            self.add('syn:多维切片')
        self.generic_visit(n)

    def visit_Assign(self, n):
        t = n.targets
        if len(t) > 1:
            self.add('syn:链式赋值 a = b = 0')
        for tg in t:
            if isinstance(tg, (ast.Tuple, ast.List)):
                self.add('syn:元组解包赋值 a, b = ...')
                if isinstance(n.value, ast.Tuple) and len(tg.elts) == len(n.value.elts) and \
                        sorted(map(ast.unparse, tg.elts)) == sorted(map(ast.unparse, n.value.elts)) and \
                        list(map(ast.unparse, tg.elts)) != list(map(ast.unparse, n.value.elts)):
                    self.add('syn:交换 a, b = b, a')
                if any(isinstance(e, ast.Starred) for e in tg.elts):
                    self.add('syn:星号解包 a, *b = ...')
        if isinstance(n.value, ast.BinOp) and isinstance(n.value.op, ast.Mult) and isinstance(n.value.left, ast.List):
            self.add('syn:[x] * n 初始化')
        self.generic_visit(n)

    def visit_For(self, n):
        if isinstance(n.target, (ast.Tuple, ast.List)):
            self.add('syn:for 中解包 for i, x in ...')
        if n.orelse:
            self.add('syn:for ... else')
        self.generic_visit(n)

    def visit_While(self, n):
        if n.orelse:
            self.add('syn:while ... else')
        self.generic_visit(n)

    def visit_NamedExpr(self, n):
        self.add('syn:海象运算符 :='); self.generic_visit(n)

    def visit_Lambda(self, n):
        self.add('syn:lambda'); self.generic_visit(n)

    def visit_Nonlocal(self, n):
        self.add('syn:nonlocal')

    def visit_Global(self, n):
        self.add('syn:global')

    def visit_JoinedStr(self, n):
        self.add('syn:f-string'); self.generic_visit(n)

    def visit_Compare(self, n):
        if len(n.ops) >= 2:
            self.add('syn:链式比较 a < b < c')
        for op in n.ops:
            if isinstance(op, (ast.In, ast.NotIn)):
                self.add('syn:in / not in 成员判断')
            if isinstance(op, (ast.Is, ast.IsNot)):
                self.add('syn:is / is not')
        self.generic_visit(n)

    def visit_IfExp(self, n):
        self.add('syn:三元表达式 x if c else y'); self.generic_visit(n)

    OPS = {ast.FloorDiv: '//', ast.Mod: '%', ast.Div: '/', ast.Pow: '**', ast.BitAnd: '&', ast.BitOr: '|',
           ast.BitXor: '^', ast.LShift: '<<', ast.RShift: '>>', ast.MatMult: '@'}

    def visit_BinOp(self, n):
        o = self.OPS.get(type(n.op))
        if o:
            self.add(f'op:{o}')
        if isinstance(n.op, ast.Pow) and isinstance(n.left, ast.Constant) and n.left.value == 10 and \
                isinstance(n.right, ast.Constant) and isinstance(n.right.value, int) and n.right.value >= 9:
            self.add('syn:10 ** 9 等大数(当无穷/取模)')
        if isinstance(n.op, ast.Mod) and isinstance(n.left, ast.Constant) and isinstance(n.left.value, str):
            self.add('syn:% 字符串格式化')
        self.generic_visit(n)

    def visit_AugAssign(self, n):
        o = self.OPS.get(type(n.op))
        if o:
            self.add(f'op:{o}')
        self.add('syn:增量赋值 +=')
        self.generic_visit(n)

    def visit_UnaryOp(self, n):
        if isinstance(n.op, ast.Invert):
            self.add('op:~')
        self.generic_visit(n)

    def visit_BoolOp(self, n):
        self.add('syn:and/or 短路'); self.generic_visit(n)

    def visit_Yield(self, n):
        self.add('syn:yield 生成器'); self.generic_visit(n)

    def visit_YieldFrom(self, n):
        self.add('syn:yield 生成器'); self.generic_visit(n)

    def visit_Try(self, n):
        self.add('syn:try/except'); self.generic_visit(n)

    def visit_With(self, n):
        self.add('syn:with'); self.generic_visit(n)

    def visit_Assert(self, n):
        self.add('syn:assert'); self.generic_visit(n)

    def visit_Delete(self, n):
        self.add('syn:del'); self.generic_visit(n)

    def visit_Match(self, n):
        self.add('syn:match/case'); self.generic_visit(n)

    def visit_Import(self, n):
        for a in n.names:
            self.add(f'import:import {a.name}')

    def visit_ImportFrom(self, n):
        for a in n.names:
            self.add(f'import:from {n.module} import {a.name}')

    def visit_Constant(self, n):
        if isinstance(n.value, int) and not isinstance(n.value, bool) and abs(n.value) in (10 ** 9 + 7,):
            self.add('syn:MOD = 1_000_000_007')


def mark_nested(tree):
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for m in ast.walk(n):
                if m is not n and isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m._nested = True


CALL_RE = re.compile(r'(?<![\w.])([A-Za-z_]\w*)\s*\(|\.([A-Za-z_]\w*)\s*\(')


def regex_census(code):
    c = collections.Counter()
    for a, b in CALL_RE.findall(code):
        if a:
            if a in BARE:
                c['mod:' + BARE[a]] += 1
            elif a in BUILTIN_FUNCS:
                c['builtin:' + a] += 1
        elif b:
            c['method:.' + b] += 1
    return c


def py2_textual(code, c):
    """python2-only markers detectable from text"""
    if re.search(r'^\s*print\s+[^(\s=]', code, re.M):
        c['py2:print 语句'] += len(re.findall(r'^\s*print\s+[^(\s=]', code, re.M))
    if re.search(r'class\s+\w+\(object\)', code):
        c['py2:class X(object)'] += 1
    if '"""\n' in code and ':type ' in code:
        c['py2:docstring 类型注释 :type'] += 1


def main():
    data = json.load(open(SRC))
    keys = {a: collections.Counter() for a in AUTHORS}  # occurrences
    files = {a: collections.Counter() for a in AUTHORS}  # files containing
    example = {a: {} for a in AUTHORS}
    kwc = {a: collections.Counter() for a in AUTHORS}
    st = {a: collections.Counter() for a in AUTHORS}
    failed_examples = []
    for r in data:
        a = r['author']
        st[a]['files'] += 1
        if not r['code']:
            st[a]['files_no_code'] += 1
            continue
        fc = collections.Counter()
        any_ok = False
        for code in r['code']:
            st[a]['blocks'] += 1
            if looks_like_text(code):
                st[a]['blocks_text_skipped'] += 1
                continue
            tree, status, fixed, err = try_parse(code)
            st[a]['blocks_' + status] += 1
            if tree is None:
                c = regex_census(code)
                failed_examples.append((r['file'], str(err)[:80]))
            else:
                any_ok = True
                mark_nested(tree)
                v = Census(tree)
                v.visit(tree)
                c = v.c
                for (fn, k), n in v.kw.items():
                    kwc[a][f'{fn}|{k}'] += n
            if status in ('fixed',) and fixed != code:
                c['py2:需修复才能用 py3 解析'] += 1
            py2_textual(code, c)
            fc.update(c)
        st[a]['files_parsed' if any_ok else 'files_failed'] += 1
        keys[a].update(fc)
        for k in fc:
            files[a][k] += 1
            ex = example[a].get(k)
            fn = r['file'][:4]
            if ex is None:
                example[a][k] = r['file']
    allkeys = set(keys[AUTHORS[0]]) | set(keys[AUTHORS[1]])
    rows = []
    for k in allkeys:
        cat, name = k.split(':', 1)
        rows.append({
            'key': k, 'category': cat, 'name': name,
            'label': METHOD_LABEL.get(name[1:], '其他') if cat == 'method' else '',
            'occ': {a: keys[a][k] for a in AUTHORS},
            'files': {a: files[a][k] for a in AUTHORS},
            'total_occ': sum(keys[a][k] for a in AUTHORS),
            'total_files': sum(files[a][k] for a in AUTHORS),
            'example': {a: example[a].get(k, '') for a in AUTHORS},
        })
    rows.sort(key=lambda x: (-x['total_files'], -x['total_occ'], x['key']))
    out = {
        'authors': AUTHORS,
        'stats': {a: dict(st[a]) for a in AUTHORS},
        'failed_blocks': failed_examples,
        'keywords': {a: dict(kwc[a].most_common()) for a in AUTHORS},
        'rows': rows,
    }
    json.dump(out, open('/home/claude/pyfuncs/census.json', 'w'), ensure_ascii=False, indent=1)
    write_md(out)
    print(json.dumps(out['stats'], ensure_ascii=False, indent=1))
    print('failed:', failed_examples)


CAT_TITLE = [('builtin', '内置函数'), ('method', '对象方法'), ('mod', '标准库 / 第三方库（已合并 bare name 与 module.name）'),
             ('deco', '装饰器'), ('op', '运算符'), ('syn', '语法特性与惯用法'), ('py2', 'Python 2 特征'),
             ('import', 'import 语句')]


def short(f):
    return f.split(' · ')[0]


def write_md(out):
    A = out['authors']
    L = ['# Python 函数使用普查（灵茶山艾府 vs yiduobo）', '']
    L.append('统计口径：`occ` = 出现次数（AST 节点计数），`files` = 出现该项的题解文件数。别名已合并（如 `heappush` 与 '
             '`heapq.heappush` 计为 `heapq.heappush`）。按 files 合计降序。')
    L.append('')
    L.append('| 作者 | 文件数 | 无代码文件 | 代码块 | 直接解析 | 修复后解析 | 部分解析 | 失败(用正则) | 跳过的非代码块 |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for a in A:
        s = out['stats'][a]
        L.append(f"| {a} | {s.get('files', 0)} | {s.get('files_no_code', 0)} | {s.get('blocks', 0)} | {s.get('blocks_ok', 0)} | "
                 f"{s.get('blocks_fixed', 0)} | {s.get('blocks_partial', 0)} | {s.get('blocks_failed', 0)} | {s.get('blocks_text_skipped', 0)} |")
    L.append('')
    for cat, title in CAT_TITLE:
        rows = [r for r in out['rows'] if r['category'] == cat]
        if cat == 'method':
            rows = [r for r in rows if r['total_files'] >= 2]
        L.append(f'## {title}（{len(rows)} 项）')
        L.append('')
        extra = '| 类型 ' if cat == 'method' else ''
        L.append(f'| 名称 {extra}| 灵神 files | 灵神 occ | yiduobo files | yiduobo occ | 示例（灵神） | 示例（yiduobo） |')
        L.append('|---|' + ('---|' if extra else '') + '---|---|---|---|---|---|')
        for r in rows:
            lab = f"| {r['label']} " if extra else ''
            L.append(f"| `{r['name']}` {lab}| {r['files'][A[0]]} | {r['occ'][A[0]]} | {r['files'][A[1]]} | {r['occ'][A[1]]} | "
                     f"{short(r['example'][A[0]])} | {short(r['example'][A[1]])} |")
        L.append('')
    open('/home/claude/pyfuncs/census.md', 'w').write('\n'.join(L))


if __name__ == '__main__':
    main()
