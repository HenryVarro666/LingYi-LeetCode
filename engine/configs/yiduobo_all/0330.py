CONFIG = dict(
    num=330, title='按要求补齐数组', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='已覆盖 1..x · 倍增补数', tags=['灵神题单', '贪心与思维', '难度分 2952'],
    code='''
class Solution(object):
    def minPatches(self, nums, n):

        x = 1
        res = 0
        k = 0
        if k < len(nums):
            p = nums[k]
        while x <= n:
            if k < len(nums) and p <= x:
                x += p
                k += 1
                if k < len(nums):
                    p = nums[k]
            else:
                x += x
                res += 1

        return res
''',
    call='Solution().minPatches([1,3,8], 12)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"前 k 个数 + 补的数已覆盖 ==1..{S['x']-1}==，下一个要覆盖 ==x = {S['x']}==" if 'x' in S else '', size=32),
        dict(type='array', var='nums', pointers={'k': 'blue'}, label='nums', h=200,
             color=lambda S, i, v: ('green' if 'k' in S and i < S['k'] else None)),
        dict(type='text', fn=lambda S: f"已补 {S['res']} 个数" if 'res' in S else '', size=30),
    ],
    watch=[('x', 'x', 'cyan'), ('k', 'k', 'blue'), ('p', 'p', 'purple'), ('res', 'res', 'green'), 'n'],
    captions={
        'x = 1': '`x = 1`：这里 x 是「下一个要覆盖的数」，目前覆盖 `1..x-1`（空）',
        'res = 0': '`res` 记补了几个数',
        'k = 0': '`k` 指向 nums 里下一个待考察的数',
        'if k < len(nums):': '先取出第 `k` 个数 `p`',
        'p = nums[k]': '`p = nums[{k}] = {p}`',
        'while x <= n': lambda S, B, r: (f'`x = {S.x} <= n = {S.n}`：还有数没覆盖到，继续' if S.x <= S.n
                                         else f'`x = {S.x} > n = {S.n}`：1..n 都覆盖了 → 结束'),
        'if k < len(nums) and p <= x': lambda S, B, r: (f'`p = {S.p} <= x = {S.x}`：`1+p <= 1+x`，两段区间能合并 → 成立' if S.k < len(S.nums) and S.p <= S.x
                                                        else (f'`p = {S.p} > x = {S.x}`：x 落在缝里，后面的数更大也盖不住 → 必须补' if S.k < len(S.nums)
                                                              else 'nums 用完了，只能补数')),
        'x += p': '合并成 `1..x+p-1`，下一个要覆盖 `x = {x}`',
        'k += 1': '`k` → {k}',
        'x += x': '补入 `{B.x}` 最优：覆盖扩成 `1..2x-1`，下一个 `x = {x}`',
        'res += 1': '补了一个数，`res` = {res}',
        'return res': '一共补 `{res}` 个数',
    },
    cards=dict(
        one_liner='盯住「下一个要覆盖的数 x」：接得上就并入，接不上就补 x',
        complexity='时间 `O(len(nums) + log n)`，空间 `O(1)`',
        problem=['已排序正整数数组 `nums` 与 `n`，补最少的数让 `1..n` 都能表示为若干数之和',
                 '示例：`nums=[1,5,10], n=20` → `2`',
                 '本视频：`[1,3,8], n=12` → `2`'],
        quote='若p <= x，那么这两个区间就可以合并成为1到x + p；否则的话，一定有x < x + 1 < 1 + p，此时无法覆盖到x + 1。',
        quote_src='—— yiduobo 题解原文（x 为已覆盖上界）',
        idea=['设已覆盖 `1..x`，要覆盖 `x+1`',
              '下个数 `p` 不超过 `x`：并入，覆盖到 `x+p`',
              '否则后面的数更大，也盖不住，必须补一个数：补 `x+1` 最优，覆盖到 `2x+1`',
              '代码里 `x` 存的是下一个要覆盖的数，所以补数就是 `x += x`'],
        summary=['时间 `O(len(nums) + log n)`，空间 `O(1)`',
                 '易错：代码的 x 是「已覆盖上界 + 1」，与文字推导差 1',
                 '补数选 x（当前要覆盖的数）：补更小的数扩得更少',
                 '对比灵神：灵神把 0 也算进区间，用 [0, s-1] 描述；这里用 1..x 描述'],
    ),
)
