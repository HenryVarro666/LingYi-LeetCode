ORIG = [1, 2, 3, 4, 5, 6]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    n = S.get('n', 1)
    cv.text((x0 + 18, y0 + 4), 'res（p = 当前最后一行已填了几个）', 24, T['muted'], bold=True)
    if not res:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2 + 10), '空', 30, T['dim'], anchor='mm')
        return
    cell = min(84, (x1 - x0 - 120) / max(n, 1))
    rh = min(84, (y1 - y0 - 60) / max(len(res), 1))
    sx = x0 + 90 + ((x1 - x0 - 120) - cell * n) / 2
    sy = y0 + 56
    for r, row in enumerate(res):
        cv.text((sx - 14, sy + r * rh + rh / 2), f'行{r}', 20, T['muted'], anchor='rm')
        for c in range(n):
            X, Y = sx + c * cell, sy + r * rh
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + rh - 2), fill=T['panel2'], r=6, outline=T['border'], width=1)
        for c, v in enumerate(row):
            fresh = r == len(res) - 1 and c == len(row) - 1
            X, Y = sx + c * cell, sy + r * rh
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + rh - 2), fill=T['green'] if fresh else T['blue'], r=6,
                    outline=T['yellow'] if fresh else T['border'], width=3 if fresh else 1)
            cv.text((X + cell / 2, Y + rh / 2), v, 28, T['bg'], anchor='mm', bold=True)


CONFIG = dict(
    num=2022, title='将一维数组转变成二维数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='行计数器 p · 满 n 个另起一行',
    tags=[],
    code='''
class Solution(object):
    def construct2DArray(self, original, m, n):

        res = []
        if len(original) != m * n:
            return res

        p = 0
        for num in original:
            if p == 0:
                res.append([])
            res[-1].append(num)
            p += 1
            if p == n:
                p = 0
        
        return res
''',
    call=f'Solution().construct2DArray({ORIG}, 2, 3)',
    expect=[[1, 2, 3], [4, 5, 6]],
    skip=['p += 1'],
    views=[
        dict(type='array', var='original', label='original（蓝 = 当前这个数 num）', cell=64, h=190,
             color=lambda S, i, v: 'blue' if v == S.get('num') else None,
             dim=lambda S, i, v: 'num' in S and v < S['num']),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('m', 'm'), ('n', 'n'), ('p', 'p', 'blue'), ('num', 'num', 'yellow')],
    captions={
        'res = []': '`res` 是答案矩阵，先放空',
        'if len(original) != m * n': lambda S, B, r: (f'`len(original) = {len(S.original)}`，`m × n = {S.m * S.n}` → 对不上，没法转换，直接返回空'
                                                       if len(S.original) != S.m * S.n else f'`len(original) = {len(S.original)}` = `m × n` → 可以转换'),
        8: '`p`：当前最后一行已经填了几个数，开始为 0',
        15: '`p` 清零：下一个数要另起新的一行',
        'for num in original': lambda S, B, r: ('所有数都放完了' if 'num' in B and S.num == B.num else f'取下一个数 `num = {S.num}`'),
        'if p == 0': lambda S, B, r: ('`p == 0`：当前行还没开头 → 另起新的一行' if S.p == 0 else f'`p = {S.p}`：当前行还没满，接着往后放'),
        'res[-1].append(num)': '把 `{num}` 加到最后一行末尾：`res[-1] = {res[-1]}`',
        'if p == n': lambda S, B, r: (f'放进去后这一行有 `{S.p}` 个数，`p == n = {S.n}`：满了 → 下一个数另起新行' if S.p == S.n
                                      else f'放进去后这一行有 `{S.p}` 个数，`p < n = {S.n}`：还没满'),
        'return res': '全部放完，返回 `{res}`',
    },
    cards=dict(
        one_liner='用计数器 p 数这一行放了几个，满 n 个就另起一行',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计答案）',
        problem=['把一维数组 `original` 按顺序填成 `m` 行 `n` 列的二维数组',
                 '`original` 的个数必须==恰好等于== `m × n`，否则返回空数组',
                 '示例：`[1,2,3,4], m=2, n=2` → `[[1,2],[3,4]]`；`[3], m=1, n=2` → `[]`'],
        quote='首先判断original的长度是否等于m * n，若不等于，说明无法转换，直接返回空。……使用一个行计数器p计算当前行已经填充了多少个数',
        quote_src='—— yiduobo 题解原文',
        idea=['长度不等于 `m * n` 直接返回空',
              '一趟遍历：`p == 0` 说明要开新行，`res.append([])`',
              '每次把数字放进最后一行并 `p += 1`，`p == n` 时清零'],
        summary=['时间 `O(mn)`，空间 `O(1)`（不计答案）',
                 '注意先判长度再转换，否则最后一行放不满',
                 '`p` 到 `n` 要清零，下一个数才会另起新行',
                 '原文提到 Python 有内置转换方式，这里作者手动实现了一遍'],
    ),
)
