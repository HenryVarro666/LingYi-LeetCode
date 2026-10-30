import re

WORD = 'XCIV'
_V = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
_UNIT = {'V': 'I', 'X': 'I', 'L': 'X', 'C': 'X', 'D': 'C', 'M': 'C'}  # 每个字符前面可能出现的“单位一”


def _add_of(s, i):
    """yiduobo 的规则：本位应该累加多少"""
    ch = s[i]
    if ch in _UNIT and i > 0 and s[i - 1] == _UNIT[ch]:
        return _V[ch] - 2 * _V[_UNIT[ch]]
    return _V[ch]


_ADDS = [_add_of(WORD, i) for i in range(len(WORD))]
_PRE = [0]
for _a in _ADDS:
    _PRE.append(_PRE[-1] + _a)


def _done(S):
    """已经累加进 res 的字符个数（累加量都是正数，前缀和严格递增）"""
    res = S.get('res')
    return _PRE.index(res) if res in _PRE else 0


def _adds(S):
    if 'res' not in S:
        return None
    k = _done(S)
    return [f'+{a}' if i < k else '' for i, a in enumerate(_ADDS)]


def _add_color(S, i, v):
    if not v:
        return None
    return 'orange' if _ADDS[i] != _V[WORD[i]] else 'green'


def _str_color(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    if i == S['index'] - 1 and S['char'] in _UNIT and WORD[i] == _UNIT[S['char']]:
        return 'purple'
    return None


def _formula(S):
    if 'index' not in S:
        return '从左往右逐位累加 `res`'
    i, ch = S['index'], S['char']
    if ch in _UNIT and i > 0 and S['s'][i - 1] == _UNIT[ch]:
        u = _UNIT[ch]
        return f'`{u}{ch}` = {_V[ch] - _V[u]}，但 `{u}` 已加过 {_V[u]} → 本位只加 `{_V[ch]} − 2×{_V[u]}` = =={_add_of(WORD, i)}=='
    return f'`{ch}` 前面不是它的“单位一” → 照常加 =={_V[ch]}=='


def _chain_cap(S, B, ret):
    """if / elif char == 'X' 这一串判断"""
    ch = S.char
    m = re.search(r"char == '(\w)'", _LINES[S._line - 1])
    want = m.group(1)
    if ch == want:
        if want == 'I':
            return '`char` 是 `I`：单位一，前面不会有更小的 → 直接 `+1`'
        return f'`char` 是 `{want}` → 再看它前面是不是 `{_UNIT[want]}`'
    return f'`{ch}` 不是 `{want}`，继续往下判断'


def _prev_cap(S, B, ret):
    i, ch = S.index, S.char
    u = _UNIT[ch]
    if i == 0:
        return f'`index = 0`：`{ch}` 是第一个字符，前面没有字符 → 照常加'
    p = S.s[i - 1]
    if p == u:
        return f'前一位 `s[{i - 1}] = {p}`：==单位{"五" if ch in "VLD" else "十"}前面是单位一== → 特殊情况'
    return f'前一位 `s[{i - 1}] = {p}` 不是 `{u}` → 普通情况'


def _res_cap(S, B, ret):
    ch, i = S.char, S.index
    add = S.res - B.res
    if add != _V[ch]:
        u = _UNIT[ch]
        return (f'`{u}{ch}` = {_V[ch] - _V[u]}，可 `{u}` 已经累加过 {_V[u]} → '
                f'这里只加 =={add}==，`res` = {S.res}')
    return f'累加 `{ch}` = {add}，`res` = {S.res}'


CODE = '''
class Solution(object):
    def romanToInt(self, s):
        res = 0
        for index, char in enumerate(s):
            if char == 'I':
                res += 1
            elif char == 'V':
                if index > 0 and s[index - 1] == 'I':
                    res += 3
                else:
                    res += 5
            elif char == 'X':
                if index > 0 and s[index - 1] == 'I':
                    res += 8
                else:
                    res += 10
            elif char == 'L':
                if index > 0 and s[index - 1] == 'X':
                    res += 30
                else:
                    res += 50
            elif char == 'C':
                if index > 0 and s[index - 1] == 'X':
                    res += 80
                else:
                    res += 100
            elif char == 'D':
                if index > 0 and s[index - 1] == 'C':
                    res += 300
                else:
                    res += 500
            else:
                if index > 0 and s[index - 1] == 'C':
                    res += 800
                else:
                    res += 1000

        return res
'''
_LINES = CODE.strip('\n').split('\n')

CONFIG = dict(
    num=13, title='罗马数字转整数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='逐位累加 · 特殊情况补差',
    tags=['字节30天', '面试经典150'],
    code=CODE,
    call=f'Solution().romanToInt("{WORD}")',
    expect=94,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符，紫 = 它前面的“单位一”）', cell=130, h=250,
             pointers={'index': 'blue'}, color=_str_color),
        dict(type='array', var=_adds, label='每一位实际累加的值（橙 = 特殊情况）', cell=130, index=False, h=185,
             color=_add_color),
        dict(type='text', fn=_formula, size=27, h=80),
        dict(type='text', fn=lambda S: '补差表：`IV` +3　`IX` +8　`XL` +30　`XC` +80　`CD` +300　`CM` +800', size=24, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '从左往右按位累加，`res` 从 0 开始',
        'for index, char': lambda S, B, ret: (f'看第 `{S.index}` 位：`char = {S.char}`' if B.get('index') != S.index or 'index' not in B
                                              else '所有字符都累加完了'),
        "char == '": _chain_cap,
        'if index > 0 and': _prev_cap,
        'res +=': _res_cap,
        'return res': '返回 `res` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='从左往右累加；碰到 IV、XC 这类，前面多加的那次在这里补回来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个罗马数字（I V X L C D M），转成整数',
                 '通常小的在大的右边；==特例==：IV=4、IX=9、XL=40、XC=90、CD=400、CM=900',
                 '示例：`"MCMXCIV"` → `1994`；本视频：`"XCIV"` → `94`'],
        quote='如果出现了一个单位五，且前面是一个单位一，那么这里应该算做单位四。但是==先前已经累加过一次单位一了，所以这里继续累加一个单位三即可==。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右扫，单位一（I、X、C）先照常加上',
              '轮到单位五 / 单位十时，若前一位是单位一：`IV` 加 `3`，`IX` 加 `8`',
              '同理 `XL` 加 30、`XC` 加 80、`CD` 加 300、`CM` 加 800'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '核心：`IV` = 4 = 1 + ==3==，前面那个 1 已经加过了，只补差值',
                 '易错：判断前一位要先保证 `index > 0`',
                 '对比灵神：灵神用哈希表 + “左小取负”统一六种情况，代码更短',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
