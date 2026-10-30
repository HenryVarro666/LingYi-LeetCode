CONFIG = dict(
    num=3852, title='不同频率的最小数对', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 最小值作 x',
    code='''
class Solution:
    def minDistinctFreqPair(self, nums: List[int]) -> List[int]:
        cnt = Counter(nums)
        mn = min(nums)

        cnt_min = cnt[mn]
        min_y = min((y for y, c in cnt.items() if c != cnt_min), default=None)

        if min_y is None:
            return [-1, -1]
        return [mn, min_y]
''',
    call='Solution().minDistinctFreqPair([2,2,3,3,4,5,5,5])',
    expect=[2, 4],
    views=[
        dict(type='array', var='nums', h=200, cell=80,
             color=lambda S, i, v: 'green' if 'mn' in S and v == S['mn'] else None),
        dict(type='map', var='cnt', h=330, fmt=lambda k, v: f'{k} → {v} 次'),
        dict(type='text', fn=lambda S: (f"`x = mn = {S['mn']}`，频率 `cnt_min = {S['cnt_min']}`" if 'cnt_min' in S else ''), size=32),
    ],
    watch=['mn', 'cnt_min', 'min_y'],
    captions={
        'cnt = Counter': '统计每个数的出现次数：`{dict(cnt)}`',
        'mn = min(nums)': '最小值 `mn = {mn}`：直接取它当 ==x==，另一个频率不同的数必然更大，`x < y` 自动成立',
        'cnt_min = cnt[mn]': 'x 的频率 `cnt_min = {cnt_min}`',
        'min_y = min': '在所有==频率不等于 {cnt_min}== 的数里取最小：`min_y = {min_y}`',
        'if min_y is None': lambda S, B, r: ('`min_y` 不是 None → 存在合法的 y' if S.min_y is not None
                                           else '`min_y` 是 None → 所有数频率都一样，无解'),
        'return [-1, -1]': '没有频率不同的数，返回 `[-1, -1]`',
        'return [mn, min_y]': '答案 `[x, y] = [{mn}, {min_y}]`',
    },
    cards=dict(
        one_liner='最小值直接当 x，再找频率不同的最小 y',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `nums` 里选两个不同的值 `x < y`，它们的出现次数不同',
                 '先让 `x` 尽量小，再让 `y` 尽量小；没有就返回 `[-1, -1]`',
                 '本视频：`[2,2,3,3,4,5,5,5]` → `[2,4]`'],
        quote='如果有两个出现次数不同的元素，那么直接把 min(nums) 作为 x，即可满足题目要求。由于 x 是最小值，另一个出现次数不同的数必然大于 x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['若所有数频率相同则无解；否则最小值 `mn` 一定能当 `x`',
              '理由：总有某个数和 `mn` 频率不同，它必然更大',
              '`y`：频率不等于 `cnt[mn]` 的最小元素，用生成器加 `min(..., default=None)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`min` 对空生成器会报错，所以要写 `default=None`',
                 '无解时 `min_y` 为 `None`，别忘了返回 `[-1, -1]`'],
    ),
)
