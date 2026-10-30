SRC, TGT = 'abcc', 'bcdc'
ORIG = ['a', 'b', 'ab', 'c', 'e']
CHG = ['b', 'c', 'bc', 'e', 'd']
COST = [1, 2, 2, 1, 1]
STRS = []
for _s in ORIG + CHG:
    if _s not in STRS:
        STRS.append(_s)
STRS = sorted(STRS, key=len)


def _d(S, a, b):
    dis = S.get('dis')
    if dis is None:
        return float('inf')
    return dis.get(a, {}).get(b, float('inf'))


def _tbl(S):
    return [[_d(S, a, b) for b in STRS] for a in STRS]


def _tcolor(S, i, j, v):
    line = S.get('_line', 0)
    if line == 17 and 'k' in S and S.get('k') == STRS[i] and S['k'] == STRS[j]:
        return None
    if line in (16, 17, 18) and 'k' in S and (STRS[i] == S['k'] or STRS[j] == S['k']) and v != float('inf'):
        return 'yellow'
    if i == j:
        return None
    if line >= 19 and 's' in S and 't' in S and (STRS[i], STRS[j]) == (S['s'], S['t']):
        return 'green'
    return None


def _win(S):
    size = S.get('size')
    i = S.get('i')
    if i is None or size is None or S.get('_line', 0) < 25:
        return None
    return i - size


def _fcolor(S, i, v):
    return None


def _txt(S):
    line = S.get('_line', 0)
    if line < 24 or 'f' not in S:
        return '`dis[x][y]` = 把子串 x 变成 y 的最小成本（Floyd）；`f[i]` = 把 `source[:i]` 变成 `target[:i]` 的最小成本'
    i = S.get('i')
    if i is None:
        return ''
    size = S.get('size')
    if size is not None and line >= 26 and 's' in S and S.get('i', 0) >= size:
        s, t = S['s'], S['t']
        ok = s in S['len_to_strs'][size] and t in S['len_to_strs'][size]
        return (f'末尾 `{size}` 位：`{s}` → `{t}`' + (f'，`dis = {_d(S, s, t)}`，`f[{i - size}] = {S["f"][i - size]}`' if ok else '，不在可替换集合里')) if True else ''
    return f'`f[{i}]`：`source[:{i}]` = `{SRC[:i]}` 变成 `{TGT[:i]}`'


