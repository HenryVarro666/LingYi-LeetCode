S0, K0 = '010010', 2


def _txt(S):
    if 'z' not in S:
        return '要把 `s` 里的 0 全翻成 1：先数出 0 的个数 `z`'
    n, z, k = S['n'], S['z'], S['k']
    return f'`n = {n}`，`z = {z}`（0 的个数），`k = {k}`；每个 0 要翻奇数次，每个 1 要翻偶数次'


def _ms(S):
    if 'm' not in S:
        return ''
    return f"本情况的下界 `m = {S['m']}`；当前 `ans = {S.get('ans')}`"


CONFIG = dict(
    num=3666, title='使二进制字符串全为 1 的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='数学：分 m 奇偶求下界',
    tags=['图论算法', '难度分 2477'],
    code='''
class Solution:
    def minOperations(self, s: str, k: int) -> int:
        n = len(s)
        z = s.count('0')
        if z == 0:
            return 0
        if k == n:
            return 1 if z == n else -1

        ans = inf
        # 情况一：操作次数 m 是偶数
        if z % 2 == 0:  # z 必须是偶数
            m = max((z + k - 1) // k, (z + n - k - 1) // (n - k))  # 下界
            ans = m + m % 2  # 把 m 往上调整为偶数

        # 情况二：操作次数 m 是奇数
        if z % 2 == k % 2:  # z 和 k 的奇偶性必须相同
            m = max((z + k - 1) // k, (n - z + n - k - 1) // (n - k))  # 下界
            ans = min(ans, m | 1)  # 把 m 往上调整为奇数

        return ans if ans < inf else -1
''',
    call=f'Solution().minOperations({S0!r}, {K0})',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（绿 = 1，红 = 0，红色个数就是 z）', cell=96, h=190,
             color=lambda S, i, v: 'red' if v == '0' else 'green'),
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='text', h=90, size=30, fn=_ms),
    ],
    watch=['n', 'z', 'k', 'm', ('ans', 'ans', 'green')],
    max_steps=60,
    captions={
        'z = s.count': '`z` = 0 的个数 = =={z}==；它们必须翻奇数次，其余 `{n-z}` 个 1 必须翻偶数次',
        'if z == 0': '`z = {z}`：没有 0 才不用操作，这里要继续',
        'if k == n': '`k == n`（{k} == {n}）？不是；下面公式里分母有 `n-k`，这里先排除 `k = n` 的特殊情况',
        'ans = inf': '`ans` 先设为无穷，两种情况都不成立就返回 -1',
        'if z % 2 == 0': lambda S, B, r: (f'总翻转次数 `m·k` 减去 `z` 必须是偶数；若 `m` 为偶数，则 `z` 必须是偶数：`z = {S.z}` → '
                                          + ('成立，可以试 m 为偶数' if S.z % 2 == 0 else '不成立，跳过')),
        'm = max((z + k - 1) // k, (z + n - k - 1)': '偶数 m 的下界：`ceil(z/k)` = {(z+k-1)//k} 与 `ceil(z/(n-k))` = {(z+n-k-1)//(n-k)}（0 最多翻 m-1 次）取大 → ==m = {m}==',
        'ans = m + m % 2': '`m` 是偶数下界，奇数就加 1 凑成偶数：`ans = {ans}`',
        'if z % 2 == k % 2': lambda S, B, r: (f'`m` 为奇数时，`z` 与 `k` 奇偶必须相同：`{S.z % 2}` 与 `{S.k % 2}` → '
                                              + ('相同，可以试 m 为奇数' if S.z % 2 == S.k % 2 else '不同，跳过')),
        'm = max((z + k - 1) // k, (n - z + n': '奇数 m 的下界：`ceil(z/k)` = {(z+k-1)//k} 与 `ceil((n-z)/(n-k))` = {(n-z+n-k-1)//(n-k)}（1 最多翻 m-1 次）取大 → ==m = {m}==',
        'ans = min(ans, m | 1)': '`m | 1` 把 m 调成奇数 = {m | 1}，和偶数情况取最小 → `ans = {min(B.ans, m | 1)}`',
        'return ans if': '`ans = {ans}`，不是无穷 → 返回 =={ans}==',
    },
    cards=dict(
        one_liner='设 0 有 z 个，操作 m 次：分 m 奇偶，各求下界取最小',
        complexity='时间 `O(n)`（数 0），空间 `O(1)`',
        problem=['二进制串 `s`，每次恰好选 `k` 个不同下标翻转，问全变 1 的最少操作次数，不行返回 `-1`',
                 f'本视频：`s = "{S0}", k = {K0}` → `2`',
                 '示例：`s = "0101", k = 3` → `2`'],
        quote='这 z 个 0 必须翻转奇数次，其余 n-z 个 1 必须翻转偶数次。mk-z 是偶数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总翻转 `m·k` 至少要 `z` 次：`m ≥ ceil(z/k)`',
              '`m` 偶数：0 至多翻 `m-1` 次 → `m ≥ ceil(z/(n-k))`；`m` 奇数：1 至多翻 `m-1` 次 → `m ≥ ceil((n-z)/(n-k))`',
              '下界一定取得到（Gale-Ryser 定理），两种情况取最小；`ceil(a/b) = (a+b-1)//b`'],
        summary=['时间 `O(n)`（数 0），空间 `O(1)`；已知 z 则 `O(1)`',
                 '易错：`k == n` 要特判（分母 `n-k` 为 0）；`z == 0` 答案是 0',
                 '`m + m % 2` 调成偶数，`m | 1` 调成奇数',
                 '另一种写法：方法一 BFS + 有序集合，状态是 0 的个数 z，思路同 2612 题'],
    ),
)
