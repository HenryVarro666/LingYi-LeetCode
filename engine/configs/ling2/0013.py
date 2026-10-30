TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

_R = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
WORD = 'MCMXCIV'


def _y(S):
    """pairwise 每次多读一个字符：Tracked.k 就是 y 的下标；循环结束后为 None"""
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) and k >= 1 else None


def _x(S):
    k = _y(S)
    return None if k is None else k - 1


def _done(S):
    """已经计入 ans 的字符个数"""
    s = S.get('s')
    if s is None:
        return 0
    if S.get('_line') == RET_LINE:
        return len(s)
    k = _y(S)
    if k is None:
        return len(s) - 1 if 'ans' in S and isinstance(S.get('x'), int) else 0
    i = k - 1
    if S.get('_line') == ADD_LINE:
        return i + 1
    return i


def _contrib(S):
    s = S.get('s')
    if s is None:
        return None
    s = str(s)
    out = []
    n = _done(S)
    for i, ch in enumerate(s):
        if i >= n:
            out.append('')
        elif i == len(s) - 1:
            out.append(f'+{_R[ch]}')
        else:
            v = _R[ch]
            out.append(f'+{v}' if v >= _R[s[i + 1]] else f'−{v}')
    return out


def _formula(S):
    if 'ans' not in S:
        return '规则：==左边的数比右边小==，它就取相反数（IV 中的 I 是 −1）'
    if S.get('_line') == RET_LINE:
        return f"最后一个字符右边没有邻居 → 一定是加：`{S['ans']} + {_R[str(S['s'])[-1]]}`"
    x, y = S.get('x'), S.get('y')
    if isinstance(x, int) and isinstance(y, int) and _y(S) is not None:
        if x >= y:
            return f'`x = {x} ≥ y = {y}` → 累加 ==+{x}=='
        return f'`x = {x} < y = {y}` → 小数在大数左边，累加 ==−{x}=='
    if isinstance(x, str):
        return f'相邻的一对：`{x}{y}`'
    return '相邻对已全部处理'


def _for_cap(S, B, ret):
    if _y(S) is None:
        return '相邻对都处理完了，循环结束（最后一个字符还没加）'
    i = _y(S) - 1
    return f'遍历相邻字符：`s[{i}] = {S.x}`，`s[{i + 1}] = {S.y}`'


def _add_cap(S, B, ret):
    x, y = S.x, S.y
    if x >= y:
        return f'`{x} ≥ {y}`：x 不比右边小 → 累加 `+{x}`，`ans` = {S.ans}'
    return f'`{x} < {y}`：小数在大数左边 → ==x 取相反数==，累加 `−{x}`，`ans` = {S.ans}'


CODE = '''
# 单个罗马数字到整数的映射
ROMAN = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
}

class Solution:
    def romanToInt(self, s: str) -> int:
        ans = 0
        for x, y in pairwise(s):  # 遍历 s 中的相邻字符
            x, y = ROMAN[x], ROMAN[y]
            # 累加 x 或者 -x，这里 y 只是用来辅助判断 x 的正负
            ans += x if x >= y else -x
        return ans + ROMAN[s[-1]]  # 加上最后一个罗马数字
'''

_LINES = CODE.strip('\n').split('\n')
ADD_LINE = next(i + 1 for i, l in enumerate(_LINES) if 'ans += x' in l)
RET_LINE = next(i + 1 for i, l in enumerate(_LINES) if 'return ans' in l)


def _color(S, i, v):
    if S.get('_line') == RET_LINE and i == len(str(S['s'])) - 1:
        return 'pink'
    if i == _x(S):
        return 'blue'
    if i == _y(S):
        return 'pink'
    return None


CONFIG = dict(
    num=13, title='罗马数字转整数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='相邻比较 · 小在左取负',
    tags=['字节30天', '面试经典150'],
    code=CODE,
    setup=TRACK,
    call=f'Solution().romanToInt(Tracked("{WORD}"))',
    expect=1994,
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（蓝 = x，粉 = y）', cell=120, h=250,
             pointers={_x: 'blue', _y: 'pink'}, pointer_labels={_x: 'x', _y: 'y'}, color=_color),
        dict(type='array', var=_contrib, label='每个字符的贡献（+ 加 / − 减）', cell=120, index=False, h=185,
             color=lambda S, i, v: ('green' if v.startswith('+') else 'red') if v else None),
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='text', fn=lambda S: '`ROMAN`：I=1  V=5  X=10  L=50  C=100  D=500  M=1000', size=24, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加每个字符的贡献，从 0 开始',
        'for x, y in pairwise': _for_cap,
        'x, y = ROMAN[x], ROMAN[y]': lambda S, B, ret: (f'查哈希表：`{B.x}` → `{S.x}`，`{B.y}` → `{S.y}`' +
                                                        ('（用哈希表省掉一堆 if-else）' if _y(S) == 1 else '')),
        'ans += x': _add_cap,
        'return ans': '最后一个罗马数字右边没有邻居，一定是加：`{ans} + {ret - ans}` = =={ret}==',
    },
    cards=dict(
        one_liner='相邻两个数，左边比右边小就取相反数，全部加起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个罗马数字（I V X L C D M），转成整数',
                 '通常小的在大的右边；==特例==：IV=4、IX=9、XL=40、XC=90、CD=400、CM=900',
                 '示例：`"MCMXCIV"` → `1994`（M + CM + XC + IV）'],
        quote='设 x=s[i-1], y=s[i]，这是两个相邻的罗马数字。==如果 x 的数值小于 y 的数值，那么 x 的数值要取相反数==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['六种特殊规则可以==统一==成一条：只看相邻两个数的大小',
              '`IV` 中的 I 相当于 `−1`，`CM` 中的 C 相当于 `−100`',
              '用哈希表存「字符 → 数值」，避免写一堆 if-else'],
        summary=['时间 `O(n)`，空间 `O(1)`（哈希表只有 7 项）',
                 '`pairwise` 只覆盖到倒数第二个字符：==最后一个字符要单独加上==',
                 '`y` 只用来辅助判断 `x` 的正负，`y` 自己在下一对里才计入',
                 '相等时（如 `II`）是加，所以条件写 `x >= y`'],
    ),
)
