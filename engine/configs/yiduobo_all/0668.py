def _tab(S):
    return [[a * b for b in range(1, S['n'] + 1)] for a in range(1, S['m'] + 1)]


def _color(S, i, j, v):
    mid = S.get('mid')
    if mid is None:
        return None
    if 'index' in S and S.get('cnt') is not None and (i == S['index'] - 1 and S['m'] <= S['n'] or j == S['index'] - 1 and S['m'] > S['n']) and v <= mid:
        return 'green'
    return 'blue' if v <= mid else None


def _txt(S):
    mid = S.get('mid')
    if mid is None:
        return f"二分排名：答案在 `[{S['l']}, {S['r']}]`"
    c = sum(v <= mid for r in _tab(S) for v in r)
    return f"`mid = {mid}` 在表里排名 ==`{c}`==（蓝色 `≤ mid` 的个数），要 `≥ k = {S['k']}`"


CONFIG = dict(
    num=668, title='乘法表中第k小的数', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 枚举较短一维算排名',
    tags=[],
    code='''
class Solution(object):
    def findKthNumber(self, m, n, k):

        l = 1
        r = m * n

        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for index in range(1, min(m, n) + 1):
                cnt += min(mid // index, max(m, n))
            if cnt >= k:
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call='Solution().findKthNumber(3, 4, 6)',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='table', var=_tab, label='乘法表 m×n（蓝 = ≤ mid，绿 = 当前枚举的那一行）', color=_color, rows=lambda S: list(range(1, S['m'] + 1)), cols=lambda S: list(range(1, S['n'] + 1)), h=300),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'mid', 'index', 'cnt', ('k', 'k', 'green')],
    captions={
        'l = 1': '答案最小是 `1`',
        'r = m * n': '答案最大是表里最大的 `m * n = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l}` < `r = {S.r}`：区间没缩完 → 继续' if S.l < S.r else f'`l = r = {S.l}`：找到了'),
        'mid = (': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'cnt = 0': '统计 `mid` 在表里的排名：`≤ mid` 的数有几个',
        'for index in range': '枚举较短的一维（行和列里取短的），一共 `{min(m, n)}` 条',
        'cnt += min': '`mid` 除以 `{index}` = `{mid // index}`，这一行 / 列最多 `{max(m, n)}` 个 → 取小，`cnt` = {cnt}',
        'if cnt >= k': lambda S, B, r: (f'排名 `cnt = {S.cnt}` ≥ `k = {S.k}`：第 k 小 ≤ mid' if S.cnt >= S.k
                                        else f'排名 `cnt = {S.cnt}` < `k = {S.k}`：mid 太小了'),
        'r = mid': '`r = mid = {r}`：`mid` 本身可能就是答案，保留',
        'l = mid + 1': '`mid` 排名不够，排除它：`l = mid + 1 = {l}`',
        'return l': '第 `k` 小是 =={l}==',
    },
    cards=dict(
        one_liner='算出 x 在表里的排名，再二分找排名 ≥ k 的最小 x',
        complexity='时间 `O(min(m,n) log(mn))`，空间 `O(1)`',
        problem=['`m × n` 的乘法表，`mat[i][j] = i * j`（下标从 1 开始），求第 `k` 小的数',
                 '示例：`m=3, n=3, k=5` → `3`',
                 '本视频：`m=3, n=4, k=6` → `4`'],
        quote='我们可以枚举行和列中较短的那一维，计算x在当前行或列中排第几，然后将这个排名累加，就是x在当前表中的排名。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x` 在第 `index` 行（或列）里的位置是 `x // index`，但不会超过另一维长度',
              '只枚举较短的一维，把各条的位置累加 → ==x 的排名==',
              '排名随 x 单调不减 → 二分 `x`，`cnt >= k` 就收右边界'],
        summary=['时间 `O(min(m,n) log(mn))`，空间 `O(1)`',
                 '`cnt >= k` 时 `r = mid`（不排除 mid），否则 `l = mid + 1`',
                 '`min(mid // index, max(m, n))`：别忘了不能超过另一维长度',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神用开区间 + 优化的整行累加；yiduobo 只枚举较短一维'],
    ),
)
