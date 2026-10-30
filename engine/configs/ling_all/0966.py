CONFIG = dict(
    num=966, title='元音拼写检查器', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='三张哈希表 · 倒序建表', tags=[],
    code='''
class Solution:
    def spellchecker(self, wordlist: List[str], queries: List[str]) -> List[str]:
        origin = set(wordlist)
        lower_to_origin = {}
        vowel_to_origin = {}
        trans = str.maketrans("aeiou", "?????")  # 替换元音为 '?'

        for s in reversed(wordlist):
            lower = s.lower()
            lower_to_origin[lower] = s  # 例如 kite -> KiTe
            vowel_to_origin[lower.translate(trans)] = s  # 例如 k?t? -> KiTe

        for i, q in enumerate(queries):
            if q in origin:  # 完全匹配
                continue
            lower = q.lower()
            if lower in lower_to_origin:  # 不区分大小写的匹配
                queries[i] = lower_to_origin[lower]
            else:  # 不区分大小写+元音模糊匹配
                queries[i] = vowel_to_origin.get(lower.translate(trans), "")
        return queries
''',
    call='Solution().spellchecker(["KiTe","kite","hare","Hare"], ["kite","Kite","Hear","keti","keet"])',
    expect=['kite', 'KiTe', '', 'KiTe', ''],
    views=[
        dict(type='array', var='wordlist', label='wordlist', h=140, cell=100,
             color=lambda S, i, v: 'purple' if S['_line'] in (9, 10, 11) and S.get('s') == v else None),
        dict(type='map', var='lower_to_origin', label='lower_to_origin（忽略大小写）', h=150, font=26),
        dict(type='map', var='vowel_to_origin', label='vowel_to_origin（元音→?）', h=150, font=26),
        dict(type='array', var='queries', label='queries（原地改写成答案）', pointers={'i': 'blue'}, h=170, cell=100),
    ],
    watch=['s', 'lower', 'q', ('i', 'i', 'blue')],
    captions={
        'origin = set': '`origin`：存原始单词，用来判断==完全匹配==（区分大小写）',
        'lower_to_origin = {}': '第二级：key 是全小写，value 是原单词',
        'vowel_to_origin = {}': '第三级：key 是全小写且元音都换成 `?`',
        'trans = str.maketrans': '`trans` 把 aeiou 都映射成 `?`',
        'for s in reversed': '==倒着遍历==：同一个 key 后写的覆盖先写的，最左边的单词最后写入，保证返回第一个匹配',
        'lower = s.lower()': '`{s}` 转小写得 `{lower}`',
        'lower_to_origin[lower] = s': '`lower_to_origin[{lower!r}] = {s!r}`：越靠左的单词越晚写入、越后覆盖',
        'vowel_to_origin[lower': '`vowel_to_origin[{lower.translate(trans)!r}] = {s!r}`：元音抹成 `?` 当 key',
        'for i, q in enumerate': '依次处理查询 `{q}`',
        'if q in origin': lambda S, B, r: f'`{S.q}` 在 origin 里？{"是：完全匹配，原样保留" if S.q in S.origin else "否：继续降级"}',
        'continue': '完全匹配优先级最高，保持原词不动',
        'lower = q.lower()': '`{q}` 转小写得 `{lower}`',
        'if lower in lower_to_origin': lambda S, B, r: f'`{S.lower}` 在 lower_to_origin 中？{"是：大小写匹配" if S.lower in S.lower_to_origin else "否：试元音模糊"}',
        'queries[i] = lower_to_origin': '大小写匹配，换成表里最左的原词 `{queries[i]}`',
        'queries[i] = vowel_to_origin': lambda S, B, r: f'元音模糊：`{S.lower.translate(S.trans)}` 查 vowel_to_origin → ' + (f'命中 `{S.queries[S.i]}`' if S.queries[S.i] else '没有，返回空串'),
        'return queries': '返回改写后的 `queries`',
    },
    cards=dict(
        one_liner='三级匹配三张表：完全、忽略大小写、元音模糊',
        complexity='时间 `O((n+m)L)`，空间 `O(nL)`',
        problem=['按优先级把查询词纠正为单词表里的词：完全匹配 > 大小写匹配 > 元音错误匹配',
                 '大小写、元音错误都取单词表中==第一个==匹配项，没有则返回空串',
                 '本视频：词表 `[KiTe,kite,hare,Hare]` → 答案 `[kite,KiTe,"",KiTe,""]`'],
        quote='题目要求返回单词列表中的第一个匹配项，即最靠左的匹配项。我们可以倒着遍历 wordlist，处理每个字符串。这样对于相同的 key，哈希表中的 value 就是 wordlist 中的最靠左的匹配项了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['完全匹配：用哈希集合 `origin`',
              '大小写匹配：key = 小写串；元音模糊：key = 小写串且元音换成 `?`',
              '倒序建表，让最左的单词最后写入，覆盖后面的'],
        summary=['时间 `O((n+m)L)`，`L <= 7`；空间 `O(nL)`',
                 '易错：正序建表会留下最靠右的匹配；要么倒序写入，要么 `setdefault`',
                 '易错：完全匹配必须区分大小写，且优先于另两级',
                 '代码直接在 `queries` 上原地改写答案'],
    ),
)
