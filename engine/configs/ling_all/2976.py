L5 = 'abcde'


def _sub(S):
    d = S.get('dis')
    return [r[:5] for r in d[:5]] if d else None


def _color(S, i, j, v):
    k = S.get('k')
    if k is None or k >= 5:
        return None
    if i == k or j == k:
        return 'blue'
    return None


_EDGES = [(0, 1, 2), (1, 2, 5), (2, 1, 5), (2, 4, 1), (4, 1, 2), (3, 4, 20)]


def _floyd_upto(k):
    d = [[inf] * 5 for _ in range(5)]
    for i in range(5):
        d[i][i] = 0
    for x, y, c in _EDGES:
        d[x][y] = min(d[x][y], c)
    for m in range(min(k, 5)):
        for i in range(5):
            for j in range(5):
                d[i][j] = min(d[i][j], d[i][m] + d[m][j])
    return d


def _cap_k(S, B, ret):
    k = S.get('k')
    if k is None:
        return '开始 Floyd'
    pk = B.get('k')
    if pk is not None and k == pk:
        return '`k` 枚举完毕：`dis` 已是任意两字母的最小成本'
    head = f'中转字母换成 `{chr(97 + k)}`' if k < 5 else f'中转字母 `{chr(97 + k)}`（没有边，不会有变化）'
    if pk is None or pk >= 5:
        return head
    old, new = _floyd_upto(pk), _floyd_upto(pk + 1)
    parts = [f'`{L5[a]}→{L5[b]}`：{fmt_(old[a][b])} → =={fmt_(new[a][b])}=='
             for a in range(5) for b in range(5) if old[a][b] != new[a][b]]
    done = f'刚用 `{chr(97 + pk)}` 中转完：' + ('；'.join(parts) if parts else '没有变化')
    return done + '。' + head


def fmt_(x):
    return '∞' if x == inf else str(x)


def _info(S):
    if 'source' not in S or 'dis' not in S or 'ans' not in S:
        return '边：`a→b` 2，`b→c` 5，`c→b` 5，`c→e` 1，`e→b` 2，`d→e` 20'
    d = S['dis']
    parts = [f'{x}→{y}:{fmt_(d[ord(x) - 97][ord(y) - 97])}' for x, y in zip(S['source'], S['target'])]
    return '逐位成本：`' + '  '.join(parts) + f'`  合计 =={S["ans"]}=='


CONFIG = dict(
    num=2976, title='转换字符串的最小成本 I', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Floyd 求字母间最小转换成本',
    tags=['灵神题单·图论算法', '难度分 1882'],
    code='''
class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        dis = [[inf] * 26 for _ in range(26)]
        for i in range(26):
            dis[i][i] = 0

        for x, y, c in zip(original, changed, cost):
            x = ord(x) - ord('a')
            y = ord(y) - ord('a')
            dis[x][y] = min(dis[x][y], c)

        for k in range(26):
            for i in range(26):
                if dis[i][k] == inf:
                    continue  # 巨大优化！
                for j in range(26):
                    dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

        ans = sum(dis[ord(x) - ord('a')][ord(y) - ord('a')] for x, y in zip(source, target))
        return ans if ans < inf else -1
''',
    call="Solution().minimumCost('abcd', 'acbe', ['a','b','c','c','e','d'], ['b','c','b','e','b','e'], [2,5,5,1,2,20])",
    expect=28,
    skip=['for i in range(26)', 'dis[i][i] = 0', 'for x, y, c in zip', 'x = ord(x)', 'y = ord(y)', 'if dis[i][k]', 'continue',
          'for j in range(26)', 'dis[i][j] = min'],
    max_steps=30,
    views=[
        dict(type='string', var='source', label='source', h=150, cell=60),
        dict(type='string', var='target', label='target', h=150, cell=60),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='table', var=_sub, label='dis（只画 a–e；行 = 起点，列 = 终点，蓝 = 中转 k）', h=380, cell=62,
             rows=list(L5), cols=list(L5), color=_color),
    ],
    watch=[('k', "chr(97 + k) if k < 26 else ''", 'blue'), ('ans', 'ans', 'green')],
    captions={
        'dis = [[inf]': '`dis[x][y]`：字母 x 变成字母 y 的最小成本，先全设成 ∞（还没有路）',
        'dis[x][y] = min': lambda S, B, r: f'规则 `{chr(97 + S.x)}→{chr(97 + S.y)}` 成本 `{S.c}`：`dis` 取更小者 = =={S.dis[S.x][S.y]}==（同一对可能有多条规则）',
        'for k in range': _cap_k,
        'ans = sum': '逐位累加 `dis[source[i]][target[i]]`：=={ans}==（相同字母成本 0）',
        'return ans if': '`ans < inf` 才可行，否则有位置变不过去 → `-1`；这里返回 =={ret}==',
    },
    cards=dict(
        one_liner='字母当点、规则当边：Floyd 一次算出任意两字母的最小成本',
        complexity='时间 `O(n+m+26^3)`，空间 `O(26^2)`',
        problem=['`original[i]` 能以 `cost[i]` 的成本变成 `changed[i]`，可以连续变',
                 '把 `source` 变成 `target` 的最小总成本，不可能则返回 `-1`',
                 '本视频：`abcd → acbe` 返回 `28`'],
        quote='建图，从 original[i] 向 changed[i] 连边，边权为 cost[i]。然后用 Floyd 算法求图中任意两点最短路，得到 dis 矩阵。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个位置互相独立：只看 `source[i]` 变成 `target[i]` 的最小成本',
              '字母只有 26 个：先 ==Floyd 预处理 26×26== 的最短路，之后每位 `O(1)` 查表',
              '循环顺序必须是 `k, i, j`，`k` 是中转点；`dis[i][k] == inf` 就跳过，是巨大优化',
              '视频里 `k` 循环内部的细节折叠了：只看每个 `k` 结束后 `dis` 的变化'],
        summary=['时间 `O(n+m+26^3)`，空间 `O(26^2)`',
                 '同一对 `(x,y)` 可能有多条规则：取 `min`，不是覆盖',
                 '`dis[i][i] = 0`：字母不变不花钱',
                 '任何一位不可达，累加和是 `inf`，最后要判成 `-1`'],
    ),
)
