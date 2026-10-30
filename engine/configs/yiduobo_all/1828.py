CONFIG = dict(
    num=1828, title='统计一个圆中点的数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力枚举 · 距离比较',
    code='''
class Solution(object):
    def countPoints(self, points, queries):

        res = []
        for cx, cy, r in queries:
            res.append(0)
            for x, y in points:
                if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                    res[-1] += 1
        
        return res
''',
    call='Solution().countPoints([[1,3],[3,3],[5,3],[2,2]], [[2,3,1],[4,3,1],[1,1,2]])',
    expect=[3, 2, 2],
    views=[
        dict(type='text', size=30, h=70,
             fn=lambda S: '点 points = ' + ' '.join((f'==[{p[0]},{p[1]}]==' if 'x' in S and p == [S['x'], S['y']] else f'[{p[0]},{p[1]}]') for p in S['points'])),
        dict(type='text', size=30, h=70,
             fn=lambda S: '圆 queries = ' + ' '.join((f'==[{q[0]},{q[1]},{q[2]}]==' if 'cx' in S and q == [S['cx'], S['cy'], S['r']] else f'[{q[0]},{q[1]},{q[2]}]') for q in S['queries'])),
        dict(type='text', size=34, h=70,
             fn=lambda S: (f"距离² = `({S['x']}−{S['cx']})² + ({S['y']}−{S['cy']})²` = =={(S['x']-S['cx'])**2+(S['y']-S['cy'])**2}==，半径² = `{S['r']**2}`"
                           if 'x' in S and 'cx' in S else '')),
        dict(type='array', var='res', label='res', h=130, color=lambda S, i, v: 'green'),
    ],
    watch=['cx', 'cy', 'r', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 存每个查询的答案',
        'for cx, cy, r in queries': lambda S, B, rr: (f'取一个查询圆：圆心 `({S.cx}, {S.cy})`，半径 `{S.r}`' if B.get('cx') is None or [B.get('cx'),B.get('cy'),B.get('r')] != [S.cx,S.cy,S.r] else '所有查询处理完，循环结束'),
        'res.append(0)': '这个圆的计数先置 0',
        'for x, y in points': lambda S, B, rr: (f'检查点 `({S.x}, {S.y})`' if B.get('x') is None or [B.get('x'),B.get('y')] != [S.x,S.y] else '所有点检查完，这个圆的计数确定'),
        'if (x - cx)': lambda S, B, r: (f"`({S.x}-{S.cx})² + ({S.y}-{S.cy})²` = {(S.x-S.cx)**2+(S.y-S.cy)**2}，"
                                        f"半径² = {S.r**2}：" + ('距离不超过半径 → 在圆内（含边界）' if (S.x-S.cx)**2+(S.y-S.cy)**2 <= S.r**2 else '距离大于半径 → 在圆外')),
        'res[-1] += 1': '点在圆内，当前圆的计数加一：`res[-1] = {res[-1]}`',
        'return res': '每个查询的答案：`{res}`',
    },
    cards=dict(
        one_liner='数据很小：每个圆都扫一遍所有点，比较距离平方',
        complexity='时间 `O(m·n)`，空间 `O(1)`（不计答案）',
        problem=['`points[i]` 是点坐标，`queries[j] = [cx, cy, r]` 是一个圆',
                 '对每个圆，统计在圆内（含边界）的点数',
                 '示例：`points=[[1,3],[3,3],[5,3],[2,2]]`，三个圆 → `[3,2,2]`'],
        quote='由于题目的数据规模很小，所以朴素的算法是可行的。枚举每个query中的圆，然后遍历所有的点，判断点是否在圆中。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举圆，内层枚举点', '判断条件：点到圆心距离 ≤ 半径',
              '两边平方，比较整数，避免开根号'],
        summary=['时间 `O(m·n)`，空间 `O(1)`',
                 '易错：边界上的点也算在圆内，用 `<=`',
                 '用距离平方比较，全程整数，没有精度问题',
                 '作者提到可用计算几何优化，但没给出做法'],
    ),
)
