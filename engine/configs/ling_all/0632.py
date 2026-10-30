COLS = ['blue', 'pink', 'green']


def _ridx(S):
    return S['pairs'].index((S['r'], S['i']))


CONFIG = dict(
    num=632, title='最小区间', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序合并 + 滑动窗口（empty 计数）',
    tags=['滑动窗口与双指针', '常用数据结构'],
    code='''
class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        pairs = sorted((x, i) for (i, arr) in enumerate(nums) for x in arr)
        ans_l, ans_r = -inf, inf
        empty = len(nums)
        cnt = [0] * empty
        left = 0
        for r, i in pairs:
            if cnt[i] == 0:  # 窗口包含 nums[i] 中的数
                empty -= 1
            cnt[i] += 1
            while empty == 0:  # 每个列表都至少有一个数在窗口中
                l, j = pairs[left]
                if r - l < ans_r - ans_l:
                    ans_l, ans_r = l, r
                cnt[j] -= 1
                if cnt[j] == 0:  # 窗口不包含 nums[j] 中的数
                    empty += 1
                left += 1
        return [ans_l, ans_r]
''',
    call='Solution().smallestRange([[4,10,15],[0,9,12],[5,18]])',
    expect=[0, 5],
    views=[
        dict(type='array', var=lambda S: [x for x, _ in S['pairs']], label='pairs 的元素值（颜色 = 所属列表，框 = 窗口）', cell=96, h=190,
             window=('left', _ridx),
             color=lambda S, i, v: COLS[S['pairs'][i][1]],
             dim=lambda S, i, v: 'r' in S and not (S['left'] <= i <= _ridx(S))) ,
        dict(type='array', var=lambda S: [j for _, j in S['pairs']], label='所属列表编号', cell=96, h=170,
             color=lambda S, i, v: COLS[v], index=False),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"窗口 `[{S['pairs'][S['left']][0]}, {S['r']}]`，还缺 ==`{S['empty']}`== 个列表；当前最小区间 ==`[{S['ans_l']}, {S['ans_r']}]`==" if 'r' in S and 'empty' in S else '')),
    ],
    watch=[('left', 'left', 'cyan'), ('r', 'r', 'pink'), ('i', 'i', 'yellow'), ('empty', 'empty', 'purple'), ('cnt', 'cnt', 'blue'), ('ans_l', 'ans_l', 'green'), ('ans_r', 'ans_r', 'green')],
    captions={
        'pairs = sorted': '把所有元素连同所属列表编号一起排序：`(值, 编号)`。合法区间就是它的一个连续子数组，要求 0..k-1 的编号都出现',
        'ans_l, ans_r = -inf': '答案区间先设成「无穷大」，遇到更短的合法窗口才替换',
        'left = 0': '`left = 0`：窗口左端',
        'empty = len': '`empty` = 窗口里还没出现的列表个数，初始 k = {empty}；`empty == 0` 就是合法',
        'cnt = [0]': '`cnt[j]` = 窗口中来自列表 j 的元素个数',
        'for r, i in pairs': '枚举窗口右端：值 `r = {r}`，来自列表 `{i}`',
        'if cnt[i] == 0': lambda S, B, rr: (f'`cnt[{S.i}] = 0`：列表 {S.i} 第一次出现在窗口里，还缺的列表少一个' if S.cnt[S.i] == 0 else f'`cnt[{S.i}] = {S.cnt[S.i]}`：窗口里已有列表 {S.i} 的数，缺口不变'),
        'empty -= 1': '`empty` → {empty}',
        'cnt[i] += 1': '`cnt` = {cnt}',
        'while empty == 0': lambda S, B, rr: ('`empty == 0`：每个列表都有数在窗口里 → 合法，试着收缩左端' if S.empty == 0 else f'`empty = {S.empty}`：还缺列表，继续右扩'),
        'l, j = pairs': '窗口左端 `l = {l}`（来自列表 {j}）；当前窗口 `[{l}, {r}]`',
        'if r - l <': lambda S, B, rr: (f'长度 `{S.r - S.l}` < 当前最短 `{S.ans_r - S.ans_l}`：更短，更新答案' if S.r - S.l < S.ans_r - S.ans_l else f'长度 `{S.r - S.l}` 不比 `{S.ans_r - S.ans_l}` 短：不更新（相等时保留靠左的）'),
        'ans_l, ans_r = l': '答案更新为 `[{ans_l}, {ans_r}]`',
        'cnt[j] -= 1': '左端元素 `{l}` 离开窗口：`cnt[{j}] = {cnt[j]}`',
        'if cnt[j] == 0': lambda S, B, rr: (f'`cnt[{S.j}] = 0`：窗口里没有列表 {S.j} 的数了，不再合法，`empty` 加一' if S.cnt[S.j] == 0 else f'列表 {S.j} 在窗口里还有数，仍然合法，继续收缩'),
        'left += 1': '`left` → {left}',
        'return [': '最小区间 `{ret}`',
    },
    cards=dict(
        one_liner='所有数带上列表编号排好序，找包含所有编号的最短窗口',
        complexity='时间 `O(L log L)`，空间 `O(L)`（L 为元素总数）',
        problem=['`k` 个非递减列表，找最小区间，使每个列表至少有一个数落在其中',
                 '比较：区间更短者小，一样短则左端点更小',
                 '示例：`[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]` → `[20,24]`',
                 '本视频：`[[4,10,15],[0,9,12],[5,18]]`'],
        quote='合法区间等价于 pairs 的一个连续子数组，满足列表编号 0,1,2,…,k-1 都在这个子数组中。',
        quote_src='—— 灵茶山艾府题解方法二',
        idea=['把全部元素合并排序成 `(值, 所属列表)` 的数组',
              '子数组越长越容易包含所有编号 → 单调性，用滑动窗口',
              '`empty` 记还没出现的列表数，免得每次检查 k 个计数'],
        summary=['时间 `O(L log L)`，瓶颈在排序；归并 k 路可降到 `O(L log k)`',
                 '`empty` 的更新：`cnt` 0→1 时减，1→0 时加',
                 '合法时 ==先更新答案再缩左端==，要缩到不合法为止',
                 '灵神方法一：最小堆维护每个列表的当前元素，堆顶是左端点，`r` 是它们的最大值'],
    ),
)
