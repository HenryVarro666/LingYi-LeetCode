CONFIG = dict(
    num=3105, title='最长的严格递增或递减子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='两趟扫描 · 分别找递增、递减',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def longestMonotonicSubarray(self, nums):

        res = 0
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] > nums[q - 1]:
                q += 1
            res = max(res, q - p)
            p = q
        
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] < nums[q - 1]:
                q += 1
            res = max(res, q - p)
            p = q
        
        return res
''',
    call='Solution().longestMonotonicSubarray([1,4,3,2,2,5,6,7,8])',
    expect=5,
    views=[
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink'}, window=('p', 'q - 1'), h=300,
             label='nums（蓝 = p 段起点，粉 = q，框 = 当前段 p..q-1）'),
        dict(type='text', fn=lambda S: f"当前段 `[{S['p']}, {S['q'] - 1}]`，长度 `q − p = {S['q'] - S['p']}`" if 'q' in S and S['q'] > S['p'] else ''),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记最长长度',
        'p = 0': '`p` 回到 0，从头开始扫',
        'while p < len': lambda S, B, r: (f'`p = {S.p}`，还没扫完 → 处理以 p 开头的一段' if S.p < len(S.nums) else f'`p = {S.p}` 已到数组末尾 → 这一趟结束'),
        'q = p + 1': '`q` 从 `p + 1` 起向后找这一段的末尾',
        'while q < len(nums) and nums[q] >': lambda S, B, r: (
            f'`nums[{S.q}] = {S.nums[S.q]} > nums[{S.q-1}] = {S.nums[S.q-1]}` → 仍然递增，继续'
            if S.q < len(S.nums) and S.nums[S.q] > S.nums[S.q-1] else '到末尾或不再递增 → 这一段结束'),
        'while q < len(nums) and nums[q] <': lambda S, B, r: (
            f'`nums[{S.q}] = {S.nums[S.q]} < nums[{S.q-1}] = {S.nums[S.q-1]}` → 仍然递减，继续'
            if S.q < len(S.nums) and S.nums[S.q] < S.nums[S.q-1] else '到末尾或不再递减 → 这一段结束'),
        'q += 1': '`q` → {q}',
        'res = max': '这一段长 `{q} - {p} = {q-p}`；`res = max({B.res}, {q-p}) = {res}`',
        'p = q': '==下一段从 q 开始==（`q` 处不满足延长条件，它是新段的起点）：`p` → {p}',
        'return res': '递增、递减两趟取最大，答案 `{res}`',
    },
    cards=dict(
        one_liner='递增扫一趟，递减再扫一趟，取最长',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求最长的严格递增或严格递减子数组的长度',
                 '单个元素也算（长度 1）',
                 '示例：`[1,4,3,3,2]` → `2`；`[3,2,1]` → `3`'],
        quote='先使用两个指针进行一趟遍历，找出nums中所有的递增子数组，接下来再使用两个指针进行一趟遍历，找出nums中所有的递减子数组，最后取其中最长的长度作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：`p` 为段头，`q` 向右扩到不再严格递增，`p = q`',
              '第二趟：同样的写法，条件换成严格递减',
              '两趟里的最大段长就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`（两趟，各 `O(n)`）',
                 '`q` 从 `p + 1` 开始，所以每一段至少长 1，全相等数组答案为 1',
                 '`p = q` 不用回退：同一方向的段不会重叠',
                 '原文是 Python 3 也能运行的写法，未做修改',
                 '对比灵神：灵神一趟遍历，用 `inc` 定基调并回退一格；yiduobo 分两趟，不用处理重叠'],
    ),
)
