CONFIG = dict(
    num=1943, title='描述绘画结果', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分思想 · 端点排序后合并同位置',
    tags=['灵神题单', '常用数据结构', '难度分 1969'],
    code='''
class Solution(object):
    def splitPainting(self, segments):

        points = []
        for start, end, color in segments:
            points.append([start, color])
            points.append([end, -color])
        
        points = sorted(points, key=lambda d:d[0])

        now = 0
        last = 0
        start = None
        p = 0
        res = []
        while p < len(points):
            while p + 1 < len(points) and points[p][0] == points[p + 1][0]:
                now += points[p][1]
                p += 1
            
            now += points[p][1]
            if start is not None and last > 0:
                res.append([start, points[p][0], last])
            last = now
            start = points[p][0]
            
            p += 1
        
        if start < points[p - 1][0] and last > 0:
            res.append([start, points[p - 1][0], last])
        return res
''',
    call='Solution().splitPainting([[1,7,9],[6,8,15],[8,10,7]])',
    expect=[[1, 6, 9], [6, 7, 24], [7, 8, 15], [8, 10, 7]],
    views=[
        dict(type='text', fn=lambda S: (f"`now` = 当前位置的颜色和 =={S['now']}==；`last` = 上一段的颜色和 `{S['last']}`，上一段起点 `start` = `{S['start']}`" if 'now' in S and 'last' in S else '每个线段拆成 起点 `+color`、终点 `-color` 两个点')),
        dict(type='array', var='points', label='points：[位置, 颜色变化]（已按位置排序）', h=240, cell=150, pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if v[1] > 0 else 'pink'),
        dict(type='array', var='res', label='res：[起点, 终点, 颜色和]', h=170, cell=150),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'orange'), ('last', 'last', 'cyan'), ('start', 'start', 'purple')],
    captions={
        'points.append([start, color])': '线段 `[{start}, {end}, {color}]` 的起点：位置 `{start}` 处颜色 `+{color}`',
        'points.append([end, -color])': '终点：位置 `{end}` 处颜色 `-{color}`',
        'points = sorted': '只有端点会改变颜色，按位置排序：从左到右一趟处理',
        'now = 0': '`now`：扫到当前点时的颜色和',
        'last = 0': '`last`：上一段的颜色和（`0` 表示没有颜色）',
        'start = None': '`start`：上一段的起点，还没有',
        'p = 0': '`p` 指向当前处理的点',
        'while p < len(points)': lambda S, B, r: (f"`p = {S['p']} < {len(S['points'])}`：还有点没处理" if S['p'] < len(S['points']) else '所有点处理完 → 结束循环'),
        'while p + 1 < len(points)': lambda S, B, r: (f"`points[{S['p']}]` 和 `points[{S['p']+1}]` 位置都是 `{S['points'][S['p']][0]}` → 先把前一个合并进 `now`" if S['p'] + 1 < len(S['points']) and S['points'][S['p']][0] == S['points'][S['p']+1][0] else f"后面一个点位置不同，同位置的点合并完了"),
        'now += points[p][1]': lambda S, B, r: f"`now += {S['points'][S['p']][1]}` → `{S['now']}`：位置 `{S['points'][S['p']][0]}` 处的颜色变化累加进来",
        'if start is not None and last > 0': lambda S, B, r: (f"上一段 `[{S['start']}, {S['points'][S['p']][0]})` 颜色和 `last = {S['last']} > 0` → 结算成一段" if S['start'] is not None and S['last'] > 0 else '还没有上一段，或上一段没有颜色 → 不结算'),
        'res.append([start': '加入答案：`[{start}, {points[p][0]}, {last}]`',
        'last = now': '本位置之后的颜色和是 `{now}`，记成新的 `last`',
        'start = points[p][0]': '新的一段从位置 `{start}` 开始',
        'p += 1': '`p` → {p}',
        'if start < points[p - 1][0]': lambda S, B, r: f"别忘了最后一段：`start = {S['start']} < {S['points'][S['p']-1][0]}` 且 `last = {S['last']} > 0`？" + ('是 → 加入' if S['start'] < S['points'][S['p']-1][0] and S['last'] > 0 else '否 → 不加'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='把端点排好序，同位置的合并，相邻端点之间就是一段',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['线段 `[start, end, color]` 是半开区间，重叠处颜色求和，求最少数目的不重叠区间',
                 '颜色集合不同的段不能合并（即使颜色和相同）',
                 '本视频：`[[1,7,9],[6,8,15],[8,10,7]]` → `[[1,6,9],[6,7,24],[7,8,15],[8,10,7]]`'],
        quote='因此在具体实现上，不需要使用差分数组来保存这些点，而是直接将这些点在数轴上的下标和对应的颜色保存起来，然后从小到大排序，接下来一趟遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典差分：起点加 color，终点减 color，但这里只存端点，不开数轴数组',
              '遍历时先把同一位置的点全部并入 `now`',
              '遇到新位置：若上一段 `last > 0`，就把 `[start, 当前位置)` 结算进答案，再更新 `last`、`start`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：同一位置的多个端点要先合并再结算，否则会出现长度为 0 的段',
                 '颜色都大于 0，所以 `last > 0` 就表示上一段有颜色',
                 '循环外还要补一次判断，防止漏掉最后一段（原文说明「不要忘记」）',
                 '对比灵神：灵神每个端点各处理一次，用 `pos < 下一个 pos` 去掉空段；这里用内层 while 先合并同位置'],
    ),
)
