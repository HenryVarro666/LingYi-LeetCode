def _top(S):
    if 't' not in S:
        return ''
    t = S['t']
    if 'j' in S and S['_line'] in (8, 9, 10, 11):
        return f'从 `i = {S["i"]}` 起，把连续的非 a 字符各减一，遇到 a 就停'
    if 'i' in S and S['_line'] >= 14:
        return '全是 a：必须操作一次，把最后一个 a 改成 z 损失最小'
    return '找第一个不是 a 的位置 `i`：它前面的 a 一动就会变成 z，变大'


CONFIG = dict(
    num=2734, title='执行子串操作后的字典序最小字符串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='首个非 a 起连续减一',
    tags=['灵神题单', '难度分 1405'],
    code='''
class Solution:
    def smallestString(self, s: str) -> str:
        t = list(s)
        for i, c in enumerate(t):
            if c == 'a':
                continue
            # 继续向后遍历
            for j in range(i, len(t)):
                if t[j] == 'a':
                    break
                t[j] = chr(ord(t[j]) - 1)
            return ''.join(t)
        # 所有字母均为 a
        t[-1] = 'z'
        return ''.join(t)
''',
    call='''Solution().smallestString("abcab")
Solution().smallestString("aa")''',
    expect='az',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（原串）', cell=84),
        dict(type='array', var='t', label='t（i = 起点，j = 正在减一的位置；绿 = 已减一）', cell=84,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'green' if 'i' in S and v != S['s'][k] else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('c', 'c', 'cyan')],
    captions={
        't = list(s)': '把 `s` 转成列表 `t`，方便原地修改',
        'for i, c in enumerate': lambda S, B, r: f"从左往右扫：`i = {S.i}`，`c = '{S.c}'`",
        "if c == 'a'": lambda S, B, r: (f"`c = 'a'` → 跳过：把 a 减一会变成 z，字典序变大，所以子串不能包含 a" if S.c == 'a'
                                        else f"`c = '{S.c}'` 不是 a → 就从 `i = {S.i}` 开始操作"),
        'continue': '跳过这个 a，看下一个字符',
        'for j in range(i': '继续向后遍历：`j = {j}`',
        "if t[j] == 'a'": lambda S, B, r: (f"`t[{S.j}] = 'a'` → 遇到 a 就停，子串到此为止" if S.t[S.j] == 'a'
                                           else f"`t[{S.j}] = '{S.t[S.j]}'` 不是 a → 继续减一，越靠前改动越划算"),
        'break': '子串结束，跳出内层循环',
        't[j] = chr': '`t[{j}]` 减一 → `{t[j]}`',
        "return ''.join(t)": '`t` 拼回字符串 → `{ret}`',
        "t[-1] = 'z'": '所有字母均为 a，但题目==必须操作一次==：把最后一个 a 改成 z，让字典序变大得最少',
    },
    cards=dict(
        one_liner='跳过前导 a，从第一个非 a 起一路减一直到遇到 a',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选 `s` 的一个非空子串，把每个字符替换成字母表前一个（`a` 变 `z`），==恰好一次==',
                 '返回能得到的字典序最小的字符串',
                 '示例：`"cbabc"` → `"baabc"`；本视频：`"abcab"` → `"aabab"`，`"aa"` → `"az"`'],
        quote='把 a 替换成 z 会让字典序变大，所以被替换的子串不能包含 a。反过来，如果子串不含 a，那么对其操作可以让 s 字典序变小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子串里不能有 a，于是从左到右找第一个不等于 a 的 `s[i]`',
              '从 `i` 开始每个字符减一，直到结尾或遇到 a，越靠前变小越划算',
              '细节：全是 a 也必须操作一次，把最后一个 a 改成 z'],
        summary=['时间 `O(n)`，空间 `O(n)`（`t` 列表）',
                 '易错：全是 a 时不能直接返回原串，要把最后一个改成 z',
                 '只改==第一段==连续非 a，后面的非 a 不动',
                 '同类题：字典序最小/最大的贪心，优先改高位'],
    ),
)
