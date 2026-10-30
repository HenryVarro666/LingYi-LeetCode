NUMS = [-4, -3, -3, -1, 0, 0, 2, 5, 7]


def _color(S, i, v):
    if v < 0 and 'neg' in S:
        return 'red'
    if v > 0 and 'pos' in S:
        return 'green'
    return None


def _top(S):
    n = len(NUMS)
    if 'pos' in S:
        j = n - S['pos']
        return f"`bisect_right(nums, 0) = {j}`：第一个 `> 0` 的下标 → 正数有 `n − {j}` = =={S['pos']}== 个"
    if 'neg' in S:
        return f"`bisect_left(nums, 0) = {S['neg']}`：第一个 `≥ 0` 的下标 → 前面 =={S['neg']}== 个都是负数"
    return '有序数组：负数在左、0 在中间、正数在右 → ==二分出两条分界线=='


CONFIG = dict(
    num=2529, title='正整数和负整数的最大计数', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='二分查找 · 两条分界线',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def maximumCount(self, nums: List[int]) -> int:
        neg = bisect_left(nums, 0)
        pos = len(nums) - bisect_right(nums, 0)
        return max(neg, pos)
''',
    call=f'Solution().maximumCount({NUMS})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=27, h=90),
        dict(type='array', var='nums', label='nums（红 = 负数，绿 = 正数，0 两边都不算）', color=_color,
             pointers={'neg': 'red', 'len(nums) - pos': 'green'},
             pointer_labels={'neg': '第一个 ≥0', 'len(nums) - pos': '第一个 >0'}, cell=96, h=320),
    ],
    watch=[('neg', 'neg', 'red'), ('pos', 'pos', 'green'), ('n', 'len(nums)')],
    captions={
        'neg = bisect_left': '二分找第一个 `≥ 0` 的下标 `{neg}`：它==左边恰好 {neg} 个数==，全是负数',
        'pos = len': '二分找第一个 `> 0` 的下标 `{len(nums) - pos}`：从它到末尾 `{len(nums)} − {len(nums) - pos}` = =={pos}== 个正数',
        'return max': '`max(neg, pos) = max({neg}, {pos})` = =={ret}==',
    },
    cards=dict(
        one_liner='有序数组里，负数个数 = 第一个 ≥0 的下标，正数个数 = n − 第一个 >0 的下标',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`nums` 非递减有序，返回 ==正整数个数和负整数个数的较大值==；`0` 不算',
                 '示例：`[-2,-1,-1,1,2,3]` → `3`；`[-3,-2,-1,0,0,1,2]` → `3`',
                 '本视频：`[-4,-3,-3,-1,0,0,2,5,7]` → 负 4、正 3 → `4`'],
        quote='二分找到第一个 ≥0 的数的下标 i，那么下标在 [0,i−1] 中的数都小于 0，这恰好有 i 个。同样地，二分找到第一个 >0 的数的下标 j，……这有 ==n−j== 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`< x` 的元素个数 = `lowerBound(nums, x)`',
              '`> x` 的元素个数 = `n − lowerBound(nums, x+1)`，即 `n − bisect_right(nums, x)`',
              '取 `x = 0`，两次二分就分出负数段和正数段'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`bisect_left` 求 `≥ 0` 的第一个位置，`bisect_right` 求 `> 0` 的第一个位置，别搞反',
                 '中间的 0 两边都不算，所以 `neg + pos` 可能小于 `n`',
                 '方法一：直接遍历统计 `neg`、`pos`，`O(n)` 也能过'],
    ),
)
