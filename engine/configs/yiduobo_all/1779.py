CONFIG = dict(
    num=1779, title='找到最近的有相同 X 或 Y 坐标的点', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描 + 曼哈顿距离',
    tags=[],
    code='''
class Solution(object):
    def nearestValidPoint(self, x, y, points):

        res = -1
        max_dis = None
        for index in range(len(points)):
            px, py = points[index]
            if px == x or py == y:
                if max_dis is None or abs(px - x) + abs(py - y) < max_dis:
                    max_dis = abs(px - x) + abs(py - y)
                    res = index
        
        return res
''',
    call='Solution().nearestValidPoint(3, 4, [[1,2],[3,1],[2,4],[2,3],[4,4]])',
    expect=2,
    views=[
        dict(type='table', var='points', label='points（列：x / y），目标 (x, y) = (3, 4)', h=330,
             cols=['x', 'y'],
             color=lambda S, i, j, v: ('green' if i == S.get('res') else
                                       ('yellow' if i == S.get('index') else None))),
        dict(type='text', fn=lambda S: ('第 %s 个点 (%s, %s)：距离 = |%s−%s| + |%s−%s| = ==%s==' % (
            S['index'], S['px'], S['py'], S['px'], S['x'], S['py'], S['y'],
            abs(S['px'] - S['x']) + abs(S['py'] - S['y']))) if 'px' in S and 'index' in S else '', size=26, h=70),
    ],
    watch=['index', ('px', 'px'), ('py', 'py'), ('max_dis', 'max_dis', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = -1': '先假设没有合法点：`res = -1`',
        'max_dis = None': '`max_dis` 记录目前最小距离，还没有所以是 `None`',
        'px, py = points': '取出第 `{index}` 个点：`({px}, {py})`',
        'if px == x or py == y': lambda S, B, r: ('`px = %s, py = %s`，与 (%s, %s) %s → %s' % (
            S['px'], S['py'], S['x'], S['y'],
            '至少一个坐标相同' if (S['px'] == S['x'] or S['py'] == S['y']) else '两个坐标都不同',
            '合法，继续比距离' if (S['px'] == S['x'] or S['py'] == S['y']) else '不合法，跳过')),
        'if max_dis is None or': lambda S, B, r: ('距离 `%s`，当前最小 `%s`：==更小== → 更新' % (abs(S['px'] - S['x']) + abs(S['py'] - S['y']), S['max_dis'])
                                                  if S['max_dis'] is None or abs(S['px'] - S['x']) + abs(S['py'] - S['y']) < S['max_dis']
                                                  else '距离 `%s` 不小于当前最小 `%s`（相等也不换，保留靠前的）→ 不更新' % (abs(S['px'] - S['x']) + abs(S['py'] - S['y']), S['max_dis'])),
        'max_dis = abs': '最小距离更新为 `{max_dis}`',
        'res = index': '答案记为下标 `{res}`',
        'return res': '扫描完毕，距离最小且最靠前的合法点下标是 `{res}`',
    },
    cards=dict(
        one_liner='只看同行或同列的点，取曼哈顿距离最小且最靠前的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定当前位置 `(x, y)` 和点列表 `points`',
                 '合法点：横坐标或纵坐标与 `(x, y)` 相同',
                 '返回曼哈顿距离最小的合法点下标，相同取小下标，没有则 `-1`'],
        quote='直接一趟扫描，根据曼哈顿距离的定义计算所有具有相同x或y的点到(x, y)的距离，然后取距离最小且最靠前的点作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个点，先判断 `px == x or py == y`',
              '合法就算 `|px−x| + |py−y|`，只在严格更小时更新',
              '严格小于保证距离相同时留下靠前的下标'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：必须用严格 `<`，否则会选到靠后的同距离点',
                 '易错：没有合法点时返回 `-1`',
                 '变量名 `max_dis` 实际存的是最小距离',
                 '原文为 Python 2 写法，Python 3 下可直接运行，代码未改'],
    ),
)
