CONFIG = dict(
    num=1957, title='删除字符使字符串变好', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='看结果数组末尾两个字符',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1358'],
    code='''
class Solution(object):
    def makeFancyString(self, s):

        res = []
        for char in s:
            if len(res) >= 2 and res[-1] == char and res[-2] == char:
                continue
            res.append(char)
        
        return ''.join(res)
''',
    call='Solution().makeFancyString("aaabaaaa")',
    expect='aabaa',
    views=[
        dict(type='string', var='s', h=240, pointers={},
             color=lambda S, i, v: None),
        dict(type='array', var='res', label='res（保留的字符）', h=200, index=False),
    ],
    watch=[('char', 'char', 'blue')],
    captions={
        'res = []': '`res` 存放保留下来的字符',
        'for char in s': lambda S, B, r: (f'取下一个字符 `{S.char}`' if 'char' in S else '遍历结束'),
        'if len(res) >= 2': lambda S, B, r: (f'`res` 末尾两个都是 `{S.char}`，再加就三连了 → 跳过' if len(S.res) >= 2 and S.res[-1] == S.char and S.res[-2] == S.char else (f'`res` 才 {len(S.res)} 个字符，不会三连' if len(S.res) < 2 else f'`res` 末尾两个是 `{S.res[-2]}{S.res[-1]}`，和 `{S.char}` 不全相同')),
        'continue': '不加入答案，直接看下一个字符',
        'res.append(char)': '加入答案：`res` = `{"".join(res)}`',
        "return ''.join": '把数组拼回字符串：=={ret!r}==',
    },
    cards=dict(
        one_liner='新字符和答案末尾两个都相同，就不要它',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['没有三个连续相同字符的字符串是好字符串',
                 '删除最少的字符使 `s` 变好，返回结果',
                 '示例：`"aaabaaaa"` → `"aabaa"`'],
        quote='直接一趟遍历，使用一个数组来储存留下来的字符。若当前字符与答案中的最后一个以及倒数第二个字符都相同，那么就不将该字符加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['边遍历边构造答案数组 `res`',
              '加入新字符前，看 `res[-1]` 和 `res[-2]` 是否都等于它',
              '都相等就跳过，否则加入，遍历完拼成字符串'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判断 `len(res) >= 2`，避免下标越界',
                 '被跳过的字符不影响 `res` 末尾，所以后面的同字符仍会被跳过',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '对比灵神：灵神用计数器，yiduobo 直接回看答案末尾'],
    ),
)
