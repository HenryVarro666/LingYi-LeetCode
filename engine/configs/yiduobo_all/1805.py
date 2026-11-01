CONFIG = dict(
    num=1805, title='字符串中不同整数的数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历记录数字起点 + 哈希表',
    code='''
class Solution(object):
    def numDifferentIntegers(self, word):
        num_set = set()
        start = None
        for index, char in enumerate(word):
            if char >= '0' and char <= '9':
                if start is None:
                    start = index
            else:
                if start is not None:
                    while start < index - 1 and word[start] == '0':
                        start += 1
                    num_set.add(word[start:index])
                start = None

        if start is not None:
            while start < len(word) - 1 and word[start] == '0':
                start += 1
            num_set.add(word[start:])

        return len(num_set)
''',
    call='Solution().numDifferentIntegers("a1b01c001d23")',
    expect=2,
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前字符 index，粉 = 数字起点 start）', cell=64,
             pointers={'index': 'blue', 'start': 'pink'}, h=190),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: repr(x), h=150, font=34),
    ],
    watch=[('index', 'index', 'blue'), ('start', 'start', 'pink'), ('num_set', 'num_set', 'green')],
    captions={
        'num_set = set()': '`num_set` 存去掉前导零后的数字串',
        4: '`start` 记录当前数字串的起点，`None` 表示不在数字里',
        'for index, char': lambda S, B, r: (f'看第 `{S.index}` 个字符 `{S.char!r}`' if 'index' not in B or S.index != B.index else '字符都看完了'),
        "if char >= '0'": lambda S, B, r: (f'`{S.char!r}` 是数字' if '0' <= S.char <= '9' else f'`{S.char!r}` 是字母，数字串到此结束'),
        'if start is None': lambda S, B, r: ('`start` 是 None → 这是新数字串的开头，记下起点' if S.start is None
                                             else '已经在数字串里，继续往后'),
        'start = index': '`start = {start}`',
        'if start is not None': lambda S, B, r: (f'`start = {S.start}`：刚好有一个数字串 `{S.word[S.start:S.index]!r}` 结束了' if S.start is not None
                                                  else '`start` 是 None，前面不是数字串，什么也不做'),
        'while start < index - 1': lambda S, B, r: (f'`{S.word[S.start:S.index]!r}` 开头是 `0` 且至少还有两位 → 跳过前导零'
                                                    if S.start < S.index - 1 and S.word[S.start] == '0'
                                                    else f'没有前导零了（或只剩一位）→ 数字串 `{S.word[S.start:S.index]!r}`'),
        'start += 1': '`start` → {start}',
        'num_set.add(word[start:index])': '`{word[start:index]!r}` 加入集合 → `{sorted(num_set)}`',
        14: '重置 `start = None`，等下一个数字串',
        'if start is not None:': lambda S, B, r: ('遍历结束，末尾还有一个没收尾的数字串，单独处理' if S.start is not None
                                                  else '遍历结束，末尾不是数字，不用收尾'),
        'start < len(word) - 1': lambda S, B, r: (f'末尾数字串 `{S.word[S.start:]!r}` 跳过前导零' if S.start < len(S.word) - 1 and S.word[S.start] == '0'
                                                  else f'末尾数字串 `{S.word[S.start:]!r}` 没有前导零了'),
        'num_set.add(word[start:])': '末尾数字串 `{word[start:]!r}` 加入集合 → `{sorted(num_set)}`',
        'return': '哈希表大小 = 不同整数的个数：`{ret}`',
    },
    cards=dict(
        one_liner='一趟遍历切出数字串，去前导零后放进哈希表',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`word` 由数字和小写字母组成，把字母看作分隔符，得到若干整数',
                 '忽略前导零后值相同的整数只算一个，求不同整数的个数',
                 '本视频：`"a1b01c001d23"` → `2`'],
        quote='字符串长度可达1000，那么对于部分语言来说是不适合将字符串转为整数储存的，而使用字符串储存的话则需要注意处理前导0的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到数字且 `start` 为空，就记下起点；遇到字母且 `start` 非空，就收一个数字串',
              '收尾时跳过前导 0，但至少保留最后一位，再放进集合',
              '遍历结束后，末尾若还在数字里，要再收一次'],
        summary=['原文为 Python 2 风格，仅删去了类型说明文档字符串，其余无需改动',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：`"000"` 只能去到 `"0"`，所以循环条件是 `start < index - 1`',
                 '易错：字符串以数字结尾时，循环里没有机会收尾，必须在循环后补一次',
                 '对比灵神：灵神直接切出数字段，这里自己维护起点指针'],
    ),
)
