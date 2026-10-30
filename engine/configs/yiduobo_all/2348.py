CONFIG = dict(
    num=2348, title='全 0 子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='连续 0 分段 · 等差数列求和',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1316'],
    code='''
class Solution(object):
    def zeroFilledSubarray(self, nums):

        k = 0
        res = 0
        for num in nums:
            if num == 0:
                k += 1
            else:
                res += k * (k + 1) // 2
                k = 0
        
        return res + k * (k + 1) // 2
''',
    call='Solution().zeroFilledSubarray([1,3,0,0,2,0,0,4])',
    expect=6,
    views=[
        dict(type='array', var='nums', h=300,
             color=lambda S, i, v: 'cyan' if v == 0 else None,
             label='nums（青色 = 0）'),
        dict(type='text', h=140, fn=lambda S: f"当前这段连续 0 的长度 `k = {S['k']}`，可提供 `{S['k']}×{S['k']+1}/2 = {S['k']*(S['k']+1)//2}` 个子数组" if 'k' in S else ''),
    ],
    watch=['num', ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        4: '`k` 统计最近一段连续 0 的个数',
        5: '`res` 累计已经结束的各段提供的子数组数',
        6: lambda S, B, r: f'取下一个数 `num = {S.num}`' if 'num' in S else '遍历结束',
        'if num == 0': lambda S, B, r: (f'`num = 0` → 属于最近这一段连续 0' if S.num == 0 else f'`num = {S.num}` 非 0 → 最近这一段 0 结束了'),
        'k += 1': '这段 0 又长了一个：`k = {k}`',
        'res += k * (k + 1) // 2': '长为 `{B.k}` 的一段 0 提供 `{B.k}×({B.k}+1)/2` = =={B.k * (B.k + 1) // 2}== 个子数组 → `res = {res}`',
        11: '重新开始统计下一段：`k = 0`',
        'return res': '别漏了最后一段：`{res - k*(k+1)//2}` + `{k}×({k}+1)/2` = =={ret}==',
    },
    cards=dict(
        one_liner='连续 k 个 0 能提供 k(k+1)/2 个全 0 子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums`，统计全为 0 的连续子数组个数',
                 '示例：`[1,3,0,0,2,0,0,4]` → `6`'],
        quote='对于一段连续的k个0，其中有k个长度为1的全0子数组，k - 1个长度为2的全0子数组，...，1个长度为k的全0子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['按非 0 把数组切成若干段连续 0',
              '每段长 `k`：`k + (k-1) + … + 1 = k(k+1)/2`',
              '遇到非 0 才结算这一段，所以遍历完还要再结算最后一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：数组以 0 结尾时，最后一段在循环里没被结算，要在 return 处补上',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神按右端点累加，不用算等差数列'],
    ),
)
