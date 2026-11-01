def _re(S):
    p = S.get('p')
    if p is None:
        return '通配符 → 正则：`?` 变成 `.`，`*` 变成 `.*`'
    if S.get('_line', 0) >= 5:
        return f"正则：`^{p}$`，用它去匹配整个 `s`"
    return f"当前 `p = {p}`"


CONFIG = dict(
    num=44, title='通配符匹配', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='通配符转正则（Go 原文转写）',
    tags=['灵神题单·动态规划'],
    setup='import re',
    code='''
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        p = p.replace("?", ".")
        p = p.replace("*", ".*")
        return re.compile("^" + p + "$").search(s) is not None
''',
    call='Solution().isMatch("adceb", "*a?*b")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（输入字符串）', cell=84, h=170),
        dict(type='string', var='p', label='p（通配符模式，会被逐步改写成正则）', cell=84, h=170),
        dict(type='text', fn=_re, size=30, h=110),
    ],
    watch=[('s', 's'), ('p', 'p', 'pink')],
    captions={
        'p.replace("?"': '把 `?` 换成 `.`：`.` 在正则里正好匹配任意单个字符，`p = {p}`',
        'p.replace("*"': '把 `*` 换成 `.*`：任意字符重复 0 次或多次，正好是任意字符序列，`p = {p}`',
        're.compile': lambda S, B, ret: f"前后加 `^` 和 `$` 要求==完全匹配==，正则 `^{S.p}$` 匹配 `{S.s}`：=={ret}==",
    },
    cards=dict(
        one_liner='两种通配符，翻译成标准正则就能直接匹配',
        complexity='时间取决于正则引擎，空间 `O(m)`',
        problem=['`s` 是字符串，`p` 是含 `?` 和 `*` 的模式',
                 '`?` 匹配任意单个字符；`*` 匹配任意长度（含 0）的字符序列',
                 '`p` 必须==完整匹配==整个 `s`',
                 '示例：`s = "adceb"`，`p = "*a?*b"` → `true`'],
        quote='将题目中的两种通配符转换成标准正则写法。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`?` 对应正则的 `.`（任意单个字符）',
              '`*` 对应正则的 `.*`（任意字符重复任意次）',
              '前后加 `^`、`$`，保证是整串匹配，而不是部分匹配'],
        after=[dict(heading='常规做法对比', lines=[
            '二维 DP：`f[i][j]` 表示 `s` 前 `i` 个字符能否被 `p` 前 `j` 个字符匹配',
            '`p[j]` 是 `*` 时：`f[i][j] = f[i][j-1] or f[i-1][j]`',
            '这个写法只有三行，把匹配交给正则引擎，适合当作“知道有这个捷径”的补充'])],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`regexp.MustCompile(...).MatchString` 对应 `re.compile(...).search`）',
                 '这是调库的偷懒写法；常规解法是二维 DP 或贪心双指针',
                 '易错：必须加 `^` 和 `$`，否则只要子串匹配就会返回 true',
                 '题目保证 `p` 里只有小写字母、`?`、`*`，所以不用转义其他正则符号'],
    ),
)
