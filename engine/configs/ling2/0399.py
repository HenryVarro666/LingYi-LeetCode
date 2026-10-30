EQS = [["a", "b"], ["b", "c"]]
VALS = [2.0, 3.0]
QS = [["a", "c"], ["b", "a"], ["a", "e"]]


def _uf(S):
    if 'self.fa' in S and 'self.mul' in S:
        return S['self.fa'], S['self.mul']
    u = S.get('uf')
    if u is not None and hasattr(u, 'fa') and hasattr(u, 'mul'):
        return u.fa, u.mul
    return None, None


def _names(S):
    m = S.get('variable_to_id') or {}
    return {v: k for k, v in m.items()}


def _nm(S, i):
    return _names(S).get(i, str(i))


def _g(v):
    return f'{v:g}' if isinstance(v, float) else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    fa, mul = _uf(S)
    cv.text((x0 + 18, y0 + 4), '并查集（箭头指向 fa；x · mul[x] = 代表元的值）', 24, T['muted'], bold=True)
    if fa is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    names = _names(S)
    n = len(fa)

    def depth(i):
        d = 0
        while fa[i] != i and d < n:
            i = fa[i]
            d += 1
        return d
    rows = {}
    for i in range(n):
        rows.setdefault(depth(i), []).append(i)
    pos = {}
    for d, ids in rows.items():
        gap = (x1 - x0 - 80) / len(ids)
        for k, i in enumerate(ids):
            pos[i] = (x0 + 40 + gap * (k + 0.5), y0 + 90 + d * 140)
    hot = set()
    if S.get('_line', 0) in range(11, 17) and isinstance(S.get('x'), int):
        hot.add(S['x'])
    for i in range(n):
        if fa[i] != i:
            (ax, ay), (bx, by) = pos[i], pos[fa[i]]
            cv.arrow((ax, ay - 34), (bx, by + 34), T['blue'], 3, 14)
            cv.text(((ax + bx) / 2 + 12, (ay + by) / 2), f'×{_g(mul[i])}', 26, T['yellow'], anchor='lm', bold=True)
    for i in range(n):
        X, Y = pos[i]
        root = fa[i] == i
        c = T['orange'] if i in hot else (T['green'] if root else T['panel2'])
        cv.d.ellipse((X - 34, Y - 34, X + 34, Y + 34), fill=c, outline=T['border'], width=2)
        cv.text((X, Y), names.get(i, str(i)), 30, T['bg'] if (root or i in hot) else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + 44, Y), f'mul={_g(mul[i])}', 22, T['muted'], anchor='lm', mono=True)


def _cap_find_if(S, B, ret):
    fa = S.fa
    x = S.x
    if fa[x] != x:
        return f'`{_nm(S, x)}` 不是代表元（`fa = {_nm(S, fa[x])}`）→ 先递归找到根'
    return f'`{_nm(S, x)}` 就是代表元'


def _cap_mul_upd(S, B, ret):
    x = S.x
    return (f'路径压缩：`mul[{_nm(S, x)}] ×= mul[{_nm(S, S.fa[x])}]` → `{_g(S["self.mul"][x])}`，'
            f'变成 `{_nm(S, x)}` ==直接到根==的比值')


def _cap_merge_mul(S, B, ret):
    x, frm, to, v = S.x, S.from_, S.to, S.value
    m = S['self.mul']
    return (f'`mul[{_nm(S, x)}] = mul[to] × value / mul[from] = {_g(m[to])} × {_g(v)} / {_g(B["self.mul"][frm])}`'
            f' = =={_g(m[x])}==')


def _cap_q_if(S, B, ret):
    c, d = S.c, S.d
    if c == -1 or d == -1:
        return '有变量没在条件里出现过 → 答案 `-1.0`'
    return f'`{_nm(S, c)}` 和 `{_nm(S, d)}` 在同一个集合 → 可以算' if S.ans is not None else ''


