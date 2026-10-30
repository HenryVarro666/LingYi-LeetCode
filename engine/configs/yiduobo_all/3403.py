def _color(S, x, v):
    if 'p' not in S or 'q' not in S:
        return None
    p, q, L = S['p'], S['q'], S.get('length', 0)
    if S['_line'] >= 23:
        return 'green' if p <= x < p + len(S['word']) - S['numFriends'] + 1 else None
    if p <= x < p + L or q <= x < q + L:
        return 'green'
    if x == p + L and p + L < len(S['word']):
        return 'blue'
    if x == q + L and q + L < len(S['word']):
        return 'pink'
    return None


CONFIG = dict(
    num=3403, title='从盒子中找出字典序最大的字符串 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='最大后缀 · 截取前缀',
    tags=['灵神题单·贪心与思维', '灵神题单·字符串', '难度分 1762'],
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
    call='Solution().answerString("cacbcacb", 3)',
    expect='cbcacb',
    views=[
        dict(type='string', var='word', label='word（绿 = 已相等部分，蓝 = word[p+length]，粉 = word[q+length]）', cell=84, h=250,
             pointers={'p': 'blue', 'q': 'pink'}, color=_color),
        dict(type='text', size=26, fn=lambda S: (
            f"当前最大后缀起点 `p = {S['p']}`，对手 `q = {S['q']}`，已相等 `length = {S.get('length', 0)}`" if 'q' in S else '')),
        dict(type='text', size=24, fn=lambda S: (
            f"答案长度上限 `len(word) − numFriends + 1 = {len(S['word']) - S['numFriends'] + 1}`" if 'word' in S else '')),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('length', 'length', 'yellow')],
    skip=['q = 1', 'length = 0'],
    captions={
        'if numFriends == 1': '`numFriends = {numFriends}`：需要分割。（为 1 时不能分，直接返回 `word`）',
        'p = 0': '`p` 记录目前最大后缀的起点，`q = 1` 是要比较的另一个后缀起点',
        'while q + length': lambda S, B, r: (f'`q + length = {S.q + S.length} < {len(S.word)}`：还没比到末尾' if S.q + S.length < len(S.word)
                                             else '`q + length` 到末尾，所有后缀比完了'),
        'if word[p + length] == word[q + length]': lambda S, B, r: (
            f"`word[{S.p + S.length}] = {S.word[S.p + S.length]}` == `word[{S.q + S.length}] = {S.word[S.q + S.length]}` → 两个后缀前 `length` 位相同，继续比下一位"
            if S.word[S.p + S.length] == S.word[S.q + S.length]
            else f"`word[{S.p + S.length}] = {S.word[S.p + S.length]}` ≠ `word[{S.q + S.length}] = {S.word[S.q + S.length]}` → 出现不同，看谁大"),
        'length += 1': '相同的长度 `length` → {length}',
        'elif word[p] < word[q + length]': lambda S, B, r: (
            f"`word[p] = {S.word[S.p]}` < `word[q + length] = {S.word[S.q + S.length]}` → 这个字母比 `p` 开头还大，`q + length` 之前的起点都不用考虑"
            if S.word[S.p] < S.word[S.q + S.length]
            else f"`word[p] = {S.word[S.p]}` ≥ `word[q + length] = {S.word[S.q + S.length]}` → 不满足，再看下一个条件"),
        'p = q + length': '`p` 跳到 `{p}`，`q = p + 1 = {p + 1}` 重新比较',
        'q = p + 1': '`q` → {q}，`length` 清零重新比',
        'elif word[p + length] < word[q + length]': lambda S, B, r: (
            f"`word[{S.p + S.length}] = {S.word[S.p + S.length]}` < `word[{S.q + S.length}] = {S.word[S.q + S.length]}` → q 开头的后缀更大"
            if S.word[S.p + S.length] < S.word[S.q + S.length]
            else f"`word[{S.p + S.length}] = {S.word[S.p + S.length]}` > `word[{S.q + S.length}] = {S.word[S.q + S.length]}` → p 开头的后缀更大"),
        'p = q': '`q` 开头的后缀更大 → `p = {p}`',
        'q += 1': '`q` → {q}，`length` 清零重新比',
        'q += length + 1': '`p` 开头的更大，保留；`q` 跳过已比较的部分 → {q}',
        'return word[p:': lambda S, B, r: f"最大后缀从 `p = {S.p}` 开始，截取 `{len(S.word) - S.numFriends + 1}` 位 → `{r}`",
    },
    cards=dict(
        one_liner='答案必是最大后缀的前 len−k+1 位，用双指针求最大后缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `word` 分成 `numFriends` 个非空子串，所有分法得到的子串都放进盒子',
                 '求盒子里==字典序最大==的字符串',
                 '示例：`"dbca"`，`2` → `"dbc"`；本视频：`"cacbcacb"`，`3` → `"cbcacb"`'],
        quote='字典序最大的子串必然是word的某个后缀。……最终答案就是word中字典序最大的后缀的长度为len(word) - numFriends + 1的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['不限长度时，最大子串一定是后缀：子串后面再接字符只会更大',
              '划分要求让答案长度 ≤ `len − numFriends + 1`（其余每段留 1 个字符）',
              '用 1163 题的双指针 `p, q` 找出最大后缀，再截取前缀'],
        result='最大后缀 `"cbcacb"`，长度刚好是 6 → `"cbcacb"` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`；第二题 II 数据到 2×10^5 也可用同样方法',
                 '`numFriends == 1` 要单独处理，答案是整个 `word`',
                 '最大后缀不足 `len − numFriends + 1` 位时，切片自然取到末尾',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
