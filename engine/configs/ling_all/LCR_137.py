def _tokens(p):
    out, i = [], 0
    while i < len(p):
        if i + 1 < len(p) and p[i + 1] == '*':
            out.append(p[i:i + 2])
            i += 2
        else:
            out.append(p[i])
            i += 1
    return out


def _explain(t):
    if len(t) == 2:
        c = '任意字符' if t[0] == '.' else f"'{t[0]}'"
        return f'`{t}` = {c} 重复 0 次或多次'
    return '`.` = 任意单个字符' if t == '.' else f"`{t}` = 恰好一个 '{t}'"


def _regex(S):
    if 'p' not in S:
        return ''
    toks = _tokens(S['p'])
    return '输入 `p` 拆成：' + '　'.join(f'==[{t}]==' for t in toks)


def _explain_line(S):
    if 'p' not in S:
        return ''
    return '；'.join(_explain(t) for t in _tokens(S['p']))


CONFIG = dict(
    num='LCR 137', title='模糊搜索验证', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='直接用正则表达式（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def articleMatch(self, s: str, p: str) -> bool:
        return re.compile("^" + p + "$").match(s) is not None
''',
    setup='import re',
    call='Solution().articleMatch("aab", "c*a*b")',
    expect=True,
    views=[
        dict(type='string', var='s', label='article = s', h=170),
        dict(type='string', var='p', label='input = p（含通配符）', h=170),
        dict(type='text', fn=_regex, size=34, h=80),
        dict(type='text', fn=_explain_line, size=28, h=90),
        dict(type='text', fn=lambda S: ('正则：`^' + S['p'] + '$` 整串匹配 s' if 'p' in S else ''), size=34, h=80),
    ],
    watch=[('s', 's', 'blue'), ('p', 'p', 'pink')],
    captions={
        'return re.compile': '拼出正则 `^{p}$`：`^` 和 `$` 保证==整个字符串==都要匹配；`.` 和 `*` 的含义与题目完全一致 → 匹配 `{s}` 的结果是 =={ret}==',
    },
    cards=dict(
        one_liner='题目的 . 和 * 就是正则语法，直接交给正则引擎',
        complexity='取决于正则引擎实现；Go 的 regexp 保证线性时间',
        problem=['`.` 匹配任意单个字符，`*` 匹配零个或多个前面的那个元素',
                 '要求 `input` 匹配==整个== `article`，不是子串',
                 '示例：`aa` 与 `a*` → `true`；`aa` 与 `a` → `false`',
                 '本视频：`aab` 与 `c*a*b` → `true`'],
        quote='func articleMatch(s, p string) bool { return regexp.MustCompile("^" + p + "$").MatchString(s) }',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['`.`、`*` 的语义和正则表达式一致，不用自己写 DP',
              '前后各加 `^`、`$`，把「找子串」变成「整串匹配」',
              '`c*a*b`：`c*` 取 0 个，`a*` 取 2 个，`b` 取 1 个，刚好是 `aab`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`regexp.MustCompile(...).MatchString(s)` 对应 `re.compile(...).match(s) is not None`',
                 '时间复杂度取决于正则引擎；面试若要求手写，需用 DP（`f[i][j]` 表示前 i、j 个字符是否匹配）',
                 '易错点：忘记 `^` `$` 会变成子串匹配；`re.match` 只锚定开头，故仍需 `$`',
                 '本题与主站第 10 题相同'],
    ),
)
