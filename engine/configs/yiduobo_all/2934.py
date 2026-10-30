def _txt(S, B):
    if 'v1' not in S:
        return '末位要么不变要么互换：分别检测，再合并结果'
    i = S.get('i')
    return f"上限：nums1 ≤ `{S['v1']}`，nums2 ≤ `{S['v2']}`，已交换 ==`{S['s']}`== 次"


CONFIG = dict(
    num=2934, title='最大化数组末位元素的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举末位 · 一趟遍历检测', tags=['灵神题单', '难度分 1803'],
    code='''
class Solution(object):
    def minOperations(self, nums1, nums2):

        def calc(v1, v2):
            s = 0
            for i in range(len(nums1) - 1):
                if nums1[i] <= v1 and nums2[i] <= v2:
                    continue
                if nums1[i] <= v2 and nums2[i] <= v1:
                    s += 1
                else:
                    return -1
            return s

        s1 = calc(nums1[-1], nums2[-1])
        s2 = calc(nums2[-1], nums1[-1])
        if s1 == -1:
            if s2 == -1:
                return -1
            else:
                return s2 + 1
        elif s2 == -1:
            return s1
        else:
            return min(s1, s2 + 1)
''',
    call='Solution().minOperations([2,3,4,5,9], [8,8,4,4,4])',
    expect=2,
    views=[
        dict(type='array', var='nums1', label='nums1', pointers={'i': 'blue'}, h=250, cell=100),
        dict(type='array', var='nums2', label='nums2', pointers={'i': 'blue'}, h=250, cell=100),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=[('v1', 'v1', 'blue'), ('v2', 'v2', 'pink'), ('s', 's', 'yellow'), ('s1', 's1', 'green'), ('s2', 's2', 'green')],
    captions={
        's = 0': '`s` 统计需要交换的下标数；要求 nums1 都 ≤ `{v1}`，nums2 都 ≤ `{v2}`',
        'for i in range': '检查下标 `{i}`：`({nums1[i]}, {nums2[i]})`',
        'if nums1[i] <= v1 and nums2[i] <= v2': lambda S, B, r: (f'`{S.nums1[S.i]} ≤ {S.v1}` 且 `{S.nums2[S.i]} ≤ {S.v2}`：不换就合法 → 不需要交换' if (S.nums1[S.i] <= S.v1 and S.nums2[S.i] <= S.v2)
                                                                     else f'不换不行（`{S.nums1[S.i]}` 或 `{S.nums2[S.i]}` 超了上限）→ 再看换了行不行'),
        'continue': '这一位保持原样，看下一位',
        'if nums1[i] <= v2 and nums2[i] <= v1': lambda S, B, r: (f'换了以后 `{S.nums2[S.i]} ≤ {S.v1}` 且 `{S.nums1[S.i]} ≤ {S.v2}`：==交换后合法==' if (S.nums1[S.i] <= S.v2 and S.nums2[S.i] <= S.v1)
                                                                  else '换不换都超上限 → 这个末位方案无解'),
        's += 1': '必须交换这一位：`s` = =={s}==',
        'return -1': '这个末位方案不可行，返回 `-1`',
        'return s': '这个方案需要 =={s}== 次交换',
        's1 = calc': '末位保持不变：`s1` = =={s1}==',
        's2 = calc': '末位互换：`s2` = =={s2}==（还要再算上交换末位自己的 1 次）',
        'if s1 == -1': '`s1 = {s1}`：{"不行" if s1 == -1 else "可行"}',
        'if s2 == -1': '`s2 = {s2}`：{"也不行 → 无解" if s2 == -1 else "可行"}',
        'return s2 + 1': '只有互换末位可行：交换 `s2` 次再加末位本身 1 次 = =={s2 + 1}==',
        'return s1': '只有末位不变可行：答案 `s1` = =={s1}==',
        'return min': '两种都可行：`min(s1, s2 + 1)` = `min({s1}, {s2 + 1})` = =={s1 if s1 < s2 + 1 else s2 + 1}==',
    },
    cards=dict(
        one_liner='末位要么不变要么互换，各自一趟遍历数交换次数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['只能交换同一下标的 `nums1[i]` 与 `nums2[i]`',
                 '要使两个数组的末位分别是各自的最大值，求最少交换次数，不行返回 `-1`',
                 '示例：`[2,3,4,5,9]`、`[8,8,4,4,4]` → `2`'],
        quote='若nums1[i] <= v1且nums2[i] <= v2，那么不需要交换；若nums1[i] <= v2且num2[i] <= v1，那么执行交换后可以满足……',
        quote_src='—— yiduobo 题解原文',
        idea=['既然只能同下标交换，最终末位要么是原来的，要么互换过',
              '定下末位 `v1`、`v2`，问题变成：每个下标换不换，才能让 nums1 都 ≤ v1、nums2 都 ≤ v2',
              '不换行就不换；只有换了才行才换；都不行则无解',
              '末位互换的方案，自己还要多算 1 次交换，所以是 `s2 + 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`calc` 只遍历前 `n-1` 位，末位的交换要在 `s2 + 1` 里补上',
                 '易错：两个方案可能一个返回 `-1`，合并时要分情况',
                 '对比灵神：灵神把末位也放进循环，yiduobo 把末位单独处理'],
    ),
)
