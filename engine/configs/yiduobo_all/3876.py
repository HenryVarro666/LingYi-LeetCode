CONFIG = dict(
    num=3876, title='构造奇偶一致的数组 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='分类讨论 + 最小奇偶数', tags=['灵神题单', '贪心与思维', '难度分 1444'],
    code='''
class Solution(object):
    def uniformArray(self, nums1):
        
        mi_o, mi_e = None, None
        for v in nums1:
            if v % 2 == 1:
                if mi_o is None or mi_o > v:
                    mi_o = v
            else:
                if mi_e is None or mi_e > v:
                    mi_e = v
        
        return mi_e is None or mi_o is None or mi_e > mi_o
''',
    call='Solution().uniformArray([8, 3, 6, 5, 4])',
    expect=True,
    views=[
        dict(type='array', var='nums1', label='nums1', h=260,
             color=lambda S, i, v: ('green' if v % 2 == 1 else 'blue') if 'v' in S and v == S['v'] else None),
        dict(type='text', fn=lambda S: f"最小奇数 `mi_o = {S.get('mi_o')}`，最小偶数 `mi_e = {S.get('mi_e')}`"),
    ],
    watch=['v', ('mi_o', 'mi_o', 'green'), ('mi_e', 'mi_e', 'blue')],
    captions={
        'mi_o, mi_e = None': '`mi_o` 记最小奇数，`mi_e` 记最小偶数，还没见到就是 `None`',
        'if v % 2 == 1': '`v={v}` 是{"奇" if v % 2 else "偶"}数',
        'mi_o = v': '更新最小奇数：`mi_o = {mi_o}`',
        'mi_e = v': '更新最小偶数：`mi_e = {mi_e}`',
        'return': '一方不存在即全奇或全偶，直接 true；否则偶数都减去最小奇数，要求 `mi_e > mi_o`：`{mi_e} > {mi_o}` → =={ret}==',
    },
    cards=dict(
        one_liner='全奇全偶直接成立，否则比较最小偶数和最小奇数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums2[i]` 取 `nums1[i]` 或 `nums1[i]-nums1[j]`（j≠i 且差 ≥ 1）',
                 '问能否让 `nums2` 全奇或全偶',
                 '示例：`[8,3,6,5,4]` → `true`'],
        quote='由于与偶数做减法不会改变一个元素的奇偶性，那么在这里就要么需要让所有偶数减去某个奇数从而使得nums2全奇，要么就要让所有奇数减去某个奇数从而使得nums2全偶。',
        quote_src='—— yiduobo 题解',
        idea=['减偶数不改变奇偶性，要改变只能减奇数',
              '后一种（奇数变偶数）因为没有比最小奇数更小的奇数，做不到',
              '只能让偶数减最小奇数，有解当且仅当最小偶数大于最小奇数'],
        summary=['一趟遍历找 `mi_o`、`mi_e`',
                 '任一为 `None` 就是全偶或全奇，返回 true',
                 '3875 题没有「差 ≥ 1」的限制，答案恒为 true',
                 '易错：比较前要先判断 `None`'],
    ),
)
