def _pos(S):
    s = S['s']
    k = s.find('ba')
    return k


CONFIG = dict(
    num=2124, title='检查是否所有 A 都在 B 之前', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='子串判断 "ba"（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def checkString(self, s: str) -> bool:
        return "ba" not in s
''',
    call='Solution().checkString("aabbab")',
    expect=False,
    views=[
        dict(type='text', size=34, fn=lambda S: (
            f"字符串里有 `\"ba\"`：在下标 =={S['s'].find('ba')}== → 有 b 在 a 前面 → ==false==" if 'ba' in S['s']
            else '字符串里没有 `"ba"` → 所有 a 都在 b 前 → ==true==')),
        dict(type='string', var='s', h=300, cell=110,
             color=lambda S, i, v: 'pink' if (_pos(S) >= 0 and i in (_pos(S), _pos(S) + 1)) else ('blue' if v == 'a' else 'green')),
    ],
    watch=[('s', 's', 'blue')],
    captions={
        'return "ba" not in s': lambda S, B, ret: (
            f'找子串 `"ba"`：在下标 {S.s.find("ba")} 找到（`s[{S.s.find("ba")}]=b`，`s[{S.s.find("ba")+1}]=a`）→ ==b 排在 a 前面== → 返回 `{ret}`'
            if "ba" in S.s else '整串里找不到 `"ba"` → 不存在 b 紧挨着 a → 返回 `True`'),
    },
    cards=dict(
        one_liner='合法的串一定长成 aaa…bbb，只要出现 "ba" 就不合法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a` 和 `b`，问是否每个 `a` 都在每个 `b` 之前',
                 '示例：`"aaabbb"` → `true`，`"abab"` → `false`，`"bbb"` → `true`',
                 '本视频：`"aabbab"` → `false`'],
        quote='func checkString(s string) bool { return !strings.Contains(s, "ba") }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['合法串必然是 ==若干 a 后面跟若干 b==，形如 `aa…abb…b`',
              '只要有一个 b 出现在某个 a 前面，那串里必然有相邻的 `"ba"`（从 b 走到 a 总要经过一次 b 变 a）',
              '反过来，没有 `"ba"` 就不可能出现 b 后面再有 a'],
        after=[dict(heading='换个角度想', lines=['合法串 = 若干 `a` + 若干 `b`，只允许 a 变 b 一次', '`"ba"` 就是「b 变回 a」的那个位置', '原文只有这一行：找不到 `"ba"` 就是合法'])],
        summary=['原文为 Go，已按原逻辑转写为 Python：`strings.Contains` 对应 `in`',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：别写成找 `"ab"`；没有 a 或没有 b（如 `"bbb"`）也合法',
                 '一行搞定的写法依赖「合法串只有 a 到 b 的一次切换」这个结构性质'],
    ),
)
