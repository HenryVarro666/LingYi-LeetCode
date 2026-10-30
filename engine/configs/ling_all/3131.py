CONFIG = dict(
    num=3131, title='找出与数组相加的整数 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='最小值对最小值', tags=[],
    code='''
class Solution:
    def addedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        return min(nums2) - min(nums1)
''',
    call='Solution().addedInteger([2, 6, 4], [9, 7, 5])',
    expect=3,
    views=[
        dict(type='array', var='nums1', label='nums1', h=190, cell=100, color=lambda S, i, v: 'cyan' if v == min(S['nums1']) else None),
        dict(type='array', var='nums2', label='nums2', h=190, cell=100, color=lambda S, i, v: 'orange' if v == min(S['nums2']) else None),
        dict(type='text', h=80, size=34, fn=lambda S: f"`min(nums2) − min(nums1)` = `{min(S['nums2'])} − {min(S['nums1'])}` = =={min(S['nums2']) - min(S['nums1'])}=="),
        dict(type='text', h=70, fn=lambda S: f"验证：`nums1` 每个数加 {min(S['nums2']) - min(S['nums1'])} → `{[v + min(S['nums2']) - min(S['nums1']) for v in S['nums1']]}`，排序后和 `nums2` 一致"),
    ],
    watch=[],
    captions={
        'return min': '最小的数加上 x 后还是最小的：`min(nums1) + x = min(nums2)` → `x = {min(nums2)} − {min(nums1)}` = =={ret}==',
    },
    cards=dict(
        one_liner='每个数都加 x，最小值也加 x：两个最小值相减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums1` 每个元素都加上同一个整数 `x`', '加完后与 `nums2` 包含相同的整数且频次相同', '求 `x`',
                 '示例：`[2,6,4]` 与 `[9,7,5]` → `3`'],
        quote='考虑数组中的最小元素，有 min(nums1) + x = min(nums2)，即 x = min(nums2) - min(nums1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['整体平移 x，顺序不变，最小值还是最小值', '所以只看最小值就能解出 x，不用排序也不用匹配',
              '`min(nums2) - min(nums1)` 一行搞定'],
        after=[dict(heading='再看一个例子', lines=['`nums1 = [10]`，`nums2 = [5]`', '`x = 5 - 10 = -5`：x 为负数，就是元素减小', '`nums1 = [1,1,1,1]` 与 `nums2 = [1,1,1,1]` → `x = 0`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x` 可能是负数（如 `[10]` → `[5]` 得 `-5`），别漏掉符号',
                 '题目保证 `x` 存在，所以无需再验证',
                 '同样的思路：整体平移不改变相对顺序，取最小（或最大）值即可'],
    ),
)
