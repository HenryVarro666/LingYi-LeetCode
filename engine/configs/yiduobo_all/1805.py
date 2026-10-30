def _txt(S):
    if 'num_set' not in S:
        return '用哈希集合装“去掉前导 0 的数字串”，最后数集合大小'
    st = S.get('start')
    cur = f"正在读的数字段从下标 `{st}` 开始" if st is not None else '当前不在数字段中'
    return f"{cur}；集合里已有 `{len(S['num_set'])}` 个不同整数"


def _cur(S):
    st, i = S.get('start'), S.get('index')
    if st is None or i is None:
        return None
    return st


CONFIG = dict(
    num=1805, title='字符串中不同整数的数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 字符串去前导零入哈希集合',
    tags=[],
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
    call="Solution().numDifferentIntegers('a1b01c2d30')",
    expect=3,
    views=[
        dict(type='text', h=70, fn=_txt),
        dict(type='string', var='word', pointers={'index': 'blue', 'start': 'pink'}, h=250,
             color=lambda S, i, v: ('green' if S.get('start') is not None and 'index' in S and S['start'] <= i < S['index'] else None)),
        dict(type='set', var='num_set', label='num_set（不同的整数，字符串形式）', fmt=lambda x: f"'{x}'", h=170),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('start', 'start', 'pink'), ('集合大小', 'len(num_set)', 'green')],
    captions={
        'num_set = set()': '哈希集合：去重，最后集合大小就是答案',
        5: '`start` 记录当前数字段的起点；`None` 表示现在不在数字段里',
        'for index, char': lambda S, B, ret: ('所有字符都看完了，退出循环' if B.get('index') == S.index else f"看 `word[{S.index}] = {S.char!r}`"),
        "if char >= '0'": lambda S, B, ret: (f"`{S.char!r}` 是数字 → 属于某个整数" if '0' <= S.char <= '9'
                                              else f"`{S.char!r}` 是字母 → 一个数字段可能在这里结束"),
        'if start is None': lambda S, B, ret: ('`start` 是 None：这是新数字段的第一位' if B.get('start') is None
                                                else '`start` 已有值：还在同一个数字段里，什么也不用做'),
        'start = index': '数字段起点 `start = {start}`',
        11: lambda S, B, ret: (f"刚才有数字段 `[{S.start}, {S.index})` → 现在结算它" if B.get('start') is not None
                                                      else '`start` 是 None：前面也是字母，没有数字段要结算'),
        'while start < index - 1': lambda S, B, ret: (
            f"去前导 0：`word[{S.start}] = '0'` 且不是最后一位 → ==跳过这个 0==" if S.start < S.index - 1 and S.word[S.start] == '0'
            else f"`word[{S.start}]` 不是前导 0（或只剩最后一位）→ 数字串确定为 `{S.word[S.start:S.index]!r}`"),
        'start += 1': '`start` → {start}（保留最后一位，避免 `0` 被删成空串）',
        14: lambda S, B, ret: (f"`{S.word[S.start:S.index]!r}` 集合里已经有了 → ==不增加==，仍是 `{len(S.num_set)}` 个" if S.word[S.start:S.index] in B['num_set']
                               else f"`{S.word[S.start:S.index]!r}` 是新的 → 加入集合，共 `{len(S.num_set)}` 个"),
        15: '这一段处理完（或本来就是字母）→ 重置 `start = None`',
        17: '循环结束后 `start` 不是 None：最后还有一段数字没结算 → 在这里结算',
        18: lambda S, B, ret: (
            f"结尾处同样去前导 0：`word[{S.start}] = '0'` → ==跳过=="  if S.start < len(S.word) - 1 and S.word[S.start] == '0'
            else f"`word[{S.start}]` 不是前导 0（或只剩最后一位）→ 数字串为 `{S.word[S.start:]!r}`"),
        'num_set.add(word[start:])': '==字符串以数字结尾，循环里没人结算它==：加入 `{word[start:]!r}`，共 `{len(num_set)}` 个',
        'return len(num_set)': '集合里有 `{num_set}` → 答案 `{ret}`',
    },
    cards=dict(
        one_liner='把每段数字去掉前导 0 后放进集合，数集合大小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`word` 由数字和小写字母组成，把所有字母当作分隔符，得到若干整数',
                 '返回其中==不同整数==的个数；`01` 与 `1` 是同一个整数',
                 '本视频：`"a1b01c2d30"` → `{1, 2, 30}` → `3`'],
        quote='这里的字符串长度可达1000，那么对于部分语言来说是不适合将字符串转为整数储存的，而使用字符串储存的话则需要注意处理前导0的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：碰到数字记下 `start`，碰到字母就结算这一段',
              '整数可能很长，不转成 int：直接用==字符串==，去掉前导 0 后放进集合',
              '结尾如果还在数字段里，循环里没机会结算，要在循环外补一次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '去前导 0 的条件是 `start < index - 1`：至少留一位，纯 `0` 不能被删光',
                 '易错：字符串以数字结尾时，必须在循环后再结算一次',
                 '原文为 Python 2 风格，本题代码无需改动（类继承 `object` 保留）'],
    ),
)
