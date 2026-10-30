def _cmp(S, B, ret):
    p, f, w = S.p, S.f, S.numWays
    if p > S.n:
        return '`p` 越过末尾：numWays 与 `f` 完全一致 → 跳出内层 while'
    if w[p - 1] == f[p]:
        return f'`numWays[{p - 1}] = {w[p - 1]}` = `f[{p}] = {f[p]}`：金额 {p} 已被现有面值凑够 → 继续看下一个'
    return f'`numWays[{p - 1}] = {w[p - 1]}` ≠ `f[{p}] = {f[p]}`：第一个不一致的金额是 =={p}=='


CONFIG = dict(
    num=3592, title='硬币面值还原', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='找第一个不同点 · 完全背包累加',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1701'],
    code='''
class Solution(object):
    def findCoins(self, numWays):
        
        n = len(numWays)
        f = [0] * (n + 1)
        f[0] = 1
        res = []

        p = 1
        while p <= n:
            while p <= n and numWays[p - 1] == f[p]:
                p += 1
            
            if p == n + 1:
                break
                
            if numWays[p - 1] - f[p] != 1:
                return []

            res.append(p)

            for v in range(p, n + 1):
                f[v] += f[v - p]

        return res
''',
    call='Solution().findCoins([1,2,2,3,4])',
    expect=[1, 2, 5],
    skip=['for v in range'],
    max_steps=70,
    views=[
        dict(type='text', size=24, h=50, fn=lambda S: '`numWays[k]` 对应金额 k+1；`f[v]` = 已确定面值能凑出金额 v 的方案数'),
        dict(type='array', var='numWays', label='numWays（目标）', h=190, cell=80,
             color=lambda S, k, v: 'blue' if S.get('p') is not None and k == S['p'] - 1 else None),
        dict(type='array', var='f', label='f（当前）', h=190, cell=80, pointers={'p': 'blue', 'v': 'pink'},
             color=lambda S, k, v: 'yellow' if S.get('v') == k else None),
        dict(type='array', var='res', label='res（已确定的面值）', h=130, cell=80),
    ],
    watch=[('p', 'p', 'blue'), ('n', 'n', 'cyan'), ('res', 'res', 'green')],
    captions={
        'f[0] = 1': '`f[0] = 1`：金额 0 有 1 种凑法，背包的起点',
        'res = []': '`res` 按从小到大收集面值',
        'p = 1': '`p` 从金额 1 开始往后找',
        'while p <= n and': _cmp,
        'p += 1': '这一格已经对上，不用管 → `p = {p}`',
        'if p == n + 1': lambda S, B, r: ('`p = n+1`：全部对上 → ==break==' if S.p == S.n + 1
                                          else '还没扫完，`p` 停在第一个不一致的位置'),
        'numWays[p - 1] - f[p]': lambda S, B, r: (f'差值 = `{S.numWays[S.p - 1]} − {S.f[S.p]}` = {S.numWays[S.p - 1] - S.f[S.p]}：'
                                                  + ('刚好多 1 种，说明 ==金额 %d 本身就是一种硬币==' % S.p if S.numWays[S.p - 1] - S.f[S.p] == 1
                                                     else '不是 1 → 无解，返回 `[]`')),
        'res.append': '确定新面值 `{p}`：`res = {res}`',
        'f[v] += f[v - p]': '用面值 `{p}` 正序累加：`f[{v}] += f[{v - p}]` → =={f[v]}==（可重复使用）',
        'return res': '`res = {res}`',
    },
    cards=dict(
        one_liner='谁先对不上，谁就是下一个最小面值',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`numWays[v]` 是固定面值（每种无限枚）凑出金额 `v` 的方案数，下标从 1 计',
                 '面值已丢失，还原所有面值并升序返回，无解返回空数组',
                 '示例：`[1,2,2,3,4]` → `[1,2,5]`'],
        quote='找出第一个 numWays 与 f 不同的下标 p，若此时 numWays[p] 刚好比 f[p] 多 1，那么说明下一种面值最小的硬币的面值就是 p，否则无解。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小的非零项必须恰好是 1：用一枚面值 `p` 的硬币凑出 `p`',
              '确定面值后，用 `f[v] += f[v - p]` 正序更新（完全背包）',
              '再从 `p+1` 找第一个和 `f` 不同的位置，重复，直到两数组完全相同'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`numWays` 下标从 0，金额从 1，所以读 `numWays[p - 1]`',
                 '差值必须恰好为 1，多或少都无解',
                 '原文即 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神逐个金额判断；yiduobo 用内层 while 跳到第一个不同点'],
    ),
)
