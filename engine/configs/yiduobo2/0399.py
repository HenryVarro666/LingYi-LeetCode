EQS = [["a", "b"], ["b", "c"]]
VALS = [2.0, 3.0]
QS = [["a", "c"], ["b", "a"], ["a", "e"]]


def _g(v):
    if isinstance(v, float):
        from fractions import Fraction
        fr = Fraction(v).limit_denominator(1000)
        return str(fr.numerator) if fr.denominator == 1 else f'{fr.numerator}/{fr.denominator}'
    return str(v)


def _names(E):
    f = E.get('f')
    return list(f.keys()) if isinstance(f, dict) else []


def _table(E):
    f = E.get('f')
    if not isinstance(f, dict) or not f:
        return None
    ns = list(f.keys())
    return [[_g(f[r][c]) if c in f[r] else '' for c in ns] for r in ns]


def _color(E, r, c, v):
    ns = _names(E)
    if r >= len(ns) or c >= len(ns):
        return None
    R, C = ns[r], ns[c]
    x, y, tmp = E.get('x'), E.get('y'), E.get('tmp')
    if E.get('_line', 0) >= 34 and x in ns and y in ns:
        if (R, C) == (x, y):
            return 'yellow'
        if tmp in ns and (R, C) == (x, tmp):
            return 'blue'
        if tmp in ns and (R, C) == (tmp, y):
            return 'pink'
    if R == C and v:
        return None
    return None


def _cap_dfs_if(E, B, ret):
    x, y, f = E.x, E.y, E.f
    if y in f[x] or x in f[y]:
        return f'`{x}/{y}` 已经知道了（`f[{x}][{y}]` 有值）→ 直接返回'
    return f'`{x}` 和 `{y}` 之间没有边 → 从 `{x}` 出发 dfs，枚举邻接点 tmp'


def _cap_used(E, B, ret):
    t = E.tmp
    if not E.used[t]:
        return f'邻接点 `tmp = {t}` 不在当前路径上 → 递归求 `{t}/{E.y}`'
    return f'`{t}` 已经在当前路径上（`used`）→ 跳过，防止绕圈'


def _cap_found(E, B, ret):
    x, y, t, f = E.x, E.y, E.tmp, E.f
    if y in f[t] and f[t][y] > 0:
        return f'求出了 `{t}/{y} = {_g(f[t][y])}` → 可以用 `{x}/{t} × {t}/{y}` 得到 `{x}/{y}`'
    return f'`{t}/{y}` 求不出来 → 枚举下一个 tmp'


_qn = [0]


def _cap_q(E, B, ret):
    _qn[0] += 1
    if _qn[0] > len(QS):
        return '询问都回答完了'
    return f'第 {_qn[0]} 个询问：`{E.x} / {E.y} = ?`'


