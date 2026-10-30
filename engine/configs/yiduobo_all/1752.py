def _top(S):
    if 'p' not in S:
        return ''
    n = len(S['nums'])
    if S['_line'] <= 8:
        return f"第一段：`p = {S['p']}`，一路找非递减的最后一个位置"
    return f"第二段：从 `p = {S['p']}` 往后检查：非递减，且都 `<= nums[0] = {S['nums'][0]}`"


CONFIG = dict(
    num=1752, title='检查数组是否经排序和轮转得到', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='找断点 p，再检查后半段',
    code='''
class Solution(object):
    def check(self, nums):

        n = len(nums)
        p = 0
        while p < n - 1 and nums[p] <= nums[p + 1]:
            p += 1
        
        if p == n - 1:
            return True
        
        p += 1
        while p < n - 1 and nums[p] <= nums[p + 1] and nums[p] <= nums[0]:
            p += 1
        
        if p == n - 1 and nums[p] <= nums[0]:
            return True

        return False
''',
    call='Solution().check([3,4,5,1,2])',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（绿 = 第一段，橙 = 第二段）', cell=90, pointers={'p': 'pink'},
             color=lambda S, i, v: (None if 'p' not in S else
                                    ('green' if i <= S['p'] else None) if S['_line'] <= 8 else
                                    ('orange' if i >= S['p'] else None))),
    ],
    watch=[('p', 'p', 'pink'), 'n', ('nums[0]', 'nums[0]', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'p = 0': '`p` 从 0 出发，找第一个满足 `nums[p] > nums[p+1]` 的断点',
        'while p < n - 1 and nums[p] <= nums[p + 1]:': lambda S, B, r: (
            f'`nums[{S.p}] = {S.nums[S.p]} <= nums[{S.p+1}] = {S.nums[S.p+1]}` → 还是非递减，继续往右' if S.p < S.n - 1 and S.nums[S.p] <= S.nums[S.p + 1]
            else ('走到末尾了，没有断点' if S.p >= S.n - 1 else f'`nums[{S.p}] = {S.nums[S.p]} > nums[{S.p+1}] = {S.nums[S.p+1]}` → ==找到断点 p=={S.p}')),
        9: lambda S, B, r: ('`p == n - 1`：没有断点，数组本身非递减 → 直接 True' if S.p == S.n - 1
                                          else f'`p = {S.p} != n - 1`：存在断点，要检查后半段'),
        'return True': '返回 `True`',
        7: '`p` → {p}，继续往右',
        12: '`p` 跳到断点后的第一个数 `nums[{p}] = {nums[p]}`，后半段从这里开始',
        14: '`p` → {p}，继续检查后半段',
        'while p < n - 1 and nums[p] <= nums[p + 1] and': lambda S, B, r: (
            f'`nums[{S.p}] = {S.nums[S.p]}`：后面不递减，且 `<= nums[0] = {S.nums[0]}` → 继续' if S.p < S.n - 1 and S.nums[S.p] <= S.nums[S.p + 1] and S.nums[S.p] <= S.nums[0]
            else '后半段检查结束（走到末尾或违反条件）'),
        16: lambda S, B, r: (
            f'走到末尾 `p = {S.p}`，且 `nums[{S.p}] = {S.nums[S.p]} <= nums[0] = {S.nums[0]}` → 满足三个条件' if S.p == S.n - 1 and S.nums[S.p] <= S.nums[0]
            else '没走到末尾或最后一个数超过 `nums[0]` → 不满足'),
        'return False': '后半段不满足条件 → 返回 `False`',
    },
    cards=dict(
        one_liner='找到唯一的断点，后半段必须非递减且都不超过 nums[0]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是否由一个非递减数组轮转得到（可含重复）',
                 '示例：`[3,4,5,1,2]` → `true`；`[2,1,3,4]` → `false`',
                 '本视频：`[3,4,5,1,2]` → `true`'],
        quote='数组中存在且仅存在一个位置p，满足nums[p] > nums[p + 1]；从nums[p + 1]到nums[n - 1]中的每个数都必须小于等于nums[0]。',
        quote_src='—— yiduobo 题解原文',
        idea=['没轮转过：整个数组非递减，第一个循环直接走到末尾 → `True`',
              '轮转过：第一个循环停在断点 `p`，前半段 `0..p` 已经非递减',
              '第二个循环检查 `p+1..n-1` 也非递减，并且每个数 `<= nums[0]`（和前半段接得上）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第二个循环结束后还要单独判断最后一个数 `nums[p] <= nums[0]`',
                 '原文为 Python 2 风格，类名 `Solution(object)` 在 Python 3 中同样可用，代码未改',
                 '对比灵神：灵神数「严格递减」的次数，yiduobo 分成前后两段分别验证'],
    ),
)
