S1, S2, S3 = 'abc', 'bd', 'abbdc'


def _color(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    ln = S.get('_line')
    if isinstance(i, int) and isinstance(j, int) and ln is not None and ln >= 10:
        if (r, c) == (i - 1, j):
            return 'blue'                            # 上：第 i+j 位由 s1 的第 i 位匹配
        if (r, c) == (i, j - 1):
            return 'pink'                            # 左：由 s2 的第 j 位匹配
    return 'green' if v is True else None


def _k3(S):
    i, j = S.get('i'), S.get('j')
    if isinstance(i, int) and isinstance(j, int) and i + j > 0:
        return i + j - 1
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if not isinstance(j, int):
        return '`f[i][j]`：`s1` 的==前 i 位==与 `s2` 的==前 j 位==交错后，能否构成 `s3` 的前 `i+j` 位'
    if i == 0 and j == 0:
        return '情况 1：`i = j = 0`，三个串都为空 → `True`'
    if i == 0:
        return f'情况 2：`i = 0`，只能由 s2 匹配：看左边 + `s2[{j - 1}]` vs `s3[{j - 1}]`'
    if j == 0:
        return f'情况 3：`j = 0`，只能由 s1 匹配：看上边 + `s1[{i - 1}]` vs `s3[{i - 1}]`'
    return f'情况 4：`s3` 第 `{i + j}` 位 ← s1 第 `{i}` 位（上）或 s2 第 `{j}` 位（左）'


def _elif0(S, B, ret):
    i, j, f = S.i, S.j, S.f
    if f[i][j - 1] and S2[j - 1] == S3[j - 1]:
        return f'左边 `f[0][{j - 1}]` 为 True，且 `s2[{j - 1}] = s3[{j - 1}] = {S2[j - 1]}` → 成立'
    if not f[i][j - 1]:
        return f'左边 `f[0][{j - 1}]` 已经是 False → 不成立，`f[0][{j}]` 保持 False'
    return f'`s2[{j - 1}] = {S2[j - 1]}` ≠ `s3[{j - 1}] = {S3[j - 1]}` → 不成立，保持 False'


def _col0(S, B, ret):
    i, f = S.i, S.f
    if f[i - 1][0] and S1[i - 1] == S3[i - 1]:
        return f'上边 `f[{i - 1}][0]` 为 True，且 `s1[{i - 1}] = s3[{i - 1}] = {S1[i - 1]}` → 成立'
    if not f[i - 1][0]:
        return f'上边 `f[{i - 1}][0]` 已经是 False → 不成立，保持 False'
    return f'`s1[{i - 1}] = {S1[i - 1]}` ≠ `s3[{i - 1}] = {S3[i - 1]}` → 不成立，保持 False'


def _both(S, B, ret):
    i, j, f = S.i, S.j, S.f
    k = i + j - 1
    up = f[i - 1][j] and S1[i - 1] == S3[k]
    left = f[i][j - 1] and S2[j - 1] == S3[k]
    if up:
        return f's1 匹配：上边 `f[{i - 1}][{j}]` 为 True 且 `s1[{i - 1}] = s3[{k}] = {S3[k]}` → ==成立=='
    if left:
        return f's1 匹配不行；s2 匹配：左边 `f[{i}][{j - 1}]` 为 True 且 `s2[{j - 1}] = s3[{k}] = {S3[k]}` → ==成立=='
    return f'`s3[{k}] = {S3[k]}`：上边、左边两种匹配都不行 → `f[{i}][{j}]` 保持 False'


def _set(S, B, ret):
    i, j = S.i, S.j
    if i == 0 and j == 0:
        return '`f[0][0] = True`：s1、s2、s3 都为空'
    return f'`f[{i}][{j}] = True`：s1 前 `{i}` 位 + s2 前 `{j}` 位 能拼出 `s3[:{i + j}] = "{S3[:i + j]}"`'


CONFIG = dict(
    num=97, title='交错字符串', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='前缀匹配 DP · 四种情况',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def isInterleave(self, s1, s2, s3):
        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False

        f = [[False] * (n + 1) for index in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = True
                    elif f[i][j - 1] and s2[j - 1] == s3[j - 1]:
                        f[i][j] = True
                else:
                    if j == 0:
                        if f[i - 1][j] and s1[i - 1] == s3[i - 1]:
                            f[i][j] = True
                    elif (f[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (f[i][j - 1] and s2[j - 1] == s3[i + j - 1]):
                        f[i][j] = True

        return f[m][n]
''',
    call=f'Solution().isInterleave({S1!r}, {S2!r}, {S3!r})',
    expect=True,
    skip=['n = len(s2)', 'for j in range', 'if i == 0', 'if j == 0'],
    views=[
        dict(type='text', fn=_formula, h=84, size=24),
        dict(type='string', var='s3', label='s3（黄 = 这一格要匹配的第 i+j 位）', cell=72,
             color=lambda S, i, v: 'yellow' if i == _k3(S) else None,
             dim=lambda S, i, v: _k3(S) is not None and i > _k3(S)),
        dict(type='table', var='f', label='f[i][j]（行 = s1 前 i 位，列 = s2 前 j 位；蓝 上 · 粉 左）',
             rows=lambda S: ['∅'] + list(S1), cols=lambda S: ['∅'] + list(S2),
             cursors=[('i', 'j', 'yellow')], color=_color, cell=96, h=440),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('f[m][n]', 'f[m][n]', 'green')],
    captions={
        'm = len(s1)': '`m = {m}`，`n = {len(s2)}`（注意：这里 ==m 是 s1 的长度==，n 是 s2 的长度）',
        'if m + n != len(s3)': '`{m} + {n} = {len(s3)}`：长度相等才可能交错组成',
        'f = [[False]': '`f` 开 `(m+1) × (n+1)`，全部先填 False',
        'for i in range': lambda S, B, ret: (f'第 `i = {S.i}` 行：s1 用前 `{S.i}` 位' if S.get('i') != B.get('i')
                                             else '全部格子算完'),
        'f[i][j] = True': _set,
        'elif f[i][j - 1] and s2[j - 1] == s3[j - 1]': _elif0,
        'if f[i - 1][j] and s1[i - 1] == s3[i - 1]': _col0,
        'elif (f[i - 1][j]': _both,
        'return f[m][n]': '`f[m][n]`：s1、s2 全部用完，能否拼出整个 s3 → =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j]：s1 前 i 位和 s2 前 j 位，能否交错拼出 s3 前 i+j 位',
        complexity='时间 `O(mn)`，空间 `O(mn)`（滚动数组可到 `O(min(m, n))`）',
        problem=['判断 `s3` 能否由 `s1` 和 `s2` ==交错==组成（各自字母的相对顺序不变）',
                 '示例：`"aabcc"`、`"dbbca"` → `"aadbbcbcac"`：`true`',
                 '本视频：`s1 = "abc"`，`s2 = "bd"`，`s3 = "abbdc"` → `true`'],
        quote='与串有关的问题中，涉及到位置匹配的，大多数都是动态规划去解决，状态也一般是==某个串的前i位与某个串的前j位满足XXXX==。',
        quote_src='—— yiduobo 题解',
        idea=['情况 1：`i = j = 0`，都为空 → True',
              '情况 2 / 3：只有一个串可用，看左边（或上边）是否为 True 且当前字母相同',
              '情况 4：`s3` 第 `i+j` 位由 s1 第 i 位或 s2 第 j 位匹配，==有一个成立即可=='],
        result='`f[3][2] = True`：`"abc"` 和 `"bd"` 能交错拼出 `"abbdc"` ✓',
        summary=['时间 `O(mn)`，空间 `O(mn)`；滚动数组可优化到 `O(min(m, n))`',
                 '下标：f 用「前 i 位」，所以字母是 `s1[i-1]`、`s2[j-1]`、`s3[i+j-1]`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神从右往左想 `dfs(i,j)` 再 1:1 翻译成递推；yiduobo 直接按前缀分四种情况'],
    ),
)
