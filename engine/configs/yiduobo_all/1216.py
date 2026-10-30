S0 = 'abcda'
K0 = 2


def _live(S):
    return all(x in S for x in ('left', 'right', 'length', 'f')) and S.get('right', 99) < len(S0) and S['right'] - S['left'] == S['length'] - 1


def _cell(S, a, b, v):
    if not _live(S):
        return None
    l, r = S['left'], S['right']
    if (a, b) == (l, r):
        return 'yellow'
    if r - l >= 2:
        if S0[l] == S0[r]:
            return 'green' if (a, b) == (l + 1, r - 1) else None
        return 'blue' if (a, b) in ((l + 1, r), (l, r - 1)) else None
    return None


def _formula(S):
    if not _live(S):
        return '`f[left][right]`：把 `s[left..right]` 变成回文串，最少要删几个字符'
    l, r = S['left'], S['right']
    if r - l == 0:
        return f'`f[{l}][{r}] = 0`：一个字符本身就是回文'
    if S0[l] == S0[r]:
        return f'`s[{l}] = s[{r}] = {S0[l]}`：两端相等，删数取决于里面 `f[{l + 1}][{r - 1}]`' if r - l >= 2 else f'`s[{l}] = s[{r}]`：两个字符相等，不用删'
    if r - l == 1:
        return f'`s[{l}] = {S0[l]} ≠ s[{r}] = {S0[r]}`：删掉一个就行'
    return f'`s[{l}] = {S0[l]} ≠ s[{r}] = {S0[r]}`：`min(f[{l + 1}][{r}], f[{l}][{r - 1}]) + 1`'


CONFIG = dict(
    num=1216, title='验证回文字符串 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 最少删除次数',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def isValidPalindrome(self, s, k):

        n = len(s)

        f = [[None] * n for _ in range(n)]
        for length in range(1, n + 1):
            for left in range(n):
                right = left + length - 1
                if right >= n:
                    break
                if left == right:
                    f[left][right] = 0
                elif left == right - 1:
                    if s[left] == s[right]:
                        f[left][right] = 0
                    else:
                        f[left][right] = 1
                else:
                    if s[left] == s[right]:
                        f[left][right] = f[left + 1][right - 1]
                    else:
                        f[left][right] = min(f[left + 1][right], f[left][right - 1]) + 1
        
        return f[0][n - 1] <= k
''',
    call=f'Solution().isValidPalindrome({S0!r}, {K0})',
    expect=True,
    skip=['for left in range', 'right = left + length - 1', 'else:', 'if right >= n', 'if s[left] == s[right]:', 'elif left == right - 1'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = left，粉 = right）', h=190, cell=80, pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[left][right] = 最少删除次数（黄 = 正在算，蓝/绿 = 依赖）', h=380, cell=64,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_cell),
    ],
    watch=[('length', 'length', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('k', 'k', 'orange')],
    captions={
        'n = len(s)': '`n = {n}`，`k = {k}`：最多允许删 `k` 个字符',
        'f = [[None]': '`f[left][right]`：把 `s[left..right]` 删成回文串的==最少删除次数==',
        'for length in range': lambda S, B, r: (f'区间长度 `length = {S.length}`：==先算短的，再算长的==' if S.get('length') != B.get('length') else '所有区间都算完了'),
        'if left == right': '`[{left}, {right}]` 只有一个字符' if False else lambda S, B, r: (f'`[{S.left}, {S.right}]` 只有一个字符' if S.left == S.right else f'`[{S.left}, {S.right}]` 不止一个字符'),
        'f[left][right] = 0': lambda S, B, r: (f'一个字符本身是回文，`f[{S.left}][{S.right}] = 0`' if S.left == S.right else f'两个字符相等，`f[{S.left}][{S.right}] = 0`' if S.right == S.left + 1 else f'`s[{S.left}] = s[{S.right}]`，两端不用删，`f[{S.left}][{S.right}] = f[{S.left + 1}][{S.right - 1}]` = 0'),
        'f[left][right] = 1': '两个字符不同，删一个：`f[{left}][{right}] = 1`',
        'f[left][right] = f[left + 1][right - 1]': '`s[{left}]` = `s[{right}]` = {s[left]}：两端不用删，`f[{left}][{right}] = f[{left+1}][{right-1}]` = =={f[left][right]}==',
        'f[left][right] = min(': '`s[{left}]={s[left]}` ≠ `s[{right}]={s[right]}`：删一端，`min({f[left+1][right]}, {f[left][right-1]}) + 1` = =={f[left][right]}==',
        'break': '`right` 超出末尾，这个长度算完，换下一个长度',
        'return f[0][n - 1] <= k': '`f[0][{n-1}] = {f[0][n-1]}`，`k = {k}`：`{f[0][n-1]} <= {k}` → =={ret}==',
    },
    cards=dict(
        one_liner='看两端：相等不用删，不等删一个，取删得少的',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你字符串 `s` 和整数 `k`，问能否==最多删除 k 个字符==，把 `s` 变成回文串',
                 '能返回 `true`，否则 `false`',
                 '示例：`s = "abcdeca"`，`k = 2` → `true`；本视频：`"abcda"`，`k = 2` → `true`'],
        quote='令f[left][right]表示将字符串中left到right修正成回文串所需的最少操作次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个字符 `f = 0`；两个字符：相等 `0`，不等 `1`',
              '更长的区间：两端相等 `f[left+1][right-1]`；不等则删一端 `min(f[left+1][right], f[left][right-1]) + 1`',
              '算完比较 `f[0][n-1] <= k`',
              '递推要先算短区间，所以外层枚举长度'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：两端不等时要 `+ 1`；`right = left + length - 1` 要判断越界',
                 '原文已是 Python 3 可运行的写法，代码未做改动',
                 '等价于 `n` 减去最长回文子序列的长度（1312 / 516 同类）'],
    ),
)
