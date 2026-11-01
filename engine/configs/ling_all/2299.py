def _mask(S):
    m = S.get('mask', 0)
    names = [('小写', 1), ('大写', 2), ('数字', 4), ('特殊', 8)]
    return '  '.join(f"{n}{'✓' if m & b else '·'}" for n, b in names) + f"    `mask = {m:04b}`"


CONFIG = dict(
    num=2299, title='强密码检验器 II', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='位掩码记录四类字符（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def strongPasswordCheckerII(self, password: str) -> bool:
        if len(password) < 8:
            return False
        mask = 0
        for i, c in enumerate(password):
            if i > 0 and c == password[i - 1]:
                return False
            if c.islower():
                mask |= 1
            elif c.isupper():
                mask |= 2
            elif c.isdigit():
                mask |= 4
            else:
                mask |= 8
        return mask == 15
''',
    call="Solution().strongPasswordCheckerII('Ab3$xYz-')",
    expect=True,
    views=[
        dict(type='string', var='password', pointers={'i': 'blue'}, h=220,
             color=lambda S, i, v: 'blue' if S.get('i') == i else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', fn=_mask, h=90),
    ],
    watch=['i', 'c', ('mask', 'mask', 'green')],
    captions={
        'len(password) < 8': '长度 `{len(password)}`：{"不足 8 位 → 直接不合格" if len(password) < 8 else "够 8 位，继续检查"}',
        'mask = 0': '`mask` 用 4 个二进制位记录四类字符是否出现过',
        'for i, c in': '逐个字符检查，`c = {c!r}`',
        'if i > 0 and c': '和前一个字符比：`{c!r}` vs `{password[i-1]!r}` → 不同，继续',
        'mask |= 1': '`{c!r}` 是小写字母 → 置位 1：`mask = {mask:04b}`',
        'mask |= 2': '`{c!r}` 是大写字母 → 置位 2：`mask = {mask:04b}`',
        'mask |= 4': '`{c!r}` 是数字 → 置位 4：`mask = {mask:04b}`',
        'mask |= 8': '`{c!r}` 都不是字母数字 → 一定是特殊字符，置位 8：`mask = {mask:04b}`',
        'return mask == 15': '`mask = {mask:04b}`：四位全 1（15）才是强密码 → =={mask == 15}==',
    },
    cards=dict(
        one_liner='用 4 个二进制位记录四类字符，最后看是否全为 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['强密码：长度至少 8，含小写、大写、数字、特殊字符各一个，且没有相邻相同字符',
                 '特殊字符只会是 `!@#$%^&*()-+`',
                 '示例：`"Ab3$xYz-"` → `true`'],
        quote='先判断长度；遍历时若与前一个字符相同直接返回 false；用 mask 记录小写、大写、数字、其他四类，最后 mask == 15。',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['题目保证字符只有字母、数字和特殊字符，所以「都不是」就是特殊字符',
              '四类各占一位：1 / 2 / 4 / 8，全出现则 `mask = 15`',
              '相邻重复一遇到就 `return False`，不用等遍历结束'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Go 的 `switch` 转写为 `if/elif/else`，`unicode.IsLower` 等对应 `str.islower()` 等',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：长度判断别漏；`i > 0` 防止 `password[-1]` 误比较'],
    ),
)
