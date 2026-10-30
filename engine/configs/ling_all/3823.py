def _first(S):
    """第一轮（f = islower）还是第二轮：第一轮结束后特殊字符已是反转状态"""
    sp = [c for c in S['s'] if not c.islower()]
    return [c for c in S['t'] if not c.islower()] != sp[::-1] or S['_line'] == 15


def _skip(S, ch):
    return ch.islower() if _first(S) else not ch.islower()


CONFIG = dict(
    num=3823, title='反转一个字符串里的字母后反转特殊字符', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 带条件的反转',
    tags=['难度分 1250'],
    code='''
class Solution:
    def reverse(self, t: List[str], f: 'Callable[[str], bool]') -> None:
        i, j = 0, len(t) - 1
        while i < j:
            while i < j and f(t[i]):
                i += 1
            while i < j and f(t[j]):
                j -= 1
            t[i], t[j] = t[j], t[i]
            i += 1
            j -= 1

    def reverseByType(self, s: str) -> str:
        t = list(s)
        self.reverse(t, str.islower)
        self.reverse(t, lambda ch: not ch.islower())
        return ''.join(t)
''',
    call='Solution().reverseByType(")ebc#da@f(")',
    expect='(fad@cb#e)',
    views=[
        dict(type='array', var=lambda S: S.get('t'), label='t（蓝 = i，粉 = j；两轮各反转一类字符，另一类被跳过）', cell=76,
             pointers={'i': 'blue', 'j': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'i, j = 0': '`i` 从左、`j` 从右，向中间靠拢：`i = {i}`，`j = {j}`',
        'while i < j:': lambda S, B, r: (f'`i = {S.i} < j = {S.j}` → 继续' if S.i < S.j else f'`i = {S.i} >= j = {S.j}` → 相遇，这一轮结束'),
        'while i < j and f(t[i])': lambda S, B, r: (f'`i = {S.i}` 已追上 `j`，不再移动' if S.i >= S.j else
                                                   f'`t[{S.i}] = {S.t[S.i]!r}` 满足 f → 要被跳过，`i` 右移' if _skip(S, S.t[S.i])
                                                   else f'`t[{S.i}] = {S.t[S.i]!r}` 不满足 f → 它是要反转的字符，`i` 停下'),
        'while i < j and f(t[j])': lambda S, B, r: (f'`j = {S.j}` 已追上 `i`，不再移动' if S.i >= S.j else
                                                   f'`t[{S.j}] = {S.t[S.j]!r}` 满足 f → 要被跳过，`j` 左移' if _skip(S, S.t[S.j])
                                                   else f'`t[{S.j}] = {S.t[S.j]!r}` 不满足 f → 它是要反转的字符，`j` 停下'),
        'i += 1': '`i` 右移 → {i}',
        'j -= 1': '`j` 左移 → {j}',
        't[i], t[j] = ': lambda S, B, r: (f'`i == j = {S.i}`：同一个位置，自己换自己，等于没动' if S.i == S.j else f'`i`、`j` 都停在要反转的字符上 → 交换 `t[{S.i}]` 与 `t[{S.j}]`'),
        't = list(s)': '字符串不可变，先转成列表 `t`',
        'self.reverse(t, str.islower)': '第一轮：`f = islower` 为真的是小写字母，被==跳过==，剩下的特殊字符互相交换',
        'self.reverse(t, lambda': '第二轮：`f` 为真的是特殊字符，被==跳过==，剩下的小写字母互相交换',
        "return ''.join": lambda S, B, ret: f'拼回字符串：`{ret!r}`',
    },
    cards=dict(
        one_liner='相向双指针，只交换同一类字符',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`',
        problem=['先反转所有小写字母（放回原位），再反转所有特殊字符',
                 '示例：`")ebc#da@f("`',
                 '→ `"(fad@cb#e)"`'],
        quote='前置题目：344. 反转字符串，我的题解。',
        quote_src='—— 灵茶山艾府题解',
        idea=['封装 `reverse(t, f)`：`f(ch)` 为真的字符表示「要跳过」',
              '`i`、`j` 各自跳过 `f` 为真的字符，停下时两个都是目标字符，交换',
              '调用两次：换一个谓词 `f`，就分别反转两类字符，互不影响'],
        summary=['时间 `O(n)`，空间 `O(n)`（转列表）',
                 '易错：内层 while 也要写 `i < j`，防止越界或越过对方',
                 '为在引擎里运行，类型注解 `Callable[...]` 加了引号，逻辑未改',
                 '同一个 `reverse` 复用两次，换谓词函数即可；两类字符位置互不干扰，先后顺序无所谓'],
    ),
)
