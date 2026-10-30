def _color(S, i, v):
    if 'mode' not in S:
        return None
    if v == S['mode']:
        return 'green'
    return None


def _txt(S):
    if 'freq1' not in S or 'i' not in S:
        return '先找支配元素 `mode`，再枚举分割点，左右两边都要过半'
    i, n, f1, t = S['i'], len(S['nums']), S['freq1'], S['total']
    return (f'左 `[0..{i}]`：`{f1}×2` vs `{i + 1}`　｜　右 `[{i + 1}..{n - 1}]`：`{t - f1}×2` vs `{n - i - 1}`')


CONFIG = dict(
    num=2780, title='合法分割的最小下标', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 枚举分割点',
    tags=['动态规划', '数学算法', '难度分 1550'],
    code='''
class Solution:
    def minimumIndex(self, nums: List[int]) -> int:
        mode, total = Counter(nums).most_common(1)[0]
        freq1 = 0
        for i, x in enumerate(nums):
            freq1 += x == mode
            if freq1 * 2 > i + 1 and (total - freq1) * 2 > len(nums) - i - 1:
                return i
        return -1
''',
    call='Solution().minimumIndex([2,1,3,1,1,1,7,1,2,1])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'i': 'yellow'}, window=(lambda S: 0, 'i'), color=_color, h=300,
             label='nums（绿 = 支配元素 mode，黄框 = 左半 nums[0..i]）'),
    ],
    watch=[('mode', 'mode', 'green'), ('total', 'total', 'purple'), ('freq1', 'freq1', 'blue'), 'i'],
    captions={
        'Counter(nums)': '支配元素 `mode` = =={mode}==，总共出现 `total` = =={total}== 次（超过一半）',
        'freq1 = 0': '`freq1` = 左半里 `mode` 的个数；右半的个数 = `total − freq1`',
        'for i, x in enumerate': '枚举分割点：左半 `nums[0..{i}]`，共 {i+1} 个数',
        'freq1 += x == mode': '`x = {x}`{"，是 mode" if x == mode else "，不是 mode"} → `freq1` = =={freq1}==',
        'if freq1 * 2': lambda S, B, r: (
            f'左：`{S.freq1}×2 = {S.freq1 * 2}` {">" if S.freq1 * 2 > S.i + 1 else "≤"} `{S.i + 1}`；'
            f'右：`{S.total - S.freq1}×2 = {(S.total - S.freq1) * 2}` {">" if (S.total - S.freq1) * 2 > len(S.nums) - S.i - 1 else "≤"} `{len(S.nums) - S.i - 1}`'
            + ('　==两边都过半==' if S.freq1 * 2 > S.i + 1 and (S.total - S.freq1) * 2 > len(S.nums) - S.i - 1
               else '　至少一边没过半，继续')),
        'return i': '两边的支配元素都是 `mode` → 最小合法分割下标 =={i}==',
        'return -1': '枚举完都没有合法分割 → `-1`',
    },
    cards=dict(
        one_liner='两半的支配元素必须就是原数组的支配元素',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['支配元素：出现次数超过数组长度一半的数',
                 '在下标 `i` 把 `nums` 切成两段，两段的支配元素都等于原数组的才合法',
                 '返回最小的合法 `i`，没有就 `-1`；示例：`[2,1,3,1,1,1,7,1,2,1]` → `4`'],
        quote='分割出的两个数组的支配元素就是原数组的支配元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两段都过半 `freq` 相加就超过 `n/2`，所以支配元素只可能是原来的 `mode`',
              '先求出 `mode` 和 `total`，不用再找别的候选',
              '枚举 `i` 时累计左半个数，右半个数 = `total − freq1`，两边都 `×2 >` 长度即合法'],
        summary=['时间 `O(n)`，空间 `O(n)`（Counter）；用摩尔投票法可降到 `O(1)`',
                 '易错：左半长度是 `i + 1`，右半长度是 `n − i − 1`',
                 '判断用 `freq×2 > 长度`，避免除法和奇偶讨论',
                 '前后缀分解：右半的统计 = 总量 − 左半'],
    ),
)
