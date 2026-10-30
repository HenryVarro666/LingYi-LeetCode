CONFIG = dict(
    num=2000, title='反转单词前缀', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针交换（Go 原文转写）',
    tags=['滑动窗口与双指针', '难度分 1199'],
    code='''
class Solution:
    def reversePrefix(self, s: str, ch: str) -> str:
        j = s.find(ch)
        if j < 0:
            return s
        t = list(s)
        i = 0
        while i < j:
            t[i], t[j] = t[j], t[i]
            j -= 1
            i += 1
        return ''.join(t)
''',
    call="Solution().reversePrefix('abcdefd', 'd')",
    expect='dcbaefd',
    views=[
        dict(type='string', var='s', label='s（原串）', h=170, cell=80, pointers={'j': 'pink'}),
        dict(type='array', var='t', label='t（正在反转的字符数组；蓝 = i，粉 = j）', h=220, cell=80,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, x: ('blue' if k == S['i'] else 'pink' if k == S['j'] else None) if 'i' in S and 'j' in S and S['i'] < S['j'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'j = s.find(ch)': lambda S, B, r: (f'`ch = {S.ch!r}` 第一次出现在下标 `j = {S.j}`：要反转的是 `s[0..{S.j}]`' if S.j >= 0 else f'`s` 里没有 `{S.ch}`，`j = -1`'),
        'if j < 0': lambda S, B, r: ('找不到 `ch`，不用反转' if S.j < 0 else f'`j = {S.j} ≥ 0`：找到了，继续'),
        'return s': '没有 `ch`，原样返回 `{s}`',
        't = list(s)': '字符串不能原地改，先拷成字符数组 `t`',
        'i = 0': '`i` 从头开始，`j` 从 `ch` 的位置往回走，两头向中间靠',
        'while i < j': lambda S, B, r: (f'`i = {S.i} < j = {S.j}`：还有一对没换' if S.i < S.j else f'`i = {S.i} ≥ j = {S.j}`：指针相遇或交错，反转完成'),
        't[i], t[j] = t[j], t[i]': '交换 `t[{i}]` 与 `t[{j}]`，`t` = `{"".join(t)}`',
        'j -= 1': '`j` 左移到 {j}',
        'i += 1': '`i` 右移到 {i}',
        "return ''.join(t)": "拼成字符串返回 `{ret}`",
    },
    cards=dict(
        one_liner='找到 ch 的位置 j，把 [0, j] 首尾交换成反转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你字符串 `word` 和字符 `ch`，找到 `ch` 第一次出现的下标 `j`',
                 '把 `word[0..j]` 这一段==反转==；找不到就不动',
                 '示例：`word = "abcdefd"`，`ch = "d"` → `"dcbaefd"`'],
        quote='j := strings.IndexByte(s, ch) …… for i := 0; i < j; i++ { t[i], t[j] = t[j], t[i]; j-- }',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['`find` 先定位 `j`，没有就直接返回原串',
              '`i` 从 0 往右，`j` 从 `ch` 往左，每次交换一对再各走一步',
              '循环条件 `i < j` 会随着 `j` 的递减而变化，相遇就结束'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`strings.IndexByte` → `s.find`，`[]byte` → `list`',
                 '时间 `O(n)`，空间 `O(n)`（字符串不可变，要拷贝一份）',
                 '易错：Go 的 `for i := 0; i < j; i++` 每轮重新判断 `i < j`，而 `j` 在循环体里减小，所以用 `while` 写',
                 '找不到 `ch` 时 `find` 返回 -1，直接返回原串'],
    ),
)
