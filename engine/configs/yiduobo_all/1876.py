CONFIG = dict(
    num=1876, title='长度为三且各字符不同的子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 · 保留前两个字符',
    tags=[],
    code='''
class Solution(object):
    def countGoodSubstrings(self, s):

        if len(s) < 3:
            return 0

        first = s[0]
        second = s[1]
        res = 0
        for now in s[2:]:
            if first != second and first != now and second != now:
                res += 1
            first, second = second, now
        
        return res
''',
    call='Solution().countGoodSubstrings("aababcabc")',
    expect=4,
    views=[
        dict(type='string', var='s', cell=80, h=200),
        dict(type='text', size=30, h=80, fn=lambda S: f"窗口 `{S['first']}` `{S['second']}` `{S['now']}`" if 'now' in S else ''),
    ],
    watch=['first', 'second', 'now', ('res', 'res', 'green')],
    captions={
        'if len(s) < 3': '长度不足 3，没有长度为 3 的子串',
        'first = s[0]': '窗口第一个字符 `first = {first}`',
        'second = s[1]': '窗口第二个字符 `second = {second}`',
        'res = 0': '`res` 统计好子串个数',
        'for now in s': '当前字符 `now = {now}`，窗口 `{first}{second}{now}`',
        'if first != second': lambda S, B, r: (f'`{S.first}` `{S.second}` `{S.now}` 两两不同 → ==好子串==' if len({S.first, S.second, S.now}) == 3
                                               else f'`{S.first}` `{S.second}` `{S.now}` 有重复 → 不算'),
        'res += 1': '`res` → {res}',
        'first, second = second, now': '窗口右移：原来的第二个变第一个，当前字符变第二个 → `{first}` `{second}`',
        'return res': '共 `{res}` 个',
    },
    cards=dict(
        one_liner='用 first、second 记住窗口前两个字符，每来一个新字符就判断一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['不含重复字符的字符串叫好字符串',
                 '求 `s` 中长度为 3 的好子串个数（重复出现要重复计）',
                 '示例：`"aababcabc"` → `4`'],
        quote='我在这里采用的是类似滑动窗口的做法，使用两个遍历分别保留窗口中的第一个字符和第二个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`first`、`second` 是窗口里已有的两个字符，`now` 是新加入的',
              '三个字符互不相等就 `res += 1`，然后窗口右移一格'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先处理 `len(s) < 3` 的情况，否则 `s[1]` 可能越界',
                 '右移用 `first, second = second, now`，同时赋值不会弄丢旧值',
                 '原文为 Python 2 风格，本题无需改动代码',
                 '对比灵神：灵神直接下标取 `s[i-2..i]`，yiduobo 用两个变量滚动'],
    ),
)
