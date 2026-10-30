P = [[1, 1], [3, 4], [-1, 0], [0, -3], [2, -3]]


def _cell(S, r, c, v):
    i = S.get('index')
    if i is None:
        return None
    return 'pink' if r == i else 'blue' if r == i - 1 else None


def _text(S):
    i = S.get('index')
    if i is None:
        return '两点间的时间 = 水平距离、竖直距离里的==较大值=='
    p = S['points']
    dx, dy = abs(p[i][0] - p[i - 1][0]), abs(p[i][1] - p[i - 1][1])
    return f'`|dx| = {dx}`，`|dy| = {dy}` → 走斜线到同行或同列，再直走 → ==`{max(dx, dy)}`== 秒'


CONFIG = dict(
    num=1266, title='访问所有点的最小时间', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='相邻点距离取 max 后求和',
    tags=['灵神题单', '难度分 1303'],
    code='''
class Solution(object):
    def minTimeToVisitAllPoints(self, points):
        res = 0
        for index in range(1, len(points)):
            res += max(abs(points[index][0] - points[index - 1][0]), abs(points[index][1] - points[index - 1][1]))

        return res
''',
    call=f'Solution().minTimeToVisitAllPoints({P!r})',
    expect=12,
    views=[
        dict(type='table', var='points', label='points（蓝 = 上一个点，粉 = 这次要去的点）', h=380, cell=76,
             rows=lambda S: [f'{k}' for k in range(len(S['points']))], cols=['x', 'y'], color=_cell),
        dict(type='text', fn=_text, size=26, h=70),
    ],
    watch=[('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总时间',
        'for index in range': lambda S, B, r: ('每一对相邻点都算过了，循环结束' if B.get('index') == S.index and S.index == len(S.points) - 1 and B.get('res') == S.res and S.res > 0
                                               else f'看第 `{S.index - 1}` 个点到第 `{S.index}` 个点，==必须按顺序走=='),
        'res += max': '水平距离 `{abs(points[index][0] - points[index - 1][0])}`，竖直距离 `{abs(points[index][1] - points[index - 1][1])}`：先走斜线再直走，取较大值 → `res` = =={res}==',
        'return res': '把相邻点的时间加起来：=={ret}==',
    },
    cards=dict(
        one_liner='相邻两点：走斜线，耗时 = 水平、竖直距离的较大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['平面上有 `n` 个点，每秒横走、竖走或斜走一格',
                 '必须按顺序访问所有点，求最少时间',
                 '示例：`[[1,1],[3,4],[-1,0]]` → `7`'],
        quote='若两个点不在同行也不在同列，走斜线就是最好的选择，那么可以不断走斜线，直到两个点在同一行或者同一列，然后再进行水平或者竖直的移动即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['顺序固定，只需遍历相邻点，把每段时间加起来',
              '不同行也不同列就一直斜走，直到同行或同列，再直走',
              '所以每段耗时就是 `max(水平距离, 竖直距离)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不能重排顺序：题目要求按数组顺序访问',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串',
                 '对比灵神：同一个结论，他称之为切比雪夫距离，并用 `pairwise` 遍历'],
    ),
)
