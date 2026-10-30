_NUMS = [7, 1, 3, 2, 1]


def _fstate(S):
    if 'f' not in S or S['_line'] < 12:
        return ''
    f = S['f']
    n = len(S['nums'])
    return f'`f[k]` = 前 k 个数最多能配几对，已算到 `f[{len(f) - 1}]` = =={f[-1]}==（共 {n} 个数，需要 `p = {S["p"]}` 对）'


def _head(S):
    if 'left' not in S:
        return ''
    if 'mid' in S and S.get('_line', 0) not in (8, 9, 10, 25, 26, 27):
        return f'答案范围 `[{S["left"]}, {S["right"]}]`，当前猜 `mid = {S["mid"]}`'
    return f'答案范围 `[{S["left"]}, {S["right"]}]`'


CONFIG = dict(
    num=2616, title='最小化数对的最大差值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 打家劫舍式 DP',
    tags=['难度分 2155'],
    code='''
class Solution(object):
    def minimizeMax(self, nums, p):

        nums.sort()
        left = 0
        right = nums[-1] - nums[0]
        while left < right:
            mid = (left + right) >> 1
            f = [0, 0]
            for index in range(1, len(nums)):
                f.append(f[-1])
                if nums[index] - nums[index - 1] <= mid:
                    f[-1] = max(f[-1], f[-3] + 1)

            if f[-1] >= p:
                right = mid
            else:
                left = mid + 1

        return left
''',
    call=f'Solution().minimizeMax({_NUMS}, 2)',
    expect=1,
    views=[
        dict(type='text', fn=_head, h=60),
        dict(type='array', var='nums', label='nums（排序后；蓝 = index，它和左邻居 index-1 尝试配对）', cell=84, h=210,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'cyan' if 'index' in S['_inner'] and i == S['_inner']['index'] - 1 else None),
        dict(type='array', var=lambda S: S['f'] if 'f' in S and S['_line'] >= 12 else None, label='f（f[k] = 前 k 个数的最多配对数）', cell=76, h=210),
        dict(type='text', fn=_fstate, h=60),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'index', ('p', 'p')],
    skip=['f = [0, 0]', 'for index in range', 'f.append(f[-1])'],
    captions={
        'nums.sort()': '先排序：数对==只选相邻的数==最划算 → `{nums}`',
        'left = 0': '二分下界 `left = 0`（差值最小可能是 0）',
        'right = nums[-1]': '二分上界 `right = {nums[-1]} − {nums[0]} = {right}`（最大差，任意配都行）',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`：答案还没锁定，继续' if B.left < B.right
                                               else f'`left = right = {B.left}`：范围缩成一个数，就是答案'),
        'mid = (left + right)': '猜最大差值 `mid = ({left} + {right}) >> 1 = {mid}`，下面用 DP 数能配几对',
        'if nums[index] - nums[index - 1] <= mid': lambda S, B, r: (
            f'`nums[{S.index}]` 先放弃，`f[{S.index + 1}] = {S.f[-1]}`；`{S.nums[S.index]} − {S.nums[S.index - 1]} = {S.nums[S.index] - S.nums[S.index - 1]} <= {S.mid}` → 可以配对，试试用它'
            if S.nums[S.index] - S.nums[S.index - 1] <= S.mid else
            f'`nums[{S.index}]` 先放弃，`f[{S.index + 1}] = {S.f[-1]}`；`{S.nums[S.index]} − {S.nums[S.index - 1]} = {S.nums[S.index] - S.nums[S.index - 1]} > {S.mid}` → 配不了，保持放弃'),
        'f[-1] = max(f[-1], f[-3] + 1)': '配对 `nums[{index - 1}], nums[{index}]`：`max(放弃, f[{index - 1}] + 1)` → `f[{index + 1}] = {f[-1]}`',
        'if f[-1] >= p': lambda S, B, r: (f'`f[-1] = {S.f[-1]} >= p = {S.p}` → 能配够 `p` 对，`mid` 可行' if S.f[-1] >= S.p
                                          else f'`f[-1] = {S.f[-1]} < p = {S.p}` → 配不够，`mid` 太小'),
        'right = mid': '可行 → 答案不大于 mid：`right = {right}`',
        'left = mid + 1': '不可行 → 答案一定更大：`left = {left}`',
        'return left': '`left == right`，答案 =={left}==',
    },
    max_steps=130,
    cards=dict(
        one_liner='差值上限越大越好配，二分它；判定用打家劫舍式 DP',
        complexity='时间 `O(n log U)`（外加排序 `O(n log n)`），空间 `O(n)`',
        problem=['数组 `nums` 里选 `p` 对下标，每个下标最多用一次',
                 '要让这 `p` 对的最大差值尽量小，求这个最小值',
                 '本视频：`[7,1,3,2,1]`，`p = 2` → `1`'],
        quote='数对间的最大差值越大，就越容易构造出足够的数对，也就是说在这里可以使用二分答案来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，最小的数要么放弃，要么和==次小值==配对（成功率最高，大数留给后面）',
              '这和打家劫舍一样：`f[i+1] = max(f[i], f[i-1] + 1)`，后一项要求差值 `<= mid`',
              '`f[n] >= p` 说明 mid 可行，收上界；否则抬下界'],
        summary=['时间 `O(n log U)`，U 为最大差；空间 `O(n)`',
                 '`f` 初始 `[0, 0]`，`f[-3]` 对应 f[index-1]（跳过配对的两个数）',
                 '闭区间写法：可行 `right = mid`，不可行 `left = mid + 1`',
                 '原文为 Python 2 风格，代码未改',
                 '对比灵神：灵神用贪心 `i += 2` 一遍扫描，不需要 DP 数组'],
    ),
)
