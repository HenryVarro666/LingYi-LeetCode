SENT = 'cat  a-b. b8d -ab x!y ba-c'

CONFIG = dict(
    num=2047, title='句子中的有效单词数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='逐条检查：数字、连字符、标点（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def countValidWords(self, sentence: str) -> int:
        ans = 0
        for s in sentence.split(): # 按照空格分割
            if any(c in "0123456789" for c in s): # 不能包含数字
                continue
            i = s.find('-')
            if i >= 0 and ("-" in s[i+1:] or # 应至多包含一个连字符
                           i == 0 or i == len(s)-1 or not s[i-1].islower() or not s[i+1].islower()): # 连字符左右应均为小写字母
                continue
            for ch in "!.,":
                j = s.find(ch)
                if j >= 0 and j < len(s)-1: # 标点符号应当位于末尾
                    break
            else:
                ans += 1 # 单词是有效的
        return ans
''',
    call=f'Solution().countValidWords({SENT!r})',
    expect=3,
    views=[
        dict(type='array', var=lambda S: S['sentence'].split(), label='sentence.split()（蓝 = 当前 token）', cell=130, h=200, index=False,
             color=lambda S, i, v: 'blue' if 's' in S and i == S['sentence'].split().index(S['s']) else None),
        dict(type='string', var='s', label='当前 token（逐字符看）', cell=84, h=220,
             pointers={'i if i >= 0 else None': 'orange'}, pointer_labels={'i if i >= 0 else None': '-'}),
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"当前 `s = '{S['s']}'`，已有 `ans = {S['ans']}` 个有效单词" if 's' in S else '先把句子按空白切成 token')),
    ],
    watch=[('s', 's', 'blue'), ('i', 'i', 'orange'), ('j', 'j', 'cyan'), ('ans', 'ans', 'green')],
    max_steps=90,
    captions={
        'ans = 0': '`ans` 统计有效单词数',
        'for s in sentence.split()': '`split()` 自动吃掉多余空格；看第一个/下一个 token：`s = "{s}"`',
        'any(c in': lambda S, B, ret: (f'`"{S.s}"` 里有数字 → ==无效==，跳过' if any(c in "0123456789" for c in S.s) else f'`"{S.s}"` 不含数字，继续查连字符'),
        'continue': '这个 token 已经无效，直接看下一个',
        'i = s.find': lambda S, B, ret: (f'连字符位置 `i = {S.i}`' if S.i >= 0 else '没有连字符 `i = -1`，这条规则通过'),
        'if i >= 0 and': lambda S, B, ret: (
            '没有连字符，不用查' if S.i < 0 else
            (f'`i = {S.i}`：有第二个连字符 / 在开头 / 在结尾 / 左右不是小写字母 → ==无效==' if (
                '-' in S.s[S.i+1:] or S.i == 0 or S.i == len(S.s)-1 or not S.s[S.i-1].islower() or not S.s[S.i+1].islower())
             else f'连字符在 `{S.i}`，只有一个且两侧都是小写字母 → 通过')),
        'i == 0 or i == len(s)-1': '续上一行：连字符不能在两端，且左右两个字符都得是小写字母',
        'for ch in "!.,"': '逐个检查三种标点：`ch = "{ch}"`',
        'j = s.find(ch)': lambda S, B, ret: (f'标点 `{S.ch}` 的位置 `j = {S.j}`' if S.j >= 0 else f'没有标点 `{S.ch}`'),
        'if j >= 0 and': lambda S, B, ret: (f'`j = {S.j} < len(s)-1 = {len(S.s)-1}`：标点不在末尾 → ==无效=='
                                            if (S.j >= 0 and S.j < len(S.s)-1) else '这个标点不存在或在末尾 → 没问题'),
        'break': '标点位置不对：跳出循环，`else` 不会执行，不计数',
        'ans += 1': '三条规则都通过 → ==有效单词==，`ans = {ans}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='先按空白切词，再逐条验：无数字、连字符合法、标点在末尾',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['token 有效：不含数字；至多一个连字符且两侧是小写字母；至多一个标点且在末尾',
                 '返回句子中有效单词的数目',
                 '示例：`"cat and  dog"` → `3`；本视频用 `"cat  a-b. b8d -ab x!y ba-c"`'],
        quote='按照空格分割；不能包含数字；应至多包含一个连字符；连字符左右应均为小写字母；标点符号应当位于末尾；单词是有效的',
        quote_src='—— 灵茶山艾府题解（代码注释）',
        idea=['`split()` 按任意多个空白切 token',
              '有数字直接丢；再用 `find` 找连字符，查位置和两侧字符',
              '最后查 `!.,` 三种标点，只要不在末尾就无效'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`continue next` 标签 → `for ... else`，`strings.Fields` → `split()`，内层 `i` 改名 `j`）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：连字符在开头/结尾，或两侧不是小写字母（如 `1-s`、`a-!`）都无效',
                 '原文还给了正则写法 `^[a-z]*([a-z]-[a-z])?[a-z]*[!.,]?$`，一行搞定，此处不演示'],
    ),
)
