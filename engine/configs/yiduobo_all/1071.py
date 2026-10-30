def _t(S):
    if 'l' in S and 'o' in S and 'tmp' not in S:
        return f"求 `len(str1)` 与 `len(str2)` 的最大公约数：`l = {S['l']}`，`o = {S['o']}`" + ('，o 为 0 → ==l 就是 gcd==' if S['o'] == 0 else '')
    if 'tmp' in S:
        return f"拼出的 `tmp = {S['tmp']}`（候选公因子 `{S['str1'][:S['l']]}` 重复拼成）"
    return '最大公因子的长度，必然是两个字符串长度的最大公约数'


CONFIG = dict(
    num=1071, title='字符串的最大公因子', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='长度的最大公约数 + 拼接验证',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def gcdOfStrings(self, str1, str2):

        m = len(str1)
        n = len(str2)

        l, o = m, n
        while o:
            l, o = o, l % o
        
        if m < n:
            tmp = str1[:l] * (m // l)
            if tmp != str1:
                return ''
            tmp += str1[:l] * ((n - m) // l)
            if tmp == str2:
                return str1[:l]
            else:
                return ''
        else:
            tmp = str1[:l] * (n // l)
            if tmp != str2:
                return ''
            tmp += str1[:l] * ((m - n) // l)
            if tmp == str1:
                return str1[:l]
            else:
                return ''
''',
    call="Solution().gcdOfStrings('ABABAB', 'ABAB')",
    expect='AB',
    views=[
        dict(type='string', var='str1', h=170, label='str1'),
        dict(type='string', var='str2', h=170, label='str2'),
        dict(type='text', fn=_t, h=120),
    ],
    watch=['m', 'n', 'l', 'o', 'tmp'],
    captions={
        'm = len': '`m = len(str1) = {m}`',
        'n = len': '`n = len(str2) = {n}`。设公因子 P，则 str1 = P×(m/len P)，str2 = P×(n/len P)',
        'l, o = m, n': '`l, o = {l}, {o}`：用辗转相除求 `len(str1)` 与 `len(str2)` 的最大公约数',
        'while o': '`o = {o}`：不为 0 就继续',
        'l, o = o, l % o': '辗转相除：`(l, o)` → `({l}, {o})`',
        'if m < n': '`m = {m}`，`n = {n}`：`m < n` → {m < n}。先拿短的那条去验证，再补上长度差',
        'tmp = str1[:l] * (m': '候选公因子 `P = str1[:{l}] = {str1[:l]}`；重复 `m // l` 次，看能否拼成 str1：`tmp = {tmp}`',
        'tmp = str1[:l] * (n': '候选公因子 `P = str1[:{l}] = {str1[:l]}`；重复 `n // l` 次，看能否拼成 str2：`tmp = {tmp}`',
        'if tmp != str1': lambda S, B, r: ('`tmp != str1`：P 拼不出 str1 → 无公因子，返回空串' if S.tmp != S.str1 else '`tmp == str1`：P 能拼出 str1，继续验证 str2'),
        'if tmp != str2': lambda S, B, r: ('`tmp != str2`：P 拼不出 str2 → 无公因子，返回空串' if S.tmp != S.str2 else '`tmp == str2`：P 能拼出 str2（较短的串），继续把差的部分补上去验证较长的串'),
        'tmp += str1[:l] * ((n': '再补 `(n - m) // l` 个 P，得到 `tmp = {tmp}`，它应该等于 str2',
        'tmp += str1[:l] * ((m': '再补 `(m - n) // l` 个 P，得到 `tmp = {tmp}`，它应该等于 str1',
        'if tmp == str2': lambda S, B, r: ('`tmp == str2`：两个串都由 P 拼成 → 答案是 P' if S.tmp == S.str2 else '`tmp != str2`：不成立 → 返回空串'),
        'if tmp == str1': lambda S, B, r: ('`tmp == str1`：两个串都由 P 拼成 → 答案是 P' if S.tmp == S.str1 else '`tmp != str1`：不成立 → 返回空串'),
        'return str1[:l]': '返回最大公因子 `{str1[:l]}`',
    },
    cards=dict(
        one_liner='公因子长度 = 两个长度的最大公约数，再拼接验证',
        complexity='时间 `O(m + n)`，空间 `O(m + n)`',
        problem=['若字符串 `t` 重复若干次能得到 `s`，就说 `t` 能除尽 `s`',
                 '给两个字符串，返回能同时除尽它们的最长字符串，没有则返回空串',
                 '示例：`str1 = ABABAB`，`str2 = ABAB` → `AB`'],
        quote='len(P)必然是len(str1)和len(str2)的最大公约数，设其为l。求出l之后，还需判断str1[:l] * m是否等于str1，且str1[:l] * n是否等于str2即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 P 是最大公因子：`str1 = P×m`，`str2 = P×n`',
              '若 `m`、`n` 有公约数 k，答案就该是 `kP`，与 P 最大矛盾 → ==m、n 互质==',
              '所以 `len(P) = gcd(len(str1), len(str2))`，只要验证 `str1[:l]` 能拼出两个串'],
        summary=['时间 `O(m + n)`，空间 `O(m + n)`',
                 '易错：只取 str1 的前 `l` 个字符当候选，另一个串靠拼接验证',
                 '代码先拼较短的串，再补长度差拼成较长的串，省去一次重复拼接',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
