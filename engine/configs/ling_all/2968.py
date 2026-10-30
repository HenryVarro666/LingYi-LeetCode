def _mid(S):
    if 'left' not in S or 'right' not in S or S['left'] > S['right']:
        return None
    return (S['left'] + S['right']) // 2


def _txt(S, B):
    if 'right' not in S:
        return '排序后，要变成同一个数的元素必在连续子数组里'
    nums, l, r = S['nums'], S['left'], S['right']
    if l > r:
        return ''
    m = nums[(l + r) // 2]
    return f"窗口 `[{l}, {r}]` 全变成中位数 `{m}`：操作次数 `s = {S['s']}`，`k = {S['k']}`，窗口长 =={r - l + 1}=="


CONFIG = dict(
    num=2968, title='执行操作使频率分数最大', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 · 滑窗 · 中位数贡献法',
    tags=['常用数据结构', '难度分 2444'],
    code='''
class Solution:
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = left = s = 0  # s 是窗口元素与窗口中位数的差之和
        for right, x in enumerate(nums):
            s += x - nums[(left + right) // 2]
            while s > k:
                s += nums[left] - nums[(left + right + 1) // 2]
                left += 1
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().maxFrequencyScore([1,2,6,4,9,5], 4)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（排序后；框 = 窗口，黄 = 窗口中位数）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), cell=96, h=250,
             color=lambda S, i, v: 'yellow' if 'right' in S and S['left'] <= S['right'] and i == (S['left'] + S['right']) // 2 else None,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'orange'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    skip=['ans = left = s = 0'],
    captions={
        'nums.sort()': '排序：变成同一个数的元素，必然是排序后的一段连续子数组',
        'for right, x': lambda S, B, r: ('右端点枚举完毕' if ('right' in B and B.right == S.right) else f'枚举窗口右端点 `right = {S.right}`，新元素 `x = {S.x}` 要加入窗口'),
        's += x - nums[(left + right) // 2]': 'x 移入：操作次数增加 `x - mid1 = {x} - {nums[(left + right) // 2]}`，`s` = {s}',
        'while s > k': '`s = {s}` 与 `k = {k}`：{"超过预算，缩小窗口" if s > k else "没超预算，窗口合法"}',
        's += nums[left]': '`nums[left]` 移出：操作次数增加 `nums[left] - mid2 = {B.nums[B.left]} - {B.nums[(B.left + B.right + 1) // 2]}` → `s = {s}`',
        'left += 1': '`left` 右移到 {left}',
        'ans = max': '窗口长 `{right - left + 1}`：`ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最大频率分数 `{ans}`',
    },
    cards=dict(
        one_liner='排序后滑窗，窗口内全变成中位数，增量 O(1) 维护操作次数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次可把某个数 `+1` 或 `-1`，至多 `k` 次',
                 '求操作后众数出现次数的最大值',
                 '示例：`[1,2,6,4], k = 3` → `3`；本视频：`[1,2,6,4,9,5], k = 4` → `3`'],
        quote='把 a 的所有元素变为 a 的==中位数==是最优的。',
        quote_src='—— 灵茶山艾府题解（中位数贪心）',
        idea=['排序后，要变成一样的数必在连续子数组里，滑动窗口枚举右端点',
              '窗口内变成中位数最省，`s` 就是窗口各元素到中位数的距离和',
              '新元素移入，`s` 增加 `x - mid1`；左端移出，增加 `nums[left] - mid2`，不用前缀和'],
        summary=['时间 `O(n log n)`，排序是瓶颈；空间 `O(1)`',
                 '中位数用 `(left + right) // 2`，移出时用 `(left + right + 1) // 2`（第二个中位数）',
                 '另一种写法：前缀和 `O(1)` 算距离和，空间 `O(n)`',
                 '同类题：462、2033、2448、2607、1703'],
    ),
)
