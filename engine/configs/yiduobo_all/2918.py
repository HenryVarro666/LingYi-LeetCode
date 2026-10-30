CONFIG = dict(
    num=2918, title='数组的最小相等和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计零的个数 + 比较两和', tags=['灵神题单', '贪心与思维', '难度分 1526'],
    code='''
class Solution(object):
    def minSum(self, nums1, nums2):

        s1 = s2 = 0
        x = y = 0
        for v in nums1:
            s1 += v
            if v == 0:
                x += 1
        
        for v in nums2:
            s2 += v
            if v == 0:
                y += 1
        
        s1 += x
        s2 += y

        if s1 == s2:
            return s1
        elif s1 > s2:
            if y > 0:
                return s1
            else:
                return -1
        elif x > 0:
            return s2
        else:
            return -1
''',
    call='Solution().minSum([3, 2, 0, 1, 0], [6, 5, 0])',
    expect=12,
    views=[
        dict(type='array', var='nums1', label='nums1', h=200, color=lambda S, i, v: 'orange' if v == 0 else None),
        dict(type='array', var='nums2', label='nums2', h=200, color=lambda S, i, v: 'orange' if v == 0 else None),
        dict(type='text', fn=lambda S: f"nums1：和 `s1={S['s1']}`，0 的个数 `x={S['x']}`；nums2：和 `s2={S['s2']}`，0 的个数 `y={S['y']}`"),
    ],
    watch=[('s1', 's1', 'blue'), ('x', 'x', 'orange'), ('s2', 's2', 'pink'), ('y', 'y', 'orange')],
    captions={
        'if v == 0': '`v={v}`，是 0 吗？是的话 0 的个数加一',
        's1 += x': '每个 0 至少换成 1，`s1` 加上 `x` → `s1 = {s1}`',
        's2 += y': '`s2` 加上 `y` → `s2 = {s2}`',
        'if s1 == s2': '两个最小可能和 `s1={s1}`、`s2={s2}`，相等就不用补了',
        'elif s1 > s2': '`s1 > s2`？要把 s2 补到 s1，需要 nums2 里有 0（`y={y}`）',
        'elif x > 0': '`s1 < s2`，要补 s1，需要 nums1 里有 0（`x={x}`）',
        'return s2': '`x > 0`，把 nums1 的某个 0 调大补到 s2 → 返回 =={ret}==',
        'return s1': '返回 =={ret}==',
        'return -1': '较小的一边没有 0，补不上 → `-1`',
    },
    cards=dict(
        one_liner='先统计和与 0 的个数，每个 0 至少是 1',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['两个数组里的 0 都要换成正整数，使两数组和相等且最小',
                 '做不到返回 `-1`',
                 '示例：`[3,2,0,1,0]` 与 `[6,5,0]` → `12`'],
        quote='可以先分别遍历两个数组，统计其中0的个数x、y以及数组之和s1、s2，那么可能的数组最小和就是s1 + x以及s2 + y。',
        quote_src='—— yiduobo 题解',
        idea=['遍历得到 `s1, x` 和 `s2, y`，再把 `x`、`y` 加进和里',
              '`s1 == s2`：直接返回',
              '较小的一边需要有 0 才能补齐，否则 `-1`'],
        summary=['分三种：相等、`s1>s2`、`s1<s2`',
                 '`s1>s2` 要看 nums2 有没有 0（`y>0`），反之看 `x>0`',
                 '每个 0 至少替换为 1，所以下界是 `s + 零的个数`',
                 '两次循环分别统计两个数组'],
    ),
)
