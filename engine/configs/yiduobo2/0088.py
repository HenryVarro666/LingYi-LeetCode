def _branch(S, B, ret):
    m, n = B.m, B.n
    if m == 0:
        return '`m == 0`：nums1 的数用完了 → 只能填 nums2 的'
    return f'`m = {m}`，nums1 还有数'


def _branch_n(S, B, ret):
    if B.n == 0:
        return '`n == 0`：nums2 的数用完了 → 填 nums1 剩下的（其实就是原地不动）'
    return f'`n = {B.n}`，nums2 也还有数 → 比较两个末尾'


def _cmp(S, B, ret):
    a, b = B.nums1[B.m - 1], B.nums2[B.n - 1]
    if a <= b:
        return f'`nums1[{B.m - 1}] = {a} <= nums2[{B.n - 1}] = {b}`：nums2 的末尾更大（或相等）'
    return f'`nums1[{B.m - 1}] = {a} > nums2[{B.n - 1}] = {b}`：nums1 的末尾更大'


def _now_color(S, i, v):
    if 'now' not in S:
        return None
    if i > S['now'] or (S.get('_line') in (6, 7, 9, 10, 13, 14, 16, 17) and i == S['now']):
        return 'green'
    return None


CONFIG = dict(
    num=88, title='合并两个有序数组', difficulty='Easy', category='双指针',
    author='yiduobo', technique='从后往前 · 每次放较大的数',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def merge(self, nums1, m, nums2, n):
        now = m + n - 1
        while now >= 0:
            if m == 0:
                nums1[now] = nums2[n - 1]
                n -= 1
            elif n == 0:
                nums1[now] = nums1[m - 1]
                m -= 1
            else:
                if nums1[m - 1] <= nums2[n - 1]:
                    nums1[now] = nums2[n - 1]
                    n -= 1
                else:
                    nums1[now] = nums1[m - 1]
                    m -= 1
            now -= 1
''',
    call='''nums1 = [1, 2, 3, 0, 0, 0]
Solution().merge(nums1, 3, [2, 5, 6], 3)
nums1''',
    expect=[1, 2, 2, 3, 5, 6],
    views=[
        dict(type='text', fn=lambda S: (f"nums1 还剩前 `m = {S['m']}` 个，nums2 还剩前 `n = {S['n']}` 个；"
                                        f"`now = m + n − 1`" if 'now' in S else ''), h=60),
        dict(type='array', var='nums1', label='nums1（绿 = 已放好的位置）', cell=88,
             pointers={'m - 1': 'blue', 'now': 'yellow'}, color=_now_color,
             dim=lambda S, i, v: 'now' in S and S['m'] - 1 < i <= S['now'] and not _now_color(S, i, v), h=230),
        dict(type='array', var='nums2', label='nums2（暗 = 已放进 nums1）', cell=88,
             pointers={'n - 1': 'pink'}, dim=lambda S, i, v: 'n' in S and i >= S['n'], h=200),
    ],
    watch=[('m', 'm', 'blue'), ('n', 'n', 'pink'), ('now', 'now', 'yellow')],
    captions={
        'now = m + n - 1': '从后往前填：第一个要填的位置 `now = m + n - 1 = {now}`',
        'while now >= 0': lambda S, B, r: (f'`now = {B.now} >= 0`，继续填' if B.now >= 0 else '`now = -1`：所有位置都填好了'),
        'if m == 0': _branch,
        'elif n == 0': _branch_n,
        'if nums1[m - 1] <= nums2[n - 1]': _cmp,
        6: 'nums1 没数了：直接搬 nums2 的末尾 `nums1[{now}] = {nums1[now]}`',
        9: 'nums2 没数了：`nums1[{now}] = nums1[{m - 1}]`，==自己赋值给自己==',
        13: '较大的是 nums2 的末尾：`nums1[{now}] = {nums1[now]}`',
        16: '较大的是 nums1 的末尾：`nums1[{now}] = {nums1[now]}`',
        'n -= 1': 'nums2 用掉一个：`n` → {n}',
        'm -= 1': 'nums1 用掉一个：`m` → {m}',
        'now -= 1': '`now` → {now}',
    },
    cards=dict(
        one_liner='nums1 后面有空位：从后往前，每次把两个末尾里较大的放到 now',
        complexity='时间 `O(m + n)`，空间 `O(1)`',
        problem=['`nums1`、`nums2` 按==非递减==排列，分别有 `m`、`n` 个元素',
                 'nums1 长度为 `m + n`（后 n 个是 0），把 nums2 ==原地==合并进 nums1',
                 '示例：`nums1 = [1,2,3,0,0,0], m = 3`',
                 '`nums2 = [2,5,6], n = 3` → `[1,2,2,3,5,6]`'],
        quote='由于题目保证了nums1中空间充足，那么我们可以==从后往前==，每次将……==较大的数==加入到nums1的now = m + n - 1这个位置上，同时更新m、n以及now即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接把 `m`、`n` 当成「还剩几个」用，末尾就是 `m - 1`、`n - 1`',
              '较大的数一定排在最后 → 放到 `now`，对应的计数减一',
              '某一边用完了（`m == 0` 或 `n == 0`），就只从另一边拿'],
        summary=['时间 `O(m + n)`，空间 `O(1)`',
                 '`while now >= 0`：每个位置都写一遍；`n == 0` 后其实是 nums1 自己赋值给自己',
                 '对比灵神：灵神循环到 `p2 < 0` 就停，nums1 剩下的数不用动',
                 '易错：先判 `m == 0` / `n == 0`，否则 `nums1[m - 1]` 会取到 `nums1[-1]`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
