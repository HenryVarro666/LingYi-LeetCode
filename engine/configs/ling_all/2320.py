_F = [1, 2]
for _ in range(8):
    _F.append(_F[-1] + _F[-2])


def _top(S):
    n = S.get('n')
    if n is None:
        return ''
    return f"街道一侧有 `f[{n}] = {_F[n]}` 种放法，两侧互不影响 → `{_F[n]} × {_F[n]}` = =={_F[n] ** 2}=="


CONFIG = dict(
    num=2320, title='统计放置房子的方式数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='一侧 DP + 乘法原理',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1608'],
    code='''
MOD = 1_000_000_007
MX = 10_001

f = [1, 2]
while len(f) < MX:
    f.append((f[-1] + f[-2]) % MOD)

class Solution:
    def countHousePlacements(self, n: int) -> int:
        return f[n] ** 2 % MOD
''',
    call='Solution().countHousePlacements(5)',
    expect=169,
    views=[
        dict(type='array', var=_F, label='f[i]：一侧前 i 个地块的放法数（f[i] = f[i-1] + f[i-2]）', h=230,
             pointers={'n': 'blue'},
             color=lambda S, i, v: 'green' if i == S.get('n') else None),
        dict(type='text', size=30, fn=_top),
        dict(type='text', size=28, fn=lambda S: '`f[i-1]`：第 i 块不放；`f[i-2]`：第 i 块放，第 i-1 块必须空'),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return f[n]': lambda S, B, r: f"查表：一侧 `f[{S.n}] = {_F[S.n]}` 种；两侧独立，==乘法原理== `{_F[S.n]} × {_F[S.n]}` = {r}，再对 `MOD` 取余",
    },
    cards=dict(
        one_liner='先算一侧：f[i] = f[i-1] + f[i-2]，两侧相乘',
        complexity='时间 `O(1)`（预处理 `O(MX)`），空间 `O(1)`',
        problem=['街道两侧各 `n` 个地块，每个地块可放一所房子',
                 '同一侧不能有相邻的两所房子；两侧互不影响',
                 '示例：`n = 2` → `9`；本视频 `n = 5` → `169`'],
        quote='单独考虑一侧的房子，定义 $f[i]$ 表示前 $i$ 个地块的放置方案数……由于两侧的房屋互相独立，根据乘法原理，答案为 $f[n]^2$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第 `i` 块不放：前 `i-1` 块随意，`f[i] = f[i-1]`',
              '第 `i` 块放：第 `i-1` 块必须空，前 `i-2` 块随意，`f[i] = f[i-2]`',
              '边界 `f[0] = 1`（空也是一种）、`f[1] = 2`；两侧相乘'],
        before=[dict(heading='预处理表 f', lines=['`f = [1, 2, 3, 5, 8, 13, 21, 34, ...]`', '这就是斐波那契数列：和 198. 打家劫舍的递推一致', '先把 `n ≤ 10^4` 的 `f` 全部算好，每次查表'])],
        summary=['查表 `O(1)`；预处理 `O(MX)`，只做一次',
                 '易错点：==答案是 f[n] 的平方==，不是 f[n] × 2；平方后要再取模',
                 'DP 过程中取模是安全的：加法和乘法都满足同余',
                 '思考题（同一列不能都盖）：两侧不再独立，要用 3 种状态的 DP',
                 '同类题：198. 打家劫舍、70. 爬楼梯'],
    ),
)
