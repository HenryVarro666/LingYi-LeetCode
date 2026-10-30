CONFIG = dict(
    num=1876, title='长度为三且各字符不同的子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗（两个变量存前两个字符）',
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
        dict(type='string', var='s', label='s', cell=84, h=200),
        dict(type='text', size=40, h=140,
             fn=lambda S: f"窗口：`{S['first']}` `{S['second']}` `{S['now']}`" if 'now' in S else (f"窗口：`{S['first']}` `{S['second']}` ..." if 'second' in S else '')),
        dict(type='text', size=34, h=100,
             fn=lambda S: (f"三个字符{'互不相同' if len({S['first'], S['second'], S['now']}) == 3 else '有重复'}" if 'now' in S else '')),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'first = s[0]': '窗口第一个字符 `first = {first}`',
        'second = s[1]': '窗口第二个字符 `second = {second}`',
        'for now in s[2:]': '取下一个字符作第三个（取完就结束），`now` 当前为 `{now}`',
        'if first != second': lambda S, B, r: (f"`{S.first}` `{S.second}` `{S.now}` 两两不同 → ==好子串==" if len({S.first, S.second, S.now}) == 3
                                               else f"`{S.first}` `{S.second}` `{S.now}` 有相同字符 → 不是好子串"),
        'res += 1': '好子串 +1：`res` → =={res}==',
        'first, second = second, now': '窗口右移：原来的第二个成为新的第一个 `first = {first}`，当前字符成为新的第二个 `second = {second}`',
        'return res': '全部窗口看完，共 `{res}` 个好子串',
    },
    cards=dict(
        one_liner='用 first、second 记住前两个字符，now 是第三个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串里长度为 3 且三个字符互不相同的子串叫“好子串”，数出有几个（重复出现要重复计）',
                 '示例：`"aababcabc"` → `4`（abc、bca、cab、abc）'],
        quote='使用两个遍历分别保留窗口中的第一个字符和第二个字符。对于当前字符，若三个字符不相等，那么将答案加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['窗口只有 3 格，不用下标，用 `first`、`second` 两个变量存前两个字符',
              '三个字符两两比较，全不等才计数',
              '窗口右移：`second` 变新的 `first`，`now` 变新的 `second`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '长度不足 3 要先返回 0，否则 `s[1]` 会越界',
                 '三个字符要比较三对：first/second、first/now、second/now，缺一对就会漏判',
                 '长度固定为 3，所以也可以直接用 set 判重'],
    ),
)
