CONFIG = dict(
    num=3823, title='反转一个字符串里的字母后反转特殊字符', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='分类入栈 · 从尾部弹出',
    tags=['难度分 1250'],
    code='''
class Solution(object):
    def reverseByType(self, s):
        
        lower = []
        sp = []
        for c in s:
            if 'a' <= c <= 'z':
                lower.append(c)
            else:
                sp.append(c)

        res = []
        for c in s:
            if 'a' <= c <= 'z':
                res.append(lower[-1])
                lower.pop()
            else:
                res.append(sp[-1])
                sp.pop()
        
        return ''.join(res)
''',
    call='Solution().reverseByType(")ebc#da@f(")',
    expect='(fad@cb#e)',
    views=[
        dict(type='string', var='s', label='s', cell=76),
        dict(type='array', var=lambda S: list(S['lower']) if 'lower' in S else None, label='lower（小写字母，右端是下一个被弹出的）', cell=76),
        dict(type='array', var=lambda S: list(S['sp']) if 'sp' in S else None, label='sp（特殊字符，右端是下一个被弹出的）', cell=76),
        dict(type='array', var=lambda S: list(S['res']) if 'res' in S else None, label='res（答案）', cell=76),
    ],
    watch=[('c', 'c', 'blue'), ('len(lower)', 'len(lower)', 'green'), ('len(sp)', 'len(sp)', 'orange')],
    captions={
        'lower = []': '`lower` 收集所有小写字母',
        'sp = []': '`sp` 收集所有特殊字符',
        'for c in s': '遍历：`c = {c!r}`',
        "if 'a' <= c <= 'z'": lambda S, B, r: (f"`{S.c!r}` 是小写字母" if 'a' <= S.c <= 'z' else f"`{S.c!r}` 是特殊字符"),
        'lower.append': '`lower` 末尾加入 `{c!r}` → `{lower}`',
        'sp.append': '`sp` 末尾加入 `{c!r}` → `{sp}`',
        'res = []': '第二趟遍历：位置类型不变，内容取反过来的那一端',
        'res.append(lower[-1])': '这个位置是字母 → 取 `lower` 最后一个 `{lower[-1]!r}`（即反转后该放的）',
        'res.append(sp[-1])': '这个位置是特殊字符 → 取 `sp` 最后一个 `{sp[-1]!r}`',
        'lower.pop()': '用掉了就弹出，`lower` 剩 `{lower}`',
        'sp.pop()': '用掉了就弹出，`sp` 剩 `{sp}`',
        "return ''.join": lambda S, B, ret: f'拼接得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='两类字符互不相关：各自倒着取，填回原位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['先反转小写字母，再反转特殊字符，各自放回原位置',
                 '示例：`")ebc#da@f("`',
                 '→ `"(fad@cb#e)"`'],
        quote='反转小写字母与反转特殊字符是互不相关的，也就是说可以一起执行。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：把小写字母放进 `lower`，特殊字符放进 `sp`',
              '第二趟：位置是字母就从 `lower` 末尾取，是特殊字符就从 `sp` 末尾取',
              '取完就 `pop`，相当于倒着读'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：两类字符要分别维护，不能共用一个列表',
                 '对比灵神：灵神用相向双指针原地交换，这里用两个列表倒着取',
                 '原文就是 Python 3 可运行的写法，未做修改'],
    ),
)
