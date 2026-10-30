CONFIG = dict(
    num=1436, title='旅行终点站', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 出度为 0',
    tags=[],
    code='''
class Solution(object):
    def destCity(self, paths):

        ind = {}
        for a, b in paths:
            if a not in ind:
                ind[a] = 0
            ind[a] += 1

            if b not in ind:
                ind[b] = 0
        
        for city in ind:
            if ind[city] == 0:
                return city
''',
    call='Solution().destCity([["B","C"],["D","B"],["C","A"]])',
    expect='A',
    views=[
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"当前线路 ==`{S['a']} → {S['b']}`==" if 'a' in S and 'b' in S and 'city' not in S
                           else (f"检查城市 ==`{S['city']}`==：出边数 `{S['ind'][S['city']]}`" if 'city' in S
                                 else '`ind[城市]` = 这个城市的出边条数'))),
        dict(type='map', var='ind', label='ind：城市 → 出边数', fmt=lambda k, v: f"'{k}': {v}", h=260, font=36),
    ],
    watch=['a', 'b', 'city', ('ind', 'dict(ind)', 'green')],
    captions={
        'ind = {}': '`ind` 记每个城市「出去的线路」有几条',
        'for a, b in paths': '取一条线路：从 `{a}` 到 `{b}`',
        'if a not in ind': lambda S, B, r: (f'`{S.a}` 还没登记 → 成立，先记 0' if S.a not in S.ind else f'`{S.a}` 已登记 → 不成立'),
        'ind[a] = 0': '登记 `{a}`：出边数起步为 0',
        'ind[a] += 1': '`{a} → {b}` 是 `{a}` 的一条出边：`ind[{a!r}]` = =={ind[a]}==',
        'if b not in ind': lambda S, B, r: (f'`{S.b}` 还没登记 → 成立，它目前没有出边' if S.b not in S.ind else f'`{S.b}` 已登记 → 不成立，保持原值'),
        'ind[b] = 0': '`{b}` 只作为终点出现，登记为 0：只进不出',
        'for city in ind': '遍历所有城市，找出边数为 0 的：`city = {city!r}`',
        'if ind[city] == 0': lambda S, B, r: (f'`ind[{S.city!r}] = {S.ind[S.city]}`：有出边 → 不是终点' if S.ind[S.city]
                                              else f'`ind[{S.city!r}] = 0`：只进不出 → 成立，就是终点'),
        'return city': '`{ret}` 只进不出，是旅行终点站',
    },
    cards=dict(
        one_liner='终点站只进不出：出边数为 0 的那个城市',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`paths[i] = [A, B]` 表示从 A 直接前往 B，线路无环、连成一条',
                 '求没有任何出边的终点站',
                 '示例：`[["B","C"],["D","B"],["C","A"]]` → `"A"`'],
        quote='比价基础的题目，找出只进不出的那个城市即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['用字典统计每个城市的出边条数，起点加一',
              '终点只要登记成 0，不会增加',
              '最后扫一遍字典，出边数为 0 的就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '终点城市可能从未作为起点出现，所以必须在字典里为 `b` 也登记一项 0',
                 '题目保证恰有一个终点，所以找到就返回',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行',
                 '对比灵神：灵神用两个集合 set_a/set_b 一次遍历；yiduobo 用出边计数'],
    ),
)
