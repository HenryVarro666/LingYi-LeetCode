MSG = ['hello', 'python', 'world', 'fun']
BAN = ['leetcode', 'world', 'hello']

CONFIG = dict(
    num=3295, title='举报垃圾信息', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希集合 · 命中两个就返回',
    tags=[],
    code='''
class Solution(object):
    def reportSpam(self, message, bannedWords):

        banned_set = set(bannedWords)
        cnt = 0
        for word in message:
            if word in banned_set:
                cnt += 1
                if cnt == 2:
                    return True

        return False
''',
    call=f'Solution().reportSpam({MSG!r}, {BAN!r})',
    expect=True,
    views=[
        dict(type='array', var='message', label='message（蓝 = 当前单词，绿 = 命中）', cell=175, h=230,
             color=lambda S, i, v: (None if S.get('word') is None else ('green' if v in S['banned_set'] and i <= S['message'].index(S['word']) else ('blue' if v == S['word'] else None))) if 'banned_set' in S else None),
        dict(type='set', var='banned_set', label='banned_set', fmt=lambda x: f"'{x}'", h=170, font=30),
        dict(type='text', h=90, size=34, fn=lambda S: f"已命中 `cnt = {S['cnt']}`，达到 2 就是垃圾信息" if 'cnt' in S else ''),
    ],
    watch=['word', ('cnt', 'cnt', 'green')],
    captions={
        'banned_set = set': '作者说可以做成 trie 树或哈希表，这里用哈希集合：`bannedWords` 去重后放进 `banned_set`',
        'cnt = 0': '`cnt` 统计 `message` 里有多少个单词在 `banned_set` 里',
        'for word in message': '取下一个单词 `word = {word}`',
        'if word in banned_set': lambda S, B, r: (f'`{S.word}` 在 `banned_set` 中 → 命中' if S.word in S.banned_set else f'`{S.word}` 不在 `banned_set` 中 → 跳过'),
        'cnt += 1': '命中一个，`cnt` → =={cnt}==',
        'if cnt == 2': lambda S, B, r: ('`cnt == 2`：已有两个违禁词，不用再看后面的了' if S.cnt == 2 else '`cnt = %d`，还不到 2 个，继续往后看' % S.cnt),
        'return True': '至少两个单词命中 → 返回 `True`',
    },
    cards=dict(
        one_liner='遍历 message，命中 banned 的单词数到 2 就返回',
        complexity='时间 `O((n+m)l)`，空间 `O(ml)`',
        problem=['`message` 里至少有两个单词出现在 `bannedWords` 中 → 返回 `true`',
                 '示例：`["hello","world","leetcode"]`，`bannedWords = ["world","hello"]` → `true`',
                 '本视频：`["hello","python","world","fun"]` → `true`'],
        quote='将bannedWords做成trie树或者哈希表，然后遍历message中的所有单词，判断是否有两个单词出现在bannedWords中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `bannedWords` 做成集合，查询 `O(1)`',
              '遍历 `message`，用 `cnt` 记命中次数',
              '`cnt` 一到 2 就立刻 `return True`，后面不用再看'],
        summary=['时间 `O((n+m)l)`，空间 `O(ml)`',
                 '易错点：重复出现的违禁词每次都算一个',
                 '对比灵神：灵神 `sum(... ) > 1` 一行统计；这里手动计数并提前返回'],
    ),
)
