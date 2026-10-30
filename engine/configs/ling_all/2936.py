CONFIG = dict(
    num=2936, title='包含相等值数字块的数量', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='跳到下一块的起点 · 二分', tags=['贪心与思维'],
    setup='''
class BigArray:
    def __init__(self, a):
        self.a = a
    def size(self):
        return len(self.a)
    def at(self, i):
        return self.a[i]
''',
    code='''
class Solution(object):
    def countBlocks(self, nums: Optional['BigArray']) -> int:
        ans, i, n = 0, 0, nums.size()
        while i < n:
            cur = nums.at(i)
            i += bisect_left(range(i, n), True, key=lambda j: nums.at(j) != cur)
            ans += 1
        return ans
''',
    call='Solution().countBlocks(BigArray([1,1,2,2,2,2,3,3,3,3]))',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前块的值 `cur = {S['cur']}`，块从下标 ==`{S['i']}`== 开始，二分找第一个 `!= {S['cur']}` 的位置" if 'cur' in S and S['i'] < S['n'] else '')),
        dict(type='array', var=lambda S: S['nums'].a, label='nums（只能 at(i) 访问）', pointers={'i': 'blue'}, h=300,
             color=lambda S, k, v: ('blue' if 'cur' in S and v == S['cur'] and k >= S['i'] else None),
             dim=lambda S, k, v: 'i' in S and k < S['i']),
    ],
    watch=[('i', 'i', 'blue'), 'n', 'cur', ('ans', 'ans', 'green')],
    captions={
        'ans, i, n': '`ans` 数块数；`i` 是当前块的起点；`n = nums.size() = {n}`（只能用 `at` 取值）',
        'while i < n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还有没数过的块' if S.i < S.n else f'`i = {S.i} = n`：整个数组数完'),
        'cur = nums.at': '这一块的值 `cur = nums.at({i}) = {cur}`',
        'i += bisect_left': '在 `[i, n)` 上二分：找第一个 `nums[j] != {cur}` 的 j。数组有序，前面全是假、后面全是真。`i` 从 {B.i} 跳到 =={i}==，一次跳过整块',
        'ans += 1': '又数完一块，`ans = {ans}`',
        'return ans': '循环次数就是块数：`{ans}`',
    },
    cards=dict(
        one_liner='每次二分跳到下一块的起点，跳几次就有几块',
        complexity='时间 `O(√S · log S)`，空间 `O(1)`',
        problem=['有序数组 `nums` 只能通过 `size()` 和 `at(i)` 访问（模拟超大数组）',
                 '数组里相等的数连成一块，数一共有多少块',
                 '本视频：`[1,1,2,2,2,2,3,3,3,3]` → `3`'],
        quote='从 i=0 开始循环，每次找后面不等于 nums[i] 的数的最小下标，作为下一轮循环的 i。循环直到 i=n 时停止。循环次数即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['块的值 `cur` 等于 `nums[i]`；块内全是 `cur`，块后第一个数 `!= cur`',
              '数组有序 → `nums[j] != cur` 对 j 单调（先假后真），可以对 j 二分',
              '用 `bisect_left` 配 `key` 一行搞定；二分结果加到 `i` 上就是下一块起点'],
        summary=['时间 `O(√S log S)`：S 为元素和，块数最多约 √S 个，每次二分 `O(log S)`',
                 '空间 `O(1)`',
                 '`bisect_left(range(i, n), True, key=...)` 需要 Python 3.10+，返回的是相对 `i` 的偏移',
                 '数组本身不给直接访问，所以不能线性扫描；本视频用 `BigArray` 类模拟 `size/at`',
                 '对比 yiduobo：他二分的是块的最后一个位置，再 +1'],
    ),
)
