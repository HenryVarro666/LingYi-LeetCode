CONFIG = dict(
    num=1037, title='有效的回旋镖', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='向量外积判共线',
    tags=[],
    code='''
class Solution(object):
    def isBoomerang(self, points):

        if points[0][0] == points[1][0] and points[0][1] == points[1][1]:
            return False

        if points[0][0] == points[2][0] and points[0][1] == points[2][1]:
            return False
        
        if points[1][0] == points[2][0] and points[1][1] == points[2][1]:
            return False
        
        x1 = points[1][0] - points[0][0]
        y1 = points[1][1] - points[0][1]

        x2 = points[2][0] - points[0][0]
        y2 = points[2][1] - points[0][1]

        return x1 * y2 - x2 * y1 != 0
''',
    call='Solution().isBoomerang([[1, 1], [2, 3], [3, 2]])',
    expect=True,
    views=[
        dict(type='array', var='points', h=130, label='points', cell=120, fmt=lambda v: f'({v[0]},{v[1]})'),
        dict(type='text', size=36, fn=lambda S: (f"v1 = ({S['x1']}, {S['y1']})" if 'y1' in S else '')
             + (f"，v2 = ({S['x2']}, {S['y2']})" if 'y2' in S else '')),
        dict(type='text', size=36, fn=lambda S: (f"外积 = `{S['x1']}×{S['y2']} − {S['x2']}×{S['y1']}` = =={S['x1']*S['y2']-S['x2']*S['y1']}==" if 'y2' in S else '')),
    ],
    watch=['x1', 'y1', 'x2', 'y2'],
    max_steps=40,
    captions={
        'points[0][0] == points[1][0]': '点 0 和点 1 是否重合？重合就不是三个不同的点 → 不重合，继续',
        'points[0][0] == points[2][0]': '点 0 和点 2 是否重合？不重合，继续',
        'points[1][0] == points[2][0]': '点 1 和点 2 是否重合？不重合，继续',
        'x1 = ': '向量 v1 的 x 分量：`x1 = {x1}`',
        'y1 = ': '向量 v1 的 y 分量：`y1 = {y1}`，v1 = `({x1}, {y1})`',
        'x2 = ': '向量 v2 的 x 分量：`x2 = {x2}`',
        'y2 = ': '向量 v2 的 y 分量：`y2 = {y2}`，v2 = `({x2}, {y2})`',
        'return x1 * y2': '外积 `{x1}×{y2} − {x2}×{y1} = {x1*y2 - x2*y1}`，不为 0 → 不共线 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='三点不重合且向量外积不为 0，就不共线，是回旋镖',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给三个点 `points`，判断它们是否是一个回旋镖',
                 '回旋镖：三点互不相同，且不在同一条直线上',
                 '示例：`[[1,1],[2,3],[3,2]]` → `true`'],
        quote='若这个计算结果为0，说明v1和v2共线，返回false，否则返回true。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排除任意两点重合的情况',
              '把 p1→p0、p2→p0 看成向量 v1、v2',
              '共线时夹角 0 或 180 度，sin 为 0，外积 `x1*y2 - x2*y1` 为 0'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：重合的点外积也是 0，但要先单独判，这里三次比较已覆盖',
                 '只用整数乘减，没有除法和斜率，避免除零和精度问题',
                 '代码逐字照搬，未做改动'],
    ),
)
