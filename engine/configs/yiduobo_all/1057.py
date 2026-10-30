CONFIG = dict(
    num=1057, title='校园自行车分配', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='全部配对排序 + 贪心分配',
    code='''
class Solution(object):
    def assignBikes(self, workers, bikes):

        match = []
        n = len(workers)
        m = len(bikes)

        for i in range(n):
            for j in range(m):
                match.append([abs(workers[i][0] - bikes[j][0]) + abs(workers[i][1] - bikes[j][1]), i, j])
        
        match.sort()
        used_worker = set()
        used_bike = set()
        res = [None] * n
        for _, i, j in match:
            if i not in used_worker and j not in used_bike:
                res[i] = j
                used_worker.add(i)
                used_bike.add(j)
        
        return res
''',
    call='Solution().assignBikes([[0,0],[2,1],[3,3]], [[1,2],[3,3],[0,1]])',
    expect=[2, 0, 1],
    views=[
        dict(type='text', size=30, fn=lambda S: f"工人 `workers = {S['workers']}`"),
        dict(type='text', size=30, fn=lambda S: f"自行车 `bikes = {S['bikes']}`"),
        dict(type='text', size=26, fn=lambda S: "`match` = " + ' '.join('`' + str(x).replace(' ', '') + '`' for x in S['match']) if S['match'] else "`match`（[距离, 工人, 车]）还是空的"),
        dict(type='array', var='res', label='res[工人] = 自行车', h=200, pointers={'i': 'blue'}),
        dict(type='text', size=30, fn=lambda S: f"已分配工人 `{sorted(S['used_worker'])}`　已分走车 `{sorted(S['used_bike'])}`" if 'used_worker' in S else ''),
    ],
    watch=['i', 'j', 'used_worker', 'used_bike'],
    max_steps=90,
    captions={
        'match.append': '工人 `{i}` 与车 `{j}` 的曼哈顿距离 = =={match[-1][0]}==，加入 `match`',
        'match.sort': '排序：先比距离，距离相同比工人编号，再相同比车编号——正好就是题目的分配优先级',
        'for _, i, j in match': '按优先级取下一个配对：距离 `{_}`，工人 `{i}`，车 `{j}`',
        'if i not in used_worker': lambda S, B, r: (f'工人 `{S.i}` 和车 `{S.j}` 都还空着 → ==分配==' if S.i not in S.used_worker and S.j not in S.used_bike
                                                     else f'工人 `{S.i}` 或车 `{S.j}` 已被占用 → 跳过这一对'),
        'res[i] = j': '工人 `{i}` 得到车 `{j}`：`res = {res}`',
        'used_worker.add': '标记工人 `{i}` 已分配',
        'used_bike.add': '标记车 `{j}` 已被分走',
        'return res': '全部分配完成 → `{res}`',
    },
    cards=dict(
        one_liner='把所有「人-车」配对排好序，从前往后挑没被占用的',
        complexity='时间 `O(nm·log(nm))`，空间 `O(nm)`',
        problem=['平面上有 n 个工人和 m 个自行车（n ≤ m）',
                 '每次挑曼哈顿距离最短的「工人-车」配对；距离相同取工人编号小的，再相同取车编号小的',
                 '示例：工人 `[[0,0],[2,1],[3,3]]`，车 `[[1,2],[3,3],[0,1]]` → `[2,0,1]`'],
        quote='题目自行车分配的规则是按照曼哈顿距离为第一关键字，工人编号为第二关键字，自行车编号为第三关键字来进行的，那么最自然的想法就是两两枚举工人和自行车',
        quote_src='—— yiduobo 题解原文',
        idea=['把 `[距离, 工人, 车]` 作为列表，`sort` 默认就是按三个关键字依次比较',
              '遍历排好的配对：工人和车都空着就分配，用两个集合记录占用情况',
              '先出现的配对优先级最高，所以贪心不会出错'],
        summary=['时间 `O(nm·log(nm))`，空间 `O(nm)`',
                 '易错点：列表顺序必须是 `[距离, 工人, 车]`，排序才符合题意',
                 '工人和车要==同时==判断是否已被占用',
                 '距离范围小（≤ 2000）时可以桶排序优化到 `O(nm)`'],
    ),
)
