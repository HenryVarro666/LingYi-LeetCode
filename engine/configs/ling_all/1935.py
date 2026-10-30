CONFIG = dict(
    num=1935, title='可以输入的最大单词数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='位运算表示字母集合',
    tags=[],
    code='''
class Solution:
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        broken_mask = 0
        for c in brokenLetters:
            broken_mask |= 1 << (ord(c) - ord('a'))  # 把 c 加到集合中

        ans = 0
        ok = True
        for c in text:
            if c == ' ':  # 上一个单词遍历完毕
                ans += ok
                ok = True
            elif broken_mask >> (ord(c) - ord('a')) & 1:  # c 在 brokenLetters 中
                ok = False
        ans += ok  # 最后一个单词
        return ans
''',
    call="Solution().canBeTypedWords('leet code go', 'lt')",
    expect=2,
    views=[
        dict(type='string', var='brokenLetters', label='brokenLetters（损坏的键）', h=150),
        dict(type='text', fn=lambda S: f"broken_mask = `{bin(S['broken_mask'])[2:]}`（第 k 位为 1 表示字母表第 k 个字母损坏）" if 'broken_mask' in S else '', h=70),
        dict(type='string', var='text', label='text', cell=48, h=230,
             dim=lambda S, i, v: v == ' '),
    ],
    watch=[('c', 'c', 'blue'), ('ok', 'ok', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'broken_mask |= ': '`{c}` 是第 `{ord(c) - 97}` 个字母 → 把第 {ord(c) - 97} 位置 1：`broken_mask = {bin(broken_mask)[2:]}`',
        'ans = 0': '`ans` 统计能打出的单词数',
        "if c == ' '": lambda S, B, r: ("遇到空格：上一个单词结束" if S.c == ' ' else f"`{S.c}` 不是空格，继续看这个字母"),
        11: '结算上一个单词：`ans += ok`（ok 为 {ok}）→ `ans = {ans}`',
        12: '开始新单词，重新假设能打出',
        8: '假设当前单词能打出',
        'elif broken_mask': lambda S, B, r: (f"`{S.c}`：`broken_mask >> {ord(S.c)-97} & 1` = {S.broken_mask >> (ord(S.c)-97) & 1}" + (" → ==键坏了==，这个单词打不出" if S.broken_mask >> (ord(S.c)-97) & 1 else " → 键完好")),
        'ok = False': '`ok = False`：当前单词作废',
        'ans += ok  # 最后': '最后一个单词后面没有空格，要在循环外补结算：`ans = {ans}`',
        'return ans': '共 `{ans}` 个单词能完整输入',
    },
    cards=dict(
        one_liner='把损坏的键压成一个整数，查一个字母只要移位再按位与',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['`brokenLetters` 里的字母键坏了，统计 `text` 中能完整打出的单词数',
                 '示例：`text = "hello world"`，`brokenLetters = "ad"` → `1`',
                 '本视频：`"leet code go"`，坏键 `"lt"` → `2`'],
        quote='把 brokenLetters 视作一个字母集合，我们需要判断单词中的字母是否在这个集合中。集合可以用二进制数表示，集合的运算可以用位运算快速计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把坏键放进 `broken_mask`：字母 `c` 对应第 `ord(c)-ord(a)` 位',
              '边扫 `text` 边判断：遇到坏键就 `ok = False`，遇到空格结算上一个单词',
              '最后一个单词后没有空格，要在循环外再 `ans += ok`'],
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '易错点：==最后一个单词==要在循环外结算',
                 '优化前的写法：`text.split()` 加 `all(c not in brokenLetters ...)`，时间 `O(nm)`',
                 '`ans += ok` 利用 True 就是 1'],
    ),
)
