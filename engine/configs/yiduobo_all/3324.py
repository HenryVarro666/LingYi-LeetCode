T = 'bca'


def _screen(S):
    if 'now' not in S:
        return '先加一个 `a`，再把它一步步改成 target 里对应的字母'
    scr = ''.join(S['now'])
    return f'屏幕：`{scr}`　　目标：`{S["target"]}`'


CONFIG = dict(
    num=3324, title='出现在屏幕上的字符串序列', difficulty='Medium', category='字符串',
    author='yiduobo', technique='先加 a 再逐个修正',
    tags=[],
    code='''
class Solution(object):
    def stringSequence(self, target):
        
        res = []
        now = []
        while len(now) < len(target):
            now.append('a')
            res.append(''.join(now))

            while now[-1] != target[len(now) - 1]:
                now[-1] = chr(ord(now[-1]) + 1)
                res.append(''.join(now))
        
        return res
''',
    call=f'Solution().stringSequence({T!r})',
    expect=['a', 'b', 'ba', 'bb', 'bc', 'bca'],
    views=[
        dict(type='string', var='target', label='target（箭头 = 正在填的位置）', cell=96, h=170,
             pointers={'len(now) - 1': 'blue'}),
        dict(type='text', h=100, size=32, fn=_screen),
        dict(type='array', var='res', label='res（出现过的字符串）', cell=110, h=200),
    ],
    watch=[('now', "''.join(now)", 'yellow'), ('len(now)', 'len(now)', 'blue'), ('len(res)', 'len(res)', 'green')],
    captions={
        'res = []': '`res` 按顺序记录屏幕上出现的字符串',
        'now = []': '`now` 是屏幕上当前的字符列表',
        'while len(now) < len(target)': lambda S, B, r: (f'`len(now) = {len(S.now)} < {len(S.target)}`：还没填满，继续' if len(S.now) < len(S.target)
                                                         else f'`len(now) = {len(S.now)}` 填满了 → 结束'),
        "now.append('a')": '按键 1：只能追加 `a`，屏幕变成 `{"".join(now)}`',
        'res.append(\'\'.join(now))': '记下屏幕上的 `{"".join(now)}`',
        'while now[-1] != target': lambda S, B, r: (f'`{S.now[-1]}` 还不是目标 `{S.target[len(S.now) - 1]}` → 继续按键 2' if S.now[-1] != S.target[len(S.now) - 1]
                                                    else f'`{S.now[-1]}` 已经是目标字母，这一位定下来了'),
        'now[-1] = chr': '按键 2：最后一位改成下一个字母 `{now[-1]}`',
        'return res': '全部输入完毕，共 `{len(res)}` 个字符串',
    },
    cards=dict(
        one_liner='只有按键 2 能改字符，且只能改最后一个：先 a 后修正',
        complexity='时间 `O(26·n^2)`，空间 `O(n)`',
        problem=['键盘两个键：末尾追加 `a`、把最后一个字符变成下一个字母',
                 '按最少按键输入 `target`，返回屏幕上出现过的所有字符串',
                 '示例：`target = "abc"` → `a, aa, ab, aba, abb, abc`'],
        quote='输入序列必然是先一个1添加一个\'a\'，然后若干个2将最后这个\'a\'修正成target中对应的字符，重复这个过程直到填充完整个字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有第二种操作能修正字符，且只能修正最后一个',
              '所以每填一位：追加 `a`，再按键 2 直到等于 `target` 对应位',
              '外层 `while` 控制长度，内层 `while` 控制修正'],
        summary=['时间 `O(26·n^2)`（每次 `join` 是 `O(n)`），空间 `O(n)`',
                 '`target[len(now) - 1]` 是刚追加的那位对应的目标字母',
                 '每次追加和每次修改后都要记录一次，不能漏掉 `a` 本身',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神用 `for s[-1] in` 一行枚举，yiduobo 用内层 while 逐步 +1'],
    ),
)
