B1 = [2, 3, 5, 2, 3, 9]
B2 = [1, 4, 5, 1, 4, 9]

CONFIG = dict(
    num=2561, title='重排水果', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='哈希表计数差 · 排序后取小的一半',
    tags=['灵神题单', '难度分 2222'],
    code='''
class Solution(object):
    def minCost(self, basket1, basket2):

        cnt = {}
        for v in basket1:
            cnt[v] = cnt.get(v, 0) + 1
        for v in basket2:
            cnt[v] = cnt.get(v, 0) - 1
        
        swap_list = []
        for v, freq in cnt.items():
            if freq % 2 != 0:
                return -1
            for _ in range(abs(freq) // 2):
                swap_list.append(v)
        
        mi = min(cnt.keys())
        swap_list.sort()
        res = 0
        for index in range(len(swap_list) // 2):
            res += min(mi * 2, swap_list[index])
        
        return res
''',
    call=f'Solution().minCost({B1}, {B2})',
    expect=3,
    skip=['cnt = {}', 'res = 0', 'for _ in range', 'swap_list = []'],
    views=[
        dict(type='array', var='basket1', label='basket1', cell=70, h=140),
        dict(type='array', var='basket2', label='basket2', cell=70, h=140),
        dict(type='map', var='cnt', label='cnt[v]：basket1 里 v 的个数 − basket2 里 v 的个数', font=26, h=230,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var=lambda S: S.get('swap_list'), label='swap_list：要交换的水果（每种取差值的一半）', cell=70, h=140,
             pointers={'index': 'blue'}, dim=lambda S, i, v: 'index' in S and i >= len(S['swap_list']) // 2),
        dict(type='text', fn=lambda S: (f"最小成本 `mi = {S['mi']}`，只遍历 `swap_list` 的前 `{len(S['swap_list'])//2}` 个" if 'mi' in S else ''), size=26),
    ],
    watch=[('v', 'v', 'yellow'), ('freq', 'freq', 'pink'), ('mi', 'mi', 'blue'), ('res', 'res', 'green')],
    captions={
        'for v in basket1': lambda S, B, r: ('`basket1` 统计完了，接着遍历 `basket2` 做减法' if S.get('v') == B.get('v')
                                             else f'遍历 `basket1`：取到水果 `{S.v}`，它的计数加一'),
        'for v in basket2': lambda S, B, r: ('两个篮子都统计完了：差值为 0 的不用换，非零的才要换' if S.get('v') == B.get('v')
                                             else f'遍历 `basket2`：取到水果 `{S.v}`，它的计数减一，和 `basket1` 里的抵消'),
        'cnt[v] = cnt.get(v, 0) + 1': lambda S, B, r: f'`basket1` 里的 `{S.v}`：`cnt[{S.v}] = {S.cnt[S.v]}`',
        'cnt[v] = cnt.get(v, 0) - 1': lambda S, B, r: f'`basket2` 里的 `{S.v}`：`cnt[{S.v}] = {S.cnt[S.v]}`',
        'for v, freq in cnt.items()': lambda S, B, r: ('差值都检查完了，接着排序' if (S.get('v'), S.get('freq')) == (B.get('v'), B.get('freq'))
                                                       else f'检查水果 `{S.v}`：个数差 `freq = {S.freq}`'),
        'if freq % 2': lambda S, B, r: (f'`freq = {B.freq}` 是奇数：不能把一半换到另一边 → 无解，返回 `-1`' if B.freq % 2
                                        else (f'`freq = 0`：两边一样多，不用换' if B.freq == 0 else f'`freq = {B.freq}` 是偶数：其中一半（`{abs(B.freq)//2}` 个）要换到另一个篮子')),
        'swap_list.append': '把 `{v}` 加入 `swap_list`：现在有 `{len(swap_list)}` 个要交换的数',
        'mi = min': '`mi = {mi}`：全体水果的最小成本，可以当==中间水果==，先后各换一次，代价 `2×mi`',
        'swap_list.sort()': '`swap_list` 从小到大排序：`{swap_list}`，成本小的和成本大的配对，代价由小的决定',
        'for index in range': lambda S, B, r: (f'只遍历前一半：`index = {S.index}`' if 'index' in S and S.get('index') != B.get('index')
                                               else '前一半都累加完了'),
        'res += min': '`swap_list[{index}] = {swap_list[index]}` 和 `2×mi = {mi*2}` 取较小值累加：`res = {res}`',
        'return res': '返回最小交换成本 `{res}`',
    },
    cards=dict(
        one_liner='数量差的一半就是要交换的数，排序后只付小的那一半',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个果篮各 `n` 个水果，交换 `basket1[i]` 和 `basket2[j]` 的成本为 `min(两者)`',
                 '求让两个果篮排序后相等的最小总成本，不可能则返回 `-1`',
                 '示例：`[4,2,2,2]`、`[1,4,1,2]` → `1`'],
        quote='另一种处理方法则是使用一个成本最小的水果作为中间水果，先与一种水果交换，再与另一种水果交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表统计每种水果的数量差；差为奇数就无解',
              '差的一半放进 `swap_list`；排序后小的和大的配对',
              '每个数的成本不超过「最小成本的两倍」，所以只累加前一半，每项取 `min(mi×2, 该数)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`mi` 取所有水果（两个篮子）的最小值；只累加 `swap_list` 前一半',
                 '原文为 Python 2 写法，两处 `range(.../2)` 的整数除法已改为 `//`'],
    ),
)
