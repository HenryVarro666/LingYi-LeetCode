W = 'FlaG'

CONFIG = dict(
    num=520, title='检测大写字母', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='数大写字母个数 · 分类讨论',
    code='''
class Solution:
    def detectCapitalUse(self, word: str) -> bool:
        cnt = sum(c.isupper() for c in word)
        return cnt == 0 or cnt == len(word) or cnt == 1 and word[0].isupper()
''',
    call=f'Solution().detectCapitalUse({W!r})',
    expect=False,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"大写字母个数 `cnt = {S['cnt']}`，长度 `n = {len(S['word'])}`" if 'cnt' in S else '先数一数 word 里有几个大写字母')),
        dict(type='string', var='word', label='word（绿 = 大写字母）', cell=110, h=260,
             color=lambda S, i, v: 'green' if v.isupper() else None),
        dict(type='text', size=26, fn=lambda S: ('三种合法情形：`cnt == 0`（全小写）、`cnt == n`（全大写）、`cnt == 1` 且首字母大写' )),
    ],
    watch=[('cnt', 'cnt', 'green'), ('n', 'len(word)'), ('首字母大写', 'word[0].isupper()')],
    captions={
        'cnt = sum': '逐个字母 `isupper()` 再求和：`{word}` 里有 =={cnt}== 个大写字母',
        'return cnt == 0': lambda S, B, ret: (
            f"`cnt == 0`？{S.cnt == 0}；`cnt == n = {len(S.word)}`？{S.cnt == len(S.word)}；"
            f"`cnt == 1` 且首字母大写？{S.cnt == 1 and S.word[0].isupper()} → 都不满足 ==不合法==，返回 `False`"
            if not ret else '满足其中一种情形，返回 `True`'),
    },
    cards=dict(
        one_liner='数出大写字母个数 cnt，只有三种情形合法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['大写用法正确：==全大写==、==全小写==、==只有首字母大写==',
                 '给定 `word`，判断大写用法是否正确',
                 '示例：`"USA"` → `true`，`"FlaG"` → `false`'],
        quote='设 word 中的大写字母的个数为 cnt。分类讨论：cnt=0 全小写；cnt=n 全大写；cnt=1 且 word[0] 是大写字母，只有首字母大写。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不逐个比较字符，只数一个数 `cnt`',
              '`cnt` 为 0、`n`，或 1 且首字母大写，就是合法的',
              '本视频：`"FlaG"` 有 2 个大写，三种情形都不满足'],
        after=[dict(heading='三种合法情形对照', lines=[
            '`cnt == 0`：全小写，如 `"leetcode"`',
            '`cnt == n`：全大写，如 `"USA"`',
            '`cnt == 1` 且 `word[0]` 大写：只有首字母大写，如 `"Google"`',
            '其余都不合法，如 `"FlaG"`（2 个大写）、`"gOogle"`（大写不在首位）'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`cnt == 1` 时必须检查大写的恰好是首字母，如 `"gOogle"` 不合法',
                 '`and` 优先级高于 `or`，所以第三项整体是一个条件',
                 '另一种写法：`word.islower() or word.isupper() or word.istitle()`，库函数一行搞定'],
    ),
)
