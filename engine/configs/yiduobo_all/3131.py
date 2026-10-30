CONFIG = dict(
    num=3131, title='找出与数组相加的整数 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='有序对应 · 最小值之差', tags=[],
    code='''
class Solution(object):
    def addedInteger(self, nums1, nums2):

        return min(nums2) - min(nums1)
''',
    call='Solution().addedInteger([10, 4, 7, 4], [6, 0, 3, 0])',
    expect=-4,
    views=[
        dict(type='array', var='nums1', label='nums1', h=190, cell=100, color=lambda S, i, v: 'cyan' if v == min(S['nums1']) else None),
        dict(type='array', var='nums2', label='nums2', h=190, cell=100, color=lambda S, i, v: 'orange' if v == min(S['nums2']) else None),
        dict(type='text', h=80, size=34, fn=lambda S: f"`min(nums2) − min(nums1)` = `{min(S['nums2'])} − {min(S['nums1'])}` = =={min(S['nums2']) - min(S['nums1'])}=="),
        dict(type='text', h=70, fn=lambda S: f"排序后逐个对应：`{sorted(S['nums1'])}` → `{sorted(S['nums2'])}`，差都是 =={min(S['nums2']) - min(S['nums1'])}=="),
    ],
    watch=[],
    captions={
        'return min': '最小对最小：`x = min(nums2) − min(nums1)` = `{min(nums2)} − {min(nums1)}` = =={ret}==',
    },
    cards=dict(
        one_liner='加 x 不会打乱大小顺序：最小对最小，次小对次小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums1` 所有元素加上整数 `x`，要和 `nums2` 每种元素出现次数都相同', '求 `x`',
                 '本视频：`[10,4,7,4]` 与 `[6,0,3,0]` → `-4`'],
        quote='nums1中的最小值加上x后就应该变成nums2中的最小值，nums1中的次小值加上x后就应该变成nums2中的次小值，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个数组排序后必须一一对应，对应位的差都是 `x`', '所以最小值之差就是 `x`',
              '证明：若 `nums1[a] < nums1[b]` 却对到 `nums2[d] > nums2[c]`，所需的 x 会更大，顺序被打乱，矛盾'],
        after=[dict(heading='为什么顺序不能乱', lines=['设 `nums1[a] < nums1[b]`，`nums2[c] < nums2[d]`', '`nums2[c]-nums1[b] < nums2[d]-nums1[b] < nums2[d]-nums1[a]`', '小对小所需的 x 更小，说明变换时不能打乱顺序'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x` 可以为负，也可以为 0',
                 '证明靠的是不等式链：`nums2[c]-nums1[b] < nums2[d]-nums1[b] < nums2[d]-nums1[a]`',
                 '对比灵神：灵神从「最小值平移后仍是最小值」直接得出；yiduobo 补了排序对应的反证'],
    ),
)