CONFIG = dict(
    num=399, title='除法求值', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='带权并查集',
    tags=['热题173', '面试经典150'],
    code='''
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己，自己 * 1 = 自己
        self.fa = list(range(n))  # 代表元
        self.mul = [1.0] * n  # x 的值 * mul[x] = x 的代表元的值

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        fa = self.fa
        if fa[x] != x:
            root = self.find(fa[x])
            self.mul[x] *= self.mul[fa[x]]  # 更新 x 到其代表元的 mul 值
            fa[x] = root
        return fa[x]

    # 判断 x 和 y 是否在同一个集合
    def same(self, x: int, y: int) -> bool:
        # 如果 x 的代表元和 y 的代表元相同，那么 x 和 y 就在同一个集合
        # 这就是代表元的作用：用来快速判断两个元素是否在同一个集合
        return self.find(x) == self.find(y)

    # 合并 from 和 to，新增信息 to / from = value
    # 其中 to 和 from 表示未知量，下文的 x 和 y 也表示未知量
    def merge(self, from_: int, to: int, value: float) -> None:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return
        #    x --------- y
        #   /           /
        # from ------- to
        # 已知 x/from = mul[from] 和 y/to = mul[to]，现在合并 from 和 to，新增信息 to/from = value
        # 由于 y/from = (y/x) * (x/from) = (y/to) * (to/from)
        # 所以 y/x = (y/to) * (to/from) / (x/from) = mul[to] * value / mul[from]
        self.mul[x] = self.mul[to] * value / self.mul[from_]
        self.fa[x] = y


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # 把不同字符串映射为不同的数字，方便使用并查集
        variable_to_id = {}
        for equation in equations:
            for s in equation:
                if s not in variable_to_id:
                    variable_to_id[s] = len(variable_to_id)

        # 初始化并查集
        uf = UnionFind(len(variable_to_id))
        for (a, b), value in zip(equations, values):
            uf.merge(variable_to_id[b], variable_to_id[a], value)

        # 回答询问
        ans = []
        for c, d in queries:
            c = variable_to_id.get(c, -1)
            d = variable_to_id.get(d, -1)
            if c != -1 and d != -1 and uf.same(c, d):
                #    c * mul[c] = d * mul[d] = 代表元的值
                # => c / d = mul[d] / mul[c]
                ans.append(uf.mul[d] / uf.mul[c])
            else:
                ans.append(-1.0)
        return ans
''',
    call=f'Solution().calcEquation({EQS}, {VALS}, {QS})',
    expect=[6.0, 0.5, -1.0],
    views=[
        dict(type='map', var='variable_to_id', label='variable_to_id（字符串 → 编号）', h=96, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=190, label='调用栈'),
    ],
    watch=[('x', 'x'), ('y', 'y'), ('value', 'value', 'yellow'), ('c', 'c'), ('d', 'd'), ('ans', 'ans', 'green')],
    skip=['for equation in equations', 'for s in equation', 'if s not in variable_to_id', 'fa = self.fa',
          'for c, d in queries'],
    captions={
        'variable_to_id[s] = len': '新变量 `"{s}"` → 编号 `{variable_to_id[s]}`',
        'variable_to_id = {}': '把不同字符串映射为不同的数字，方便使用并查集',
        'uf = UnionFind(': '初始化并查集：`{len(variable_to_id)}` 个集合',
        'self.fa = list(range(n))': '一开始每个元素的代表元都是自己',
        'self.mul = [1.0] * n': '自己 × 1 = 自己：`mul` 全是 `1.0`',
        'for (a, b), value in zip': lambda S, B, ret: (f'已知 `{S.a} / {S.b} = {_g(S.value)}`：即 `to / from = value`，to = `{S.a}`，from = `{S.b}`'
                                                       if 'a' in S and ('a' not in B or (B.a, B.b) != (S.a, S.b)) else '所有条件都合并完了'),
        'uf.merge(': lambda S, B, ret: f'`merge(from={S.b}, to={S.a}, value={_g(S.value)})`',
        'x, y = self.find(from_)': lambda S, B, ret: f'先找 from = `{_nm(S, S.from_)}` 和 to = `{_nm(S, S.to)}` 的代表元',
        'if fa[x] != x': _cap_find_if,
        'root = self.find(fa[x])': lambda S, B, ret: f'递归：找 `{_nm(S, S.fa[S.x])}` 的代表元',
        'self.mul[x] *= self.mul[fa[x]]': _cap_mul_upd,
        'fa[x] = root': lambda S, B, ret: f'`fa[{_nm(S, S.x)}]` 直接指向根 `{_nm(S, S.root)}`',
        'return fa[x]': lambda S, B, ret: f'`{_nm(S, S.x)}` 的代表元是 `{_nm(S, ret)}`',
        'if x == y': lambda S, B, ret: (f'代表元 `{_nm(S, S.x)}` ≠ `{_nm(S, S.y)}` → 需要合并' if S.x != S.y else '已在同一集合'),
        'self.mul[x] = self.mul[to]': _cap_merge_mul,
        'self.fa[x] = y': lambda S, B, ret: f'`{_nm(S, S.x)}` 挂到 `{_nm(S, S.y)}` 下面：`{_nm(S, S.x)} × {_g(S["self.mul"][S.x])} = {_nm(S, S.y)}`',
        'ans = []': '开始回答询问',
        'c = variable_to_id.get': lambda S, B, ret: f'询问 `{B.c} / {B.d}`：`{B.c}` → 编号 `{S.c}`',
        'd = variable_to_id.get': lambda S, B, ret: f'`{B.d}` → 编号 `{S.d}`' + ('（==没出现过==）' if S.d == -1 else ''),
        'if c != -1 and d != -1': lambda S, B, ret: (f'`{_nm(S, S.c)}`、`{_nm(S, S.d)}` 都在条件里出现过 → 调用 `same` 看是否在同一集合'
                                                     if S.c != -1 and S.d != -1 else '有变量没在条件里出现过 → `-1.0`'),
        'return self.find(x) == self.find(y)': '`same`：分别找两者的代表元，相同就在同一个集合',
        'ans.append(uf.mul[d] / uf.mul[c])': lambda S, B, ret: (f'代表元相同。`{_nm(S, S.c)} · mul[{_nm(S, S.c)}] = {_nm(S, S.d)} · mul[{_nm(S, S.d)}]`'
                                                                f' → `{_nm(S, S.c)} / {_nm(S, S.d)}` = `{_g(S.uf.mul[S.d])} / {_g(S.uf.mul[S.c])}` = =={_g(S.ans[-1])}=='),
        'ans.append(-1.0)': '无法确定 → `-1.0`',
        'return ans': '返回 `{ret}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='只记录每个元素与代表元的比值，同一集合内任意两数之比 = mul 之比',
        complexity='时间 `O((n + q) log n)`（只写了路径压缩），空间 `O(nL)`',
        problem=['已知若干 `A / B = value`，回答询问 `C / D = ?`',
                 '无法确定（或变量没出现过）时答案为 `-1.0`',
                 '示例：`a/b = 2`，`b/c = 3`；询问 `a/c` → `6`，`b/a` → `0.5`，`a/e` → `-1`'],
        quote='我们不需要知道代表元的值，也不需要知道每个元素的值，只需要知道每个元素与其代表元的==比值==……比如昨天下了一个西湖的雨，今天下了两个西湖的雨……并不需要知道西湖有多少水。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `x · mul[x] = x 的代表元的值`',
              '同一集合：`c · mul[c] = d · mul[d]` → `c / d = mul[d] / mul[c]`',
              '合并 from、to：`mul[x] = mul[to] · value / mul[from]`'],
        summary=['时间 `O((n + q) log n)`，空间 `O(nL)`（`L ≤ 5` 为变量长度）',
                 '易错：路径压缩时要先递归，再 `mul[x] *= mul[fa[x]]`，最后才改 `fa[x]`',
                 '易错：询问里的变量可能从没出现过（如 `x / x`）→ `-1.0`',
                 '同类：带权并查集（§7.6）'],
    ),
)
