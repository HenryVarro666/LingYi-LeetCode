SHAPE = ["rlrr", "llrl", "llr."]


def _root(S, x):
    fa = S['fa']
    while fa[x] != x:
        x = fa[x]
    return x


def _cells(S):
    """每格 4 个区域里，有多少个是「候选蓄水区」(ok)。"""
    if 'ok' not in S or 'u' not in S:
        return None
    n, m = len(S['shape']), len(S['shape'][0])
    out = []
    for i in range(n):
        row = []
        for j in range(1, m + 1):
            row.append(sum(1 for a in (S['u'], S['d'], S['l'], S['r']) if S['ok'][a[i][j]]))
        out.append(row)
    return out


def _color(S, i, j, v):
    if 'ok' not in S or 'u' not in S:
        return None
    jj = j + 1
    ids = [a[i][jj] for a in (S['u'], S['d'], S['l'], S['r'])]
    cand = [x for x in ids if S['ok'][x]]
    if not cand:
        return None
    if 'ans' in S:
        z = _root(S, 0)
        if all(_root(S, x) == z for x in cand):
            return 'green'
        return 'orange'
    return 'yellow'


def _row_color(S, i, j, v):
    c = _color(S, i, j, v)
    if c:
        return c
    cur = S.get('i')
    if cur is not None and isinstance(cur, int) and i == cur and 'ans' not in S:
        return 'blue'
    return None


def _cur(S):
    i = S.get('i')
    if 'ans' in S:
        return None
    return i if isinstance(i, int) and 'ok' in S and S.get('_line', 0) > 0 else None


def _text(S):
    if 'ans' in S:
        return f"绿 = 真的有水的区域，累计 `ans = {S['ans']}`（区域数），答案 = ans // 2"
    if 'ok' not in S:
        return '每格拆成 上/下/左/右 四个区域；**列号从 1 开始**，0 号是超级汇点'
    k = sum(1 for x in S['ok'] if x)
    return f'黄 = 本行及以下，不爬到上一行就够不着边界的「候选蓄水区」；目前 ok 区域 `{k}` 个'


