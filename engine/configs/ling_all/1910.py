def _top(S):
    s, part = S.get('s'), S.get('part')
    if s is None:
        return ''
    i = S.get('i')
    if i is None:
        return f"在 `s` 里找最左边的 `{part}`"
    if i < 0:
        return f"`s` 里已经没有 `{part}`了，剩下的就是答案"
    if s[i:i + len(part)] != part:
        return f"删掉之后，`s` 变成 `{s}`，再找一遍"
    return f"最左边的 `{part}` 在下标 `{i}`"


CONFIG = dict(
    num=1910, title='删除一个字符串中所有出现的给定子字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='反复找最左出现并删除（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def removeOccurrences(self, s: str, part: str) -> str:
        while True:
            i = s.find(part)
            if i < 0:
                return s
            s = s[:i] + s[i + len(part):]
''',
    call='Solution().removeOccurrences("daabcbaabcbc", "abc")',
    expect='dab',
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝框 = 最左边的 part）', cell=80, h=260, window=('i', 'i + len(part) - 1 if s[i:i + len(part)] == part else -1'),
             color=lambda S, k, v: 'blue' if S.get('i', -1) >= 0 and S['s'][S['i']:S['i'] + len(S['part'])] == S['part'] and S['i'] <= k < S['i'] + len(S['part']) else None),
        dict(type='text', fn=lambda S: f"`part = \"{S['part']}\"`，长度 `{len(S['part'])}`", size=26),
    ],
    watch=[('i', 'i', 'blue'), ('len(s)', 'len(s)'), ('s', 's', 'green')],
    captions={
        'while True': '死循环：每轮删掉一个 `part`，直到找不到才 return',
        'i = s.find(part)': lambda S, B, ret: (f"`s.find(part)` = `{S.i}`：最左边的 `{S.part}` 从下标 `{S.i}` 开始" if S.i >= 0 else f"`s.find(part)` = `-1`：`s` 里不再含有 `{S.part}`"),
        'if i < 0': lambda S, B, ret: ('`i < 0` → ==找不到 part 了==，可以结束' if S.i < 0 else f'`i = {S.i} >= 0` → 还有 part，要继续删'),
        'return s': '没有 `part` 了，返回当前的 `s` = `"{s}"`',
        's = s[:i]': '删掉 `s[{i}:{i+len(part)}]`：左边 `s[:i]` 接上右边 `s[i+len(part):]`，得到 `"{s}"`（删完可能拼出新的 `part`，所以要回到循环开头再找）',
    },
    cards=dict(
        one_liner='找到最左边的 part 就切掉，循环到找不到为止',
        complexity='时间 `O(n^2/m)` 量级，空间 `O(n)`',
        problem=['反复找到 `s` 中==最左边==的子串 `part` 并删除，直到 `s` 里没有 `part`',
                 '返回剩下的字符串',
                 '示例：`s = "daabcbaabcbc"`，`part = "abc"` → `"dab"`'],
        quote='func removeOccurrences(s, part string) string { for { i := strings.Index(s, part); if i < 0 { return s }; s = s[:i] + s[i+len(part):] } }',
        quote_src='—— 灵茶山艾府题解（Go）',
        idea=['`find` 返回最左边出现的位置，没有就是 `-1`',
              '切掉 `part` 后，左右两段拼在一起，可能凑出新的 `part`',
              '所以不能只扫一遍，要写成死循环，找不到才返回'],
        result='三轮删除后剩下 `"dab"` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`strings.Index` 对应 `str.find`）',
                 '每轮 `find` 和拼接都是 `O(n)`，最多删 `n/m` 次',
                 '易错：删完后左右拼接可能产生新的 `part`，必须重新从头找',
                 '更快的做法：栈 + 逐字符匹配（见 yiduobo 的 KMP 解法）'],
    ),
)
