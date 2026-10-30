CONFIG = dict(
    num=3406, title='从盒子中找出字典序最大的字符串 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='最大后缀 · 双指针 p/q',
    tags=['灵神题单·字符串'],
    code='''
class Solution(object):
    def answerString(self, word, numFriends):
        
        if numFriends == 1:
            return word

        p = 0
        q = 1
        length = 0
        while q + length < len(word):
            if word[p + length] == word[q + length]:
                length += 1
            elif word[p] < word[q + length]:
                p = q + length
                q = p + 1
                length = 0
            elif word[p + length] < word[q + length]:
                p = q
                q += 1
                length = 0
            else:
                q += length + 1
                length = 0

        return word[p: p + len(word) - numFriends + 1]
''',
    call='Solution().answerString("abcabcbac", 3)',
    expect='cbac',
    views=[
        dict(type='string', var='word', label='word：蓝 = p（最大后缀起点），粉 = q（挑战者）', pointers={'p': 'blue', 'q': 'pink'}, h=230, cell=70,
             color=lambda S, idx, v: ('blue' if idx == S.get('p') else 'pink' if idx == S.get('q') else None) if 'q' in S else None),
        dict(type='text', fn=lambda S: (f"比较后缀 `word[{S['p']}:]` 与 `word[{S['q']}:]`：前 `length={S['length']}` 位相同" if 'length' in S and 'q' in S else ''), h=70),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('length', 'length', 'yellow'), 'numFriends'],
    captions={
        'if numFriends == 1': lambda S, B, r: ('只有 1 个朋友时不用切，答案就是整个 `word`' if S.numFriends == 1 else '`numFriends = {}` 不是 1，要找最大后缀'.format(S.numFriends)),
        'p = 0': '`p`：目前字典序最大的后缀的起点',
        'q = 1': '`q`：下一个要比较的后缀的起点',
        9: '`length`：`p`、`q` 两个后缀已经相同的字符数',
        16: '`length` 清零，重新比较',
        20: '`length` 清零，重新比较',
        23: '`length` 清零，重新比较',
        'while q + length': lambda S, B, r: (f'`q + length = {S.q + S.length} < {len(S.word)}`：还没比到末尾' if S.q + S.length < len(S.word) else f'`q + length = {S.q + S.length} >= {len(S.word)}`：比到末尾，`p` 就是最大后缀'),
        'if word[p + length] == word[q + length]': lambda S, B, r: (f"`'{S.word[S.p+S.length]}' == '{S.word[S.q+S.length]}'` → 还相同，继续比下一位" if S.word[S.p+S.length] == S.word[S.q+S.length] else f"`'{S.word[S.p+S.length]}' != '{S.word[S.q+S.length]}'` → 出现不同，分胜负"),
        'length += 1': '相同长度 `length` → {length}',
        'elif word[p] < word[q + length]': lambda S, B, r: (f"`word[p] = '{S.word[S.p]}' < word[q+length] = '{S.word[S.q+S.length]}'` → q 这边更大，`p` 可以直接跳到 `q+length`" if S.word[S.p] < S.word[S.q+S.length] else f"`word[p] = '{S.word[S.p]}'` 不小于 `'{S.word[S.q+S.length]}'` → 继续看"),
        'p = q + length': '`p = q + length = {p}`：这中间的起点都不可能是最大后缀',
        'q = p + 1': '`q` 从新 `p` 后一位重新开始：{q}',
        'elif word[p + length] < word[q + length]': lambda S, B, r: (f"`'{S.word[S.p+S.length]}' < '{S.word[S.q+S.length]}'` → q 更大，`p` 换成 `q`" if S.word[S.p+S.length] < S.word[S.q+S.length] else f"`'{S.word[S.p+S.length]}' > '{S.word[S.q+S.length]}'` → p 更大，`q` 跳过 `length+1` 个"),
        'p = q': '`p = q = {p}`',
        'q += 1': '`q` 后移一位：{q}',
        'q += length + 1': 'p 更大：`q` 到 `q+length` 都比不过 `p`，`q` 跳到 {q}',
        'return word[p:': '最大后缀从 `{p}` 开始，最多取 `len(word) - numFriends + 1 = {len(word) - numFriends + 1}` 位（后缀不够就取到末尾）→ `{ret}`',
    },
    cards=dict(
        one_liner='字典序最大的子串一定是某个后缀，再按长度上限截断',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `word` 切成 `numFriends` 个非空子串，每种切法收集所有子串',
                 '求所有切法里出现过的字典序最大的子串',
                 '本视频：`word="abcabcbac"`，`numFriends=3` → `"cbac"`'],
        quote='字典序最大的子串必然是word的某个后缀。……最终答案就是word中字典序最大的后缀的长度为len(word) - numFriends + 1的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['子串 `word[l:r]` 若 `r` 没到末尾，接上后面字符更大 → ==最大子串必是后缀==',
              '其余 `numFriends-1` 份各占 1 个字符，最长的一份长 `n - numFriends + 1`',
              '找最大后缀用 `p`、`q`、`length` 三变量，一遍扫描（和 1163 同一套）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`numFriends == 1` 先特判直接返回 `word`',
                 '后缀不够长时，切片会自动停在末尾，正好是「后缀自身」',
                 '同类题：1163 按字典序排在最后的子串；3403 是同题的小数据版'],
    ),
)
