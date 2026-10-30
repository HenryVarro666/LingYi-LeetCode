CONFIG = dict(
    num=3612, title='用特殊操作处理字符串 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='暴力模拟',
    tags=[],
    code='''
class Solution(object):
    def processStr(self, s):
        
        res = []
        for c in s:
            if c == '*':
                if res:
                    res.pop()
            elif c == '#':
                res.extend(res)
            elif c == '%':
                res.reverse()
            else:
                res.append(c)
        
        return ''.join(res)
''',
    call='Solution().processStr("ab#%*c")',
    expect="babc",
    views=[
        dict(type='string', var='s', label='s', cell=84, h=200),
        dict(type='array', var='res', label='res（当前字符串）', cell=84, h=260),
        dict(type='text', fn=lambda S: ("当前字符串 = \"" + ''.join(S['res']) + "\"，长度 " + str(len(S['res']))) if 'res' in S else '', size=28),
    ],
    watch=['c', ('res', "''.join(res)", 'green')],
    captions={
        'res = []': '用一个数组记录当前字符串',
        'for c in s': "读到字符 `c = '{c}'`",
        "c == '*'": lambda S, B, ret: "是 `*`：要删掉最后一个字符" if S.c == '*' else f"`'{S.c}'` 不是 `*`",
        'if res': lambda S, B, ret: ('`res` 非空，可以删' if S.res else '`res` 已空 → ==不存在最后一个字符==，什么也不做'),
        'res.pop()': '删掉最后一个字符 → `{res}`',
        "c == '#'": lambda S, B, ret: "是 `#`：复制当前 res 追加到后面" if S.c == '#' else "不是 `#`",
        'res.extend(res)': '把 res 自己追加到自己后面，长度翻倍 → `{res}`',
        "c == '%'": lambda S, B, ret: "是 `%`：反转当前 res" if S.c == '%' else "不是 `%`，只剩小写字母",
        'res.reverse()': '反转 → `{res}`',
        'res.append(c)': "小写字母直接加入末尾：`{res}`",
        'return': '处理完毕，拼成字符串 `{ret!r}`',
    },
    cards=dict(
        one_liner='长度只有 20，复制最多 2^19，放心暴力模拟',
        complexity='时间 `O(2^n)`，空间 `O(2^n)`',
        problem=['字符串 `s` 由小写字母和 `*`、`#`、`%` 组成，从左到右构造 `result`',
                 '字母加入；`*` 删最后一个（若存在）；`#` 复制追加；`%` 反转',
                 '示例：`"a#b%*"` → `"ba"`'],
        quote='由于s的长度不超过20，而只有复制操作才会快速让result的规模变大，那么在极限情况下，最终字符串的长度也不会超过2^19，因此完全可以暴力模拟。',
        quote_src='—— yiduobo 题解',
        idea=['先估计规模：只有 `#` 会让长度翻倍，所以最终长度不超过 `2^19`',
              '规模可控 → 用数组记录当前字符串，逐个字符执行对应操作'],
        summary=['时间 `O(2^n)`，空间 `O(2^n)`',
                 '易错：`*` 遇到空数组要先判断，否则 `pop` 报错',
                 '`extend(res)` 自己扩展自己，Python 会先取原长度，不会死循环',
                 '先估计结果规模，再决定能不能暴力'],
    ),
)
