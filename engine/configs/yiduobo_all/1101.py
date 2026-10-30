CONFIG = dict(
    num=1101, title='彼此熟识的最早时间', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集 · 按大小合并',
    tags=[],
    code='''
class Solution(object):
    def earliestAcq(self, logs, n):

        fa = list(range(n))
        weight = [1] * n

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for t, x, y in sorted(logs):
            fa_x = find(x)
            fa_y = find(y)

            if fa_x != fa_y:
                if weight[fa_x] < weight[fa_y]:
                    fa[fa_x] = fa_y
                    weight[fa_y] += weight[fa_x]
                    if weight[fa_y] == n:
                        return t
                else:
                    fa[fa_y] = fa_x
                    weight[fa_x] += weight[fa_y]
                    if weight[fa_x] == n:
                        return t

        return -1
''',
    call='Solution().earliestAcq([[5,2,3],[3,0,1],[9,0,3],[7,1,2]], 4)',
    expect=7,
    views=[
        dict(type='array', var='fa', label='fa（父节点；fa[i] = i 表示 i 是根）', cell=110, h=170,
             pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='array', var='weight', label='weight（以该根为代表的连通块大小）', cell=110, h=170,
             color=lambda S, i, v: 'green' if v == S['n'] else None),
        dict(type='text', h=80, size=30, fn=lambda S: (f"时间 t = {S['t']}：`{S['x']}` 与 `{S['y']}` 成为朋友" if 't' in S else '先把 logs 按时间从小到大排序')),
    ],
    watch=[('t', 't', 'yellow'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), 'fa_x', 'fa_y', ('n', 'n', 'green')],
    captions={
        'fa = list(range(n))': '一开始每个人自成一组：`fa[i] = i`',
        'weight = [1] * n': '`weight[i]`：以 i 为根的连通块有几人，开始都是 `1`',
        'for t, x, y in sorted(logs)': '按时间戳从小到大处理：时间 `{t}`，`{x}` 与 `{y}` 认识',
        'fa_x = find(x)': '`find({x})`：找 x 所在小圈子的根',
        'fa_y = find(y)': '`find({y})`：找 y 所在小圈子的根',
        'if fa_x != fa_y:': '根 `{fa_x}` 与 `{fa_y}`：{"不同 → 两个圈子要合并" if fa_x != fa_y else "相同 → 早就认识，没有新信息"}',
        'if weight[fa_x] < weight[fa_y]': '`weight[{fa_x}] = {weight[fa_x]}`，`weight[{fa_y}] = {weight[fa_y]}`：{"x 圈更小 → 挂到 y 下面" if weight[fa_x] < weight[fa_y] else "x 圈不小于 y 圈 → 把 y 圈挂到 x 下面"}',
        'fa[fa_x] = fa_y': '小圈挂到大圈：`fa[{fa_x}] = {fa_y}`',
        'fa[fa_y] = fa_x': '`fa[{fa_y}] = {fa_x}`，y 圈并入 x 圈',
        'weight[fa_y] += weight[fa_x]': '大小累加：`weight[{fa_y}] = {weight[fa_y]}`',
        'weight[fa_x] += weight[fa_y]': '大小累加：`weight[{fa_x}] = {weight[fa_x]}`',
        'if weight[fa_y] == n': '新圈子 `{weight[fa_y]}` 人，{"等于 n，所有人都相识" if weight[fa_y] == n else "还不到 n，继续"}',
        'if weight[fa_x] == n': '新圈子 `{weight[fa_x]}` 人，{"等于 n，所有人都相识" if weight[fa_x] == n else "还不到 n，继续"}',
        'return t': '合并后恰好 `n` 人在一个圈子 → 最早时间就是 ==`{t}`==',
        'return -1': '处理完所有记录仍没连成一块 → `-1`',
    },
    skip=['return fa[x]'],
    max_steps=80,
    cards=dict(
        one_liner='按时间排序合并朋友圈，圈子人数到 n 的那一刻就是答案',
        complexity='时间 `O(m log m)`，空间 `O(n)`',
        problem=['`n` 个人，`logs[i] = [时间, x, y]` 表示该时刻 x 和 y 成为朋友',
                 '朋友关系可传递：朋友的朋友也算熟识',
                 '求所有人彼此熟识的最早时间，做不到返回 `-1`',
                 '本视频：n=4，logs 含 4 条 → `7`'],
        quote='若合并后的weight等于n，就说明此时所有人都在一个连通块里，返回当前的时间戳即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['连通性判定首选并查集，额外开 `weight` 记录每个连通块的人数',
              '先按时间戳排序，一趟遍历：根不同才合并，同时更新 `fa` 和 `weight`',
              '合并时小圈挂大圈，合并后人数等于 `n` 就立刻返回当前时间'],
        summary=['时间 `O(m log m + m·α)`，排序是瓶颈，空间 `O(n)`',
                 '易错点：必须先排序；`weight` 只在根上有意义，要用根的下标',
                 '同一对人重复出现、根相同时不要重复累加人数',
                 '遍历完仍没有连通块人数到 `n` 就返回 `-1`',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `list(range(n))`'],
    ),
)
