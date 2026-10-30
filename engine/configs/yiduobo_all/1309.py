CONFIG = dict(
    num=1309, title='解码字母到整数映射', difficulty='Easy', category='字符串',
    author='yiduobo', technique='从后往前扫描',
    tags=[],
    code='''
class Solution(object):
    def freqAlphabets(self, s):

        res = []
        p = len(s) - 1
        while p >= 0:
            if s[p] == '#':
                res.append(chr(int(s[p - 2]) * 10 + int(s[p - 1]) + 96))
                p -= 3
            else:
                res.append(chr(int(s[p]) + 96))
                p -= 1
        
        return ''.join(res[::-1])
''',
    call="Solution().freqAlphabets('10#11#12')",
    expect='jkab',
    views=[
        dict(type='string', var='s', pointers={'p': 'blue'}, label='s（p 从右往左走）', h=160),
        dict(type='array', var='res', label='res（倒着收集，最后再反转）', h=160),
    ],
    watch=[('p', 'p', 'blue'), ('res', "''.join(res)", 'green')],
    captions={
        'res = []': '`res` 先放空，从后往前解码出的字母依次加进来',
        'p = len(s) - 1': '从最后一位开始：`p = {p}`',
        'while p >= 0': lambda S, B, r: (f'`p = {S.p} >= 0`，还有字符没解码' if S.p >= 0 else '`p < 0`：整串都解码完了'),
        "if s[p] == '#'": lambda S, B, r: (f"`s[{S.p}] = '#'` → 前面两位合起来是一个 j~z 的数字" if S.s[S.p] == '#'
                                          else f"`s[{S.p}] = '{S.s[S.p]}'` 不是 `#` → 单个数字就是 a~i"),
        'res.append(chr(int(s[p - 2])': '两位数 `{s[p-2]}{s[p-1]}` → 字母 =={res[-1]}==，`p` 还要往前跳三位',
        'p -= 3': '`#` 和两位数一起处理完：`p` → {p}',
        'res.append(chr(int(s[p]) + 96))': '单个数字 `{s[p]}` → 字母 =={res[-1]}==',
        'p -= 1': '只用了一位：`p` → {p}',
        'return': '倒着收集的，反转后拼起来：`{ret}`',
    },
    cards=dict(
        one_liner='遇到 # 就看前两位：从后往前扫，歧义消失',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字 `1~9` 对应 `a~i`；`10#~26#` 对应 `j~z`',
                 '把只含数字和 `#` 的字符串 `s` 还原成字母串',
                 '示例：`10#11#12` → `jkab`'],
        quote='若当前字符为#，那么就将其与之前的两个字符组合起来解码，然后往前移动三位到上一个未解码字符，否则直接解码当前字符，然后向前移动一位。',
        quote_src='—— yiduobo 题解原文',
        idea=['`#` 总是出现在两位数的后面，所以从右往左读最不容易出错',
              '看到 `#`：取前两位当十位和个位，一次吃掉 3 个字符',
              '否则一位对应一个字母；最后把结果倒序'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '字母 = `chr(数字 + 96)`，`a` 是 97',
                 '易错：`#` 前面是两位数，下标别写成 `p-1` 和 `p-2` 搞反（十位在 `p-2`）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
