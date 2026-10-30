def _tot(S):
    if 'op' not in S:
        return '`res` 从 0 开始，逐个操作看中间字符'
    op = S['op']
    return f'当前操作 `{op}`，中间字符 `{op[1]}` → ' + ('==减 1==' if op[1] == '-' else '==加 1==') + f'，`res` = =={S["res"]}=='


CONFIG = dict(
    num=2011, title='执行操作后的变量值', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 判断中间字符',
    tags=[],
    code='''
class Solution(object):
    def finalValueAfterOperations(self, operations):

        res = 0
        for op in operations:
            if op[1] == '-':
                res -= 1
            else:
                res += 1
        
        return res
''',
    call="Solution().finalValueAfterOperations(['--X', 'X++', 'X++', '++X', 'X--'])",
    expect=1,
    views=[
        dict(type='array', var='operations', h=220, label='operations'),
        dict(type='text', fn=_tot, size=30, h=160),
    ],
    watch=['op', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录 `X` 的当前值，初始为 0',
        'for op': '`for` 轮到下一个操作，`op` = `{op}`（取完最后一个就退出循环）',
        "if op[1] == '-'": '看正中间 `op[1] = {op[1]!r}`：前缀、后缀写法的中间字符都一样',
        'res -= 1': '中间是减号 → `res` 减 1，变成 `{res}`',
        'res += 1': '中间是加号 → `res` 加 1，变成 `{res}`',
        'return res': '全部操作执行完，`X` 的最终值是 ==`{res}`==',
    },
    cards=dict(
        one_liner='前缀后缀都一样：正中间那个字符说了算',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['语言只有一个变量 `X`，初始为 0',
                 '操作：`++X`、`X++` 加 1；`--X`、`X--` 减 1',
                 '示例：`["--X","X++","X++"]` → `1`'],
        quote='无论是前缀运算符还是后缀运算符，总是能够根据字符串正中间的这个字符判断出当前执行的是加操作还是减操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作串长度固定为 3，`op[1]` 就是正中间',
              '一趟遍历，按中间字符更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 风格，除类名写法外无需修改',
                 '对比灵神：灵神用一行 `sum` 生成式，yiduobo 用显式 if/else 累加'],
    ),
)
