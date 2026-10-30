CONFIG = dict(
    num=2540, title='最小公共值', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='类二路归并 · 双指针',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def getCommon(self, nums1, nums2):

        p1 = p2 = 0
        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] == nums2[p2]:
                return nums1[p1]
            elif nums1[p1] < nums2[p2]:
                p1 += 1
            else:
                p2 += 1
        
        return -1
''',
    call='Solution().getCommon([1,2,6,8,9], [3,4,6,10])',
    expect=6,
    views=[
        dict(type='array', var='nums1', pointers={'p1': 'blue'}, label='nums1', h=200),
        dict(type='array', var='nums2', pointers={'p2': 'pink'}, label='nums2', h=200),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink')],
    captions={
        'p1 = p2 = 0': '两个指针分别从两个数组的头部出发：`p1 = p2 = 0`',
        'while p1 <': lambda S, B, r: ('两个指针都没越界，继续' if S.p1 < len(S.nums1) and S.p2 < len(S.nums2) else '某个指针到了数组末尾 → 没有公共值'),
        '==': lambda S, B, r: (f'`{S.nums1[S.p1]}` == `{S.nums2[S.p2]}`：值相等，就是==最小公共值==' if S.nums1[S.p1] == S.nums2[S.p2] else f'`{S.nums1[S.p1]}` != `{S.nums2[S.p2]}`，继续比大小'),
        'elif nums1[p1] <': lambda S, B, r: (f'`{S.nums1[S.p1]} < {S.nums2[S.p2]}`：移动指向较小数的指针 `p1`' if S.nums1[S.p1] < S.nums2[S.p2] else f'`{S.nums1[S.p1]} > {S.nums2[S.p2]}`：移动指向较小数的指针 `p2`'),
        'p1 += 1': '`p1` → {p1}',
        'p2 += 1': '`p2` → {p2}',
        'return nums1[p1]': '公共值 =={ret}==',
        'return -1': '没有公共值 → `-1`',
    },
    cards=dict(
        one_liner='参考二路归并：每轮把指向较小数的指针后移',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个已排序数组，返回最小公共整数，没有返回 `-1`',
                 '示例：`[1,2,3,6]` 和 `[2,3,4,5]` → `2`',
                 '本视频：`[1,2,6,8,9]` 和 `[3,4,6,10]` → `6`'],
        quote='由于题目给出的两个数组都已经排好序了，那么在这里就可以参考二路归并的处理方法，使用两个指针分别从两个数组头部向后移动',
        quote_src='—— yiduobo 题解原文',
        idea=['每一轮把指向较小数的那个指针向后移动',
              '直到两个指针指向的值相等，或者某个指针走到末尾',
              '数组有序，所以较小的数在另一个数组里不会再出现'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '循环条件是两个指针都没越界，用 `and`',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '对比灵神：思路相同，yiduobo 直接用 `p1 / p2` 并称之为二路归并'],
    ),
)
