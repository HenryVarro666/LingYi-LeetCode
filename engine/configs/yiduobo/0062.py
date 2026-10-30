def _ready(S):
    return 'res' in S   # m、n 已改写成 m+n-2、n-1


def _num(S):
    return list(range(S['m'] - S['n'] + 1, S['m'] + 1)) if _ready(S) else None


def _den(S):
    return list(range(1, S['n'] + 1)) if _ready(S) else None


def _done(S, i, v):
    k = S.get('index')
    if k is None:
        return None
    if i + 1 < k:
        return 'green'
    if i + 1 == k:
        return 'orange'
    return None


def _formula(S):
    if not _ready(S):
        return '走法 = 若干个「下」和「右」的排列 → 组合数'
    m, n = S['m'], S['n']
    k = S.get('index', 0)
    if 'now' not in S:
        return f'答案 = `C({m}, {n})` = ({m - n + 1}×…×{m}) / (1×…×{n})，从 `res = 1` 开始逐项乘除'
    if S['res'] != comb(m - n + k, k):
        k -= 1   # 本项还没乘进 res
    return f'已乘完 {k} 项：res = `C({m - n + k}, {k})` = =={S["res"]}=='


def _balls(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '一条路径 = 一种排列：白球 = 向下（m-1 = 2 个），黑球 = 向右（n-1 = 6 个）', 24, T['muted'], bold=True)
    seq = '右右下右右右下右'
    d, gap = 66, 16
    sx = x0 + (x1 - x0 - (len(seq) * d + (len(seq) - 1) * gap)) / 2
    y = y0 + 56
    for k, ch in enumerate(seq):
        X = sx + k * (d + gap)
        white = ch == '下'
        cv.rect((X, y, X + d, y + d), fill=(235, 238, 242) if white else (14, 16, 20), outline=T['border'], width=2, r=d / 2)
        cv.text((X + d / 2, y + d / 2), ch, 28, (20, 22, 26) if white else (235, 238, 242), anchor='mm', bold=True)


CONFIG = dict(
    num=62, title='不同路径', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='组合数学：黑白球排列',
    code='''
class Solution(object):
    def uniquePaths(self, m, n):

        if m == 0 or n == 0:
            return 0

        m = m + n - 2
        n -= 1
        res = 1
        for index in range(1, n + 1):
            now = m - n + index
            res = res * now // index

        return res
''',
    call='Solution().uniquePaths(3, 7)',
    expect=28,
    views=[
        dict(type='text', fn=_formula, h=64),
        dict(type='array', var=_num, label='分子：now = m - n + index（从 m-n+1 乘到 m）',
             pointers={'index - 1': 'yellow'}, pointer_labels={'index - 1': 'index'}, color=_done, index=False, h=200),
        dict(type='array', var=_den, label='分母：index（从 1 除到 n）',
             pointers={'index - 1': 'yellow'}, pointer_labels={'index - 1': 'index'}, color=_done, index=False, h=200),
        dict(type='custom', draw=_balls, h=170),
    ],
    skip=['for index in range'],
    watch=['m', 'n', ('index', 'index', 'yellow'), 'now', ('res', 'res', 'green')],
    captions={
        'if m == 0 or n == 0': '空网格没有路径，直接返回 0（这里 `m = 3, n = 7`，不成立）',
        'm = m + n - 2': '从左上到右下，一定是 `{B.m} - 1` 步加 `{B.n} - 1` 步：一共 `m + n - 2 = {m}` 个球',
        'n -= 1': '其中 `n - 1 = {n}` 个是黑球，其余是白球 → ==排列数就是== `C({m}, {n})`',
        'res = 1': '用 `res` 累乘：`C(m, n) = (m-n+1)…(m) / (1…n)`，一项乘一项除',
        'now = m - n + index': '分子的第 {index} 项：`now = {m} - {n} + {index} = {now}`',
        'res = res * now // index': lambda S, B, ret: (
            f'`res = {B.res} × {S.now} / {S.index} = {S.res}`：乘完第 k 项后 `res = C(m-n+k, k)`，==每一步都是组合数，所以一定整除=='
            if S.index == 1 else
            f'`res = {B.res} × {S.now} / {S.index} = {S.res}` = `C({S.now}, {S.index})`' + ('，就是答案' if S.index == S.n else '')),
        'return res': '返回 `C({m}, {n}) = C({m}, {m - n})` = =={ret}==',
    },
    cards=dict(
        one_liner='路径 = 黑白球的排列，答案就是一个组合数',
        complexity='时间 `O(min(m, n))`（这份代码是 `O(n)`），空间 `O(1)`',
        problem=['机器人在 `m × n` 网格左上角，==每次只能向下或向右==走一步',
                 '问走到右下角共有多少条不同路径',
                 '示例：`m = 3, n = 7` → `28`'],
        quote='一共m + n - 2个球中，有m - 1个白球，n - 1个黑球，问有多少种排列的情况，因此最终的答案就是C(m + n - 2，m - 1)。',
        quote_src='—— yiduobo 题解',
        idea=['不管怎么走，「往下」和「往右」的步数都是固定的',
              '一条路径 = 一个「下 / 右」序列 = ==白球黑球的一种排列==',
              '从 `m+n-2` 个位置挑出放黑球的：`C(m+n-2, n-1) = C(m+n-2, m-1)`',
              '代码先把 `m` 改成总步数、`n` 改成黑球数，再逐项乘除算组合数'],
        summary=['时间 `O(n)`、空间 `O(1)`；可取 `min(m, n) - 1` 做循环次数更快',
                 '==先乘后除==：`res * now // index` 每步整除；先算 `now // index` 会错',
                 '原文为 Python 2 写法：`/` 已改为 `//`（Python 3 的 `/` 得浮点数）',
                 '原文也提到可用经典 DP：`f[i][j] = f[i-1][j] + f[i][j-1]`'],
    ),
)
