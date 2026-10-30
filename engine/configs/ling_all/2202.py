def _ok(S, i):
    k = S['k']
    return i < k - 1 or i == k


def _text(S):
    k, nums = S['k'], S['nums']
    if S.get('_line') == 3:
        return f'`n = {len(nums)}`，`k = {k}`：先看「单元素且 k 奇数」这个特例'
    idx = [i for i in range(len(nums)) if _ok(S, i)]
    vals = [nums[i] for i in idx]
    return f'`i < {k - 1}` 或 `i = {k}` → 下标 {idx} → 值 {vals} → 最大 =={max(vals)}=='


def _col(S, i, v):
    if 'k' not in S or S.get('_line') == 3:
        return None
    if _ok(S, i):
        vals = [S['nums'][j] for j in range(len(S['nums'])) if _ok(S, j)]
        return 'yellow' if v == max(vals) else 'green'
    return None


CONFIG = dict(
    num=2202, title='K 次操作后最大化顶端元素', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 哪些下标能当栈顶',
    tags=['灵神题单', '难度分 1717'],
    code='''
class Solution:
    def maximumTop(self, nums: List[int], k: int) -> int:
        if k % 2 and len(nums) == 1:
            return -1
        return max(num for i, num in enumerate(nums)
                       if i < k - 1 or i == k)
''',
    call='Solution().maximumTop([5,2,2,4,0,6], 4)',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var='nums', h=260, color=_col,
             dim=lambda S, i, v: 'k' in S and S.get('_line') != 3 and not _ok(S, i)),
    ],
    watch=['k', ('n', 'len(nums)')],
    captions={
        'if k % 2 and len': lambda S, B, r: ('`n = 1` 且 `k` 是奇数：只能删、放、删…最后栈空 → 返回 -1' if (S.k % 2 and len(S.nums) == 1)
                                              else f'`k % 2 = {S.k % 2}`，`len(nums) = {len(S.nums)}`：不是「单元素且 k 奇数」，往下走'),
        'return -1': '栈最后一定为空 → `-1`',
        'return max(': '生成器逐个枚举下标：只有 ==i < k-1 或 i == k== 的才有资格当栈顶（绿色），其中最大的是黄色 → 返回 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='为什么是这几个下标', lines=[
            '`i < k-1`：先删 `i` 个，再「删-放」凑够步数，最后一步把它放回',
            '`i = k-1`：第 `k` 步（最后一步）只能把它删掉 → ==不行==',
            '`i = k`：连删 `k` 个，它自然露出来 → ==可以==',
            '`i > k`：它上面的数删不完 → ==不行==',
            '示例 `k=4`：下标 0、1、2、4 可选，3 和 5 不行']),
              dict(heading='特判：n = 1', lines=[
            '只有一个数：栈非空就只能删，栈空就只能放回',
            '`k` 奇数 → 最后栈空 → `-1`；`k` 偶数 → 回到 `nums[0]`',
            '代码里 `k % 2 and len(nums) == 1` 就是这一句'])],
        one_liner='k 次操作后，下标 i < k-1 或 i = k 的数都能当栈顶',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是一个栈，`nums[0]` 是栈顶；每次操作==弹出栈顶==，或把弹出过的数==放回栈顶==',
                 '恰好做 `k` 次操作，求栈顶的最大值；栈一定为空则返回 `-1`',
                 '示例：`nums=[5,2,2,4,0,6], k=4` → `5`'],
        quote='可以让 i<k-1 或 i=k 的数组元素作为 k 次操作后的栈顶。这些元素的最大值即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先特判：`n=1` 且 `k` 为奇数，最后栈空 → `-1`',
              '从特殊到一般：`i=0` 可以反复删除-放回；前 `k-1` 个数都能这样做到',
              '`i=k-1` 最后一步必须删它，`i>k` 前面删不完；`i=k` 删前 k 个即可'],
        summary=['时间 `O(n)`，空间 `O(1)`（生成器不建列表）',
                 '`k=0` 时 `i<k-1` 与 `i==k` 只选中 `nums[0]`，正好是不操作的答案',
                 '易错：`i=k-1` 不能选；`n=1` 要单独处理 k 奇数的情况'],
    ),
)
