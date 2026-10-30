CONFIG = dict(
    num=3852, title='不同频率的最小数对', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 每种频率的最小值',
    code='''
class Solution(object):
    def minDistinctFreqPair(self, nums):
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        freq_mi = {}
        for v, f in freq.items():
            if f not in freq_mi:
                freq_mi[f] = v
            else:
                freq_mi[f] = min(freq_mi[f], v)
        
        x, y = -1, -1
        for mi in freq_mi.values():
            if x == -1 or x > mi:
                x, y = mi, x
            elif y == -1 or y > mi:
                y = mi
        
        if y == -1:
            return [-1, -1]
        else:
            return [x, y]
''',
    call='Solution().minDistinctFreqPair([2,2,3,3,4,5,5,5])',
    expect=[2, 4],
    views=[
        dict(type='array', var='nums', h=170, cell=80),
        dict(type='map', var='freq', h=270, fmt=lambda k, v: f'{k} → {v} 次'),
        dict(type='map', var='freq_mi', h=270, fmt=lambda k, v: f'频率 {k} → 最小值 {v}'),
        dict(type='text', fn=lambda S: (f"目前最小的两个：`x = {S['x']}`，`y = {S['y']}`" if 'x' in S else ''), size=32),
    ],
    watch=['v', 'f', 'mi', 'x', 'y'],
    captions={
        'freq[v] = freq.get': '数 `{v}` 的频率 → `freq[{v}] = {freq[v]}`',
        'if f not in freq_mi': lambda S, B, r: (f'频率 {S.f} 还没有记录 → 直接记下 `{S.v}`' if S.f not in B.freq_mi
                                              else f'频率 {S.f} 已有最小值 `{B.freq_mi[S.f]}`，要和 `{S.v}` 比较'),
        'freq_mi[f] = v': '`freq_mi[{f}] = {v}`',
        'freq_mi[f] = min': '同频率只留最小的：`min({B.freq_mi[f]}, {v})` = {freq_mi[f]}',
        'x, y = -1, -1': '`x`、`y` 表示 `freq_mi` 里最小和次小的值，-1 代表还没有',
        'if x == -1 or x > mi': lambda S, B, r: (f'`x = {S.x}`，`mi = {S.mi}`：x 为空或更大 → `mi` 成为新的最小值，旧的 x 退为 y'
                                               if (S.x == -1 or S.x > S.mi)
                                               else f'`x = {S.x}` 更小，`mi = {S.mi}` 不能当最小，继续看能否当次小'),
        'x, y = mi, x': '最小值更新：`x = {x}`，原来的最小值 `{B.x}` 退成 `y = {y}`',
        'elif y == -1 or y > mi': lambda S, B, r: (f'`y = {S.y}`，`mi = {S.mi}`：y 为空或更大 → 更新次小值' if (S.y == -1 or S.y > S.mi)
                                                 else f'`y = {S.y}` 已经比 `mi = {S.mi}` 小，不更新'),
        'y = mi': '次小值更新：`y = {y}`',
        'if y == -1': lambda S, B, r: ('`y` 仍是 -1：频率种类不足两种 → 无解' if S.y == -1 else '`y` 有值：存在两种不同频率'),
        'return [x, y]': '最小的两个值 `[{x}, {y}]`',
        'return [-1, -1]': '返回 `[-1, -1]`',
    },
    cards=dict(
        one_liner='每种频率只留最小值，再取其中最小的两个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 里选两个值 `x < y`，它们的出现次数不同',
                 '`x` 尽量小，`x` 相同则 `y` 尽量小；没有返回 `[-1, -1]`',
                 '本视频：`[2,2,3,3,4,5,5,5]` → `[2,4]`'],
        quote='对每种频率都维护一个具有对应频率的最小值，然后取这些最小值中最小的两个作为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`freq` 统计每个数的频率',
              '第二趟：`freq_mi[f]` 记录频率 `f` 对应的最小值',
              '不同频率的最小值互不相同，取最小的两个就是 `[x, y]`；不足两个则无解'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '求最小两个值用 `x`、`y` 两个变量滚动维护，不用排序',
                 '原文代码在 Python 3 下可直接运行，未作改动',
                 '对比灵神：灵神直接拿全局最小值当 x；这里按频率分组再取最小两个'],
    ),
)
