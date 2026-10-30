def _ok(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9')


def _color(S, i, v):
    if 'r' not in S:
        return None
    if i == S['l']:
        return 'blue'
    if i == S['r']:
        return 'pink'
    if (i < S['l'] or i > S['r']) and _ok(v):
        return 'green'
    return None


def _dim(S, i, v):
    return 'r' in S and (i < S['l'] or i > S['r']) and not _ok(v)


def _text(S):
    if 'ascii_l' in S and 'ascii_r' in S and 20 <= S.get('_line', 0) <= 28:
        return f"统一成大写再比：`{S['ascii_l']}`（{chr(S['ascii_l'])}） vs `{S['ascii_r']}`（{chr(S['ascii_r'])}）"
    return '`A` = 65，`a` = 97，==相差 32=='


def _cap_outer(S, B, ret):
    if B.l < B.r:
        return f'`l = {B.l} < r = {B.r}`：继续往中间扫'
    return f'`l = {B.l}`，`r = {B.r}`：两指针相遇 → 扫描结束'


def _cap_wl(S, B, ret):
    if B.l < B.r:
        return f'内层循环：找左边下一个有效字符（`l < r` 才找）'
    return '`l == r`：左指针已经追上右指针，停止跳过'


def _cap_if_l(S, B, ret):
    c = S.s[S.l]
    if _ok(c):
        return f'`s[{S.l}] = "{c}"` 是字母或数字 → `break`，左边找到了'
    return f'`s[{S.l}] = "{c}"` 是==无关字符== → 跳过'


def _cap_wr(S, B, ret):
    if B.l < B.r:
        return f'再找右边的有效字符'
    return '`l == r`：不用再找右边了'


def _cap_if_r(S, B, ret):
    c = S.s[S.r]
    if _ok(c):
        return f'`s[{S.r}] = "{c}"` 是字母或数字 → `break`，右边也找到了'
    return f'`s[{S.r}] = "{c}"` 是==无关字符== → 跳过'


def _cap_eq(S, B, ret):
    if S.l == S.r:
        return f'`l == r = {S.l}`：中间只剩（或没剩）一个字符，不用比 → `break`'
    return f'`l = {S.l}`，`r = {S.r}`：两边都停在有效字符上，开始比较'


def _cap_al(S, B, ret):
    c = S.s[S.l]
    return f'`ord("{c}") = {ord(c)}`'


def _cap_if_al(S, B, ret):
    if S.ascii_l >= 97:
        return f'`{S.ascii_l} ≥ 97`：是==小写字母== → 要减 32 变成大写'
    return f'`{S.ascii_l} < 97`：大写字母或数字，保持不变'


def _cap_if_ar(S, B, ret):
    if S.ascii_r >= 97:
        return f'`{S.ascii_r} ≥ 97`：是==小写字母== → 减 32'
    return f'`{S.ascii_r} < 97`：保持不变'


CONFIG = dict(
    num=125, title='验证回文串', difficulty='Easy', category='双指针',
    author='yiduobo', technique='双指针 + ASCII 码统一大小写',
    tags=['热题173', '面试经典150'],
    code='''
class Solution(object):
    def isPalindrome(self, s):
        l = 0
        r = len(s) - 1

        while l < r:
            while l < r:
                if (s[l] >= 'a' and s[l] <= 'z') or (s[l] >= 'A' and s[l] <= 'Z') or (s[l] >= '0' and s[l] <= '9'):
                    break
                l += 1

            while l < r:
                if (s[r] >= 'a' and s[r] <= 'z') or (s[r] >= 'A' and s[r] <= 'Z') or (s[r] >= '0' and s[r] <= '9'):
                    break
                r -= 1

            if l == r:
                break

            ascii_l = ord(s[l])
            if ascii_l >= 97:
                ascii_l -= 32
            ascii_r = ord(s[r])
            if ascii_r >= 97:
                ascii_r -= 32

            if ascii_l != ascii_r:
                return False

            l += 1
            r -= 1

        return True
''',
    call='Solution().isPalindrome("Ab, B!a")',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', label='s（绿 = 已配对，灰 = 跳过的无关字符）', cell=100,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), color=_color, dim=_dim, h=260),
        dict(type='map', var=lambda S: ({'ascii_l': S['ascii_l']} if 'ascii_l' in S else {}) |
                                     ({'ascii_r': S['ascii_r']} if 'ascii_r' in S else {}) if 'r' in S else None,
             label='ASCII 码（小写字母会被减 32）', h=110, font=28),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'ascii_l', 'ascii_r'],
    skip=[3, 9, 14],
    captions={
        'r = len(s) - 1': '两个指针 `l = 0`、`r = {r}`，从两端往中间扫',
        'l = 0': '左指针 `l = 0`',
        6: _cap_outer,
        7: _cap_wl,
        "if (s[l] >= 'a'": _cap_if_l,
        9: '`break`：停在 `s[{l}]`',
        'l += 1': lambda S, B, ret: f'`l` → {S.l}' if S._line == 10 else f'这一对配好了，两个指针往中间走：`l` → {S.l}',
        12: _cap_wr,
        "if (s[r] >= 'a'": _cap_if_r,
        14: '`break`：停在 `s[{r}]`',
        'r -= 1': '`r` → {r}',
        'if l == r': _cap_eq,
        18: '`break` 跳出外层循环',
        'ascii_l = ord': _cap_al,
        'if ascii_l >= 97': _cap_if_al,
        'ascii_l -= 32': '`{B.ascii_l} − 32 = {ascii_l}`，即 `"{chr(ascii_l)}"`',
        'ascii_r = ord': lambda S, B, ret: f'`ord("{S.s[S.r]}") = {S.ascii_r}`',
        'if ascii_r >= 97': _cap_if_ar,
        'ascii_r -= 32': '`{B.ascii_r} − 32 = {ascii_r}`，即 `"{chr(ascii_r)}"`',
        'if ascii_l != ascii_r': lambda S, B, ret: (f'`{S.ascii_l}` 和 `{S.ascii_r}` 相等：统一大小写后==相同== → 这一对配对成功'
                                                     if S.ascii_l == S.ascii_r else
                                                     f'`{S.ascii_l} ≠ {S.ascii_r}` → 不是回文'),
        'return False': '对称位置不同 → 返回 ==False==',
        'return True': '没有发现不同的一对 → 返回 ==True==',
    },
    cards=dict(
        one_liner='两个指针往中间扫，跳过无关字符，用 ASCII 码统一大小写再比',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['大写转小写、去掉所有==非字母数字==字符后，正读反读都一样 → 回文串',
                 '示例：`"A man, a plan, a canal: Panama"` → `true`',
                 '演示：`"Ab, B!a"` → 有效字符 `AbBa`，忽略大小写是回文 → `true`'],
        quote='用两个指针left与right从两端往中间扫，跳过无关的字符……若某个字符将位于a到z之间，那么将其==ascii码减去32==然后再进行对比即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个内层 `while`：分别把 `l`、`r` 推到下一个字母或数字上',
              '`A` 是 65、`a` 是 97，==相差 32==：小写字母减 32 就和大写一样',
              '数字的 ASCII 都小于 97，不受影响'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '内层循环也要判断 `l < r`，否则全是标点时会越界',
                 '`if l == r: break`：指针相遇时中间那个字符不用比',
                 '`>= 97` 判断成立的前提：此时已确认是字母数字，所以只会是小写字母',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：用 `isalnum()` + `lower()`，更简洁'],
    ),
)
