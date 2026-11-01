CONFIG = dict(
    num=1941, title='检查是否所有字符出现次数相同', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='计数数组 · 对比目标次数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def areOccurrencesEqual(self, s: str) -> bool:
        cnt = [0] * 26
        for b in s:
            cnt[ord(b) - ord('a')] += 1
        target = 0
        for c in cnt:
            if c == 0:
                continue
            if target == 0:
                target = c
            elif c != target:
                return False
        return True
''',
    call='Solution().areOccurrencesEqual("abacbc")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s', cell=84, h=150),
        dict(type='array', var='cnt', label='cnt（下标 0~25 对应 a~z）', cell=44, h=250,
             color=lambda S, i, v: ('green' if 'target' in S and v == S['target'] and v else ('pink' if v and 'target' in S and S['target'] and v != S['target'] else ('yellow' if v else None))),
             dim=lambda S, i, v: v == 0),
        dict(type='text', fn=lambda S: (f"目标次数 `target = {S['target']}`" if 'target' in S else ''), h=80),
    ],
    watch=['b', 'c', ('target', 'target', 'green')],
    captions={
        'cnt = [0]': '26 个计数器，对应 `a` ~ `z`，全为 0',
        'for b in s': '取 `s` 的下一个字符 `b = {b}`',
        'cnt[ord(b)': '`{b}` 出现次数 +1：`cnt[{ord(b) - ord("a")}] = {cnt[ord(b) - ord("a")]}`',
        'target = 0': '`target` 记第一个出现过的字符的次数，0 表示还没记',
        'for c in cnt': '看计数器 `c = {c}`',
        'if c == 0': lambda S, B, ret: ('`c = 0`：这个字母没出现过 → ==跳过==' if S.c == 0 else '`c != 0`：出现过，要参与比较'),
        'continue': '没出现过的字母不参与比较，直接看下一个',
        'if target == 0': lambda S, B, ret: ('`target == 0`：这是第一个出现过的字母' if S.target == 0 else '`target` 已经有了，下面和它比'),
        'target = c': '把第一个字母的次数 `{c}` 记作 ==目标次数==',
        'elif c != target': lambda S, B, ret: (f"`c = {S.c}` ≠ `target = {S.target}` → ==次数不同==" if S.c != S.target else f"`c = {S.c}` == `target = {S.target}` → 次数相同，继续"),
        'return False': '遇到次数不同的字母，直接返回 `False`',
        'return True': '所有出现过的字母次数都等于 `target` → 返回 `True`',
    },
    cards=dict(
        one_liner='用计数数组数出每个字母，再看出现过的是否都一样多',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['如果 `s` 中出现过的==所有==字符次数都相同，就是好字符串',
                 '返回 `s` 是不是好字符串',
                 '示例：`"abacbc"` → `true`（各 2 次）；`"aaabb"` → `false`'],
        quote='`cnt := [26]int{}`，遍历 `s` 统计次数，再用 `target` 记录第一个非零次数，其余非零次数与之比较。',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`s` 只有小写字母，用长度 26 的数组计数即可',
              '计数为 0 的字母没出现过，跳过',
              '第一个非零计数作为 `target`，之后只要有不同的就返回 `False`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`（固定 26 格）',
                 '易错：必须跳过次数 0 的字母，否则会误判',
                 '同类题：用 `Counter` 后看 `len(set(cnt.values())) == 1`'],
    ),
)
