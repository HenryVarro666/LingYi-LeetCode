CONFIG = dict(
    num=2670, title='找出不同元素数目差数组', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='前后缀分解 · 哈希集合',
    tags=[],
    code='''
class Solution:
    def distinctDifferenceArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        suf = [0] * (n + 1)
        s = set()
        for i in range(n - 1, 0, -1):
            s.add(nums[i])
            suf[i] = len(s)

        s.clear()
        ans = [0] * n
        for i, x in enumerate(nums):
            s.add(x)
            ans[i] = len(s) - suf[i + 1]
        return ans
''',
    call='Solution().distinctDifferenceArray([3,2,3,4,2])',
    expect=[-2, -1, 0, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, cell=90, h=150),
        dict(type='set', var='s', label='s（当前前缀 / 后缀里的不同元素）', fmt=lambda x: str(x), h=110),
        dict(type='array', var='suf', label='suf（suf[i] = nums[i:] 的不同元素数）', pointers={'i': 'blue'}, cell=90, h=150),
        dict(type='array', var='ans', label='ans', pointers={'i': 'blue'}, cell=90, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('len(s)', 'len(s)', 'orange')],
    captions={
        'suf = [0] * (n + 1)': '`suf[i]` 记录后缀 `nums[i:]` 的不同元素个数；多开一位让 `suf[n] = 0`，不用特判',
        's.add(nums[i])': '倒序枚举：把 `nums[{i}] = {nums[i]}` 加入集合 `s`，重复的不会增加大小',
        'suf[i] = len(s)': '`suf[{i}] = len(s) = {suf[i]}`：后缀 `nums[{i}:]` 有 {suf[i]} 个不同元素',
        's.clear()': '后缀处理完，清空集合，改用它来统计前缀',
        's.add(x)': '正序枚举：把 `x = {x}` 加入集合，`s` 此时就是前缀 `nums[0..{i}]` 的不同元素',
        'ans[i] =': '前缀 `{len(s)}` 个 − 后缀 `suf[{i+1}] = {suf[i+1]}` 个 → `ans[{i}]` = =={ans[i]}==',
        'return ans': '全部算完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='倒着数一遍后缀，正着数一遍前缀，相减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`diff[i]` = 前缀 `nums[0..i]` 的不同元素数 − 后缀 `nums[i+1..]` 的不同元素数',
                 '返回整个 `diff` 数组',
                 '示例：`[3,2,3,4,2]` → `[-2,-1,0,2,3]`'],
        quote='先倒序枚举 nums，并记录每个后缀的不同元素个数到 suf 数组中，这可以用哈希表做到。然后正序枚举 nums[i]，同样地，记录每个前缀的不同元素个数，减去 suf[i+1]，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后缀的不同个数先预处理进 `suf`，一次倒序遍历搞定',
              '再正序遍历，集合大小就是前缀的不同个数',
              '`suf` 开 `n+1` 位，最后一个位置的后缀为空，恒为 0'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suf` 数组 + 集合）',
                 '倒序循环 `range(n-1, 0, -1)` 到 1 为止：`suf[0]` 用不到',
                 '前后缀分解：先预处理一侧，再边扫另一侧边算答案'],
    ),
)
