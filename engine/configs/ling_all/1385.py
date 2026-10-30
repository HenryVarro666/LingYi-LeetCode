def _in(S, v):
    return 'x' in S and S['x'] - S['d'] <= v <= S['x'] + S['d']


def _c1(S, i, v):
    if 'x' in S and v == S['x']:
        return 'yellow'
    return None


def _c2(S, i, v):
    if 'x' not in S:
        return None
    if _in(S, v):
        return 'red'
    if v < S['x'] - S['d']:
        return None
    return 'green'


def _d2(S, i, v):
    return 'x' in S and v < S['x'] - S['d']


def _top(S):
    if 'x' not in S:
        return '对每个 `x`，问 arr2 里有没有数落在 ==闭区间 [x−d, x+d]== 里'
    x, d = S['x'], S['d']
    return f'`x = {x}`：危险区间 `[{x} − {d}, {x} + {d}]` = ==[{x - d}, {x + d}]=='


def _while(S, B, ret):
    j, a2, lo = S.j, S.arr2, S.x - S.d
    if j < len(a2) and a2[j] < lo:
        return f'`arr2[{j}] = {a2[j]} < x − d = {lo}`：它在区间左边，==对后面更大的 x 也没用== → 跳过'
    if j == len(a2):
        return f'`j = {j}`：arr2 已扫完'
    return f'`arr2[{j}] = {a2[j]} ≥ {lo}`：停下，`arr2[j]` 是 ==≥ x − d 的最小数=='


def _if(S, B, ret):
    j, a2, hi = S.j, S.arr2, S.x + S.d
    if j == len(a2):
        return f'没有 `≥ {S.x - S.d}` 的数 → 区间里没有 arr2 的数 → ==符合要求=='
    if a2[j] > hi:
        return f'`arr2[{j}] = {a2[j]} > x + d = {hi}`：最小的候选都在区间右边 → ==符合要求=='
    return f'`arr2[{j}] = {a2[j]} ≤ x + d = {hi}`：它落在区间里，`|{S.x} − {a2[j]}| ≤ {S.d}` → 不符合'


CONFIG = dict(
    num=1385, title='两个数组间的距离值', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 双指针',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1235'],
    code='''
class Solution:
    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        arr1.sort()
        arr2.sort()
        ans = j = 0
        for x in arr1:
            while j < len(arr2) and arr2[j] < x - d:
                j += 1
            if j == len(arr2) or arr2[j] > x + d:
                ans += 1
        return ans
''',
    call='Solution().findTheDistanceValue([8,4,13,5], [10,9,1,8,0], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=27, h=90),
        dict(type='array', var='arr1', label='arr1（黄 = 当前 x）', color=_c1, cell=96, h=210),
        dict(type='array', var='arr2', label='arr2（灰 = 已跳过 < x−d，红 = 落在区间里，绿 = 区间右边）',
             color=_c2, dim=_d2, pointers={'j': 'blue'}, cell=96, h=260),
    ],
    watch=[('x', 'x', 'yellow'), 'd', ('j', 'j', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'arr1.sort()': '`arr1` 排序：x 从小到大，区间 `[x−d, x+d]` 也==整体右移==',
        'arr2.sort()': '`arr2` 排序 → 可以用一个指针 `j` 单向往右扫',
        'ans = j = 0': '`ans = 0` 计数，`j = 0` 指向 arr2 开头',
        'for x in arr1': lambda S, B, r: ('arr1 遍历完毕' if 'x' in B and B.x == S.x
                                          else f'枚举 `x = {S.x}`，区间 `[{S.x - S.d}, {S.x + S.d}]`'),
        'while j < len': _while,
        'j += 1': '`j` → {j}',
        'if j == len': _if,
        'ans += 1': '`x = {x}` 符合距离要求，`ans` → =={ans}==',
        'return ans': '距离值 = =={ret}==',
    },
    cards=dict(
        one_liner='排序后区间 [x−d, x+d] 单调右移，指针 j 只往右走',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['对 `arr1` 中的元素 x，若 `arr2` 中==不存在== `|x − y| ≤ d` 的 y，就计数一次',
                 '返回计数（距离值）；示例：`[4,5,8], [10,9,1,8], d = 2` → `2`',
                 '本视频：`[8,4,13,5], [10,9,1,8,0], d = 2` → `3`（4、5、13）'],
        quote='遍历 arr1，设 x=arr1[i]，同时用另一个指针 j 维护==最小的满足 arr2[j] ≥ x−d 的数的下标==。如果发现 arr2[j] > x+d，那么 arr2 没有在 [x−d,x+d] 中的数，答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`|x − y| ≤ d` ⇔ y 在闭区间 `[x−d, x+d]` 里',
              '只需看 `≥ x−d` 的最小数：它不存在或 `> x+d` → 区间里没有数',
              '两数组都排序后，x 变大时 `x−d` 变大，`j` ==不用回头=='],
        summary=['时间瓶颈在排序 `O(n log n + m log m)`，双指针本身 `O(n + m)`',
                 '先判断 `j == len(arr2)` 再访问 `arr2[j]`，否则越界',
                 '`while` 用 `arr2[j] < x − d`（严格小于），等于 x−d 的数在区间里',
                 '方法一：只排序 arr2，对每个 x 做 `bisect_left(arr2, x − d)`'],
    ),
)
