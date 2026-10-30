S0 = 'abbc'


def _phase2(S):
    return 'p1' in S


def _f_color(S, r, c, v):
    if 'p1' in S:
        p1, p2, n = S['p1'], S.get('p2'), len(S['s'])
        if (r, c) == (0, p1):
            return 'blue'
        if p2 is not None and (r, c) == (p1 + 1, p2):
            return 'pink'
        if p2 is not None and (r, c) == (p2 + 1, n - 1):
            return 'purple'
        return 'green' if v else None
    if 'left' in S and 'right' in S and (r, c) == (S['left'], S['right']) and r <= c < len(S['s']) and S.get('_line') in (11, 14, 16, 18):
        return 'yellow'
    return 'green' if v else None


def _s_color(S, i, v):
    if 'p1' in S:
        p1, p2 = S['p1'], S.get('p2')
        if i <= p1:
            return 'blue'
        if p2 is not None:
            return 'pink' if i <= p2 else 'purple'
        return None
    if 'left' in S and 'right' in S and S.get('l') and S['left'] <= i <= S['right'] < len(S['s']):
        return 'yellow'
    return None


def _txt(S):
    ln = S.get('_line', 0)
    if 'p1' in S:
        n, p1, p2 = len(S['s']), S['p1'], S.get('p2')
        s = S['s']
        if p2 is None:
            return f"第一段 `s[0..{p1}]` = \"{s[:p1 + 1]}\"：{'==是回文==，继续找第二、三段' if S['f'][0][p1] else '不是回文，换下一个 p1'}"
        return f"`\"{s[:p1 + 1]}\"` + `\"{s[p1 + 1:p2 + 1]}\"` + `\"{s[p2 + 1:]}\"`：" + ('==三段都是回文==' if S['f'][p1 + 1][p2] and S['f'][p2 + 1][n - 1] else '后两段不全是回文')
    if 'left' in S and 'right' in S and 'l' in S and S['right'] < len(S['s']) and S['right'] >= S['left']:
        return f"区间 `s[{S['left']}..{S['right']}]`（长度 {S['l']}）是不是回文？"
    return '`f[left][right]` = `s[left..right]` 是否回文（T / F）'


CONFIG = dict(
    num=1745, title='分割回文串 IV', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间回文表 + 枚举两个切点',
    tags=['灵神题单·动态规划', '灵神题单·字符串'],
    code='''
class Solution(object):
    def checkPartitioning(self, s):

        n = len(s)
        f = [[False] * n for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n):
                right = left + l - 1
                if left + l - 1 >= n:
                    continue
                if l == 1:
                    f[left][right] = True
                elif l == 2:
                    if s[left] == s[right]:
                        f[left][right] = True
                    else:
                        f[left][right] = False
                else:
                    f[left][right] = f[left + 1][right - 1] and s[left] == s[right]
        
        for p1 in range(n - 2):
            if f[0][p1]:
                for p2 in range(p1 + 1, n - 1):
                    if f[p1 + 1][p2] and f[p2 + 1][n - 1]:
                        return True
        
        return False
''',
    call=f'Solution().checkPartitioning({S0!r})',
    expect=True,
    skip=['for left in range', 'right = left + l - 1', 'continue', 'if left + l - 1 >= n'],
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s（黄 = 正在判断的区间；后面蓝 / 粉 / 紫 = 三段）', h=150, cell=80, color=_s_color),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='table', var='f', label='f[left][right]：s[left..right] 是否回文（T 绿色）', h=360, cell=64,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0)], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             color=_f_color),
    ],
    watch=[('l', 'l', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('p1', 'p1', 'blue'), ('p2', 'p2', 'purple')],
    captions={
        'f = [[False]': '`f[left][right]` 先全设成 `False`',
        'for l in range': lambda S, B, ret: (f'按区间长度 `l = {S.l}` 从小到大算：长区间依赖里面更短的区间' if S.get('l') != B.get('l') or 'l' not in B else '所有长度都算完了'),
        'if l == 1': '`l = {l}`：{"单个字符一定是回文" if l == 1 else "长度不是 1，继续看"}',
        'f[left][right] = True': lambda S, B, ret: (f'`f[{S.left}][{S.right}]` = ==True==：' + ('单个字符是回文' if S.l == 1 else f'两个字符 `{S.s[S.left]}` = `{S.s[S.right]}` 相同')),
        'elif l == 2': '`l = {l}`：{"只要两个字符相同就是回文" if l == 2 else "长度 ≥ 3，要看里面"}',
        'if s[left] == s[right]': '`s[{left}] = {s[left]}`，`s[{right}] = {s[right]}` → {"相等" if s[left] == s[right] else "不等"}',
        'f[left][right] = False': '`f[{left}][{right}]` = ==False==：两端不同',
        'f[left][right] = f[left + 1]': '两端 `{s[left]}`、`{s[right]}` {"相同" if s[left] == s[right] else "不同"}，里面 `f[{left + 1}][{right - 1}]` = {f[left+1][right-1]} → `f[{left}][{right}]` = =={f[left][right]}==',
        'for p1 in range': lambda S, B, ret: (f'枚举第一段的右边界 `p1 = {S.p1}`' if S.get('p1') != B.get('p1') or 'p1' not in B else '没有任何切法 → False'),
        'if f[0][p1]': '第一段 `s[0..{p1}]` {"是回文，继续" if f[0][p1] else "不是回文，换下一个 p1"}',
        'for p2 in range': lambda S, B, ret: (f'枚举第二段的右边界 `p2 = {S.p2}`，三段是 `[0,{S.p1}]`、`[{S.p1 + 1},{S.p2}]`、`[{S.p2 + 1},{len(S.s) - 1}]`' if S.get('p2') != B.get('p2') or B.get('_line') == 22 else '这个 p1 下没有合适的 p2'),
        'if f[p1 + 1][p2] and': '第二段 `f[{p1 + 1}][{p2}]` = {f[p1+1][p2]}，第三段 `f[{p2 + 1}][{len(s) - 1}]` = {f[p2+1][len(s)-1]} → {"都是回文" if f[p1+1][p2] and f[p2+1][len(s)-1] else "不满足"}',
        'return True': '三段都是回文 → 返回 `True`',
        'return False': '所有切法都试过了 → 返回 `False`',
    },
    cards=dict(
        one_liner='先把所有区间的回文性查成表，再枚举两个切点',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给你字符串 `s`，能否分成 ==三个非空回文子串==',
                 '示例：`"abcbdd"` → `true`（`"a"+"bcb"+"dd"`）',
                 '本视频：`"abbc"` = `"a"` + `"bb"` + `"c"` → `true`'],
        quote='令f[l][r]表示l到r这一段是否为回文串……这样一来，就可以在O(n^2)的时间复杂度得到f。接下来只需要枚举第一个回文串的右边界p1以及第二个回文串的右边界p2。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 `l` 从小到大填表：1 个字符一定回文，2 个字符看是否相同',
              '更长的区间：==两端相同 且 里面是回文==',
              '枚举 `p1`、`p2` 切成三段，查表即可，`O(n^2)`'],
        result='找到 `"a"` + `"bb"` + `"c"` → True ✓',
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：`p1` 到 `n - 3`、`p2` 到 `n - 2`，保证三段都非空',
                 '作者提到：Manacher 能 `O(n)` 求回文，但三个中心不单调，没想出 `O(n)` 解',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
