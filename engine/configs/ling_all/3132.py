def _shift(S):
    if 'x' not in S or 'i' not in S:
        return ''
    sh = [v + S['x'] for v in S['nums1'][S['i']:]]
    return f"保留 `nums1[{S['i']}]`，`x = {S['x']}`：`nums1[{S['i']}:] + x` = =={sh}==，要在里面找子序列 `{S['nums2']}`"


def _hit(S, B, ret):
    v, x, j = S.v, S.x, S.j
    if S.nums2[j] == v + x:
        return f'`v + x = {v + x}` == `nums2[{j}]` → ==匹配上==，下面 `j` 加 1'
    return f'`v + x = {v + x}` ≠ `nums2[{j}] = {S.nums2[j]}` → 这个数不匹配，当作被移除'


CONFIG = dict(
    num=3132, title='找出与数组相加的整数 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举最小保留元素 + 判断子序列',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1620'],
    code='''
class Solution:
    def minimumAddedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        nums1.sort()
        nums2.sort()
        # 枚举保留 nums1[2] 或者 nums1[1] 或者 nums1[0]
        # 倒着枚举是因为 nums1[i] 越大答案越小，第一个满足的就是答案
        for i in range(2, 0, -1):
            x = nums2[0] - nums1[i]
            # 在 {nums1[i] + x} 中找子序列 nums2
            j = 0
            for v in nums1[i:]:
                if nums2[j] == v + x:
                    j += 1
                    # nums2 是 {nums1[i] + x} 的子序列
                    if j == len(nums2):
                        return x
        # 题目保证答案一定存在
        return nums2[0] - nums1[0]
''',
    call='Solution().minimumAddedInteger([2,5,6,7,8,10], [3,4,5,8])',
    expect=-2,
    views=[
        dict(type='array', var='nums1', label='nums1（已排序）', pointers={'i': 'blue'}, h=250,
             dim=lambda S, i, v: 'i' in S and i < S['i'],
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None),
        dict(type='array', var='nums2', label='nums2（已排序）', pointers={'j': 'pink'}, h=250,
             color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None),
        dict(type='text', fn=_shift, size=26, h=110),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('j', 'j', 'pink'), 'v'],
    captions={
        'nums1.sort()': '先排序：这样 `nums1` 最小的几个数就在最前面',
        'nums2.sort()': '`nums2` 也排序；整体加 `x` 不改变相对顺序，才能用子序列判断',
        'for i in range': '只删两个数 → 前三小里==至少保留一个==；最小保留元素只可能是下标 2、1、0。`i = {i}`',
        'x = nums2[0]': '保留 `nums1[{i}] = {nums1[i]}` 当最小，它对应 `nums2[0] = {nums2[0]}` → `x = {nums2[0]} − {nums1[i]}` = =={x}==',
        'j = 0': '`j` 指向 `nums2` 里下一个要匹配的数，从 0 开始',
        'for v in nums1[i:]': '扫描 `nums1[{i}:]`，当前 `v = {v}`，加上 `x` 后是 `{v + x}`',
        'if nums2[j] == v + x': _hit,
        'j += 1': '匹配成功，`j` → {j}',
        'if j == len(nums2)': lambda S, B, r: (f'`j = {S.j} == len(nums2)`：`nums2` 全部匹配 → ==x = {S.x} 可行==' if S.j == len(S.nums2)
                                                else f'`j = {S.j} < {len(S.nums2)}`，还没匹配完，继续扫'),
        'return x': '`i` 越大 `x` 越小，倒着枚举，第一个可行的就是最小答案：返回 ==`{x}`==',
        'return nums2[0] - nums1[0]': '前两个 `i` 都不行，题目保证有解 → 一定是保留 `nums1[0]`，无需再判断',
    },
    cards=dict(
        one_liner='前三小必留一个：枚举保留谁，再判断子序列',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums1` 删掉 2 个数，其余数都加上同一个整数 `x`，要和 `nums2` 相等（元素与频次相同）',
                 '返回最小的 `x`，保证有解',
                 '示例：`[4,20,16,12,8]`、`[14,18,10]` → `-2`；视频用 `[2,5,6,7,8,10]`、`[3,4,5,8]`'],
        quote='由于只能移除两个元素，所以 nums1 的前三小元素必定有一个是保留下来的，我们可以枚举保留下来的最小元素是 nums1[0] 还是 nums1[1] 还是 nums1[2]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['保留的最小元素确定后，`x = nums2[0] − nums1[i]` 也就确定了',
              '把 `nums1` 每个数加 `x`，问题变成：==nums2 是否为它的子序列==（同向双指针，同 392 题）',
              '`nums1[i]` 越大 `x` 越小 → 从 2 倒着枚举，第一个满足的就是答案'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '保留的最小元素不可能是 `nums1[3]` 及更大：那要删掉前三个，超过 2 个',
                 '`i = 0` 不必判断：题目保证有解，前两个都不行就是它',
                 '写法二：`all(v - x in it for v in nums2)`，用迭代器消耗来判断子序列',
                 '先排序再判断，因为整体加 `x` 不改变顺序'],
    ),
)
