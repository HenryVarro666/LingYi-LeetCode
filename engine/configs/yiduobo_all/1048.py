def _top(S):
    if 'word' not in S or S['_line'] not in (8, 9, 10, 12):
        return '`f[word]`：以 word 结尾的最优解；对每个单词只检查「删一个字母」的几个 tmp'
    if S['_line'] == 12:
        return f"`f[{S['word']!r}] = {S['l']}`，全局 `res = {S['res']}`"
    if 'pos' not in S:
        return f"当前单词 `{S['word']}`"
    w, p = S['word'], S['pos']
    t = w[:p] + w[p + 1:]
    return f"`{w}` 删去 `{w[p]}` → `{t or '空串'}`，`f.get` 得 =={S['f'].get(t, 0)}=="


CONFIG = dict(
    num=1048, title='最长字符串链', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='f[word] 状态 · 删字母找前置串',
    tags=['灵神题单', '难度分 1599'],
    code='''
class Solution(object):
    def longestStrChain(self, words):

        f = {}
        res = 1
        for word in sorted(words, key=lambda d:len(d)):
            l = 1
            for pos in range(len(word)):
                tmp = word[:pos] + word[pos + 1:]
                l = max(l, f.get(tmp, 0) + 1)
            
            f[word] = l
            res = max(res, l)
        
        return res
''',
    call='Solution().longestStrChain(["xbc","pcxbcf","xb","cxbc","pcxbc"])',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='array', var='words', label='words（原顺序，蓝 = 当前 word）', cell=120, h=170,
             color=lambda S, k, v: 'blue' if 'word' in S and v == S['word'] else None),
        dict(type='map', var='f', label='f[word]：以 word 结尾的最优解', fmt=lambda k, v: f"'{k}': {v}", h=260, font=34),
    ],
    watch=[('word', 'word', 'blue'), ('pos', 'pos', 'pink'), ('l', 'l', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = {}': '`f[word]` 不是 `f[i]`：直接用单词当状态',
        'res = 1': '`res` 至少是 1：单个单词本身就是一条链',
        'for word in sorted': lambda S, B, r: ('单词都处理完了' if S.get('word') is not None and S.word in S.f else
                                              f'按长度从小到大取 `word = "{S.word}"`，短的先算'),
        'l = 1': '`l = 1`：这个单词自己成链',
        'for pos in range': lambda S, B, r: ('`word` 的每个位置都删过了，往下记录结果' if B.get('pos') == S.pos and 'pos' in B and B.get('word') == S.word else '枚举要删去的位置 `pos`'),
        'tmp = word': '删去 `word[{pos}]` 得到前置串 `tmp = "{tmp}"`',
        'l = max': '`tmp` 的最优 `{f.get(tmp, 0)}`（不在 words 里为 0）+ 1 → `l = {l}`',
        'f[word] = l': '`f["{word}"] = {l}`，以后更长的单词可以拿它当前置',
        'res = max': '`res = max({B.res}, {l}) = {res}`：记录全局最长链',
        'return res': '最长词链长度 `{ret}`',
    },
    cards=dict(
        one_liner='f[word] 表示以单词结尾的最优解，删一个字母找前置',
        complexity='时间 `O(nlogn + nL²)`，空间 `O(nL)`',
        problem=['在 `word_A` 任意位置添加一个字母得到 `word_B`，A 就是 B 的前身',
                 '从 `words` 里选词组成词链，求最长长度',
                 '示例：`["xbc","pcxbcf","xb","cxbc","pcxbc"]` → `5`'],
        quote='相比与经典的f[i]表示以第i个单词结尾时的最优解，在这里我才用的是f[word]表示以单词word结尾的最优解。',
        quote_src='—— yiduobo 题解原文',
        idea=['像最长上升子序列，但「上升」是添加一个字母，所以先按长度排序',
              '传统 `f[i]` 要枚举所有 `words[j]` 判断能否转移',
              '用 `f[word]`，只需检查删掉每个字母后的 `tmp`，最多 L 个'],
        summary=['时间 `O(nlogn + nL²)`，每个单词删字母并拼接 `O(L²)`',
                 '`f.get(tmp, 0)`：`tmp` 不在表里就当 0，不会误插入',
                 '`res` 初始为 1，因为单个单词也是词链',
                 '对比灵神：灵神 `f[s] = res + 1` 最后统一取 `max`，这里边算边更新 `res`'],
    ),
)
