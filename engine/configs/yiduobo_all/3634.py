NUMS = [1, 6, 2, 9, 4, 12]
K = 3


def _top(S):
    if 'index' not in S:
        return '最小值越大，能容纳的最大值 `v × k` 也越大 → ==右边界单调后移=='
    i, p, a = S['index'], S['p'], S['nums']
    return f"左边界 `{i}`（最小值 `{a[i]}`），允许的最大值 `{a[i]} × {K} = {a[i] * K}`，窗口 `[{i}, {p})` 长 `{p - i}`"


def _right(S):
    return S['p'] - 1 if 'p' in S else None


def _color(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    if S['index'] < i < S['p']:
        return 'green'
    return None


def _while(S, B, ret):
    p, a, n = S.p, S.nums, len(S.nums)
    if p >= n:
        return f'`p = {p}` 已到末尾，右边界不能再扩'
    if a[p] <= S.v * S.k:
        return f'`nums[{p}] = {a[p]} ≤ {S.v} × {S.k} = {S.v * S.k}`：还能放进窗口 → p 后移'
    return f'`nums[{p}] = {a[p]} > {S.v * S.k}`：放不下了，右边界停在 `p = {p}`'


CONFIG = dict(
    num=3634, title='使数组平衡的最少移除数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 枚举左边界的变长窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1453'],
    code='''
class Solution(object):
    def minRemoval(self, nums, k):

        nums.sort()
        p = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] <= v * k:
                p += 1

            res = max(res, p - index)

        return len(nums) - res
''',
    call=f'Solution().minRemoval({NUMS}, {K})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='array', var='nums', label='nums（排序后；蓝 = 左边界 index，绿 = 窗口内，p = 第一个放不下的位置）',
             pointers={'index': 'blue', 'p': 'pink'}, window=('index', _right), color=_color, cell=120, h=320),
    ],
    watch=[('index', 'index', 'blue'), 'v', ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先从小到大排序：`{nums}`，平衡数组就是==一段连续区间==',
        'p = 0': '`p`：当前左边界对应的==最靠后的右边界==（开区间）',
        'res = 0': '`res`：最长平衡数组的长度',
        'for index, v in': lambda S, B, r: ('枚举完毕' if 'index' in B and B.index == S.index
                                            else f'枚举左边界 `index = {S.index}`，最小值 `v = {S.v}`'),
        'while p < len': _while,
        'p += 1': '`p` → {p}',
        'res = max': '窗口 `nums[{index}:{p}]` 都是平衡的：`res = max({B.res}, {p - index})` = =={res}==',
        'return len': '最长平衡数组长 `{res}` → 移除 `{len(nums)} − {res}` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举最小值，最大可容纳的右边界只会往后走',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums` 移除若干元素，使剩余 ==最大值 ≤ 最小值 × k==',
                 '求最少移除几个（不能删空）',
                 '示例：`[2,1,5], k = 2` → `1`；本视频 `[1,6,2,9,4,12], k = 3` → `2`'],
        quote='一个平衡数组中元素的最小值越大，那么其中可以包含的最大值也越大……如果将nums先从小到大进行排序，就可以通过==变长滑动窗口==来求解这个问题了。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后一趟遍历==枚举左边界==（最小值 `v`）',
              '`p` 记录最靠后的右边界：`nums[p] ≤ v × k` 就后移',
              '左边界后移时 `v` 变大，`p` 不必回退'],
        summary=['时间 `O(n log n)`，`p` 总共只移动 n 次',
                 '`p` 是开区间右端：窗口长度是 `p − index`，不用 +1',
                 '`p < len(nums)` 要先判断，防止越界',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动',
                 '对比灵神：灵神枚举最大值收缩左端；这里枚举最小值扩张右端'],
    ),
)
