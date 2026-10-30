def _pairs(S):
    a, b = S['nums1'], S['nums2']
    if S['_line'] < 6:
        return '两数组一个升序、一个降序，大的配小的'
    return '`' + ' + '.join(f'{x}×{y}' for x, y in zip(a, b)) + '` = ==' + str(sum(x * y for x, y in zip(a, b))) + '=='


CONFIG = dict(
    num=1874, title='两个数组的最小乘积和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一升一降 · 反向匹配',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minProductSum(self, nums1, nums2):

        nums1.sort()
        nums2.sort(reverse=True)

        return sum([nums1[index] * nums2[index] for index in range(len(nums1))])
''',
    call='Solution().minProductSum([5,3,4,2], [4,2,2,5])',
    expect=40,
    views=[
        dict(type='array', var='nums1', label='nums1', h=210, cell=100),
        dict(type='array', var='nums2', label='nums2', h=210, cell=100),
        dict(type='text', size=34, fn=_pairs),
    ],
    watch=['nums1', 'nums2'],
    captions={
        'nums1.sort()': '`nums1` ==升序==排序：小的在前 → {nums1}',
        'nums2.sort(reverse': '`nums2` ==降序==排序：大的在前 → {nums2}；这样同下标就是「小配大」',
        'return sum': '同下标相乘再累加：每一对都是小×大，总和最小 → =={ret}==',
    },
    cards=dict(
        before=[dict(heading='先看两个数', lines=['`a ≤ b`，`c ≤ d`，比较 `a·c + b·d` 与 `a·d + b·c`', '令 `b = a + m`，`d = c + n`（`m, n ≥ 0`）'])],
        one_liner='把大数和小数配对：一个数组升序、另一个降序',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序栈）',
        problem=['两个长度相同的数组，可以任意重排 `nums1`', '乘积和 = `Σ nums1[i] × nums2[i]`，求最小值', '示例：`[5,3,4,2]`、`[4,2,2,5]` → `40`'],
        quote='很明显，a * c + b * d >= a * d + b * c。为了使得最终结果最小，那么就应该让两个数组中的数按大小反向匹配，于是只需将nums1正序排序，nums2逆序排序，然后一趟遍历计算乘积后累加即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['任取两对：`a·c + b·d = 2ac + an + cm + mn`', '交叉配对：`a·d + b·c = 2ac + an + cm`，==少了 mn==', '所以交叉（小配大）总是不吃亏：整体一升一降'],
        after=[dict(heading='示例配对', lines=['`nums1` 升序：`[2, 3, 4, 5]`', '`nums2` 降序：`[5, 4, 2, 2]`', '`2×5 + 3×4 + 4×2 + 5×2` = ==40=='])],
        summary=['时间 `O(n log n)`，空间 `O(1)`', '`sort()` 会原地修改两个输入数组',
                 '同类：排序不等式，==同序和最大，反序和最小==', '原文只有这一种写法，没有改动'],
    ),
)
