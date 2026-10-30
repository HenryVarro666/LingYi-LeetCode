def _color(S, i, v):
    if 'v' not in S:
        return None
    if v == S['v']:
        return 'green'
    return 'blue' if v < S['v'] else None


CONFIG = dict(
    num=2681, title='英雄的力量', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='排序 + 递推左侧最小值之和 mi_s',
    tags=['灵神题单·贪心与思维', '难度分 2060'],
    code='''
class Solution(object):
    def sumOfPower(self, nums):

        res = 0
        mod = 10 ** 9 + 7
        mi_s = 0

        for v in sorted(nums):
            res += v * v * (mi_s + v)
            res %= mod
            mi_s = (mi_s + mi_s + v) % mod
        
        return res
''',
    call='Solution().sumOfPower([2, 1, 4, 3])',
    expect=316,
    views=[
        dict(type='text', size=30, fn=lambda S, B: '`mi_s` = 当前数左侧所有子集的最小值之和（初始为 0）' if 'v' not in S else
             f"v = {S['v']} 作最大值：`v·v·mi_s + v³` = {S['v']}×{S['v']}×{B['mi_s']} + {S['v']**3} ，res = =={S['res']}=="),
        dict(type='array', var='nums', color=_color, h=300,
             label='nums（原顺序，已不重要）：绿 = 当前最大值 v，蓝 = 比它小的数'),
        dict(type='text', size=26, fn=lambda S: f"`mi_s' = mi_s + mi_s + v`：含 v 的、不含 v 的、只有 v 自己 三类" if 'v' in S else ''),
    ],
    watch=[('v', 'v', 'green'), ('mi_s', 'mi_s', 'blue'), ('res', 'res', 'orange')],
    captions={
        'res = 0': '`res` 累计所有子集的得分',
        'mod = ': '答案要对 `10^9+7` 取模',
        'mi_s = 0': '`mi_s`：当前数左侧的数能组成的所有集合的==最小值之和==，最左边没有集合，所以是 0',
        'for v in sorted': lambda S, B, r: ('排序后的数都处理完，循环结束' if 'v' in B and B.v == S.v else f'排好序后，`v = {S.v}` 左边的数都不大于它：左边任意子集加上 `v`，最大值就是 `v`'),
        'res += ': '以 `v` 为最大值的得分 = `v·v·mi_s`（加上 v 的集合）+ `v³`（只选 v）= {v}×{v}×{mi_s} + {v**3} → `res` = {res}',
        'res %= mod': '取模：`res = {res}`',
        'mi_s = (': '下一个数的 `mi_s`：含 v 的集合最小值不变（`mi_s`）+ 不含 v 的（`mi_s`）+ v 单独（`v`）：`{B.mi_s}+{B.mi_s}+{v}` = =={mi_s}==',
        'return res': '所有数都当过最大值，返回 `{res}`',
    },
    cards=dict(
        one_liner='排序后，左边所有集合加上当前数，当前数就是最大值',
        complexity='时间 `O(n log n)`，空间 `O(n)`（sorted 产生新列表）',
        problem=['对数组所有非空子集，计算 `最大值² × 最小值`，求和后对 `10^9+7` 取模',
                 '示例：`[2,1,4]` → `141`',
                 '本视频演示：`[2,1,4,3]` → `316`'],
        quote='不妨设nums[index]左侧的数可构成集合中的最小值之和为mi_s，那么所有以nums[index]为最大值的子集的得分之和就是v * v * mi_s + v * v * v。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，`v` 左侧任意子集加上 `v`，`v` 就是最大值；单独选 `v` 得分 `v³`',
              '难点是最小值：换成整体求解，用 `mi_s` 保存左侧所有集合的最小值之和',
              '递推：`mi_s` 到下一个数时，含 v 的集合 + 不含 v 的集合 + v 单独成集 = `mi_s + mi_s + v`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先用旧的 `mi_s` 算得分，再更新 `mi_s`',
                 '`res` 和 `mi_s` 都要取模，避免数字爆炸',
                 '对比灵神：思路一致，灵神把 s 写成 `s*2+x`，yiduobo 写成 `mi_s+mi_s+v`'],
    ),
)
