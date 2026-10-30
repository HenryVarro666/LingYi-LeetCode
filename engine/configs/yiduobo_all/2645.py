CONFIG = dict(
    num=2645, title='构造有效字符串的最少插入数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按当前字母 a / b / c 分类讨论',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def addMinimum(self, word):
        p = 0
        res = 0
        while p < len(word):
            if word[p] == 'a':
                if p + 1 == len(word) or word[p + 1] == 'a':
                    res += 2
                    p += 1
                elif word[p + 1] == 'b':
                    if p + 2 == len(word) or word[p + 2] != 'c':
                        res += 1
                        p += 2
                    else:
                        p += 3
                elif word[p + 1] == 'c':
                    p += 2
                    res += 1
            
            elif word[p] == 'b':
                if p + 1 == len(word) or word[p + 1] != 'c':
                    res += 2
                    p += 1
                else:
                    res += 1
                    p += 2
            
            elif word[p] == 'c':
                res += 2
                p += 1
        
        return res
''',
    call='Solution().addMinimum("aacb")',
    expect=5,
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前位置 p）', cell=110, h=200, pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if i < S.get('p', 0) else None),
        dict(type='text', fn=lambda S: f'已经处理到 `p = {S.get("p", 0)}`，累计插入 `res = {S.get("res", 0)}`', size=28, h=60),
        dict(type='text', fn=lambda S: '`a` 要补 `bc`，`b` 要补 `a` 和 `c`，`c` 要补 `ab`；看下一个字母能省几个', size=24, h=60),
    ],
    watch=[('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = 0': '`p` 指向当前要处理的字母',
        'res = 0': '`res` 累计需要插入的字母数',
        'while p < len(word)': lambda S, B, r: (f'`p = {S.p} < {len(S.word)}`，继续处理' if S.p < len(S.word)
                                                else f'`p = {S.p}` 已到末尾，全部处理完'),
        "if word[p] == 'a'": lambda S, B, r: (f"`word[{S.p}] = '{S.word[S.p]}'`" + ('：是 `a`，要看后面是不是 `bc`' if S.word[S.p] == 'a' else '：不是 `a`')),
        "if p + 1 == len(word) or word[p + 1] == 'a'": lambda S, B, r: ('这个 a 后面没有字母或还是 a → ==必须补 bc==' if (S.p + 1 == len(S.word) or S.word[S.p + 1] == 'a')
                                                                  else f"下一个是 `'{S.word[S.p + 1]}'`，不是 a / 末尾"),
        "elif word[p + 1] == 'b'": lambda S, B, r: ("下一个是 `b`：看再下一个是不是 `c`" if S.word[S.p + 1] == 'b' else "下一个不是 `b`"),
        "word[p + 2] != 'c'": '`a b` 后面不是 `c` → 补一个 `c`；否则 `abc` 已完整',
        "elif word[p + 1] == 'c'": '`a c` 之间缺一个 `b`',
        "elif word[p] == 'b'": "当前不是 `a`，看是不是 `b`",
        "if p + 1 == len(word) or word[p + 1] != 'c'": 'b 前面必须补 `a`；右边不是 `c` → 还要补一个 `c`，共 2 个',
        "elif word[p] == 'c'": '当前是 `c`：只能在左边补 `ab`',
        'res += 2': '补 2 个：`res = {res}`',
        'res += 1': '补 1 个：`res = {res}`',
        'p += 1': '只用掉 1 个字母：`p` → {p}',
        'p += 2': '用掉 2 个字母：`p` → {p}',
        'p += 3': '`abc` 完整，用掉 3 个字母：`p` → {p}',
        'return res': '一共插入 =={res}== 个字母',
    },
    cards=dict(
        one_liner='字母只有三种，逐个分类讨论',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `word` 里任意位置插入 `a`、`b`、`c`',
                 '使它变成 `"abc"` 重复若干次，求最少插入数',
                 '示例：`"b"` → `2`；`"aaa"` → `6`'],
        quote='由于题目中只有三种字符，因此完全可以将所有情况都列举出来，分情况进行讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['`word[p]` 是 `a`：看后面两个字母，凑得出 `abc`、`ab`、`ac` 还是单独的 `a`',
              '`word[p]` 是 `b`：左边必须补 `a`；右边是 `c` 就补 1 个，否则补 2 个',
              '`word[p]` 是 `c`：只能在左边补 `ab`，补 2 个'],
        result='`"aacb"`：`a` 单独补 2；`ac` 补 1；`b` 补 2 → 共 5',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：访问 `word[p + 1]`、`word[p + 2]` 前先判断是否到末尾',
                 '每次按用掉的字母数移动 `p`：1、2 或 3',
                 '代码原样照搬（只删去了开头的类型说明），Python 3 直接可运行',
                 '对比灵神：灵神看相邻字母差 mod 3，yiduobo 对 a / b / c 全部枚举'],
    ),
)
