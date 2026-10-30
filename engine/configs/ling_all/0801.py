A = [0, 3, 5, 8, 9]
B = [2, 1, 4, 6, 9]


def _i(S):
    if 'a2' not in S:
        return None
    for i in range(1, len(A)):
        if A[i] == S['a2'] and B[i] == S['b2']:
            return i
    return None


def _col(S, j, v):
    i = _i(S)
    if i is None:
        return None
    return 'blue' if j == i else 'cyan' if j == i - 1 else None


def _txt(S):
    if 'not_swap' not in S:
        return '`not_swap` / `swap`：前 i 对严格递增，且第 i 对不交换 / 交换 的最小次数'
    return f"`not_swap = {S['not_swap']}`，`swap = {S['swap']}`"


def _c1(S, B_, r):
    ok = S.a1 < S.a2 and S.b1 < S.b2
    return (f'`{S.a1} < {S.a2}` 且 `{S.b1} < {S.b2}`：==同样的做法==可以接上（都不换或都换）' if ok
            else f'`{S.a1} < {S.a2}` 且 `{S.b1} < {S.b2}` 不成立：这一对==不能按同样的做法==接')


def _c2(S, B_, r):
    ok = S.b1 < S.a2 and S.a1 < S.b2
    return (f'`{S.b1} < {S.a2}` 且 `{S.a1} < {S.b2}`：==相反的做法==可以接上（一换一不换）' if ok
            else f'`{S.b1} < {S.a2}` 且 `{S.a1} < {S.b2}` 不成立：不能一换一不换')


CONFIG = dict(
    num=801, title='使序列递增的最小交换次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 交换 / 不交换',
    tags=['灵神题单', '动态规划', '难度分 2066'],
    code='''
class Solution:
    def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        not_swap, swap = 0, 1
        for (a1, b1), (a2, b2) in pairwise(zip(nums1, nums2)):  # 3.10 from itertools import pairwise
            ns = s = inf
            if a1 < a2 and b1 < b2:
                ns, s = not_swap, swap + 1
            if b1 < a2 and a1 < b2:
                ns, s = min(ns, swap), min(s, not_swap + 1)
            not_swap, swap = ns, s
        return min(not_swap, swap)
''',
    call=f'Solution().minSwap({A}, {B})',
    expect=1,
    views=[
        dict(type='array', var='nums1', label='nums1（蓝 = 当前对，青 = 上一对）', cell=96, h=170, color=_col),
        dict(type='array', var='nums2', label='nums2', cell=96, h=170, color=_col),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('a1,b1', '(a1, b1)', 'cyan'), ('a2,b2', '(a2, b2)', 'blue'), ('not_swap', 'not_swap', 'green'), ('swap', 'swap', 'orange')],
    captions={
        'not_swap, swap = 0, 1': '第 0 对：不交换要 0 次，交换要 1 次',
        'for (a1, b1)': '看相邻两对：上一对 `({a1}, {b1})`，当前对 `({a2}, {b2})`',
        'ns = s = inf': '先假设两种状态都做不到（`inf`），下面的分类讨论再更新',
        'if a1 < a2 and b1 < b2': _c1,
        'ns, s = not_swap, swap + 1': '上一对不换 → 这一对也不换：`ns = {ns}`；上一对换了 → 这一对也得换：`s = swap + 1 = {s}`',
        'if b1 < a2 and a1 < b2': _c2,
        'ns, s = min(ns, swap)': '上一对换了、这一对不换：`ns = min(.., swap)` → {ns}；上一对不换、这一对换：`s = min(.., not_swap + 1)` → {s}',
        'not_swap, swap = ns, s': '更新：`not_swap = {not_swap}`，`swap = {swap}`',
        'return min': '最后一对两种状态取小：`min({not_swap}, {swap})` = =={ret}==',
    },
    cards=dict(
        one_liner='只看相邻两对：当前这对交换 / 不交换，两个状态滚动',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个等长数组，每次可交换 `nums1[i]` 与 `nums2[i]`',
                 '求让两个数组都==严格递增==的最少交换次数',
                 f'本视频：`nums1 = {A}`，`nums2 = {B}` → `1`'],
        quote='把严格递增换一种方式表述：对所有 i (i>0)，有 nums1[i-1] < nums1[i] 且 nums2[i-1] < nums2[i]。从这一表述可以发现，我们只需要考虑相邻元素间的大小关系。',
        quote_src='—— 灵茶山艾府题解（提示 1）',
        idea=['需要额外一个维度：这一对==交换了没有==，它会影响下一对',
              '`a1<a2` 且 `b1<b2`：同样的做法（都不换 / 都换）；`b1<a2` 且 `a1<b2`：相反的做法',
              '两种情况可以同时成立，这时对每个状态取较小值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先写二维 `f[i][0/1]`，再因为只依赖上一对，压缩成两个变量',
                 '易错：交换状态要加 1；两个 `if` 不是 `elif`，可能都成立',
                 '题目保证有解，所以最后 `min` 不会是 `inf`',
                 '主页另有二维 `f` 数组写法，本视频选滚动变量版'],
    ),
)
