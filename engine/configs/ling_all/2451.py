CONFIG = dict(
    num=2451, title='差值数组不同的字符串', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='差值数组作 key · 哈希表分组',
    tags=[],
    code='''
class Solution:
    def oddString(self, words: List[str]) -> str:
        d = defaultdict(list)
        for s in words:
            d[tuple(ord(x) - ord(y) for x, y in pairwise(s))].append(s)
        x, y = d.values()
        return x[0] if len(x) == 1 else y[0]
''',
    call='Solution().oddString(["adc","wzy","abc","dgf"])',
    expect='abc',
    views=[
        dict(type='array', var='words', label='words', cell=110,
             color=lambda S, i, v: 'blue' if S.get('s') == v and S['_line'] in (4, 5) else None),
        dict(type='map', var='d', label='d：差值数组（key）→ 字符串列表', fmt=lambda k, v: f'{list(k) if isinstance(k, tuple) else k} → {v}', font=30),
    ],
    watch=['s', ('len(d)', 'len(d)', 'green')],
    captions={
        'd = defaultdict': '`d` 以「差值数组」为 key，把差值相同的字符串分到同一组',
        'for s in words': '取出字符串 `s = "{s}"`',
        '.append(s)': lambda S, B, r: f"`\"{S.s}\"` 的差值数组是 `{list(next(k for k, v in S.d.items() if S.s in v))}`（代码按 `ord(x) - ord(y)` 算，前减后，与题目差值正好反号，不影响分组），放进对应的组；现在共 `{len(S.d)}` 组",
        'x, y = d.values()': '恰好只有一个字符串不同 → `d` 里==只有两组==，分别取出 `x`、`y`',
        'return x[0]': lambda S, B, r: (f'`x` 只有 {len(S.x)} 个字符串，它就是落单的那个 → 返回 `"{r}"`' if len(S.x) == 1
                                       else f'`x` 有 {len(S.x)} 个字符串，那落单的就在 `y` 里 → 返回 `"{r}"`'),
    },
    cards=dict(
        one_liner='差值数组当 key 分组，落单的那组就是答案',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['每个字符串可转成「相邻字母位置之差」的差值数组，如 `"acb"` → `[2, -1]`',
                 '除了一个字符串，其余的差值数组都相同，找出那个不同的',
                 '示例：`["adc","wzy","abc"]` → `"abc"`'],
        quote='计算出每个字符串的 difference 数组，作为哈希表的 key。把相同 key 的字符串存到同一组中，答案为组内只有一个字符串的那个字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pairwise(s)` 给出相邻字母对，差值数组转成 `tuple` 才能当 key（代码里是前减后，只分组所以无妨）',
              '`defaultdict(list)` 按 key 分组，同组的字符串放一起',
              '只有两组：`x, y = d.values()`，哪组只有一个就返回哪组的 `[0]`'],
        result='`"abc"` 独占一组，其余三个同组 → 返回 `"abc"` ✓',
        summary=['时间 `O(mn)`，`m` 是单词数，`n` 是单词长度；空间 `O(m+n)`',
                 '易错：`list` 不能当字典 key，要转成 `tuple`',
                 '题目保证 `words.length >= 3`，所以恰好两组，才能 `x, y = d.values()`',
                 '代码用 `ord(x) - ord(y)`（前减后），与题目差值整体反号，但只用来分组，不影响结果'],
    ),
)
