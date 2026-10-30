"""Concept -> which name does each author use. Detected structurally from the AST."""
import ast, json, re, sys, collections
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from census import try_parse, looks_like_text
data = json.load(open('allcode.json'))
AUTH = ['灵茶山艾府', 'yiduobo']
C = {a: collections.defaultdict(collections.Counter) for a in AUTH}   # concept -> name -> files
EX = {a: collections.defaultdict(dict) for a in AUTH}                  # concept -> name -> example (num, line)

def U(n):
    try: return ast.unparse(n)
    except Exception: return ''

def is_name(n, nm=None):
    return isinstance(n, ast.Name) and (nm is None or n.id == nm)

def entry_funcs(tree):
    """top-level method(s) of class Solution (or any class)"""
    out = []
    for n in tree.body:
        if isinstance(n, ast.ClassDef):
            for b in n.body:
                if isinstance(b, ast.FunctionDef) and not b.name.startswith('__'):
                    out.append(b)
        elif isinstance(n, ast.FunctionDef):
            out.append(n)
    return out

def analyse(tree, num, a):
    found = collections.defaultdict(set)
    ex = {}
    def hit(concept, name, node):
        if not name or name in ('self',): return
        found[concept].add(name)
        ex.setdefault((concept, name), U(node).split('\n')[0][:90])
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef,))]
    # --- returned variable of entry method (last statement return Name)
    for f in entry_funcs(tree):
        if f.body and isinstance(f.body[-1], ast.Return) and is_name(f.body[-1].value):
            nm = f.body[-1].value.id
            # must be assigned in the function (i.e. an accumulator)
            assigned = any(isinstance(x, (ast.Assign, ast.AugAssign)) and any(is_name(t, nm) for t in (x.targets if isinstance(x, ast.Assign) else [x.target])) for x in ast.walk(f))
            if assigned: hit('返回的答案变量', nm, f.body[-1])
    params_given = set()
    for f in entry_funcs(tree):
        params_given |= {x.arg for x in f.args.args}
    for n in ast.walk(tree):
        # --- loops
        if isinstance(n, (ast.For, ast.comprehension)):
            it, tg = n.iter, n.target
            if isinstance(it, ast.Call) and is_name(it.func):
                fn = it.func.id
                if fn in ('range', 'xrange') and is_name(tg):
                    hit('range 循环下标', tg.id, it if isinstance(n, ast.comprehension) else ast.For(target=tg, iter=it, body=[], orelse=[]))
                if fn == 'enumerate' and isinstance(tg, ast.Tuple) and len(tg.elts) == 2 and all(is_name(e) for e in tg.elts):
                    hit('enumerate 的 (下标, 元素)', f'{tg.elts[0].id}, {tg.elts[1].id}', it)
                if fn == 'zip' and isinstance(tg, ast.Tuple) and all(is_name(e) for e in tg.elts) and len(tg.elts) == 2:
                    hit('zip 的两个元素', f'{tg.elts[0].id}, {tg.elts[1].id}', it)
            if is_name(it) and is_name(tg) and it.id in params_given:
                # iterate directly over an input
                cname = '直接遍历输入的元素'
                hit(cname, tg.id, ast.For(target=tg, iter=it, body=[], orelse=[]))
            if is_name(tg) and isinstance(it, ast.Subscript) and is_name(it.value) and it.value.id in ('g', 'graph', 'adj', 'edges', 'G', 'e', 'son', 'children', 'nxt', 'neighbors'):
                hit('遍历邻居', tg.id, ast.For(target=tg, iter=it, body=[], orelse=[]))
        if isinstance(n, ast.Assign):
          for t in n.targets:
              v = n.value
              # tuple of grid dims
              if isinstance(t, ast.Tuple) and len(t.elts) == 2 and all(is_name(e) for e in t.elts) and isinstance(v, ast.Tuple) and len(v.elts) == 2:
                  if all(isinstance(e, ast.Call) and is_name(e.func, 'len') for e in v.elts):
                      s0, s1 = U(v.elts[0].args[0]), U(v.elts[1].args[0])
                      if s1 == s0 + '[0]':
                          hit('网格的行数, 列数', f'{t.elts[0].id}, {t.elts[1].id}', n)
              if not is_name(t):
                  continue
              nm = t.id; vs = U(v)
              if re.fullmatch(r'(10 \*\* 9 \+ 7|1000000007|int\(1e9 ?\+ ?7\)|10 \*\* 9 \+ 7)', vs):
                  hit('取模常数 1e9+7', nm, n)
              if isinstance(v, ast.Call) and is_name(v.func):
                  fn = v.func.id
                  if fn == 'deque': hit('队列 (deque)', nm, n)
                  if fn == 'Counter': hit('计数器 Counter', nm, n)
                  if fn == 'defaultdict' and v.args and is_name(v.args[0], 'int'): hit('计数器 defaultdict(int)', nm, n)
                  if fn == 'defaultdict' and v.args and is_name(v.args[0], 'list'): hit('分组/邻接表 defaultdict(list)', nm, n)
                  if fn == 'SortedList': hit('有序集合 SortedList', nm, n)
                  if fn in ('ListNode', 'Node') and nm != 'node': hit('链表哨兵节点', nm, n)
                  if fn in ('max', 'min') and v.args and is_name(v.args[0], nm):
                      hit(f'打擂台 {fn}(变量, ...)', nm, n)
              if isinstance(v, ast.ListComp) and U(v.elt) == '[]':
                  hit('邻接表 [[] for _ in range(n)]', nm, n)
              if vs in ('set()',) : hit('空集合 set()', nm, n)
              if re.fullmatch(r'\[False\] \* .*|\[\[False\] \* .* for .*\]|\[0\] \* .*', vs) and nm in ('vis', 'visited', 'used', 'seen', 'visit', 'vist', 'book', 'v', 'flag', 'mark', 'marked'):
                  hit('访问标记数组', nm, n)
              if vs in ('True', 'False'):
                  hit('布尔标志位', nm, n)
              if vs == '{}' or vs == 'dict()':
                  hit('空字典 {}', nm, n)
              if re.fullmatch(r'\(\(?-?[01], -?[01]\)?(, \(-?[012], -?[012]\))+\)|\[\[?-?[01], -?[01]\]?(, \[-?[012], -?[012]\])+\]|\(\(-?[012], -?[012]\)(, \(-?[012], -?[012]\))+\)|\[\(-?[012], -?[012]\)(, \(-?[012], -?[012]\))+\]', vs):
                  hit('四方向/八方向数组', nm, n)
              if re.fullmatch(r'\[-?[01](, -?[01]){3,7}\]|\(-?[01](, -?[01]){3,7}\)', vs):
                  hit('方向分量数组 (dx/dy 分开写)', nm, n)
              # binary search mid
              if re.fullmatch(r'\(?(\w+) \+ (\w+)\)? (//|>>) (2|1)|(\w+) \+ \((\w+) - (\w+)\) (//|>>) (2|1)|\(?(\w+) \+ (\w+)\)? / 2', vs):
                  hit('二分的中点', nm, n)
                  m = re.match(r'\(?(\w+) \+ \(?(\w+)', vs)
                  if m:
                      m2 = re.match(r'(\w+) \+ \((\w+) - ', vs)
                      bounds = f'{m.group(1)}, {m2.group(2)}' if m2 else f'{m.group(1)}, {m.group(2)}'
                      found['二分的左右边界'].add(bounds)
                      ex.setdefault(('二分的左右边界', list(found['二分的左右边界'])[-1]), vs)
              if 'accumulate(' in vs and 'initial' in vs or re.fullmatch(r'list\(accumulate\(.*', vs):
                  hit('前缀和数组', nm, n)
        # prefix-sum array built by loop: X[i + 1] = X[i] + ...
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Subscript):
            t = n.targets[0]
            if is_name(t.value):
                tn = t.value.id
                ts = U(t.slice); vs = U(n.value)
                m = re.fullmatch(r'(\w+) \+ 1', ts)
                if m and vs.startswith(f'{tn}[{m.group(1)}] + '):
                    hit('前缀和数组', tn, n)
        # prefix sum via append: X.append(X[-1] + ...)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'append' and is_name(n.func.value) and n.args:
            if U(n.args[0]).startswith(n.func.value.id + '[-1] + '):
                hit('前缀和数组', n.func.value.id, n)
        # heap names
        if isinstance(n, ast.Call):
            f = n.func
            fn = f.id if is_name(f) else (f.attr if isinstance(f, ast.Attribute) and is_name(f.value, 'heapq') else None)
            if fn in ('heappush', 'heapify', 'heappop', 'heapreplace', 'heappushpop') and n.args and is_name(n.args[0]):
                hit('堆', n.args[0].id, n)
            # stack: X.append + X[-1] + X.pop()
        # while two-pointer conditions
        if isinstance(n, ast.While) and isinstance(n.test, ast.Compare) and len(n.test.ops) == 1 and isinstance(n.test.ops[0], (ast.Lt, ast.LtE)) \
                and is_name(n.test.left) and is_name(n.test.comparators[0]):
            hit('while 双指针/二分 左右端', f'{n.test.left.id}, {n.test.comparators[0].id}', n.test)
        if isinstance(n, ast.FunctionDef) and n.name == 'find' and n.args.args:
            arg = [x.arg for x in n.args.args if x.arg != 'self']
            for s in ast.walk(n):
                if isinstance(s, ast.Subscript) and arg and is_name(s.slice, arg[-1]):
                    base = U(s.value)
                    if base:
                        hit('并查集父节点数组', base, s); break
    # stack detection per function
    for f in funcs:
        app, neg1, pop = set(), set(), set()
        pop0 = set()
        for s in ast.walk(f):
            if isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute) and is_name(s.func.value):
                nm = s.func.value.id
                if s.func.attr == 'append': app.add(nm)
                if s.func.attr == 'pop' and not s.args: pop.add(nm)
                if s.func.attr == 'pop' and s.args and U(s.args[0]) == '0': pop0.add(nm)
            if isinstance(s, ast.Subscript) and is_name(s.value) and U(s.slice) == '-1':
                neg1.add(s.value.id)
        for nm in app & pop & neg1 - pop0:
            hit('栈 (append + [-1] + pop)', nm, f)
    # recursive / nested helper function names
    for f in funcs:
        for s in f.body:
            pass
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            for s in ast.walk(n):
                if s is not n and isinstance(s, ast.FunctionDef):
                    hit('嵌套辅助函数名', s.name, ast.parse('def %s(): pass' % s.name).body[0] if s.name.isidentifier() else s)
                    if any(isinstance(d, (ast.Name, ast.Call, ast.Attribute)) and ('cache' in U(d)) for d in s.decorator_list):
                        hit('记忆化搜索函数名', s.name, s)
    for k, names in found.items():
        for nm in names:
            C[a][k][nm] += 1
            if nm not in EX[a][k]:
                EX[a][k][nm] = (num, ex.get((k, nm), ''))

for rec in data:
    a = rec['author']
    for code in rec['code']:
        if looks_like_text(code): continue
        tree = try_parse(code)[0]
        if tree is None: continue
        try:
            analyse(tree, rec['num'], a)
        except RecursionError:
            pass
json.dump(dict(C=C, EX=EX), open('concept.json', 'w'), ensure_ascii=False)
concepts = sorted(set(C[AUTH[0]]) | set(C[AUTH[1]]))
for k in concepts:
    print('##', k)
    for a in AUTH:
        tot = sum(C[a][k].values())
        print('  ', a, tot, ' | '.join(f'{n}:{c}' for n, c in C[a][k].most_common(8)))