CONFIG = dict(
    num=399, title='除法求值', difficulty='Medium', category='图论',
    author='yiduobo', technique='带权有向图 + DFS（f[x][y] 记忆化）',
    tags=['热题173', '面试经典150'],
    code='''
class Solution(object):
    def calcEquation(self, equations, values, queries):
        f = {}
        for index in range(len(equations)):
            x, y = equations[index]
            value = values[index]
            if x not in f:
                f[x] = {}
                f[x][x] = 1.0
            if y not in f:
                f[y] = {}
                f[y][y] = 1.0
            f[x][y] = value
            f[y][x] = 1 / value

        used = {}
        for x in f:
            used[x] = False

        res = []
        for x, y in queries:
            if x not in f or y not in f:
                res.append(-1.0)
            else:
                used[x] = True
                self.dfs(x, y, f, used)
                used[x] = False
                if y in f[x]:
                    res.append(f[x][y])
                else:
                    res.append(-1.0)

        return res

    def dfs(self, x, y, f, used):
        if y in f[x] or x in f[y]:
            return

        for tmp in f[x]:
            if not used[tmp]:
                used[tmp] = True
                self.dfs(tmp, y, f, used)
                used[tmp] = False
                if y not in f[tmp] and tmp in f[y]:
                    f[tmp][y] = 1 / f[y][tmp]
                if y in f[tmp] and f[tmp][y] > 0:
                    f[x][y] = f[x][tmp] * f[tmp][y]
                    f[y][x] = 1 / f[x][y]
                    return

        return
''',
    call=f'Solution().calcEquation({EQS}, {VALS}, {QS})',
    expect=[6.0, 0.5, -1.0],
    views=[
        dict(type='grid', var=_table, label='f[x][y] = x / y（行 x，列 y；黄 = 要求的 x/y，蓝 = x/tmp，粉 = tmp/y）',
             rows=_names, cols=_names, cell=100, h=282, color=_color),
        dict(type='set', var=lambda E: {k for k, v in E['used'].items() if v} if isinstance(E.get('used'), dict) else None,
             label='used = True 的点（当前 dfs 路径）', h=100),
        dict(type='calls', h=116, label='调用栈', hide=('f', 'used')),
        dict(type='array', var='res', label='res', cell=70, h=134),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('tmp', 'tmp', 'blue'), ('value', 'value')],
    skip=[4, 6, 9, 12, 17, 18, 37, 49],
    max_steps=70,
    captions={
        'f = {}': '把 `A/B = k` 看作点 A 到点 B 的==有向边==，权重为 k；`f[x][y]` 存 `x/y`',
        'x, y = equations[index]': '条件 `{x} / {y} = {values[index]:g}`',
        7: lambda E, B, ret: (f'`{E.x}` 第一次出现 → 新建 `f[{E.x}]`，且 `{E.x}/{E.x} = 1`'
                                            if E.x not in B.f else f'`{E.x}` 已经在图里'),
        'f[x] = {}': '`f[{x}] = {{{x}: 1.0}}`',
        10: lambda E, B, ret: (f'`{E.y}` 第一次出现 → 新建 `f[{E.y}]`，且 `{E.y}/{E.y} = 1`'
                                            if E.y not in B.f else f'`{E.y}` 已经在图里'),
        'f[y] = {}': '`f[{y}] = {{{y}: 1.0}}`',
        'f[x][y] = value': '边 `{x} → {y}`：`f[{x}][{y}] = {value:g}`',
        'f[y][x] = 1 / value': '反向边 `{y} → {x}`：`f[{y}][{x}] = 1 / {value:g}`',
        'used = {}': '`used` 标记 dfs 路径上的点（防止绕圈），一开始全是 `False`',
        27: '回溯：起点 `{x}` 移出路径',
        'res = []': '开始回答询问',
        'for x, y in queries': _cap_q,
        'if x not in f or y not in f': lambda E, B, ret: (f'`{E.x if E.x not in E.f else E.y}` 没出现过 → 无法确定'
                                                          if E.x not in E.f or E.y not in E.f else '两个点都在图里 → dfs'),
        'res.append(-1.0)': '答案 `-1.0`',
        'used[x] = True': '起点 `{x}` 标记为已在路径上',
        'self.dfs(x, y, f, used)': '`dfs({x}, {y})`：尽量把 `f[{x}][{y}]` 求出来',
        'if y in f[x] or x in f[y]': _cap_dfs_if,
        'for tmp in f[x]': lambda E, B, ret: f'枚举 `{E.x}` 的邻接点 `tmp = {E.tmp}`（`{E.x}/{E.tmp} = {_g(E.f[E.x][E.tmp])}`）',
        'if not used[tmp]': _cap_used,
        'used[tmp] = True': '`{tmp}` 加入路径',
        'self.dfs(tmp, y, f, used)': '递归：求 `{tmp}/{y}`',
        'used[tmp] = False': '回溯：`{tmp}` 移出路径',
        'if y not in f[tmp] and tmp in f[y]': lambda E, B, ret: ('只知道反方向 → 取倒数' if E.y not in E.f[E.tmp] and E.tmp in E.f[E.y]
                                                                 else '不需要取倒数'),
        'if y in f[tmp] and f[tmp][y] > 0': _cap_found,
        'f[x][y] = f[x][tmp] * f[tmp][y]': lambda E, B, ret: (f'`{E.x}/{E.y} = {E.x}/{E.tmp} × {E.tmp}/{E.y} = '
                                                              f'{_g(E.f[E.x][E.tmp])} × {_g(E.f[E.tmp][E.y])} = {_g(E.f[E.x][E.y])}`，存进 f'),
        'f[y][x] = 1 / f[x][y]': lambda E, B, ret: f'顺便存下 `{E.y}/{E.x} = {_g(E.f[E.y][E.x])}`（==记忆化==，避免重复运算）',
        'if y in f[x]': lambda E, B, ret: (f'`f[{E.x}][{E.y}]` 求出来了' if E.y in E.f[E.x] else '没求出来 → `-1.0`'),
        'res.append(f[x][y])': '答案 `{x}/{y} = {res[-1]:g}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='A/B = k 看作带权有向边，x/y 就是 x 到 y 路径上的权值乘积',
        complexity='每次询问最坏 `O(V + E)`；`f` 记下算过的比值，空间 `O(V^2)`',
        problem=['已知若干 `A / B = value`，回答询问 `C / D = ?`',
                 '无法确定（或变量没出现过）时答案为 `-1.0`',
                 '示例：`a/b = 2`，`b/c = 3`；询问 `a/c` → `6`，`b/a` → `0.5`，`a/e` → `-1`'],
        quote='对于题目给出的A/B=k，可以看做是在点A到点B之间有一条==有向边==，权重为k……若可以求出tmp/y的值，那么就通过==x/tmp * tmp/y==来得到x/y，否则继续枚举下一个tmp。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个条件建两条边：`x → y` 权重 `k`，`y → x` 权重 `1/k`',
              '求 `x/y`：有边直接得出；否则从 `x` 出发 dfs，`x/y = x/tmp × tmp/y`',
              '过程中用 `f[x][y]` 保存 `x/y` 的值，==避免重复运算=='],
        summary=['`used` 标记当前路径，防止在环上绕圈',
                 '算出 `x/y` 后同时写入 `y/x = 1 / (x/y)`',
                 '变量没出现过（如 `x/x` 中的 `x` 不在图里）→ `-1.0`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '`1 / value` 中 value 是浮点数，Python 3 下结果相同，无需改',
                 '对比灵神：带权并查集，每个点只记到代表元的比值，询问近乎 `O(1)`'],
    ),
)
