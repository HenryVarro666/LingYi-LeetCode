MSG = ['hello', 'python', 'world', 'fun']
BAN = ['leetcode', 'world', 'hello']

CONFIG = dict(
    num=3295, title='举报垃圾信息', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='哈希集合 · 统计命中个数',
    tags=[],
    code='''
class Solution:
    def reportSpam(self, message: List[str], bannedWords: List[str]) -> bool:
        banned = set(bannedWords)
        seen = False
        for s in message:
            if s in banned:
                if seen:
                    return True
                seen = True
        return False
''',
    call=f'Solution().reportSpam({MSG!r}, {BAN!r})',
    expect=True,
    views=[
        dict(type='array', var='message', label='message（蓝 = 当前单词，绿 = 违禁词）', cell=175, h=230,
             color=lambda S, i, v: (None if S.get('s') is None else ('green' if v in S['banned'] and i <= S['message'].index(S['s']) else ('blue' if v == S['s'] else None))) if 'banned' in S else None),
        dict(type='set', var='banned', label='banned（bannedWords 放进哈希集合）', fmt=lambda x: f"'{x}'", h=170, font=30),
        dict(type='text', h=90, size=34, fn=lambda S: ('`seen = True`：已经命中过 1 个违禁词，再命中一个就是垃圾信息' if S.get('seen') else '`seen = False`：还没有命中过违禁词') if 'seen' in S else ''),
    ],
    watch=['s', ('seen', 'seen', 'green')],
    captions={
        'banned = set': '把 `bannedWords` 全丢进哈希集合：之后判断 `s in banned` 是 ==O(1)== 的，不用每次扫整个数组',
        'seen = False': '`seen` 记录"是否已经命中过一个违禁词"，只要记住有没有，不必记个数',
        'for s in message': '取下一个单词 `s = {s}`',
        'if s in banned': lambda S, B, r: (f'`{S.s}` 在 `banned` 中 → 是违禁词' if S.s in S.banned else f'`{S.s}` 不在 `banned` 中 → 跳过'),
        'if seen': lambda S, B, r: ('`seen = True`：之前已经命中过一个，这是第 2 个 → 垃圾信息' if S.seen else '`seen = False`：这是第 1 个违禁词，还不够，先记下来'),
        'return True': '命中了第二个违禁词 → 返回 `True`，后面的单词不用看了',
        'seen = True': '记下：已经见过 1 个违禁词，`seen = True`',
    },
    cards=dict(
        one_liner='bannedWords 放进哈希集合，数 message 命中了几个',
        complexity='时间 `O((n+m)l)`，空间 `O(ml)`',
        problem=['`message` 中至少有两个单词出现在 `bannedWords` 里，就是垃圾信息',
                 '示例：`["hello","world","leetcode"]`，`bannedWords = ["world","hello"]` → `true`',
                 '本视频：4 个单词，其中 `hello`、`world` 命中 → `true`'],
        quote='统计 message 中有多少个字符串在 bannedWords 中，如果超过 1 个，返回 true，否则返回 false。把 bannedWords 中的字符串全部丢到哈希集合中，从而加快效率。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`set(bannedWords)` 让每次查询变成 `O(1)`（字符串长度 `l ≤ 15`）',
              '遍历 `message`，用布尔变量 `seen` 记下是否命中过一次',
              '第二次命中时直接返回 `True`，不用数完整个数组'],
        summary=['时间 `O((n+m)l)`，`n`、`m` 是两个数组长度，`l ≤ 15` 是单词长度',
                 '空间 `O(ml)`：集合存下全部 `bannedWords`',
                 '易错点：要求是"至少两个"，所以是 `> 1`；重复单词每个都算一次',
                 '写法一：`sum(s in banned for s in message) > 1` 一行统计；本视频演示写法二：用 `seen` 提前返回'],
    ),
)
