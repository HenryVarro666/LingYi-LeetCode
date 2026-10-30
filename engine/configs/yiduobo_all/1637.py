def _xs(S):
    return sorted(p[0] for p in S['points'])


def _t(S):
    if 'last_x' not in S:
        return ''
    if 'x' in S and S.get('last_x') is not None:
        return f"相邻横坐标间隔 `{S['x']} − {S['last_x']}` = =={S['x'] - S['last_x']}==；目前最大 `res = {S.get('res')}`"
    return '只有 x 坐标有用：排序后看相邻间隔'


CONFIG = dict(
    num=1637, title='两点之间不包含任何点的最宽垂直面积', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按 x 排序 + 相邻差',
    tags=[],
    code='''
class Solution(object):
    def maxWidthOfVerticalArea(self, points):

        res = None
        last_x = None
        for x, y in sorted(points, key=lambda d:d[0]):
            if last_x is not None:
                if res is None or res < x - last_x:
                    res = x - last_x
            
            last_x = x
        
        return res
''',
    call='Solution().maxWidthOfVerticalArea([[3,1],[9,0],[1,0],[1,4],[5,3],[8,8]])',
    expect=3,
    views=[
        dict(type='array', var=_xs, h=170, cell=80, label='排序后的 x（y 不影响答案）',
             pointers={'last_x': 'blue'}),
        dict(type='text', fn=_t, size=26, h=70),
    ],
    watch=['x', ('last_x', 'last_x', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = None': '`res` 记录目前最宽的间隔，一开始没有',
        'last_x = None': '`last_x` 记上一个点的 x，一开始没有',
        'for x, y in sorted': '按 x 从小到大取下一个点：`x = {x}`（y 不用管）',
        'if last_x is not None': lambda S, B, r: ('有上一个点了，可以算间隔' if S.last_x is not None else '这是第一个点，没有间隔可算'),
        'if res is None or res < x - last_x': lambda S, B, r: (f"间隔 `{S.x - S.last_x}`，目前最大 `{S.res}`：" + ('更宽 → 更新答案' if (S.res is None or S.res < S.x - S.last_x) else '不更宽，不更新')),
        'res = x - last_x': '最宽间隔更新为 `res = {res}`',
        'last_x = x': '`last_x` 前进到 `{last_x}`，下一轮和它比',
        'return res': '最宽的垂直间隔是 `{res}`',
    },
    cards=dict(
        one_liner='只看 x：排序后相邻 x 的最大差就是答案',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序）',
        problem=['平面上有 `n` 个点，找两点之间==不包含任何点==的最宽垂直区域的宽度',
                 '示例：x 坐标 `3,9,1,1,5,8`',
                 '结果 `3`（x=5 与 x=8 之间）'],
        quote='虽然是平面上的点，但是实际上只需要关心x这一维，所求的就是相邻x之间的最大间隔。',
        quote_src='—— yiduobo 题解原文',
        idea=['垂直区域的宽度只和 x 有关，y 可以忽略',
              '按 x 排序后，中间不含点的区域就是相邻两点之间',
              '一趟扫描，维护上一个 x 和最大间隔'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错点：相同 x 的间隔为 0，不影响答案',
                 '只有 1 个点时没有间隔，`res` 为 None；题目保证至少 2 个点',
                 '原文为 Python 2 风格，代码未改动'],
    ),
)
