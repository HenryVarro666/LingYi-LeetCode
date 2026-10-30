CONFIG = dict(
    num=3191, title='使二进制数组全部等于 1 的最少操作次数 I', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='从左到右贪心 · 遇 0 必翻',
    tags=['贪心与思维', '难度分 1312'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        ans = 0
        for i in range(len(nums) - 2):
            if nums[i] == 0:  # 必须操作
                nums[i + 1] ^= 1
                nums[i + 2] ^= 1
                ans += 1
        return ans if nums[-2] and nums[-1] else -1
''',
    call='Solution().minOperations([0,1,1,1,0,0])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 当前长度 3 的操作窗口；绿 = 已经定下来的 1）', cell=96, h=330,
             pointers={'i': 'blue'},
             window=('i', 'i + 2'),
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] and v == 1 else None),
        dict(type='text', fn=lambda S: (f"下标 `{S['i']}` 左边都已是 1；`nums[{S['i']}] = {S['nums'][S['i']]}`" if 'i' in S and S['_line'] in (5, 6, 7, 8) else ''), size=30),
    ],
    watch=[('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'for i in range': '从左到右处理下标 `i`，到 `n-3` 为止：最后两个数没有完整的 3 连窗口',
        'if nums[i] == 0': lambda S, B, r: (f'`nums[{B.i}] = 0`：以后再也没有操作能改到它 → ==必须操作== 下标 {B.i}'
                                            if B.nums[B.i] == 0 else f'`nums[{B.i}] = 1`：已经是 1，==不能操作==（操作会把它翻成 0）'),
        'nums[i + 1] ^= 1': '操作 `i` 要翻 `i, i+1, i+2`；`nums[i]` 本该变 1，但之后不再访问，代码省略。翻转第 2 个数：`nums[{i+1}]` → `{nums[i+1]}`',
        'nums[i + 2] ^= 1': '翻转第 3 个数：`nums[{i+2}]` → `{nums[i+2]}`，窗口翻完，`nums[{i}]` 按 1 算',
        'ans += 1': '操作次数 +1：每个下标至多操作一次，所以 `ans = {ans}` 就是最少',
        'return ans': lambda S, B, r: (f'最后两个数 `{B.nums[-2]}, {B.nums[-1]}` 都是 1 → 返回 `ans = {r}`' if r != -1
                                       else '最后两个数不全是 1 → 无法做到，返回 `-1`'),
    },
    cards=dict(
        one_liner='从左到右，遇到 0 就必须翻，操作方式唯一',
        complexity='时间 `O(nk)`（`k=3`），空间 `O(1)`',
        problem=['`nums` 是 0/1 数组，一次操作可翻转==连续 3 个==元素',
                 '求全部变成 `1` 的最少操作次数，做不到返回 `-1`',
                 '示例：`[0,1,1,1,0,0]` → `3`'],
        quote='遇到 1 一定不能操作，遇到 0 一定要操作，所以==从左到右的操作方式有且仅有一种==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作顺序不影响结果，所以可以重排成从左到右',
              '同一个 `i` 操作两次等于没操作，至多一次',
              '于是遇 0 必翻、遇 1 不翻，直接模拟，剩下最后两个数检查是否为 1'],
        summary=['时间 `O(n)`，空间 `O(1)`（直接改了 `nums`）',
                 '易错：循环只到 `len(nums)-3`，最后两个数要单独检查',
                 '思考题：把 3 换成 `k`，可用差分把复杂度降到与 `k` 无关（CF1955E）'],
    ),
)
