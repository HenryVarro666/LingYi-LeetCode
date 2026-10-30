def _ss(S):
    return S['s'] + S['s']


def _ok(S):
    return 'rot' in S and 'i' in S and S['_line'] >= 8


CONFIG = dict(
    num=4021, title='得到旋转回文字符串的最少操作次数 I', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举左旋次数 + 环上距离',
    tags=['卷积'],
    code='''
class Solution:
    def minOperations(self, s: str) -> int:
        n = len(s)
        ans = inf
        for rot in range(n):
            op = rot
            for i in range(n // 2):
                d = abs(ord(s[(rot + i) % n]) - ord(s[(rot - 1 - i) % n]))
                op += min(d, 26 - d)  # 注：这里可以加个剪枝，如果 op >= ans 则 break
            ans = min(ans, op)
        return ans
''',
    call='Solution().minOperations("zffye")',
    expect=3,
    views=[
        dict(type='text', h=70, fn=lambda S: (f"左旋 `{S['rot']}` 次后：`{(S['s'] + S['s'])[S['rot']:S['rot'] + len(S['s'])]}`" + (f"，已花 op ==" + str(S['op']) + "==" if S['_line'] != 5 else '') if 'rot' in S else '')),
        dict(type='string', var=_ss, h=260, label='s + s（左旋 rot 次 = 取从 rot 开始的 n 个字符）',
             window=('rot', 'rot + n - 1'),
             pointers={'(rot + i) if _line in (8, 9) else None': 'blue', '(rot + n - 1 - i) if _line in (8, 9) else None': 'pink'},
             pointer_labels={'(rot + i) if _line in (8, 9) else None': '左', '(rot + n - 1 - i) if _line in (8, 9) else None': '右'},
             dim=lambda S, k, v: 'rot' in S and not (S['rot'] <= k <= S['rot'] + len(S['s']) - 1)),
        dict(type='text', h=70, fn=lambda S: (f"这一对：`{S['s'][(S['rot'] + S['i']) % len(S['s'])]}` 和 `{S['s'][(S['rot'] - 1 - S['i']) % len(S['s'])]}`，字母差 d = ==" + str(S['d']) + "==，环上最短 ==" + str(min(S['d'], 26 - S['d'])) + "==" if 'd' in S and 'i' in S and S['_line'] in (8, 9) else '')),
    ],
    watch=[('rot', 'rot', 'blue'), ('i', 'i', 'pink'), ('d', 'd', 'yellow'), ('op', 'op', 'orange'), ('ans', 'ans', 'green')],
    skip=['n = len', 'ans = inf'],
    max_steps=70,
    captions={
        'op = rot': '左旋 `{rot}` 次要花 `{rot}` 次操作，`op` 先记上 {op}',
        'd = abs': lambda S, B, r: (f"配对 `s[{(S.rot + S.i) % S.n}] = {S.s[(S.rot + S.i) % S.n]}` 与 `s[{(S.rot - 1 - S.i) % S.n}] = {S.s[(S.rot - 1 - S.i) % S.n]}`："
                                  f"字母差 `d = {S.d}`"),
        'op += min': '在长 26 的环上：增大小的要 `{d}` 次，绕回要 `{26 - d}` 次 → 取 `{min(d, 26 - d)}`，`op` = =={op}==',
        'ans = min': '旋转 `{rot}` 次总代价 `{op}`，`ans = min({B.ans}, {op}) = {ans}`',
        'return ans': '每种左旋都试过 → 最少操作 =={ans}==',
    },
    cards=dict(
        one_liner='枚举左旋次数，左旋后首尾配对，每对在字母环上取最短距离',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['字符串 `s`：可「某位 +1（z 后是 a）」或「左旋一位」，操作任意次',
                 '求让 `s` 变成回文串的最少操作次数',
                 '示例：`"abc"` → `2`；`"yb"` → `3`；本视频用 `"zffye"` → `4`'],
        quote='对于字母 $x$ 和 $y$（$x\\le y$），我们可以：把 $x$ 增大到 $y$，操作 $y-x$ 次；把 $y$ 增大绕回到 $x$，操作 $26-y+x$ 次。两种情况取最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左旋 `rot` 次 = `s+s` 里从 `rot` 开始的长 `n` 子串',
              '回文要求第 `i` 个与倒数第 `i` 个相等：只需递增，不必两个都动',
              '两个字母差 `d`，环长 26 → 代价 `min(d, 26-d)`，再加上左旋的 `rot` 次'],
        summary=['时间 `O(n^2)`（`n ≤ 2000`），空间 `O(1)`',
                 '别忘了把左旋次数 `rot` 也算进总代价',
                 '两个字母都递增一定不优：各少一次，结果仍相同',
                 '取模下标 `(rot - 1 - i) % n` 在 Python 里负数也安全，无需拼接 `s+s`',
                 '方法二：把字母拆成 13 个 0/1 数组，用循环自卷积（FFT）把复杂度降到 `O(26 n log n)`'],
    ),
)
