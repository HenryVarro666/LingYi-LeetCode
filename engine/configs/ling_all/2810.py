CONFIG = dict(
    num=2810, title='故障键盘', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='双端队列 + 方向标记',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def finalString(self, s: str) -> str:
        q = deque()
        tail = True
        for c in s:
            if c == 'i':
                tail = not tail  # 修改添加方向
            elif tail:  # 加尾部
                q.append(c)
            else:  # 加头部
                q.appendleft(c)
        return ''.join(q if tail else reversed(q))
''',
    call="Solution().finalString('string')",
    expect='rtsng',
    views=[
        dict(type='string', var='s', h=130, label='输入 s'),
        dict(type='text', h=60, fn=lambda S: ('当前方向：==往尾部加==（屏幕正序）' if S.get('tail') else '当前方向：==往头部加==（屏幕其实是倒着的）') if 'tail' in S else ''),
        dict(type='array', var=lambda S: list(S['q']) if 'q' in S else None, label='双端队列 q（左 = 头，右 = 尾）', h=170, cell=70),
    ],
    watch=['c', ('tail', 'tail', 'blue')],
    captions={
        'q = deque()': '准备一个==双端队列==：两头都能 `O(1)` 加字符',
        'tail = True': '`tail = True`：现在往==尾部==加字符',
        'for c in s': '读入字符 `{c}`',
        "if c == 'i'": lambda S, B, r: ('遇到 `i`：要反转' if S.c == 'i' else f'`{S.c}` 不是 `i`，正常输入'),
        'tail = not tail': '不真的反转，只==切换添加方向==：`tail` 变成 `{tail}`',
        'elif tail': lambda S, B, r: ('方向是尾部 → 加到队尾' if S.tail else '方向是头部 → 加到队头'),
        'q.append(c)': '`{c}` 加到队尾：`{"".join(q)}`',
        'q.appendleft(c)': '`{c}` 加到队头：`{"".join(q)}`（等价于反转后再往尾部加）',
        'return': lambda S, B, r: ('最终方向是尾部，队列正序就是答案：`%s`' % r if S.tail else '最终方向是头部，队列要整体反过来输出：`%s`' % r),
    },
    cards=dict(
        one_liner='反转 = 切换往哪头加字符，不用真的翻字符串',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['键盘故障：每输入 `i` 就把已写的字符串==反转==，其他字符正常输入',
                 '返回最终屏幕上的字符串',
                 '示例：`s = "string"` → `"rtsng"`'],
        quote='把反转看成是往字符串的头部添加字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['反转后再往尾部加，等价于==不反转、往头部加==',
              '两个状态：往尾部加 / 往头部加，遇到 `i` 就切换',
              '最后若处于「往头部加」状态，整体 `reversed` 一次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：结尾要看 `tail`，为假时输出 `reversed(q)`',
                 '题目保证 `s[0] != "i"`，开头不会出现反转空串的问题',
                 '同类题：双端队列、单调队列（§4.3、§4.4）；也有不用双端队列的 Go / JS 写法'],
    ),
)
