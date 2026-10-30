def _b8(x):
    return format(x & 0xFF, '08b')


def _cmp(S):
    s, i = S.get('s'), S.get('i')
    if s is None or i is None:
        return ''
    j = len(s) - 1 - i
    a, b = ord(s[i]), ord(s[j])
    ln = S['_line']
    fr = S['_inner']
    if ln in (6, 7, 8) and 'n' in fr and 'i' not in fr:
        return f"正在反转 `s[{i}] = '{s[i]}'` 的 8 位：`{_b8(fr['n'])}`"
    r = 0
    for k in range(8):
        r |= (a >> k & 1) << (7 - k)
    return (f"`'{s[i]}'` = `{_b8(a)}`，反转后 `{_b8(r)}`；`'{s[j]}'` = `{_b8(b)}`　"
            + ('==相等==' if r == b else '==不等=='))


def _top(S):
    if 's' not in S:
        return ''
    return "二进制回文：`s[i]` 的 8 位反转，必须等于对称位置 `s[-1-i]` 的 8 位"


CONFIG = dict(
    num=4030, title='判断 ASCII 值回文', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='不拼字符串 · 逐字符位反转',
    tags=['灵神题单', '位运算', '难度分 1165'],
    code='''
m0 = 0b01010101
m1 = 0b00110011
m2 = 0b00001111

def reverseBits(n: int) -> int:
    n = n >> 1 & m0 | (n & m0) << 1  # 交换相邻位
    n = n >> 2 & m1 | (n & m1) << 2  # 两个两个交换
    return n >> 4 | (n & m2) << 4  # 交换高低 4 位

class Solution:
    def isPalindromic(self, s: str) -> bool:
        for i in range(len(s) // 2 + 1):
            if reverseBits(ord(s[i])) != ord(s[-1 - i]):
                return False
        return True
''',
    call='Solution().isPalindromic("fnvf")',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（蓝 = s[i]，粉 = s[-1-i]）', cell=110, pointers={'i': 'blue', 'len(s) - 1 - i': 'pink'},
             pointer_labels={'i': 'i', 'len(s) - 1 - i': '-1-i'}, h=260),
        dict(type='text', fn=_cmp, size=26, h=110),
    ],
    watch=[('i', lambda S: S.get('i'), 'blue')],
    captions={
        'for i in range': lambda S, B, r: ('`i` 从 0 扫到 `len(s)//2`：对称位置两两比较（连中间那个也比，它和自己比）' if 'i' not in B or S.get('i') == 0 and 'i' not in B else (f"`i` → {S.i}，换下一对" if S.get('i') != B.get('i') else '`i` 已扫完，没有发现不满足的一对')),
        'return False': '`s[{i}]` 反转后和对称位置的字符不同 → 整个二进制串不是回文，返回 `False`',
        'return True': '每一对都满足「反转后相等」→ 整个 8 位二进制串是回文，返回 `True`',
        'if reverseBits': lambda S, B, r: f"比较 `reverseBits('{S.s[S.i]}')` 与对称字符 `'{S.s[-1 - S.i]}'`（`{_b8(ord(S.s[-1 - S.i]))}`）：先把 `s[{S.i}]` 的 8 位反转，看下面 3 步",
        'n >> 1 & m0': lambda S, B, r: f"相邻两位互换：`{_b8(B.n)}` → `{_b8(S.n)}`",
        'n >> 2 & m1': lambda S, B, r: f"两位一组互换：`{_b8(B.n)}` → `{_b8(S.n)}`",
        'return n >> 4': lambda S, B, r: f"高低 4 位互换，8 位反转完成：`{_b8(B.n)}` → `{_b8(r)}`；对称字符 `'{S.s[-1 - S.i]}'` = `{_b8(ord(S.s[-1 - S.i]))}`，" + ('==相等==，这一对没问题' if r == ord(S.s[-1 - S.i]) else '==不等=='),
    },
    cards=dict(
        one_liner='把每个字符的 8 位反转，对称位置要相等',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小写字符串 `s`，每个字符换成 8 位 ASCII 二进制并拼接',
                 '判断拼出来的二进制串是不是回文',
                 '示例：`"ff"` → `true`；`"leet"` → `false`；本视频：`"fnvf"` → `true`'],
        quote='只有 f、n、v 反转后仍是小写字母的 ASCII 值……但这不是通用做法。通用做法是用位运算反转一个二进制数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['整串反转 = 字符顺序倒过来，同时每个字符的 8 位也反转',
              '所以第 `i` 个字符反转后，必须等于倒数第 `i+1` 个字符',
              '8 位反转分三步：交换相邻位、两个两个交换、交换高低 4 位，各 `O(1)`'],
        result='`f↔f`、`n↔v`、`v↔n`、`f↔f` 全部满足 → 返回 `True` ✓',
        after=[dict(heading='方法一：直接拼字符串', lines=[
            '`f\'{ord(ch):08b}\'` 把每个字符转成 8 位二进制并拼接',
            '`t == t[::-1]` 判断回文，空间 `O(n)`',
            '不拼字符串的做法空间 `O(1)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：转二进制要补足 8 位（含前导零）',
                 '循环到 `len(s)//2`（含）：中间字符也要和自己比一次',
                 '同类：190 颠倒二进制位、3750 最少翻转次数得到反转二进制字符串'],
    ),
)
