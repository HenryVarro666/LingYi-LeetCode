CONFIG = dict(
    num=3843, title='频率唯一的第一个元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表的哈希表',
    tags=[],
    code='''
class Solution(object):
    def firstUniqueFreq(self, nums):
        
        freq = {}
        freq_freq = {}

        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        for f in freq.values():
            freq_freq[f] = freq_freq.get(f, 0) + 1
        
        for v in nums:
            if freq_freq[freq[v]] == 1:
                return v
        
        return -1
''',
    call='Solution().firstUniqueFreq([20,20,10,30,30,30,40,40])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'v': 'blue'}, cell=90, h=190),
        dict(type='map', var='freq', label='freq（数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=210, font=30),
        dict(type='map', var='freq_freq', label='freq_freq（次数 f → 出现过几次）', fmt=lambda k, v: f'f = {k}: {v} 次', h=210, font=30),
    ],
    watch=['v', ('f', "f if 'f' in S else ''", 'cyan'), ('freq[v]', "freq[v] if 'v' in S and v in freq else ''", 'cyan'), ('freq_freq[freq[v]]', "freq_freq[freq[v]] if 'v' in S and v in freq else ''", 'orange')],
    captions={
        'for v in nums': '看 `v = {v}`',
        'for f in freq.values()': '取出一个次数 `f = {f}`',
        'freq = {}': '`freq`：每个数出现几次',
        'freq_freq = {}': '`freq_freq`：每种「出现次数」又出现了几次',
        'freq[v] = freq.get': '`v = {v}`，`freq[{v}]` → ==`{freq[v]}`==',
        'freq_freq[f] =': '遍历到次数 `f = {f}`，`freq_freq[{f}]` → ==`{freq_freq[f]}`==',
        'if freq_freq[freq[v]] == 1': '`{v}` 出现 `{freq[v]}` 次，`freq_freq[{freq[v]}] = {freq_freq[freq[v]]}` → {"==为 1，频率唯一=="if freq_freq[freq[v]] == 1 else "不是 1，有别的数次数相同"}',
        'return v': '`{ret}` 是第一个频率唯一的数',
        'return -1': '遍历完也没找到 → `-1`',
    },
    cards=dict(
        one_liner='freq 数元素，freq_freq 数次数，再扫一遍 nums',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找 `nums` 中从左到右第一个「出现频率与众不同」的元素',
                 '频率与众不同：没有别的数出现次数和它一样；没有就返回 `-1`',
                 '示例：`[20,20,10,30,30,30]` → `20`；`[10,10,20,20]` → `-1`'],
        quote='再遍历freq中的每个值f，使用哈希表的哈希表freq_freq统计每种f出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`freq` 统计每个元素的次数',
              '第二趟：遍历 `freq` 的值 `f`，`freq_freq` 统计每种次数出现几次',
              '第三趟：按 `nums` 顺序，`freq_freq[freq[v]] == 1` 就返回 `v`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第三趟要遍历 `nums` 而不是 `freq`，才能保证「第一个」',
                 '用 `dict.get(k, 0) + 1` 代替 Counter，思路一样',
                 '对比灵神：灵神直接用 Counter，yiduobo 手写哈希表计数'],
    ),
)
