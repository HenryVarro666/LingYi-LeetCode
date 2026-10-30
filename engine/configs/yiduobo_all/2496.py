def _ci(S):
    s = S.get('s') or ''
    c = S.get('char')
    return s.index(c) if c in s else -1


CONFIG = dict(
    num=2496, title='数组中字符串的最大值', difficulty='Easy', category='字符串',
    author='yiduobo', technique='模拟 · 检测有无字母',
    tags=[],
    code='''
class Solution(object):
    def maximumValue(self, strs):

        res = 0
        for s in strs:
            flag = True
            for char in s:
                if 'a' <= char <= 'z':
                    flag = False
                    break
            
            if flag:
                v = int(s)
            else:
                v = len(s)
            
            res = max(res, v)

        return res
''',
    call='Solution().maximumValue(["a3","7","bob"])',
    expect=7,
    views=[
        dict(type='array', var='strs', label='strs（蓝 = 当前字符串）', cell=150, h=270,
             color=lambda S, k, v: 'blue' if S.get('s') == v and 'res' in S else None),
        dict(type='string', var='s', label='当前字符串 s（粉 = 当前检查的字符）', cell=90, h=230,
             color=lambda S, k, v: 'pink' if S.get('char') is not None and k == _ci(S) else None),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"当前值 `v = {S['v']}`　最大值 `res = {S['res']}`" if 'v' in S else (f"最大值 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=[('flag', 'flag', 'orange'), ('char', 'char', 'pink'), ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录目前最大的值，初始为 0（值不会是负数）',
        'for s in strs': lambda S, B, ret: (f'检查字符串 `{S.s}`' if S.get('s') is not None and S.get('s') != B.get('s') or 'flag' not in B else '遍历完所有字符串'),
        'flag = True': '`flag = True`：先假设 `{s}` 只含数字',
        'for char in s': lambda S, B, ret: (f"看字符 `'{S.char}'`" if 'char' not in B or B.get('s') != S.get('s') or B.get('char') != S.get('char') else f'`{S.s}` 的字符都看完了，没有字母，`flag` 保持 True'),
        "if 'a' <= char <= 'z'": lambda S, B, ret: (f"`'{S.char}'` 是小写字母 → 不是纯数字" if 'a' <= S.char <= 'z' else f"`'{S.char}'` 是数字，继续"),
        'flag = False': '发现字母，`flag = False`',
        'break': '已经确定含字母，不用再看后面的字符',
        'if flag': lambda S, B, ret: ('`flag` 为真：纯数字，用数值' if S.flag else '`flag` 为假：含字母，用长度'),
        'v = int(s)': '值 `v = int({s!r}) = {v}`',
        'v = len(s)': '值 `v = len({s!r}) = {v}`',
        'res = max(res, v)': '`res = max({B.res}, {v}) = {res}`',
        'return res': '最大的值是 =={res}==',
    },
    cards=dict(
        one_liner='逐个字符串检查有没有字母，决定取数值还是取长度',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['字符串的==值==：只含数字 → 十进制数值；否则 → 长度',
                 '返回 `strs` 中字符串的最大值',
                 '本视频：`["a3","7","bob"]` → 值依次为 2、7、3 → `7`'],
        quote='直接按照题目意思一趟遍历，检测当前遍历的字符串中是否出现了小写字符。如果出现了，那么就使用其长度来更新答案，否则使用其数值来更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目说只含小写字母和数字，所以有没有字母就是有没有 `a`~`z`',
              '`flag` 先设为 True；遇到字母设 False 并 `break`',
              '`flag` 为真取 `int(s)`，否则取 `len(s)`，再更新 `res`'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`res` 初始为 0 即可：所有值都 ≥ 0',
                 '`break` 让含字母的字符串不必扫完',
                 '原文本身就是 Python 3 可运行的写法，未做修改',
                 '对比灵神：一行 `isdigit()` + `max`；这里手写字符检查'],
    ),
)