CONFIG = dict(
    num=2977, title='转换字符串的最小成本 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Floyd（子串当节点）+ 划分型 DP',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 2696'],
    code='''
class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        len_to_strs = defaultdict(set)
        dis = defaultdict(lambda: defaultdict(lambda: inf))
        for x, y, c in zip(original, changed, cost):
            len_to_strs[len(x)].add(x)  # 按照长度分组
            len_to_strs[len(y)].add(y)
            dis[x][y] = min(dis[x][y], c)
            dis[x][x] = 0
            dis[y][y] = 0

        # 不同长度的字符串必然在不同的连通块中，分别计算 Floyd
        for strs in len_to_strs.values():
            for k in strs:
                for i in strs:
                    if dis[i][k] == inf:  # 加上这句话，巨大优化！
                        continue
                    for j in strs:
                        dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

        # f[i] 表示把 source[:i] 变成 target[:i] 的最小成本
        n = len(source)
        f = [0] + [inf] * n
        for i in range(1, n + 1):
            if source[i - 1] == target[i - 1]:
                f[i] = f[i - 1]  # 不修改 source[i]
            for size, strs in len_to_strs.items():  # 枚举子串长度
                if i < size:
                    continue
                s = source[i - size: i]
                t = target[i - size: i]
                if s in strs and t in strs:  # 可以替换
                    f[i] = min(f[i], dis[s][t] + f[i - size])
        return f[n] if f[n] < inf else -1
''',
    call=f'Solution().minimumCost({SRC!r}, {TGT!r}, {ORIG!r}, {CHG!r}, {COST!r})',
    expect=4,
    views=[
        dict(type='string', var='source', label='source', cell=56, h=175, window=(_win, 'i - 1')),
        dict(type='string', var='target', label='target（框 = 末尾 size 位）', cell=56, h=175, window=(_win, 'i - 1')),
        dict(type='array', var='f', label='f[i]：source[:i] → target[:i] 的最小成本', color=lambda S, i, v: 'blue' if i == S.get('i') else None, cell=56, h=175),
        dict(type='table', var=_tbl, label='dis：行 → 列 的最小成本（∞ = 变不过去）', rows=STRS, cols=STRS, color=_tcolor, cell=60, h=360),
    ],
    watch=[('i', 'i', 'blue'), ('size', 'size', 'pink'), ('s', 's', 'cyan'), ('t', 't', 'orange'), ('f[i]', 'f[i]', 'green')],
    skip=['dis = defaultdict', 'for k in strs', 'len_to_strs[len(x)]', 'len_to_strs[len(y)]', 'dis[x][x] = 0', 'dis[y][y] = 0', 'for x, y, c in zip', 'for i in strs', 'for j in strs',
          'if dis[i][k] == inf', 'continue', 'dis[i][j] = min', 'for size, strs in', 'if i < size', 's = source', 't = target', 'n = len(source)'],
    captions={
        'len_to_strs = defaultdict': '`len_to_strs` 按长度给字符串分组；`dis[x][y]` 是 x 变成 y 的最小成本，默认 `inf`',
        'dis[x][y] = min': '操作 `{x}` → `{y}` 成本 `{c}`：`dis[{x!r}][{y!r}] = {dis[x][y]}`；两个字符串都登记进 `len_to_strs[{len(x)}]`',
        'for strs in len_to_strs.values()': lambda S, B, r: ('所有长度组的 Floyd 都跑完了：`dis[x][y]` 就是 x 变成 y 的最小成本（比如 `c → e → d` 只要 2）' if B.get('strs') == S.get('strs')
                                                              else f'长度 `{len(next(iter(S.strs)))}` 的一组 `{sorted(S.strs)}`：==不同长度的字符串不可能互相变==，每组单独跑 Floyd，枚举中转点 k 补全两两之间的最短成本'),
        'f = [0]': '`f[0] = 0`（空串不用改），其余先设 `inf`',
        'for i in range(1, n + 1)': lambda S, B, r: ('`f[1..n]` 都算完了' if B.get('i') == S.get('i') else f'算 `f[{S.i}]`：把 `source[:{S.i}]` = `{S.source[:S.i]}` 变成 `{S.target[:S.i]}`'),
        'if source[i - 1] == target[i - 1]': lambda S, B, r: (f'`source[{S.i - 1}] = target[{S.i - 1}] = {S.source[S.i - 1]}`：这一位可以不改 → `f[{S.i}] = f[{S.i - 1}] = {S.f[S.i - 1]}`' if S.source[S.i - 1] == S.target[S.i - 1]
                                                                else f'`source[{S.i - 1}] = {S.source[S.i - 1]} ≠ target[{S.i - 1}] = {S.target[S.i - 1]}`：这一位==必须被某次替换覆盖=='),
        'f[i] = f[i - 1]': '不修改：`f[{i}] = {f[i]}`',
        'if s in strs and t in strs': lambda S, B, r: (f'枚举末尾 `{S.size}` 位：`{S.s}` → `{S.t}`，两个都在长度 {S.size} 的字符串集合里 → ==可以整段替换==' if S.s in S.strs and S.t in S.strs
                                                      else f'枚举末尾 `{S.size}` 位：`{S.s}` → `{S.t}`，至少一个不在集合里 → 不能整段替换'),
        'f[i] = min(f[i], dis': '`f[{i}] = min({B.f[i]}, dis[{s!r}][{t!r}] + f[{i - size}])` = `min({B.f[i]}, {dis[s][t]} + {f[i - size]})` = =={f[i]}==',
        'return f[n]': lambda S, B, r: f'`f[{S.n}] = {S.f[S.n]}` 不是 `inf` → 答案 =={r}==',
    },
    cards=dict(
        one_liner='子串当图的节点跑 Floyd，再用划分型 DP 切分 source',
        complexity='时间 `O(n² + mn + m³)`，空间 `O(n + mn + m²)`',
        problem=['把 `source` 变成 `target`：可以选子串 `x` 花 `cost` 变成 `y`（`original[j] → changed[j]`）',
                 '两次操作的区间要么==完全不相交==，要么==完全相同==（同一段可以连续改多次）；不可能返回 `-1`',
                 '本视频：`source="abcc"`，`target="bcdc"`，可改 `a→b`、`b→c`、`ab→bc`、`c→e`、`e→d` → `4`'],
        quote='不同长度的字符串必然在不同的连通块中，分别计算 Floyd',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`original / changed` 里的字符串当作图的点，边权是 `cost`；Floyd 求任意两点最短路 `dis`',
              '同一段可以改多次，所以 `x → y` 的代价就是最短路；区间不能部分重叠 → 对 `source` 做划分',
              '`f[i]` = `source[:i]` 变成 `target[:i]` 的最小成本：这位相同可以不改，或枚举末尾 `size` 位整段替换'],
        summary=['时间 `O(n² + mn + m³)`；按长度分组后 Floyd 只在同长度的字符串之间做',
                 '易错：`dis[x][x] = 0` 必须设置；`if dis[i][k] == inf: continue` 是巨大优化',
                 '枚举的是==可替换的子串长度==（至多 100 种），不是所有起点',
                 '另一种写法：把字符串存进字典树编号，DP 时沿字典树同时走 source 和 target；以及 1:1 翻译前的记忆化搜索写法',
                 '同类题：2976（单字符版）、2959（Floyd）'],
    ),
)
