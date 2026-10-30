CONFIG = dict(
    num=2363, title='合并相似的物品', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表累加 + 枚举 value',
    tags=[],
    code='''
class Solution(object):
    def mergeSimilarItems(self, items1, items2):
        d = {}
        for w, v in items1:
            d[w] = d.get(w, 0) + v
        
        for w, v in items2:
            d[w] = d.get(w, 0) + v
        
        res = []
        for w in range(1, 1001):
            if w in d:
                res.append([w, d[w]])
        
        return res
''',
    call='Solution().mergeSimilarItems([[1,1],[4,5],[3,8]], [[3,1],[1,5]])',
    expect=[[1, 6], [3, 9], [4, 5]],
    views=[
        dict(type='array', var='items1', label='items1', cell=110, h=160, font=28),
        dict(type='array', var='items2', label='items2', cell=110, h=160, font=28),
        dict(type='map', var='d', label='d：value → 总 weight', fmt=lambda k, v: f'{k}: {v}', h=170),
        dict(type='array', var='res', label='res', cell=110, h=160, font=28),
    ],
    watch=[('w', 'w', 'blue'), ('v', 'v', 'pink')],
    captions={
        'd = {}': '准备哈希表 `d`，键是 value，值是累计 weight',
        'for w, v in items1': '取出一项：value=`{w}`，weight=`{v}`',
        'for w, v in items2': '取出一项：value=`{w}`，weight=`{v}`',
        'd[w] = d.get': '`d[{w}] = d.get({w}, 0) + {v}` = =={d[w]}==（已有就累加，没有就从 0 开始）',
        'for w in range': '从小到大枚举 value，这样结果天然升序（当前 `{w}`）',
        'if w in d': '`{w}` 在 `d` 里吗？{"在 → 加入答案" if w in d else "不在 → 跳过"}',
        'res.append': '枚举 value 从 1 到 1000，遇到 `d` 里有的 `{w}` 就加入答案 `[{w}, {d[w]}]`（其余 value 不在表里，直接略过）',
        'return res': '按 value 升序的合并结果 =={res}==',
    },
    skip=['res = []', 'for w in range', 'if w in d'],
    max_steps=90,
    cards=dict(
        one_liner='哈希表累加重量，再按 value 从小到大枚举',
        complexity='时间 `O(n+m+V)`，V = 1000，空间 `O(n+m)`',
        problem=['两个物品集合，每项 `[value, weight]`',
                 '合并相同 value 的重量，按 value 升序返回',
                 '示例：`[[1,1],[4,5],[3,8]]` 与 `[[3,1],[1,5]]` → `[[1,6],[3,9],[4,5]]`'],
        quote='使用哈希表统计每种重量下的总价值，然后从1到1000枚举所有可能的重量。若当前重量在哈希表中出现过，那么就将其和对应的价值加入到答案中即可。',
        quote_src='—— yiduobo 题解（原文把 value 称作重量、weight 称作价值）',
        idea=['两个数组依次扫一遍，哈希表按 value 累加 weight',
              'value 范围只有 1 到 1000，直接按顺序枚举',
              '出现过的就放进答案，不用再排序'],
        summary=['时间 `O(n+m+V)`，不需要 `sort`，靠枚举范围保证有序',
                 '易错点：`range(1, 1001)` 右端要写 1001',
                 '原文变量名 `w` 实际是 value，`v` 是 weight，和题面相反，注意别混'],
    ),
)
