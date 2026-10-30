CONFIG = dict(
    num=3046, title='分割数组', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数',
    tags=[],
    code='''
class Solution:
    def isPossibleToSplit(self, nums: List[int]) -> bool:
        return max(Counter(nums).values()) <= 2
''',
    call='''Solution().isPossibleToSplit([1,1,2,2,3,4])
Solution().isPossibleToSplit([1,1,1,1])''',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: '两个示例依次运行：`[1,1,2,2,3,4]` → True；`[1,1,1,1]` → False', size=26),
        dict(type='array', var='nums', label='nums', cell=96,
             color=lambda S, k, v: 'yellow' if (S.get('nums') and S['nums'].count(v) > 2) else None),
        dict(type='map', var=lambda S: dict(Counter(S['nums'])), label='每个数的出现次数', h=260),
    ],
    watch=[('max 出现次数', 'max(Counter(nums).values())', 'green')],
    captions={
        'return max': lambda S, B, ret: (f"统计出现次数 `{dict(Counter(S.nums))}`，最大是 `{max(Counter(S.nums).values())}` ≤ 2 → ==每个数最多分给两个数组各一个，可以分割=="
                                         if ret else f"最大出现次数 `{max(Counter(S.nums).values())}` > 2 → 至少有两个相同的数落到同一个数组，==不能分割=="),
    },
    cards=dict(
        one_liner='只看最大出现次数：不超过 2 就能分，超过就不能',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把长度为偶数的 `nums` 平分成 `nums1`、`nums2`',
                 '两个数组内部都要==元素互不相同==',
                 '示例：`[1,1,2,2,3,4]` → `true`；`[1,1,1,1]` → `false`'],
        quote='根据题意，如果 nums[i] 的出现次数超过 2，则无法分割，否则可以分割。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个数出现 3 次，两个数组里必有一个装了两份 → 不行',
              '每个数至多 2 次：出现 2 次的一边一个，出现 1 次的随便放',
              '所以一行代码：`max(Counter(nums).values()) <= 2`'],
        result='`[1,1,2,2,3,4]` 最大次数 2 → True；`[1,1,1,1]` 出现 4 次 → False ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：是「超过 2 次」不行，恰好 2 次可以',
                 '写法二：`all(c <= 2 for c in Counter(nums).values())`，作用相同',
                 '长度偶数保证了单次数填平衡后两边一样长'],
    ),
)
