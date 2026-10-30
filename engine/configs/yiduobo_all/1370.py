CONFIG = dict(
    num=1370, title='上升下降字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='双栈交替',
    code='''
class Solution(object):
    def sortString(self, s):

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        f = []
        g = []
        for index in range(26, 0, -1):
            char = chr(index + 96)
            if char in char_dict:
                f.append([char, char_dict[char]])
            
        
        res = []
        flag = True
        while True:
            if flag:
                while f:
                    char, num = f[-1]
                    f.pop()
                    res.append(char)
                    if num > 1:
                        g.append([char, num - 1])
                
                if not g:
                    break
            else:
                while g:
                    char, num = g[-1]
                    g.pop()
                    res.append(char)
                    if num > 1:
                        f.append([char, num - 1])
            
                if not f:
                    break

            flag = not flag
            
        return ''.join(res)
''',
    call="Solution().sortString('aaaabbbcc')",
    expect='abccbaaba',
    skip=['for index in range', 'char = chr(index', 'if char in char_dict'],
    max_steps=100,
    views=[
        dict(type='map', var='char_dict', h=150),
        dict(type='stack', var='f', fmt=lambda x: f'{x[0]}×{x[1]}', label='f 正向栈（栈顶最小）', h=170),
        dict(type='stack', var='g', fmt=lambda x: f'{x[0]}×{x[1]}', label='g 反向栈（栈顶最大）', h=170),
        dict(type='text', fn=lambda S: '答案 res = ' + (''.join(S['res']) if 'res' in S else ''), size=34, h=70),
    ],
    watch=['flag', 'char', 'num', ('res', "''.join(res)", 'green')],
    captions={
        'char_dict[char] = ': '统计 `{char}` 出现次数：`{char_dict}`',
        'f.append([char, char_dict[char]])': '按 z 到 a 压栈：`{char}` 压入 f，==最小的字符最后压入，在栈顶==',
        'flag = True': '`flag = True`：先走正向（上升）',
        'while True': '一轮正向 + 一轮反向，直到两个栈都空',
        'if flag': lambda S, B, r: '`flag` 为真：弹 f，==从小到大==取字符' if S.flag else '`flag` 为假：弹 g，==从大到小==取字符',
        'char, num = f[-1]': '看 f 栈顶：字符 `{char}`，剩余 `{num}` 个',
        'f.pop()': '弹出 f 栈顶 `{char}`',
        'char, num = g[-1]': '看 g 栈顶：字符 `{char}`，剩余 `{num}` 个',
        'g.pop()': '弹出 g 栈顶 `{char}`',
        'res.append(char)': '取一个 `{char}` 加入答案：`{"".join(res)}`',
        'if num > 1': lambda S, B, r: (f'`num = {S.num} > 1`：还有剩余 → 放进另一个栈，留给反方向' if S.num > 1
                                       else f'`num = {S.num}`：这个字符用完了，不再放回'),
        'g.append': '`{char}` 还剩 `{num - 1}` 个，压入反向栈 g',
        'f.append([char, num - 1])': '`{char}` 还剩 `{num - 1}` 个，压入正向栈 f',
        'if not g': lambda S, B, r: '`g` 为空：没有字符可反向取了 → 结束' if not S.g else '`g` 非空：还要走反向一轮',
        'if not f': lambda S, B, r: '`f` 为空：没有字符可正向取了 → 结束' if not S.f else '`f` 非空：还要走正向一轮',
        'flag = not flag': '换方向：`flag = {flag}`',
        'return': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='两个栈接力：正向栈弹空，剩余的压进反向栈',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['反复做：先从小到大各取一个不同字符，再从大到小各取一个不同字符，直到取完',
                 '输出按这个顺序拼出的字符串',
                 '本视频：`aaaabbbcc` → `abccbaaba`'],
        quote='我在这里采用的做法是使用两个栈分别维护正向和反向的剩余字符数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计次数，按 z 到 a 压入 f，==f 栈顶就是最小字符==',
              '弹 f 取字符，次数减 1，还有剩余就压入反向栈 g',
              'f 弹空得到一轮上升；再弹 g 得到一轮下降，剩余压回 f，两栈都空结束'],
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '栈里存 `[字符, 次数]`，次数用完就不再压回',
                 '压栈顺序决定了栈顶：f 要从 z 压到 a，g 弹 f 时自然是大字符在顶',
                 '原文为 Python 2 风格，除删去类型文档字符串外无需改动'],
    ),
)
