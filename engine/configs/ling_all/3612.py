CONFIG = dict(
    num=3612, title='用特殊操作处理字符串 I', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='列表模拟',
    tags=[],
    code='''
class Solution:
    def processStr(self, s: str) -> str:
        ans = []
        for c in s:
            if c == '*':
                if ans:
                    ans.pop()
            elif c == '#':
                ans += ans
            elif c == '%':
                ans.reverse()
            else:
                ans.append(c)
        return ''.join(ans)
''',
    call='Solution().processStr("a#b%*")',
    expect='ba',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前处理的字符）', cell=84, h=200,
             color=lambda S, i, v: 'blue' if S.get('c') == v and i == S.get('_i', i) else None),
        dict(type='array', var='ans', label='ans（当前 result）', cell=84, h=260),
        dict(type='text', fn=lambda S: ("`ans` = \"" + ''.join(S['ans']) + "\"") if 'ans' in S else '', size=30),
    ],
    watch=['c', ('ans', "''.join(ans)", 'green')],
    captions={
        'ans = []': '用列表保存 `result`，末尾增删都是 `O(1)`',
        'for c in s': "处理字符 `c = '{c}'`",
        "c == '*'": lambda S, B, ret: f"`c = '{S.c}'` 是 `*` → 要删最后一个字符" if S.c == '*' else f"`c = '{S.c}'` 不是 `*`，看下一种操作",
        'if ans': lambda S, B, ret: ('`ans` 非空 → 可以删' if S.ans else '`ans` 为空 → ==不能 pop==（否则报错），什么也不做'),
        'ans.pop()': '删掉最后一个字符 → `ans = {ans}`',
        "c == '#'": lambda S, B, ret: "`c` 是 `#` → 复制并追加到自身后面" if S.c == '#' else "不是 `#`，继续判断",
        'ans += ans': '`ans += ans` 把自己接到自己后面：长度翻倍 → `{ans}`',
        "c == '%'": lambda S, B, ret: "`c` 是 `%` → 反转 `ans`" if S.c == '%' else "不是 `%`，那就是小写字母",
        'ans.reverse()': '原地反转 → `{ans}`',
        'ans.append(c)': "小写字母直接追加：`ans = {ans}`",
        'return': "全部处理完，拼成字符串返回 `{ret!r}`",
    },
    cards=dict(
        one_liner='直接模拟，用列表当 result，四种操作各一个分支',
        complexity='时间 `O(2^n)`，空间 `O(1)`（不计返回值）',
        problem=['从左到右处理 `s`：字母追加；`*` 删最后一个；`#` 复制追加到自身；`%` 反转',
                 '返回最终的 `result`',
                 '示例：`"a#b%*"` → `"ba"`'],
        quote='注意字符串为空的时候，不能删除最后一个字母（否则会报错）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n <= 20`，最坏把一个字母复制 `n-1` 次，长度 `2^(n-1)`，直接模拟即可',
              '`ans += ans` 复制，`ans.reverse()` 反转，`ans.pop()` 删除',
              '删除前先判 `ans` 非空'],
        summary=['时间是等比数列之和 `O(2^n)`，空间 `O(1)`（返回值不计）',
                 '易错：空列表 `pop()` 会抛异常，必须先判断',
                 '`ans += ans` 对列表是原地扩展，结果是长度翻倍的拷贝',
                 '进阶版本（3614）长度太大不能模拟，需要倒推'],
    ),
)
