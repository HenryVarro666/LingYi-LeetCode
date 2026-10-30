def _lq(S, B, ret):
    return f"`b[{S.pos}] = '{S.b[S.pos]}'` vs `b[{S.index}] = '{S.b[S.index]}'`"


CONFIG = dict(
    num=686, title='重复叠加字符串匹配', difficulty='Medium', category='字符串',
    author='yiduobo', technique='重复 n//m+2 次 · KMP 查找',
    tags=['灵神题单·字符串'],
    code='''
class Solution(object):
    def repeatedStringMatch(self, a, b):

        m = len(a)
        n = len(b)

        k = n // m + 2
        tmp = a * k

        pos = 0
        f = [0]
        for index in range(1, n):
            while pos > 0 and b[pos] != b[index]:
                pos = f[pos - 1]
            if b[pos] == b[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m * k):
            while pos > 0 and b[pos] != tmp[index]:
                pos = f[pos - 1]
            if b[pos] == tmp[index]:
                pos += 1
            if pos == n:
                if index < m * (k - 2):
                    return k - 2
                elif index < m * (k - 1):
                    return k - 1
                else:
                    return k

        return -1
''',
    call='Solution().repeatedStringMatch("abc", "cabca")',
    expect=3,
    views=[
        dict(type='string', var='b', label='b（pos = 已匹配的长度）', pointers={'pos': 'pink'}, cell=70, h=230),
        dict(type='array', var='f', label='f：b 的前缀函数（最长相同前后缀）', cell=70, h=190),
        dict(type='string', var='tmp', label='tmp = a 重复 k 次', pointers={'index': 'blue'}, cell=60, h=230),
        dict(type='text', fn=lambda S: (f"`m = {S['m']}`，`n = {S['n']}`，叠加 `k = n//m + 2 = {S['k']}` 次" if 'k' in S
                                        else '先算要叠加几次'), size=26, h=70),
    ],
    watch=[('m', 'm'), ('n', 'n'), ('k', 'k'), ('pos', 'pos', 'pink'), ('index', 'index', 'blue')],
    captions={
        'm = len(a)': '`m = {m}`，a 的长度',
        'n = len(b)': '`n = {n}`，b 的长度',
        'k = n': '叠加 `n//m + 2 = {n}//{m} + 2 =` =={k}== 次：叠 `n//m+1` 次已比 b 长，再多一份就覆盖了从 a 任意位置开始的长度 n 子串',
        'tmp = a * k': '`tmp = a * {k}` = `{tmp}`，在它里面用 KMP 找 b',
        'pos = 0': '`pos = 0`：当前已匹配的前缀长度',
        'f = [0]': '`f[i]` 记录 `b[0..i]` 的最长相同前后缀长度，`f[0] = 0`',
        'for index in range(1, n)': '求 f：`index = {index}`',
        'while pos > 0 and b[pos] != b[index]': lambda S, B, r: (
            f"`b[{S.pos}] = '{S.b[S.pos]}'` ≠ `b[{S.index}] = '{S.b[S.index]}'` → ==回退== `pos = f[pos-1]`" if S.pos > 0 and S.b[S.pos] != S.b[S.index]
            else '`pos = 0` 或已相等，不用回退'),
        'if b[pos] == b[index]': lambda S, B, r: (
            f"`b[{S.pos}] = '{S.b[S.pos]}'` == `b[{S.index}] = '{S.b[S.index]}'` → `pos` 加一" if S.b[S.pos] == S.b[S.index]
            else f"`b[{S.pos}] ≠ b[{S.index}]`，`pos` 不变"),
        'f.append(pos)': '`f[{index}] = {pos}`',
        'for index in range(m * k)': '在 tmp 里匹配：`index = {index}`',
        'while pos > 0 and b[pos] != tmp[index]': lambda S, B, r: (
            f"`b[{S.pos}] = '{S.b[S.pos]}'` ≠ `tmp[{S.index}] = '{S.tmp[S.index]}'` → 按 f 回退 `pos = f[pos-1]`" if S.pos > 0 and S.b[S.pos] != S.tmp[S.index]
            else '`pos = 0` 或字符相等，不用回退'),
        'if b[pos] == tmp[index]': lambda S, B, r: (
            f"`b[{S.pos}] = '{S.b[S.pos]}'` == `tmp[{S.index}]` → 匹配长度 `pos` 加一" if S.b[S.pos] == S.tmp[S.index]
            else f"`b[{S.pos}] ≠ tmp[{S.index}]`，这一位没匹配上"),
        'if pos == n': lambda S, B, r: (f'`pos = {S.pos} == n`：b 完整出现，匹配结束位置 `index = {S.index}`' if S.pos == S.n
                                         else f'`pos = {S.pos} < n = {S.n}`，还没匹配完'),
        'if index < m * (k - 2)': '`index = {index}` vs `m*(k-2) = {m*(k-2)}`：结束在前 `k-2` 份之内才只需 `k-2` 份',
        'elif index < m * (k - 1)': '`index = {index}` vs `m*(k-1) = {m*(k-1)}`：不在前 `k-2` 份、但在前 `k-1` 份内 → 需要 `k-1` 份',
        'return k - 2': '需要 `{k-2}` 份',
        'return k - 1': '需要 `{k-1}` 份',
        'return k\n': '结束位置落在最后一份里，需要全部 `{k}` 份',
        'return -1': '整个 tmp 都找不到 b → `-1`',
    },
    cards=dict(
        one_liner='叠够 n//m+2 份，KMP 找 b 的位置，再按结束位置数份数',
        complexity='时间 `O(n + m·k)`，空间 `O(m·k)`',
        problem=['把字符串 `a` 重复叠加若干次，使 `b` 成为它的子串，求最少叠加次数',
                 '不可能则返回 `-1`',
                 '本视频：`a = "abc"`，`b = "cabca"` → `3`'],
        quote='若b是a\'的子串，那么b必然属于其中之一。',
        quote_src='—— yiduobo 题解原文',
        idea=['叠 `n/m + 1` 次后长度已超过 b，再补一份 a，就能覆盖从 a 任意字符开始的长度 n 子串',
              '所以只要叠 `n/m + 2` 次，b 能匹配就一定匹配得上',
              '用 KMP 找 b 第一次出现的结束位置，看它落在第几份里，就知道要叠几次'],
        summary=['时间 `O(n + m·k)`，空间 `O(m·k)`',
                 '易错：结束位置按 `index` 与 `m*(k-2)`、`m*(k-1)` 比较，分成 `k-2`、`k-1`、`k` 三档',
                 '原文为 Python 2 写法，整数除法 `n / m` 已改为 `n // m`',
                 '同类：灵神也用 KMP，题解里先叠到长度 ≥ n 再多叠一份'],
    ),
)
