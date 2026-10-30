S0 = 'leetcode'
P0 = 'ee*e'


def _s_color(S, i, v):
    if 'star' not in S:
        return None
    st = S['star']
    a = S.get('i')
    if a is None:
        return None
    if a < 0:
        return None
    if a <= i < a + st:
        return 'blue'
    if S['_line'] >= 5:
        rest = P0[st + 1:]
        j = S0.find(rest, a + st)
        if j >= 0 and j <= i < j + len(rest):
            return 'green'
    return None


def _s_dim(S, i, v):
    a = S.get('i')
    return a is not None and a >= 0 and i < a + S['star'] and not (a <= i)


def _p_color(S, i, v):
    st = S.get('star')
    if st is None:
        return None
    if i == st:
        return 'yellow'
    if i < st:
        return 'blue'
    return 'green'


def _text(S):
    if 'star' not in S:
        return '模式串 `p` 里恰有一个 `*`，先找到它'
    st = S['star']
    if 'i' not in S:
        return f"`*` 在下标 `star` ==为 {st}==，把 `p` 切成：左 `{P0[:st]}` ＋ `*` ＋ 右 `{P0[st + 1:]}`"
    a = S['i']
    if a < 0:
        return '左半没找到 → 不可能匹配'
    return f"左半 `{P0[:st]}` 首次出现在下标 `i` ==为 {a}==，`*` 之后从 `s[{a + st}:]` = `{S0[a + st:]}` 里找右半 `{P0[st + 1:]}`"


CONFIG = dict(
    num=3407, title='子字符串匹配模式', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='按 * 切开 · 两次 find',
    code='''
class Solution:
    def hasMatch(self, s: str, p: str) -> bool:
        star = p.find('*')
        i = s.find(p[:star])
        return i >= 0 and p[star + 1:] in s[i + star:]
''',
    call='Solution().hasMatch("leetcode", "ee*e")',
    expect=True,
    views=[
        dict(type='text', fn=_text, size=28, h=120),
        dict(type='string', var='s', label='s（蓝 = 左半匹配处，绿 = 右半匹配处）', color=_s_color, dim=_s_dim, h=240),
        dict(type='string', var='p', label='p（蓝 = 星号左边，黄 = 星号，绿 = 星号右边）', color=_p_color, h=240),
    ],
    watch=['star', 'i', ('p[:star]', 'p[:star]', 'blue'), ('p[star+1:]', 'p[star + 1:]', 'green')],
    captions={
        'star = p.find': '`*` 在 `p` 的下标 =={star}==：左边 `{p[:star]}`，右边 `{p[star + 1:]}`',
        'i = s.find': lambda S, B, r: (f"在 `s` 里找左半 `{S.p[:S.star]}` 第一次出现的位置：`i` ==为 {S.i}==（越靠前，留给右半的空间越多）" if S.i >= 0
                                       else f"`s` 里找不到左半 `{S.p[:S.star]}`，`i = -1`"),
        'return i >= 0': lambda S, B, r: (f"`i = {S.i} >= 0` 成立；`*` 可替换任意内容，所以只要右半 `{S.p[S.star + 1:]}` 出现在 `s[{S.i + S.star}:] = {S.s[S.i + S.star:]}` 里即可 → =={r}==" if S.i >= 0
                                          else '`i < 0` → 直接返回 `False`'),
    },
    max_steps=20,
    cards=dict(
        after=[dict(heading='反例：右半找不到', lines=['`s = "car"`，`p = "c*v"`：左半 `c` 在 `i = 0`', '右半 `v` 要在 `s[1:] = "ar"` 里找，没有 → `false`', '所以左半即使找到了，右半也必须落在它的后面'])],
        one_liner='星号两边各找一次：左半尽量靠前，右半在左半之后找',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['模式串 `p` 里恰有一个 `*`，它可以换成任意长度（含 0）的任意字符串',
                 '问换完之后 `p` 能否成为 `s` 的子串',
                 '示例：`s = "leetcode"`，`p = "ee*e"` → `true`'],
        quote='把 p 分成两部分，* 左边的记作 p[:star]，右边的记作 p[star+1:]。在 s 中找 p[:star] 首次出现的位置 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`*` 能顶替任意内容，所以只需：左半出现在前，右半出现在后，两者不重叠',
              '左半取==最早==出现的位置 `i`，给右半留下最多的空间',
              '右半只需在 `s[i+star:]` 里出现，`i+star` 正是左半的结尾'],
        summary=['时间 `O(nm)`（`find` / `in` 暴力匹配），用 KMP 可到 `O(n+m)`',
                 '易错点：`*` 在开头时 `p[:star]` 为空，`s.find("")` 返回 0，仍然正确',
                 '右半要从 `i + star` 开始找，不能从 0 开始，否则会与左半重叠',
                 '思考题：多个 `*` 时，依次把每一段在前一段之后用 `find` 贪心找最早出现的位置'],
    ),
)
