NUMS, K = [1, 2, 3, 4, 5], 2


def _rd_fmt(k, v):
    return f'r={k}: x = ' + str(v)


def _txt(S):
    ln = S.get('_line', 0)
    if 'f' in S and ln in (20, 22) and 'cnt' in S:
        n = len(S['f']) - 1
        if ln == 20:
            return f'`f[{n}] = f[{n - 1}] + f[{n - 2}] × (2^cnt[{n - 1}] − 1)` = {S["f"][n - 1]} + {S["f"][n - 2]} × {(1 << S["cnt"][n - 1]) - 1} = =={S["f"][n]}=='
        return f'这一组合法子集数 `f[-1]` = =={S["f"][-1]}==，累乘进 `res`'
    return '同余数的组独立：乘法原理；组内 x 相邻不能同时选 → 打家劫舍'


CONFIG = dict(
    num=2638, title='统计 K-Free 子集的总数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按余数分组 · 打家劫舍 DP · 乘法原理',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countTheNumOfKFreeSubsets(self, nums, k):

        r_dict = {}
        for v in nums:
            r = v % k
            v //= k
            if r not in r_dict:
                r_dict[r] = []
            r_dict[r].append(v)
        
        res = 1
        for r in r_dict:
            cnt = [0] * 4
            for v in r_dict[r]:
                cnt[v] += 1
                
            f = [1, 1 << (cnt[0])]
            for v in range(1, 4):
                f.append(f[-1] + f[v - 1] * ((1 << cnt[v]) - 1))

            res *= f[-1]

        return res
''',
    call=f'Solution().countTheNumOfKFreeSubsets({NUMS!r}, {K})',
    expect=15,
    skip=['r_dict[r] = []', 'if r not in r_dict', 'r = v % k'],
    views=[
        dict(type='map', var='r_dict', label='r_dict：余数 r → 这组数的 x（数 = x·k + r）', h=150, fmt=_rd_fmt, font=30),
        dict(type='array', var='cnt', label='cnt[x]：这一组里 x 出现几次', h=170, cell=90,
             pointers={'v if _line in (16, 17) else None': 'blue'}, pointer_labels={'v if _line in (16, 17) else None': 'x'}),
        dict(type='array', var='f', label='f[i]：这一组 x < i 的数能选出的合法子集数（黄框 = 刚算出）', h=170, cell=90,
             index=True,
             color=lambda S, i, v: 'green' if S.get('_line') == 22 and i == len(S['f']) - 1 else None),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('v', 'v', 'blue'), 'r', ('res', 'res', 'green')],
    captions={
        'r_dict = {}': '按 `v % k` 的余数分组：不同组的差不会是 `k` 的倍数，可以分开算',
        'v //= k': lambda S, B, r: f'`{B.v} = {S.v} × {K} + {S.r}`：组内数写成 `x·k + r`，这里 x = =={S.v}==',
        'r_dict[r].append': '余数 `{r}` 这组加入 `x = {v}`；`x` 相邻的两个数差恰好是 `k`，不能同选',
        'res = 1': '`res` 累乘各组方案数（乘法原理）',
        'for r in r_dict': lambda S, B, r: ('所有组都处理完了' if S.res == 15 else f'处理余数 `{S.r}` 这一组：`x` = {S.r_dict[S.r]}'),
        'cnt = [0]': '`cnt[x]`：x 出现次数（原文 1001 对应 nums ≤ 1000，演示缩成 4）',
        'cnt[v] += 1': '`cnt[{v}] += 1` → {cnt}',
        'f = [1, 1 <<': '`f[0] = 1`（x < 0 没有数，只有空集）；`f[1] = 2^cnt[0]` = {f[1]}：x=0 的数可选可不选',
        'f.append': lambda S, B, r: f'`f[{len(S.f) - 1}] = f[{len(S.f) - 2}] + f[{len(S.f) - 3}] × (2^{S.cnt[len(S.f) - 2]} − 1)` = {S.f[-2]} + {S.f[-3]} × {(1 << S.cnt[len(S.f) - 2]) - 1} = =={S.f[-1]}==：不选 x={len(S.f) - 2}，或选它（非空）且放弃 x={len(S.f) - 3}',
        'res *= f[-1]': '这一组有 `{f[-1]}` 种 → `res` = {res}',
        'return res': '答案 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='按 mod k 分组，组内 x 相邻不能同选，就是打家劫舍',
        complexity='时间 `O(n + V)`，空间 `O(V)`，V 为 nums 最大值 / k',
        problem=['给你正整数数组 `nums` 和整数 `k`，子集中不能有两个数的差的绝对值恰好等于 `k`（K-Free）',
                 '返回 K-Free 子集的总数（空集也算）',
                 '本视频：`nums=[1,2,3,4,5], k=2` → `15`'],
        quote='首先将所有数按照对k取模的余数分组。不同组的数之差的绝对值必然不会是k的倍数，也就意味着不同组之间的数可以分开处理，然后使用乘法原理计算最终合法的子集数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['同组数写成 `x·k + r`：`x` 相邻（差 1）的两类数不能同时选',
              '`f[i]`：x 在 `0..i-1` 的数能选出的合法子集数；先放弃 `x=i-1`：`f[i-1]`',
              '选 `x=i-1` 的非空子集（`2^cnt − 1` 种），就不能选 `x=i-2`：`f[i-2] × (2^cnt − 1)`'],
        summary=['各组方案数相乘，每组是打家劫舍式 DP',
                 '易错：`2^cnt − 1` 要减掉空集，否则和「放弃 x=i-1」重复计数',
                 '原文为 Python 2 写法，`v /= k` 已改为 `v //= k`',
                 '原文常数 `1001`（nums ≤ 1000）；演示输入很小，视频里改成了 `4`，逻辑不变',
                 '同类：2597 美丽子集的数目（数据较小的版本）'],
    ),
)
