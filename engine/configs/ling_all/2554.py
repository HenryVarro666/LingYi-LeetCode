CONFIG = dict(
    num=2554, title='从一个范围内选择最多整数 I', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贪心 · 哈希表 + 从小到大',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1333'],
    code='''
class Solution:
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:
        ans, s = 0, set(banned)
        for i in range(1, n + 1):
            if i > maxSum: break
            if i not in s:
                maxSum -= i
                ans += 1
        return ans
''',
    call='Solution().maxCount([1,6,5,3], 9, 13)',
    expect=3,
    views=[
        dict(type='set', var='s', label='banned 集合 s', fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"选 `{S['i']}` 之后，还剩额度 `maxSum = {S['maxSum']}`，已选 `{S['ans']}` 个" if 'i' in S and 'ans' in S else ''), size=26),
    ],
    watch=['n', ('i', 'i', 'blue'), ('maxSum', 'maxSum', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans, s = 0': '`ans` 计数；`banned` 转成集合 `s`，判断是否禁用只要 `O(1)`：`{s}`',
        'for i in range': '从小到大枚举 `i = {i}`：==越小的数越省额度==',
        'if i > maxSum': lambda S, B, r: (f'`{S.i} > {S.maxSum}`：连这个数都买不起，更大的更不行 → break' if S.i > S.maxSum
                                          else f'`{S.i} > {S.maxSum}` 不成立：额度够买 `{S.i}`'),
        'if i not in s': lambda S, B, r: (f'`{S.i}` 不在 `s` 里，可以选' if S.i not in S.s else f'`{S.i}` 在 `s` 里，被禁用，跳过'),
        'maxSum -= i': '花掉 `{i}`：`maxSum` {B.maxSum} → =={maxSum}==',
        'ans += 1': '又选了一个，`ans` = =={ans}==',
        'return ans': '最多能选 `{ans}` 个整数',
    },
    cards=dict(
        one_liner='贪心：从小到大选，选不起就停',
        complexity='时间 `O(m+n)`，空间 `O(m)`',
        problem=['从 `[1, n]` 选整数，每个至多一次，不能在 `banned` 里，总和不超过 `maxSum`',
                 '求最多能选几个',
                 '示例：`banned=[1,6,5], n=5, maxSum=6` → `2`；本视频：`[1,6,5,3], 9, 13` → `3`（2+4+7）'],
        quote='贪心，优先选小的。为了快速判断一个数是否在数组 banned 中，可以将其转换成哈希表。',
        quote_src='—— 灵茶山艾府题解',
        idea=['个数最多 → 每个数尽量小 → 从 1 往上枚举',
              '`banned` 转集合，判断是否禁用 `O(1)`',
              '`i > maxSum` 时更大的数也买不起，直接 break'],
        summary=['时间 `O(m+n)`，空间 `O(m)`',
                 '易错：不能直接用 `banned` 列表判断，会退化成 `O(mn)`',
                 '思考题：`n`、`maxSum` 到 `10^18` 时，改用等差数列求和 + 二分',
                 '灵神在 `i > maxSum` 时提前 break，省掉后面的枚举'],
    ),
)
