CONFIG = dict(
    num=2656, title='K 个元素的最大和', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='反复取最大值 · 等差数列求和', tags=[],
    code='''
class Solution:
    def maximizeSum(self, nums: List[int], k: int) -> int:
        return (max(nums) * 2 + k - 1) * k // 2
''',
    call='Solution().maximizeSum([1,2,3,4,5], 3)',
    expect=18,
    views=[
        dict(type='array', var='nums', label='nums',
             color=lambda S, i, v: 'pink' if v == max(S['nums']) and i == S['nums'].index(v) else None, h=200),
        dict(type='text', size=34, fn=lambda S: f"最大值 `m = {max(S['nums'])}`，取 `{S['k']}` 次：" + ' + '.join(str(max(S['nums']) + t) for t in range(S['k'])) + f" = =={(max(S['nums']) * 2 + S['k'] - 1) * S['k'] // 2}==" if 'nums' in S else ''),
        dict(type='text', size=30, fn=lambda S: f"公式 `(2m + k − 1) × k / 2` = `(2×{max(S['nums'])} + {S['k']} − 1) × {S['k']} / 2`" if 'nums' in S else ''),
    ],
    watch=['k'],
    captions={
        'return': '最大值加一后还是最大值，反复用它：`m, m+1, …, m+k-1`。`m = {max(nums)}`，等差数列和 `({max(nums)}×2 + {k} − 1) × {k} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='最大值加一后还是最大值，反复利用它',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['恰好操作 `k` 次：选 `m`，删掉，加入 `m+1`，得分加 `m`',
                 '求最大总得分',
                 '示例：`[1,2,3,4,5], k=3` → `18`（5+6+7）'],
        quote='由于最大值加一后还是最大值，那么反复利用最大值即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设最大值为 `m`，每次都选当前最大的',
              '三次选到的是 `m, m+1, m+2, …`，共 `k` 项',
              '等差数列求和：`(2m + k − 1)·k / 2`'],
        after=[dict(heading='为什么反复选最大值', lines=['选 `m` 后 `m+1` 进数组，它比原来所有数都大，仍是最大','所以每次都能选到最大：`5, 6, 7`','总分 = `5 + 6 + 7 = 18`，和公式 `(2×5+3−1)×3/2` 一致','也可以写 `k` 次循环模拟，公式只是把循环压成 `O(1)`'])],
        summary=['时间 `O(n)`（找最大值），空间 `O(1)`',
                 '`k` 次循环累加也行，公式把它降成 `O(1)` 计算',
                 '易错点：用整除 `// 2`，`(2m+k−1)·k` 一定是偶数'],
    ),
)
