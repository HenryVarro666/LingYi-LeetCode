def _s(S):
    s = S.get('self.s')
    return None if s is None else [c - 48 for c in bytes(s)]


def _real(S):
    """实际位集：懒标记为 '1' 时，s 的每一位取反"""
    a = _s(S)
    if a is None:
        return []
    return [1 - x for x in a] if S.get('self.flip_mark') == 49 else a


def _txt(S):
    a = _s(S)
    if a is None:
        return ''
    f = S.get('self.flip_mark') == 49
    real = ''.join(map(str, _real(S)))
    return f"实际位集 = =={real}==（{'s 每位取反' if f else 's 原样'}）　`cnt1 = {S.get('self.cnt1')}`"


CONFIG = dict(
    num=2166, title='设计位集', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='懒翻转标记 + 维护 1 的个数（Go 原文转写）', tags=[],
    code='''
class Bitset:
    def __init__(self, size: int):
        self.s = bytearray(b'0' * size)
        self.flip_mark = ord('0')
        self.cnt1 = 0

    def fix(self, i: int) -> None:
        if self.s[i] == self.flip_mark:
            self.s[i] ^= 1
            self.cnt1 += 1

    def unfix(self, i: int) -> None:
        if self.s[i] != self.flip_mark:
            self.s[i] ^= 1
            self.cnt1 -= 1

    def flip(self) -> None:
        self.flip_mark ^= 1
        self.cnt1 = len(self.s) - self.cnt1

    def all(self) -> bool:
        return self.cnt1 == len(self.s)

    def one(self) -> bool:
        return self.cnt1 > 0

    def count(self) -> int:
        return self.cnt1

    def toString(self) -> str:
        if self.flip_mark == ord('1'):
            t = bytearray(len(self.s))
            for i, ch in enumerate(self.s):
                t[i] = ch ^ 1
            return t.decode()
        return self.s.decode()
''',
    call='''bs = Bitset(5)
out = [bs.fix(3), bs.fix(1), bs.flip(), bs.all(), bs.unfix(0), bs.flip(), bs.one(), bs.unfix(0), bs.count(), bs.toString()]
out''',
    expect=[None, None, None, False, None, None, True, None, 2, '01010'],
    views=[
        dict(type='text', size=28, h=110, fn=_txt),
        dict(type='array', var=lambda S: _s(S) or [], label='s（存的是「没翻转」时的位；标记为 1 时实际值取反）', cell=110, h=210,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var=_real, label='实际位集（s 按懒标记取反之后）', cell=110, h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('flip标记', "'1' if S.get('self.flip_mark') == 49 else '0'", 'purple'), ('cnt1', 'self.cnt1', 'green'), ('i', 'i', 'blue')],
    captions={
        'self.s = bytearray': '`s` 先全是 `0`，大小 `size = {size}`',
        'self.flip_mark = ord': '懒标记 `flip_mark` = `0`：表示当前没有翻转',
        'self.cnt1 = 0': '`cnt1` = 实际位集里 1 的个数，现在是 0',
        'if self.s[i] == self.flip_mark': lambda S, B, r: f"`s[{S.i}]` 是 `{chr(S['self.s'][S.i])}`，标记是 `{chr(S['self.flip_mark'])}`：" + ('相等 → 实际是 0，fix 要把它变成 1' if S['self.s'][S.i] == S['self.flip_mark'] else '不等 → 实际已经是 1，什么也不做'),
        'if self.s[i] != self.flip_mark': lambda S, B, r: f"`s[{S.i}]` 是 `{chr(S['self.s'][S.i])}`，标记是 `{chr(S['self.flip_mark'])}`：" + ('不等 → 实际是 1，unfix 要把它变成 0' if S['self.s'][S.i] != S['self.flip_mark'] else '相等 → 实际已经是 0，什么也不做'),
        'self.s[i] ^= 1': '异或 1：字符 `0`/`1` 互换，`s[{i}]` → `{chr(self.s[i])}`（只动这一位）',
        'self.cnt1 += 1': '实际多了一个 1：`cnt1` → =={self.cnt1}==',
        'self.cnt1 -= 1': '实际少了一个 1：`cnt1` → =={self.cnt1}==',
        'self.flip_mark ^= 1': '不翻整个数组，只把懒标记取反：`{chr(B.self.flip_mark)}` → `{chr(self.flip_mark)}`，==O(1)==',
        'self.cnt1 = len': '翻转后 1 和 0 互换：`cnt1 = size - cnt1` = =={self.cnt1}==',
        'return self.cnt1 == len': '`cnt1 = {self.cnt1}`，`size = {len(self.s)}` → 全是 1 吗？=={ret}==',
        'return self.cnt1 > 0': '`cnt1 = {self.cnt1}` → 至少一个 1？=={ret}==',
        'return self.cnt1': '直接返回维护好的 `cnt1 = {ret}`，不用数',
        "if self.flip_mark == ord('1')": '标记是 `{chr(self.flip_mark)}`：' + '{"已翻转，输出时要把 s 每位取反" if self.flip_mark == 49 else "没翻转，s 就是实际位集"}',
        'bytearray(len': '准备一个新数组 `t` 装取反后的结果（toString 最多 5 次，`O(size)` 可以接受）',
        't[i] = ch ^ 1': '`s[{i}]` 的 `{chr(ch)}` 取反 → `t[{i}] = {chr(t[i])}`',
        'return t.decode()': '翻转状态：取反后拼成 =="{ret}"==',
        'return self.s.decode()': '没翻转：直接输出 =="{ret}"==',
    },
    max_steps=110,
    cards=dict(
        one_liner='flip 不真翻数组：用一个懒标记，再维护 1 的个数',
        complexity='除 `toString` 为 `O(size)` 外，其余操作均为 `O(1)`',
        problem=['设计位集：`fix` 置 1、`unfix` 置 0、`flip` 翻转所有位',
                 '`all` 是否全 1、`one` 是否有 1、`count` 1 的个数、`toString` 输出',
                 '示例：`Bitset(5)` → `fix(3), fix(1), flip() ...` → `toString = "01010"`'],
        quote='不去翻转整个 s，而是用一个懒标记 flip 来表示当前是否处于翻转状态。由于偶数次翻转等于没有翻转，而奇数次翻转等于翻转一次……这也是高效解决这道题的关键。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s` 是「没发生翻转」时的位集，`cnt1` 是实际位集中 1 的个数',
              '`flip`：标记取反，`cnt1 = size - cnt1`，不碰数组',
              '`fix`：`s[i]` 等于标记（实际为 0）才改，并 `cnt1 += 1`；`unfix` 反之',
              '`toString`：标记为 `1` 时对 `s` 每位取反再输出'],
        summary=['`fix / unfix / flip / all / one / count` 均为 `O(1)`，`toString` 为 `O(size)`，空间 `O(size)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python：Go 用全局变量，这里放进实例属性',
                 '标记变量 `flip` 与方法 `flip` 同名冲突，转写时改名为 `flip_mark`；字符 `0`/`1` 用 `bytearray` 与 `^ 1` 互换',
                 '易错点：只有位真的变了才改 `cnt1`，重复 fix 同一位不能重复加'],
    ),
)
