PR = [[1, 4, 2], [2, 2, 7], [2, 1, 3]]
M, N = 2, 4
PRD = {(h, w): p for h, w, p in PR}


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 8:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if r == i and 1 <= c < j and (c <= j // 2 or c >= j - j // 2):
        return 'blue'
    if c == j and 1 <= r < i and (r <= i // 2 or r >= i - i // 2):
        return 'pink'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = 高 i 宽 j 的木块最多卖多少钱；先把标价填进表里'
    f = S['f']
    vs = [(f[i][k] + f[i][j - k], f'f[{i}][{k}]+f[{i}][{j - k}]') for k in range(1, j // 2 + 1)]
    hs = [(f[k][j] + f[i - k][j], f'f[{k}][{j}]+f[{i - k}][{j}]') for k in range(1, i // 2 + 1)]
    parts = [f'直接卖 {f[i][j]}'] if f[i][j] else ['不能直接卖']
    if vs:
        parts.append('竖切最好 ' + str(max(x for x, _ in vs)))
    if hs:
        parts.append('横切最好 ' + str(max(x for x, _ in hs)))
    return f'`f[{i}][{j}]`：' + '，'.join(parts)


def _cap_max(S):
    i, j, f = S.i, S.j, S.f
    d = PRD.get((i, j), 0)
    vs = [f[i][k] + f[i][j - k] for k in range(1, j // 2 + 1)]
    hs = [f[k][j] + f[i - k][j] for k in range(1, i // 2 + 1)]
    best = max([d] + vs + hs)
    return (f'`f[{i}][{j}]`：直接卖 `{d}`，竖切最好 `{max(vs, default=0)}`（k 只到 `{j // 2}`），'
            f'横切最好 `{max(hs, default=0)}`（k 只到 `{i // 2}`）→ 取最大 =={best}==')


CONFIG = dict(
    num=2312, title='卖木头块', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='二维 DP · 枚举切割位置（只枚举一半）',
    tags=['其他线性 DP', '难度分 2363'],
    code='''
class Solution:
    def sellingWood(self, m: int, n: int, prices: List[List[int]]) -> int:
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for h, w, p in prices:
            f[h][w] = p
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                f[i][j] = max(f[i][j],
                              max((f[i][k] + f[i][j - k] for k in range(1, j // 2 + 1)), default=0),  # 垂直切割
                              max((f[k][j] + f[i - k][j] for k in range(1, i // 2 + 1)), default=0))  # 水平切割
        return f[m][n]
''',
    call=f'Solution().sellingWood({M}, {N}, {PR!r})',
    expect=14,
    skip=['for j in range', 'for h, w, p', 'for k in range(1, j', 'for k in range(1, i'],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（行 = 高，列 = 宽；黄 = 在算，蓝 = 竖切，粉 = 横切）',
             h=420, cell=84, rows=lambda S: [str(k) for k in range(len(S['f']))], cols=lambda S: [str(k) for k in range(len(S['f'][0]))],
             color=_cell),
        dict(type='text', fn=lambda S: '标价（高×宽 → 价格）：' + '，'.join(f'`{h}×{w}` → {p}' for h, w, p in PR), size=24, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', 'f[i][j]', 'green')],
    captions={
        'f = [[0]': '`f[i][j]` 初始为 0；多开一行一列，下标 1 开始对应真实高宽',
        'f[h][w] = p': '`f[{h}][{w}] = {p}`：这个尺寸可以==直接卖掉==，先把标价填进表',
        'for i in range': lambda S, B, r: (f'开始算高度 `i = {S.i}` 的所有宽度；小尺寸一定先于大尺寸算好' if S.get('i') != B.get('i') else '所有尺寸都算完了'),
        'f[i][j] = max(': lambda S, B, r: _cap_max(S),
        'return f[m][n]': '整块 `{m} × {n}` 最多卖 `f[{m}][{n}]` = =={ret}==（最优：两块 2×2）',
    },
    cards=dict(
        one_liner='切完的两块互不影响：枚举第一刀，只看一半位置',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn)`',
        problem=['`m × n` 的木块，每次沿整条边切一刀成两块；`prices` 给出各尺寸的卖价，木块不能旋转',
                 '求切完后能卖到的==最多钱数==，可以不卖完',
                 '示例：`m=3, n=5` → `19`；视频用 `m=2, n=4`'],
        quote='对于一个高为 3 宽为 5 的木块，第一步一共有 6 种切割方案……横着切开，虽然位置不同，但得到的结果是相同的……所以本质上只有 1 种切法。',
        quote_src='—— 灵茶山艾府题解（优化）',
        idea=['每块都是「高 i 宽 j」的子问题，定义 `f[i][j]` = 最多钱数',
              '取三者最大：直接卖、竖切 `f[i][k]+f[i][j-k]`、横切 `f[k][j]+f[i-k][j]`',
              '第一刀 `k` 与 `j-k` 对称，只枚举到一半'],
        summary=['时间 `O(mn(m+n))`：mn 个状态，每个枚举 `O(m+n)` 个切点',
                 '易错：先把 `prices` 写进 `f`，再用 `max(f[i][j], ...)` 保留直接卖的收益',
                 '木块不能旋转，`h × w` 与 `w × h` 是不同尺寸',
                 '第一种写法用哈希表查价、枚举到 `j-1`，结果相同，只是慢一倍'],
    ),
)
