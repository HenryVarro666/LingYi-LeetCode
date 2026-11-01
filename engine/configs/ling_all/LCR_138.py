SETUP = '''
import re

def sscan_float(t):
    """模拟 Go 的 fmt.Sscan(t, new(big.Float), new(string)) 返回的成功读入个数：
    浮点读完且无剩余 -> 1；浮点后还有剩余文本（被第二个 string 读走）-> 2；读不出浮点 -> 0"""
    if re.fullmatch(r'[+-]?(\\d+\\.?\\d*|\\.\\d+)', t):
        return 1
    if re.match(r'[+-]?(\\d+\\.?\\d*|\\.\\d+)', t):
        return 2
    return 0

def sscanf_int(t):
    """模拟 Go 的 fmt.Sscanf(t, "%d%s", new(big.Int), new(string))：整数读完且无剩余 -> 1"""
    if re.fullmatch(r'[+-]?\\d+', t):
        return 1
    if re.match(r'[+-]?\\d+', t):
        return 2
    return 0
'''


def _info(S):
    if 'i' in S and S['i'] >= 0 and 's' in S:
        s, i = S['s'], S['i']
        out = f"`e` 把串拆成：底数 ==[{s[:i]}]==　指数 ==[{s[i+1:]}]=="
        if 'n1' in S:
            out += f"　底数读入 `{S['n1']}`"
        if 'n2' in S:
            out += f"　指数读入 `{S['n2']}`"
        return out
    return '先清洗：去掉首尾空格并转小写，再拒绝 ` bopx` 字符' if 's' in S else ''


def _color(S, idx, v):
    if 'i' in S and S['i'] >= 0:
        return 'blue' if idx < S['i'] else 'pink' if idx > S['i'] else 'yellow'
    return None


CONFIG = dict(
    num='LCR 138', title='有效数字', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='类正则：big.Float 读入底数，整数读入指数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def validNumber(self, s: str) -> bool:
        s = s.strip().lower()
        if any(c in s for c in " bopx"):
            return False
        if (i := s.find("e")) >= 0:
            n1 = sscan_float(s[:i])
            n2 = sscanf_int(s[i+1:])  # %d 强制以十进制方式读入
            return n1 == 1 and n2 == 1
        n = sscan_float(s)
        return n == 1
''',
    setup=SETUP,
    call='Solution().validNumber(" 6.5e-1 ")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s', pointers={'i': 'pink'}, color=_color, h=200),
        dict(type='text', fn=_info, size=30, h=100),
    ],
    watch=[('s', 's', 'blue'), ('i', 'i', 'pink'), ('n1', 'n1', 'green'), ('n2', 'n2', 'green')],
    captions={
        's = s.strip()': '去掉首尾空格并统一成小写（`E` → `e`）：`s = {s!r}`。题目允许首尾有空格，中间不允许',
        'any(c in s': lambda S, B, r: (f'含有 ` bopx` 之一 → ==无效==：空格只能在首尾，`b o p x` 是二、八、十六进制写法（如 `0x1p3`），题目只要十进制'
                                      if r is not None else f'`{S.s!r}` 里没有 ` bopx` → 继续'),
        'return False': '含非法字符，直接返回 ==False==',
        's.find("e")': '找指数分隔符 `e`：下标 `i = {i}`（没有则为 -1，走不含指数的分支）',
        'n1 = ': '把 `e` 前面的 `{s[:i]!r}` 当 ==big.Float== 读入：能读成一个完整的小数/整数则 `n1 = {n1}`，读不出或剩余多余字符则不是 1',
        'n2 = ': '`e` 后面的 `{s[i+1:]!r}` 单独当十进制整数读入（`%d`，允许正负号）：`n2 = {n2}`——指数要单独读，因为 big.Float 撑不住很大的指数',
        'return n1 == 1': '底数恰好读完（`n1 = {n1}`）且指数恰好读完（`n2 = {n2}`）→ 返回 =={ret}==',
        'n = sscan_float': '没有 `e`：整串当 big.Float 读入，`n = {n}`',
        'return n == 1': '`n == 1` 说明整串恰好被读成一个数，没有多余字符 → =={ret}==',
    },
    cards=dict(
        one_liner='借标准库读数：底数当浮点读，指数单独当整数读',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断字符串是否是有效数字：可有符号、小数点、`e/E` 指数，首尾可有空格',
                 '有效：`2`、`-.9`、`4.`、`3e+7`；无效：`e3`、`99e2.5`、`--6`、`1a`',
                 '本视频：`" 6.5e-1 "` → `true`'],
        quote='另一种类似正则匹配的方法是用 big.Float 来读入这个字符串，但是由于它无法支持超过 int32 范围的指数，需要稍微改造一下，把指数部分提出来读入。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`strip` + `lower`，再排除空格和 `b o p x`：它们是其他进制的写法，本题只要十进制',
              '有 `e`：前面当浮点读，后面当十进制整数读（`%d` 强制十进制）',
              '额外多读一个字符串，若它读到了东西（读入数为 2），说明没读完整串 → 无效'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`fmt.Sscan`/`Sscanf` 的读入个数判断，用 setup 里的两个小函数 `sscan_float` / `sscanf_int` 等价实现（作者代码未改）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：`e` 后面必须是整数（`99e2.5` 无效）；`e` 前面不能为空（`e3` 无效）；`.` 单独一个无效，`4.`、`.9` 有效',
                 '标准解法是手写 DFA 或直接用正则，本解法是取巧的读入法'],
    ),
)
