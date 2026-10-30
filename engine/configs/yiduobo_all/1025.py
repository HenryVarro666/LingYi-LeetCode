def _win_table(N):
    f = [None, False]
    for i in range(2, N + 1):
        f.append(any(not f[i - j] for j in range(1, i) if i % j == 0))
    return f


_F = _win_table(10)


def _row(S):
    return [('必胜' if _F[k] else '必败') for k in range(1, 11)]


CONFIG = dict(
    num=1025, title='除数博弈', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='DP 打表找规律 · 奇偶归纳',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def divisorGame(self, n):

        return n % 2 == 0
''',
    call='Solution().divisorGame(6)',
    expect=True,
    views=[
        dict(type='text', size=26, h=70,
             fn=lambda S: '先手 `n` 是偶数 → ==必胜==；奇数 → ==必败==' if 'n' in S else ''),
        dict(type='array', var=lambda S: list(range(1, 11)), label='n = 1 … 10（DP 打表：绿 = 先手必胜，红 = 先手必败）', h=230, cell=76,
             pointers={'n': 'blue'}, index=False,
             color=lambda S, i, v: 'green' if _F[v] else 'red'),
        dict(type='array', var=_row, label='f[n]（f[i] = 存在约数 j 使 f[i-j] 为必败）', h=170, cell=76, index=False,
             color=lambda S, i, v: 'green' if v == '必胜' else 'red'),
    ],
    watch=[('n', 'n', 'blue'), ('n % 2', 'n % 2', 'orange')],
    captions={
        'return n % 2 == 0': '`n = {n}`，`n % 2 = {n % 2}` → 偶数先手必胜：先拿 1，把奇数留给对手 → =={ret}==',
    },
    cards=dict(
        before=[dict(heading='DP 打表', lines=['`f[1] = 必败`：1 没有可选的 `x`', '`f[2]`：拿 1 → `f[1]` 必败，所以必胜', '`f[3]`：只能拿 1 → `f[2]` 必胜，所以必败', '`f[4]`：拿 1 → `f[3]` 必败，所以必胜……交替出现'])],
        one_liner='先用 DP 打表，发现偶数必胜、奇数必败，再归纳证明',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['黑板上有数字 `n`，爱丽丝先手。每步选 `x`：`0 < x < n` 且 `n % x == 0`，把 `n` 换成 `n - x`',
                 '无法操作的人输。双方都最优，爱丽丝赢则返回 `true`',
                 '示例：`n = 2` → `true`；`n = 3` → `false`；本视频：`n = 6`'],
        quote='可以发现实际上所有偶数的情况都是必胜的，而所有奇数的情况都是必败的，这应该不是巧合。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写 DP：`f[i]` 表示 `i` 先手是否必胜，枚举约数 `j`，只要某个 `f[i-j]` 必败，`f[i]` 就必胜',
              '打表到 `n <= 10`，规律一目了然：偶胜奇败',
              '归纳：奇数的约数都是奇数，`n-x` 必为偶数；偶数拿 1 变成奇数'],
        summary=['时间、空间都是 `O(1)`，一行 `n % 2 == 0`',
                 '归纳证明：奇数 `n` 的约数全是奇数，减完必是偶数，给对手送必胜',
                 '偶数 `n` 先拿 1，把奇数 `n-1` 丢给对手，对手必败',
                 '边界：`n = 1` 先手无法操作，必败，与奇数结论一致',
                 '做法思路：先 DP 暴力打表找规律，再证明；与 877 石子游戏同类'],
    ),
)
