CONFIG = dict(
    num=1576, title='替换所有的问号', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 贪心选 a/b/c',
    code='''
class Solution(object):
    def modifyString(self, s):

        res = []
        last = None
        n = len(s)
        for index, char in enumerate(s):
            if char == '?':
                if last != 'a' and (index + 1 >= n or s[index + 1] != 'a'):
                    res.append('a')
                    last = 'a'
                elif last != 'b' and (index + 1 >= n or s[index + 1] != 'b'):
                    res.append('b')
                    last = 'b'
                else:
                    res.append('c')
                    last = 'c'
            else:
                res.append(char)
                last = char
        
        return ''.join(res)
''',
    call="Solution().modifyString('?zs?a?b')",
    expect='azsbacb',
    setup='',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符；黄框 = 它的下一个字符）', pointers={'index': 'blue'}, cell=90, h=200,
             color=lambda S, i, v: ('yellow' if v == '?' and 'index' in S and i > S['index'] else None)),
        dict(type='array', var=lambda S: list(S['res']) if 'res' in S else None,
             label='res（绿 = 刚写入）', cell=90, h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='text', h=70, size=30,
             fn=lambda S: f"上一个字符 `last = {S['last']!r}`" if 'last' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('last', 'last', 'cyan')],
    captions={
        'res = []': '`res` 存放结果的每个字符',
        'last = None': '`last` 记录上一个位置的最终字符（含问号替换后的）；开头没有，用 `None`',
        'n = len': '`n = {n}`，后面判断下一个字符会不会越界要用',
        'for index, char': lambda S, B, r: (f'看第 `{S.index}` 个字符 `{S.char!r}`' if S.index != B.get('index', -1) else '每个字符都处理完了，for 结束'),
        "if char == '?'": lambda S, B, r: (f"`{S.char!r}` 是问号 → 要选一个和前后都不同的字母" if S.char == '?'
                                           else f"`{S.char!r}` 不是问号 → 原样保留"),
        "if last != 'a'": lambda S, B, r: (
            f"前一个是 `{S.last!r}`，后一个是 `{(S.s[S.index+1] if S.index+1 < S.n else '无')!r}`，都不是 `a`？"
            + ('是 → 用 ==a==' if (S.last != 'a' and (S.index + 1 >= S.n or S.s[S.index+1] != 'a')) else '不是 → 试 b')),
        "elif last != 'b'": lambda S, B, r: (
            f"前一个是 `{S.last!r}`，后一个是 `{(S.s[S.index+1] if S.index+1 < S.n else '无')!r}`，都不是 `b`？"
            + ('是 → 用 ==b==' if (S.last != 'b' and (S.index + 1 >= S.n or S.s[S.index+1] != 'b')) else '不是 → 只能用 c')),
        "res.append('a')": '写入 `a`',
        "res.append('b')": '写入 `b`',
        "res.append('c')": '前后一个是 a 一个是 b → 写入 ==c==（c 一定不冲突）',
        'last = ': '`last` 更新为 `{last!r}`，给下一个位置用',
        'res.append(char)': '非问号原样写入 `{char!r}`',
        'return': '拼成字符串 `{ret!r}`',
    },
    cards=dict(
        one_liner='三个字母里总有一个能躲开前后邻居',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含小写字母和 `?`，把每个 `?` 换成小写字母',
                 '要求结果里==没有连续相同的字符==；`s` 本身不含连续重复字母',
                 '示例：`"?zs"` → `"azs"`；本视频：`"?zs?a?b"`'],
        quote='题目并没有规定字符使用的次数，那么对于某个问号：若其前面和后面都不是a，那么就将其替换成a；若其前后中有a，但没有b，替换成b；有一个a和一个b，替换成c。',
        quote_src='—— yiduobo 题解原文',
        idea=['问号只有前、后两个邻居，最多挡住两个字母 → ==a、b、c 三选一必有解==',
              '从头一趟扫描，用 `last` 记住前一个位置的最终字符（可能是刚替换的）',
              '依次试 a、b，都不行就 c；末尾要先判断 `index + 1 >= n` 防越界'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '前一个字符必须用 `last`（替换后的），不能用原串 `s[index-1]`，否则连续问号会冲突',
                 '最后一个位置没有下一个字符，要先判 `index + 1 >= n`',
                 '代码与原文一致，无需修改'],
    ),
)
