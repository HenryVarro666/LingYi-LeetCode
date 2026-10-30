S0, SH = 'abcd', [3, 5, 9, 12]


def _res_aligned(S):
    """res 是倒着收集的：把它按原位置摆放，已经算好的字母在右边，往左长"""
    n = len(S['S'])
    res = S['res']
    return ['·'] * (n - len(res)) + res[::-1]


def _done(S, i):
    return 'index' in S and (i > S['index'] or (i == S['index'] and S['_line'] >= 9))


def _text(S, B):
    if 'now' not in S or 'index' not in S:
        return '第 `i` 个移位会作用到前 `i + 1` 个字母 → 字母 `S[k]` 的总移位次数 = ==`shifts[k:]` 的后缀和=='
    ln, i = S['_line'], S['index']
    if ln == 8:
        raw = B['now'] + S['shifts'][i]
        return f'`now = ({B["now"]} + {S["shifts"][i]}) % 26` = `{raw} % 26` = =={S["now"]}==（`shifts[{i}:]` 的后缀和对 26 取模）'
    if ln == 9:
        c = S['S'][i]
        v = ord(c) - 97 + S['now']
        return f"`'{c}'` 是第 `{ord(c) - 97}` 个字母，加上 `now = {S['now']}` → `{v} % 26 = {v % 26}` → ==`'{chr(v % 26 + 97)}'`=="
    return f'`now` 是 `shifts[{i}:]` 的后缀和（模 26），当前字母 `S[{i}] = \'{S["S"][i]}\'`'


CONFIG = dict(
    num=848, title='字母移位', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='后缀和 · 从后往前扫描',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def shiftingLetters(self, S, shifts):

        n = len(S)
        res = []
        now = 0
        for index in range(n - 1, -1, -1):
            now = (now + shifts[index]) % 26
            res.append(chr((ord(S[index]) - 97 + now) % 26 + 97))

        return ''.join(res[::-1])
''',
    call=f'Solution().shiftingLetters({S0!r}, {SH})',
    expect='dbxp',
    views=[
        dict(type='text', fn=_text, h=90, size=26),
        dict(type='string', var='S', label='S（蓝 = 当前字母，暗 = 已经移好位）', cell=96,
             pointers={'index': 'blue'}, color=lambda S, i, v: 'blue' if i == S.get('index') and not _done(S, i) else None,
             dim=lambda S, i, v: _done(S, i), h=190),
        dict(type='array', var='shifts', label='shifts（框 = shifts[index:]，这些移位都会作用到 S[index]）', cell=96,
             window=('index', lambda S: len(S['shifts']) - 1),
             color=lambda S, i, v: 'green' if 'index' in S and i >= S['index'] else None, h=190),
        dict(type='array', var=_res_aligned, label='res 倒着收集，这里按原位置摆放（从右往左长）', cell=96, index=False,
             color=lambda S, i, v: 'cyan' if v != '·' else None, h=140),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'green'), ('res', 'res', 'cyan')],
    captions={
        'n = len(S)': '字符串长度 `n = {n}`',
        'res = []': '`res` 用来==倒着==收集移位后的字母，最后再反转',
        'now = 0': '`now`：当前字母总共要移位的次数（对 26 取模），也就是 `shifts` 的==后缀和==',
        'for index in range': lambda S, B, r: ('`index` 已经走完 0，退出循环' if 'index' in B and B.index == S.index and S.index == 0
                                               else f'从后往前扫，`index = {S.index}`：`S[{S.index}]` 要被 `shifts[{S.index}]` 及后面所有移位影响'),
        'now = (now + shifts': lambda S, B, r: (f'`now = ({B.now} + {S.shifts[S.index]}) % 26 = {S.now}`：累加成后缀和，每个字母的总移位次数就有了'
                                                + ('；==刚好绕了一整圈 26，等于不动==' if S.now == 0 and B.now + S.shifts[S.index] > 0 else '')),
        'res.append': lambda S, B, r: (f"`S[{S.index}] = '{S.S[S.index]}'` 移 `{S.now}` 次：`({ord(S.S[S.index]) - 97} + {S.now}) % 26 = {(ord(S.S[S.index]) - 97 + S.now) % 26}`"
                                       f" → `'{S.res[-1]}'`，追加到 `res`"),
        "return ''.join": '`res` 是从后往前收集的，==反转==再拼起来：`"{ret}"`',
    },
    cards=dict(
        one_liner='第 i 个字母总共被移位 shifts[i:] 的和次：从后往前累加后缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `S` 和整数数组 `shifts`：对每个 `shifts[i] = x`，把 `S` 的前 `i + 1` 个字母各移位 `x` 次',
                 '移位 = 变成字母表里的下一个字母，`z` 的下一个是 `a`；返回最终的字符串',
                 '示例：`S = "abc"`，`shifts = [3,5,9]` → `"rpl"`；本视频：`"abcd"`，`[3,5,9,12]` → `"dbxp"`'],
        quote='可以发现，这里每个字母的总移位实际上是一个后缀和问题，于是我们可以转换思路，从后往前一趟扫描，每次先按后缀和的方式计算移位的值，然后对当前字母进行移位。',
        quote_src='—— yiduobo 题解原文',
        idea=['看样例：`a` 被移 `3 + 5 + 9` 次，`b` 被移 `5 + 9` 次，`c` 被移 `9` 次',
              '每个字母的总次数就是 `shifts[i:]` 的==后缀和==，不用真的移很多遍',
              '从后往前扫，`now` 累加 `shifts[index]`，再移当前字母 `now` 次',
              '`now` 对 26 取模：移 26 次回到原位'],
        result='`a` 移 29 次 = 3，`b` 移 26 次 = 0，`c` 移 21 次，`d` 移 12 次 → `"dbxp"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（`res` 列表）',
                 '`now` 要取模，不然后缀和会很大；字母的下标 `ord(c) - 97` 加 `now` 后再模一次',
                 '`res` 是倒着加的，最后一定要 `[::-1]` 反转',
                 '原文是 Python 2 风格写法，但在 Python 3 下可直接运行，代码未做改动',
                 '同类：前缀 / 后缀和把「前 i 个都受影响」的操作合并成一次扫描'],
    ),
)
