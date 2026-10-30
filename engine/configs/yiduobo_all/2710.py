CONFIG = dict(
    num=2710, title='移除字符串中的尾随零', difficulty='Easy', category='字符串',
    author='yiduobo', technique='从后向前找非零位', tags=[],
    code='''
class Solution(object):
    def removeTrailingZeros(self, num):

        p = len(num) - 1
        while num[p] == '0':
            p -= 1
        
        return num[:p + 1]
''',
    call="Solution().removeTrailingZeros('51230100')",
    expect='512301',
    views=[
        dict(type='string', var='num', pointers={'p': 'blue'}, h=200,
             color=lambda S, i, v: ('red' if i > S['p'] else 'green') if 'p' in S else None),
        dict(type='text', h=120, fn=lambda S: f"`p = {S['p']}`，`num[p] = {S['num'][S['p']]}`" if 'p' in S else ''),
    ],
    watch=[('p', 'p', 'blue')],
    captions={
        'p = len': '从最后一位开始：`p = len(num) - 1 = {p}`',
        'while num': '`num[{p}] = {num[p]}` 是 `0` 吗？{"是，还要往前" if num[p] == "0" else "不是，找到最后一个非零位，停下"}',
        'p -= 1': '这一位是尾随零，`p` 前移到 {p}',
        'return': '保留 `num[:p + 1]`，即到下标 `{p}` 为止 → =={ret}==',
    },
    cards=dict(
        one_liner='从末尾向前找到最后一个非零位，后面的全截掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你一个表示正整数的字符串 `num`，返回去掉尾随零后的字符串',
                 '例如 `"51230100"` → `"512301"`', '示例 2：`"123"` 没有尾随零，原样返回'],
        quote='由于题目保证num是正数，那么数字中必然存在一个非零的数位。只需从最后一位开始，向前找到位置最后的那个非零位，然后将这个非零位后面的部分截取掉就行了。',
        quote_src='—— yiduobo 题解',
        idea=['指针 `p` 从最后一位出发，遇到 `0` 就前移',
              '`p` 停下的位置就是最后一个非零位',
              '切片 `num[:p + 1]` 保留它和它前面的所有位'],
        after=[dict(heading='为什么 while 不会越界', lines=['题目保证 `num` 是正整数', '所以至少有一位非 0，`p` 最远退到它就停', '不需要再写 `p >= 0` 的判断', '这是 yiduobo 把 `rstrip` 展开成的手写版本'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==因为保证正整数，`while` 一定会停下，不会越界==',
                 '切片右端要写 `p + 1`，因为右端不包含'],
    ),
)