CONFIG = dict(
    num='LCP 71', title='集水器', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='倒着一行行并查集 + 超级汇点',
    tags=['并查集'],
    code='''
class Solution:
    def reservoir(self, shape: List[str]) -> int:
        n, m = len(shape), len(shape[0])
        # 每个格子分成四个区域（上下左右），标上序号，方便用并查集连通
        # 假设左右下还有一圈格子，直接连到超级汇点 0
        u = [[0] * (m + 2) for _ in range(n + 1)]
        d = [[0] * (m + 2) for _ in range(n + 1)]
        l = [[0] * (m + 2) for _ in range(n + 1)]
        r = [[0] * (m + 2) for _ in range(n + 1)]
        c = 1
        for i in range(n):
            for j in range(1, m + 1):  # 假设格子的列号从 1 开始，这样方便表示左右边界
                u[i][j] = c; c += 1
                d[i][j] = c; c += 1
                l[i][j] = c; c += 1
                r[i][j] = c; c += 1

        # 并查集模板
        fa = list(range(c))
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        def merge(x: int, y: int):
            fa[find(x)] = find(y)

        ok = [False] * c  # 能否容纳水
        # 倒着判断每一行，寻找可能有水的区域
        for i in range(n - 1, -1, -1):
            for j in range(m + 1):
                merge(r[i][j], l[i][j + 1])  # 连通左右
            for j, type in enumerate(shape[i], 1):
                merge(d[i][j], u[i + 1][j])  # 连通下
                # 根据格子的类型连接格子内部四个区域
                if type == '.':
                    merge(l[i][j], u[i][j])
                    merge(l[i][j], d[i][j])
                    merge(l[i][j], r[i][j])
                elif type == 'l':
                    merge(l[i][j], d[i][j])
                    merge(r[i][j], u[i][j])
                else:
                    merge(l[i][j], u[i][j])
                    merge(r[i][j], d[i][j])
            for j in range(1, m + 1):
                # 在没有连接第 i-1 行的情况下，无法到达左右下边界 => 能容纳水
                ok[l[i][j]] = find(l[i][j]) != find(0)
                ok[r[i][j]] = find(r[i][j]) != find(0)
                ok[u[i][j]] = find(u[i][j]) != find(0)
                ok[d[i][j]] = find(d[i][j]) != find(0)

        # 第一行连上超级汇点，方便后面统一判断是否在闭合区域里面
        for j in range(1, m + 1):
            merge(u[0][j], 0)

        ans = 0
        for i, b in enumerate(ok):
            if b and find(i) == find(0):  # 能容纳水，且不在闭合区域里面
                ans += 1
        return ans // 2
''',
    call=f'Solution().reservoir({SHAPE!r})',
    expect=6,
    skip=['n, m = len', 'u = [[0]', 'd = [[0]', 'l = [[0]', 'r = [[0]', 'c = 1', 'for i in range(n):',
          'u[i][j] = c', 'd[i][j] = c', 'l[i][j] = c', 'r[i][j] = c',
          'if fa[x] != x', 'fa[x] = find(fa[x])', 'return fa[x]', 'fa[find(x)] = find(y)',
          'def find', 'def merge', 'for j in range(m + 1)', 'for j, type in enumerate',
          "if type == '.'", "elif type == 'l'", 'else:', 'ok = [False]', 'fa = list(range(c))',
          'for j in range(1, m + 1):', 'for i, b in enumerate(ok)', 'if b and find(i)',
          'merge(r[i][j], l[i][j + 1])', 'merge(l[i][j], d[i][j])', 'merge(r[i][j], u[i][j])',
          'merge(l[i][j], u[i][j])', 'merge(r[i][j], d[i][j])', 'merge(l[i][j], r[i][j])',
          'ok[r[i][j]]', 'ok[u[i][j]]', 'ok[l[i][j]]'],
    max_steps=110,
    views=[
        dict(type='text', fn=_text, size=24, h=60),
        dict(type='grid', var=lambda S: [list(row) for row in S['shape']], label='shape（蓝 = 当前行；黄 = 候选蓄水；绿 = 真有水；橙 = 通向外面，水流走）',
             cell=96, h=420, color=_row_color),
    ],
    watch=[('i', 'i if "ok" in locals() else i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'merge(r[i][j], l[i][j + 1])': '把第 `{i}` 行相邻格子连通：左格的右区域 `{r[i][j]}` 与右格的左区域 `{l[i][j + 1]}` 并成一块（空气/水可以穿过）',
        'merge(d[i][j], u[i + 1][j])': lambda S, B, r: f"第 `{S.i}` 行第 `{S.j}` 格：左右邻格相连（空气/水能穿过），下区域连到下一行；`{S.type}` 隔板只连通斜线同侧的两块" + ("；最后一行的下面是边界 0" if S.i == len(S.shape) - 1 else ""),
        'merge(l[i][j], d[i][j])': '`{type}` 隔板把左/下连在一起（斜线只挡住一半）',
        'merge(r[i][j], u[i][j])': '隔板另一侧：右/上连在一起，水无法穿过斜线',
        'merge(l[i][j], u[i][j])': '`{type}` 隔板：左/上连通',
        'merge(r[i][j], d[i][j])': '`{type}` 隔板：右/下连通',
        'merge(l[i][j], r[i][j])': '没有隔板：四个区域全连通',
        'ok[d[i][j]]': lambda S, B, r: (f"第 `{S.i}` 行第 `{S.j}` 格四个区域"
            + ("（不借助上一行）" if S.i > 0 else "（顶行）") + "：" + "、".join(
                f"{nm}{'==能蓄水==' if S.ok[a[S.i][S.j]] else '够得到边界'}" for nm, a in (('上', S.u), ('下', S.d), ('左', S.l), ('右', S.r)))),
        'merge(u[0][j], 0)': '顶行的上区域接到汇点 0：它们露在水面，和外界相通',
        'ans = 0': '统计：能容纳水（ok），且和超级汇点相连（不是被封死的空气腔）才真有水',
        'ans += 1': '区域 `{i}` 能容纳水，且与 0 相连 → 真有水，`ans = {ans}`',
        'return ans': '每格 4 个区域，一格水量记 2 → `ans // 2 = {ans // 2}`',
    },
    cards=dict(
        one_liner='倒着一行行并查集：不爬高就够不到边界的区域能蓄水',
        complexity='时间 `O(nm α)`，空间 `O(nm)`',
        problem=['`shape` 里 `l`/`r` 是斜隔板，`.` 是空；集水器从水里竖直取出，每格水量 `2`',
                 '空气能穿过隔板，水不能；除密闭空间外都灌满水',
                 '取出后，能留住的水有多少？',
                 '示例：`["rlrr","llrl","llr."]` → `6`'],
        quote='判断能否容纳水：第 i 行的水，在不走到第 i-1 行的前提下，无法触及左、右、下边界。',
        quote_src='—— 灵茶山艾府题解',
        idea=['水只会往下流，所以从最后一行倒着合并：只用第 `i` 行及以下的连通关系',
              '每格拆成上下左右四区，斜线决定哪两区相连；边界和顶行都接到超级汇点 `0`',
              '行内合并完，不与 0 相连的区域 = 能蓄水；最后再接上顶行，和 0 相连才是真有水'],
        summary=['时间 `O(nm α)`，空间 `O(nm)`；每格 4 个区域，答案 `ans // 2`',
                 '易错：列号从 1 开始、左右多留一圈；`u` 要有 `n + 1` 行，最后一行的下面连到 0',
                 '==必须倒着、逐行判断 ok==，之后顶行才合并到 0，否则会把密闭腔当成漏水',
                 '同类题：959 由斜杠划分区域（同样的四区域拆法）'],
    ),
)
