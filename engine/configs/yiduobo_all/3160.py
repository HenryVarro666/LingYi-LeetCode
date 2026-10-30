CONFIG = dict(
    num=3160, title='所有球里面不同颜色的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 color + freq',
    code='''
class Solution(object):
    def queryResults(self, limit, queries):

        color = {}
        freq = {}
        res = []
        for x, y in queries:
            if x in color:
                freq[color[x]] -= 1
                if freq[color[x]] == 0:
                    freq.pop(color[x])
            
            color[x] = y
            freq[color[x]] = freq.get(color[x], 0) + 1
            res.append(len(freq))
        
        return res
''',
    call='Solution().queryResults(4, [[1,4],[2,5],[1,3],[3,4],[2,4]])',
    expect=[1, 2, 2, 3, 2],
    views=[
        dict(type='map', var='color', label='color：每个球当前的颜色', fmt=lambda k, v: f'球{k}: 色{v}', h=170, font=30),
        dict(type='map', var='freq', label='freq：每种颜色当前有几个球', fmt=lambda k, v: f'色{k}: {v}个', h=170, font=30),
        dict(type='array', var='res', label='res', h=130),
    ],
    watch=['x', 'y', ('res', 'res', 'green')],
    captions={
        'color = {}': '`color` 记录每个球是什么颜色',
        'freq = {}': '`freq` 记录每种颜色出现了多少次，键的个数就是颜色种数',
        'if x in color': '球 `{x}` {"目前有颜色 → 先把它旧颜色的次数减 1" if x in color else "目前无色 → 直接染色"}',
        'freq[color[x]] -= 1': '旧颜色 `{color[x]}` 次数减 1 → {freq[color[x]]}',
        'if freq[color[x]] == 0': '旧颜色剩 `{freq[color[x]]}` 个 → {"已经没有这种颜色了，要从 freq 删去" if freq[color[x]] == 0 else "还有球，保留"}',
        'freq.pop': '从 `freq` 删去颜色 `{color[x]}`',
        'color[x] = y': '球 `{x}` 染成 `{y}`',
        'freq[color[x]] = freq.get': '新颜色 `{y}` 次数加 1 → `freq[{y}]` = {freq[y]}',
        'res.append': '此时不同颜色数 = `len(freq)` = =={len(freq)}==',
    },
    cards=dict(
        one_liner='用 color 改色，用 freq 数颜色种数',
        complexity='时间 `O(q)`，空间 `O(q)`',
        problem=['`limit+1` 个球最初无色，每次操作 `[x, y]` 把球 `x` 染成 `y`',
                 '求每次操作后不同颜色的数目，无色的球不算',
                 '本视频：`[[1,4],[2,5],[1,3],[3,4],[2,4]]` → `[1,2,2,3,2]`'],
        quote='题目需要计算的是颜色的种数，也就是说有多少种颜色出现的次数大于等于1次，那么就还需要使用另一个哈希表freq记录每种颜色当前出现了多少次。',
        quote_src='—— yiduobo 题解原文',
        idea=['要改球的颜色 → 哈希表 `color`', '要数颜色种数 → 哈希表 `freq` 记次数，次数为 0 的颜色要删掉',
              '每次操作后 `len(freq)` 就是答案'],
        summary=['时间 `O(q)`，空间 `O(q)`',
                 '易错点：旧颜色次数减到 0 要 `pop`',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改',
                 '对比灵神：灵神用 `defaultdict`，这里用 `dict.get` 处理新颜色'],
    ),
)
