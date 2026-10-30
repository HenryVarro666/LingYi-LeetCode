CONFIG = dict(
    num=1925, title='统计平方和三元组的数目', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='本原勾股数组 · 枚举 (u, v)',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution:
    def countTriples(self, n: int) -> int:
        ans = 0
        u = 3
        while u * u < n * 2:
            v = 1
            while v < u and u * u + v * v <= n * 2:
                if gcd(u, v) == 1:
                    ans += n * 2 // (u * u + v * v)
                v += 2
            u += 2
        return ans * 2  # (a,b,c) 和 (b,a,c) 各算一次
''',
    call='Solution().countTriples(25)',
    expect=16,
    views=[
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"斜边 c = (u²+v²)/2 = =={(S['u']**2+S['v']**2)//2}==，条件 u²+v² ≤ 2n = {S['n']*2}" if 'v' in S
                           else '奇数 u > 奇数 v 且互质 → 本原勾股数，再乘 k 倍')),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"本原三元组 (a,b,c) = ({(S['u']**2-S['v']**2)//2}, {S['u']*S['v']}, {(S['u']**2+S['v']**2)//2})，倍数 k 最多 `{S['n']*2}//{S['u']**2+S['v']**2}` = {S['n']*2//(S['u']**2+S['v']**2)} 个" if 'v' in S and S['v'] < S['u'] and S['u']**2+S['v']**2 <= S['n']*2
                           else '')),
    ],
    watch=[('u', 'u', 'blue'), ('v', 'v', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计 `a < b` 的三元组个数，最后乘 2',
        'u = 3': '`u` 从 3 开始，只取奇数：u、v 都是奇数且互质，才生成本原勾股数',
        'while u * u < n * 2': lambda S, B, r: (f'`{S.u}² = {S.u*S.u} < 2n = {S.n*2}`：还可能有满足条件的 v' if S.u*S.u < S.n*2
                                               else f'`{S.u}² = {S.u*S.u} ≥ 2n = {S.n*2}`：u 太大了，结束'),
        'v = 1': '`v` 从 1 开始，同样只取奇数',
        'while v < u and': lambda S, B, r: (f'`v={S.v} < u={S.u}` 且 `{S.u*S.u}+{S.v*S.v}={S.u*S.u+S.v*S.v} <= 2n={S.n*2}`：继续' if S.v < S.u and S.u*S.u+S.v*S.v <= S.n*2
                                            else f'`{S.u*S.u}+{S.v*S.v}={S.u*S.u+S.v*S.v}` 超过 `2n={S.n*2}`（或 v ≥ u）：这个 u 结束'),
        'if gcd(u, v) == 1': lambda S, B, r: (f'`gcd({S.u}, {S.v}) = 1`：互质，得到一组==本原==勾股数' if gcd(S.u, S.v) == 1
                                              else f'`gcd({S.u}, {S.v}) = {gcd(S.u, S.v)} ≠ 1`：不是本原的，会被别的 (u,v) 的倍数覆盖'),
        'ans += n * 2 // (u * u + v * v)': '这组本原勾股数的 `k` 倍（斜边 `k·(u²+v²)/2 <= n`）共 `{n*2} // {u*u+v*v}` = `{n*2 // (u*u+v*v)}` 个 → `ans = {ans}`',
        'v += 2': '`v` 取下一个奇数 → {v}',
        'u += 2': '`u` 取下一个奇数 → {u}',
        'return ans * 2': '`(a,b,c)` 和 `(b,a,c)` 各算一次：`{ans} * 2` = =={ret}==',
    },
    cards=dict(
        one_liner='不枚举 a、b、c：直接用公式生成所有勾股数',
        complexity='时间 `O(n log n)`（枚举 O(n) 对 (u,v)，每对算一次 gcd），空间 `O(1)`',
        problem=['数出满足 `a²+b²=c²` 且 `1 <= a,b,c <= n` 的整数三元组 `(a,b,c)`',
                 '`(3,4,5)` 与 `(4,3,5)` 算两个',
                 '示例：`n=5` → `2`；`n=10` → `4`；本视频：`n=25` → `16`'],
        quote='请看 勾三股四弦五：生成勾股数的公式。（方法二：本原勾股数组）',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['每个勾股数都是某个==本原勾股数==（三边互质）的整数倍',
              '本原勾股数由奇数 `u > v` 且 `gcd(u,v)=1` 生成，`(a,b,c) = ((u²−v²)/2, uv, (u²+v²)/2)`',
              '`c*k <= n` 的 `k` 有 `2n // (u²+v²)` 个，累加后乘 2（a、b 互换）'],
        summary=['时间 `O(n log n)`，空间 `O(1)`；预处理 gcd 表可做到 `O(n)`',
                 '先统计 `a<b` 再乘 2；`a=b` 不可能（√2 是无理数）',
                 '题解另给了 `O(n²)` 暴力枚举，以及数论分块 + 莫比乌斯容斥的 `O(n^(2/3) log n)` 写法，本视频演示方法二',
                 '易错：`u`、`v` 都要取奇数，`v` 要小于 `u`'],
    ),
)
