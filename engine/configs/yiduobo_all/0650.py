N0 = 60


def _facts(S):
    if 'x' not in S:
        return f'目标 `n = {N0}`：把它拆成质因数，操作次数 = 质因数之和'
    done = []
    m = N0
    r = S['res']
    for p in range(2, N0 + 1):
        while m % p == 0 and sum(done) < r:
            done.append(p)
            m //= p
    return f'已拆出：`{" + ".join(map(str, done)) or "（无）"}` = ==`{S["res"]}`==；还剩 `n = {S["n"]}`，试除数 `x = {S["x"]}`'


def _ab(S):
    return f'`n = {S["n"]}`，`x = {S["x"]}`：{"整除，x 是一个质因数" if S["n"] % S["x"] == 0 else "不能整除，x 加 1"}' if 'x' in S else ''


CONFIG = dict(
    num=650, title='只有两个键的键盘', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='质因数分解',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minSteps(self, n):

        res = 0
        x = 2
        while n > 1:
            while n % x == 0:
                res += x
                n //= x
            x += 1

        return res
''',
    call=f'Solution().minSteps({N0})',
    expect=12,
    views=[
        dict(type='text', fn=_facts, size=30, h=150),
        dict(type='text', fn=_ab, size=30, h=110),
        dict(type='text', size=26, h=150,
             fn=lambda S: '倍增：`x` 个 A → `kx` 个 A，复制 1 次 + 粘贴 `k-1` 次 = `k` 次；若 `k = p×q`，分两步只要 `p + q` 次'),
    ],
    watch=[('n', 'n', 'blue'), ('x', 'x', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计操作次数，从 0 开始',
        'x = 2': '从最小的质数 `x = 2` 开始试除',
        'while n > 1': lambda S, B, r: f'`n = {S.n}` {"> 1：还没拆完" if S.n > 1 else "= 1：拆完了，退出"}',
        'while n % x == 0': lambda S, B, r: f'`{S.n} % {S.x} = {S.n % S.x}`：{"能整除，x 是 n 的因数" if S.n % S.x == 0 else "不能整除，换下一个 x"}',
        'res += x': '每个质因数 `x` 花 `x` 次操作（复制 1 次 + 粘贴 `x-1` 次）：`res` = =={res}==',
        'n //= x': '`n` 除掉一个 `x` → ==`{n}`==（原文 `/=` 改成 `//=`）',
        'x += 1': '`x` 的因数已除干净，试下一个：`x` → {x}（合数的因子早被小质数除掉了，所以不会误取合数）',
        'return res': '最少操作次数 = 质因数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='把 n 拆成质因数，操作次数就是质因数之和',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['记事本里初始有一个 `A`，每步只能 ==Copy All== 或 ==Paste==',
                 '求得到恰好 `n` 个 `A` 的最少操作次数',
                 '示例：`n = 3` → `3`（复制、粘贴、粘贴）；`n = 60` → `12`'],
        quote='若此时的k是合数，那么设k = pq……那么总共是使用p + q次操作。由于k是合数，那么必然有pq >= p + q，于是现在的思路就是对n进行质因数分解。',
        quote_src='—— yiduobo 题解',
        idea=['从 `x` 个 A 倍增到 `kx` 个：复制一次、粘贴 `k-1` 次，共 `k` 次',
              '`k = p×q` 合数时，先倍增 `p` 倍再倍增 `q` 倍，只要 `p+q ≤ pq` 次',
              '所以一直拆到质数为止：`n = p1×p2×…×pm`，答案 `p1+p2+…+pm`'],
        summary=['时间 `O(√n)`：`x` 最多试到 `n` 的最大质因子',
                 '易错：`n = 1` 不需要任何操作，返回 0',
                 '原文为 Python 2 写法，整数除法 `n /= x` 已改为 `n //= x`',
                 '这题也可以按 DP 做：`f[i] = min(f[j] + i/j)`，质因数分解是它的最优结论'],
    ),
)
