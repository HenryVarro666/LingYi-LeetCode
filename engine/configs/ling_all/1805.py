CONFIG = dict(
    num=1805, title='字符串中不同整数的数目', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='切出数字串 + 去前导零 + 哈希集合（Go 原文转写）',
    code='''
class Solution:
    def numDifferentIntegers(self, word: str) -> int:
        set_ = set()
        for s in re.findall(r'\\d+', word):
            while len(s) > 1 and s[0] == '0':
                s = s[1:]
            set_.add(s)
        return len(set_)
''',
    setup='import re',
    call='Solution().numDifferentIntegers("a1b01c001d23")',
    expect=2,
    views=[
        dict(type='string', var='word', label='word', cell=64, h=150),
        dict(type='text', h=80, size=32, fn=lambda S: f"当前数字串 `s` = {S['s']!r}" if 's' in S else ''),
        dict(type='set', var='set_', label='set_（去掉前导零后的数字串）', fmt=lambda x: repr(x), h=150, font=34),
    ],
    watch=[('s', 's', 'blue'), ('set_', 'set_', 'green')],
    captions={
        'set_ = set()': '集合存==去掉前导零==后的数字串，用来去重',
        'for s in': lambda S, B, r: (f'取出下一个连续数字串 `s = {S.s!r}`' if 's' in S and S.get('s') != B.get('s') or 's' not in B
                                     else '数字串都处理完了'),
        'while len(s) > 1': lambda S, B, r: (f'`s = {S.s!r}` 长度 > 1 且以 `0` 开头 → 去掉前导零' if len(S.s) > 1 and S.s[0] == '0'
                                             else f'`s = {S.s!r}` 没有前导零了（或只剩一位）→ 停止'),
        's = s[1:]': '去掉第一位 → `s = {s!r}`',
        'set_.add': '加入集合 `{s!r}`（已有则不变）→ `{sorted(set_)}`',
        'return': '集合大小就是不同整数的个数：`{ret}`',
    },
    cards=dict(
        one_liner='数字串去掉前导零后塞进集合，数集合大小',
        complexity='时间 `O(n^2)`（去前导零按切片计），空间 `O(n)`',
        problem=['把 `word` 里的字母都换成空格，剩下若干整数',
                 '数值相同（忽略前导零）算同一个整数，求不同整数的个数',
                 '示例：`"a1b01c001"` → `1`；本视频：`"a1b01c001d23"` → `2`'],
        quote='for len(s) > 1 && s[0] == \'0\' { s = s[1:] }；set[s] = struct{}{}',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['整数可能很长，不转成数字，直接当字符串处理',
              '以小写字母为分隔，切出每段数字，去掉前导零（至少保留一位）后放进集合',
              '集合自动去重，答案就是 `len(set)`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`FieldsFunc(word, IsLower)` → `re.findall(r\'\\d+\', word)`（得到相同的数字串，`import re` 放在 setup），`map[string]struct{}` → `set`',
                 '时间 `O(n^2)` 最坏（反复切片），`n ≤ 1000` 无压力；空间 `O(n)`',
                 '易错：`"0"` 本身不能被去光，所以条件是 `len(s) > 1`',
                 '易错：不能转 int 的语言要注意超长整数，字符串比较最稳'],
    ),
)
