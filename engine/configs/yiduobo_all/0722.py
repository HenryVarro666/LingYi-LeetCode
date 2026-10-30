CONFIG = dict(
    num=722, title='删除注释', difficulty='Medium', category='字符串',
    author='yiduobo', technique='逐字符扫描 + 块注释标志',
    tags=[],
    code='''
class Solution(object):
    def removeComments(self, source):

        part_flag = False
        res = []
        for line in source:
            p = 0
            if res == [] or (res[-1] != '' and not part_flag):
                res.append('')
            while p < len(line):
                if part_flag:
                    if line[p] == '*' and p + 1 < len(line) and line[p + 1] == '/':
                        p += 1
                        part_flag = False
                    p += 1

                elif line[p] == '/' and p + 1 < len(line):
                    if line[p + 1] == '/':
                        break
                    elif line[p + 1] == '*':
                        part_flag = True
                        p += 1
                    else:
                        res[-1] += line[p]
                    p += 1

                else:
                    res[-1] += line[p]
                    p += 1
        
        return res
''',
    call="Solution().removeComments(['a//b', 'c/*d', 'e*/f', 'g'])",
    expect=['a', 'cf', 'g'],
    views=[
        dict(type='text', fn=lambda S: ('' if 'part_flag' not in S else ('当前：==在块注释中==，字符都丢掉' if S['part_flag'] else '当前：正常代码，字符保留'))),
        dict(type='array', var='source', h=200, cell=150,
             color=lambda S, i, v: 'blue' if 'line' in S and v == S['line'] else None),
        dict(type='string', var='line', pointers={'p': 'blue'}, h=210),
        dict(type='array', var='res', h=170, cell=150, label='res'),
    ],
    watch=[('part_flag', 'part_flag', 'purple'), ('p', 'p', 'blue')],
    captions={
        4: '`part_flag` 记录当前是否处于块注释中',
        'for line in source': lambda S, B, r: ('所有行都处理完了 → 结束循环' if B.line == S.line else f'处理下一行：`{S.line!r}`'),
        'p = 0': '从这一行第 0 个字符开始',
        'res == []': lambda S, B, r: ('答案为空，或上一行结果非空且不在块注释里 → ==另起一行==（末尾加空串）' if B.res == [] or (B.res[-1] != '' and not B.part_flag) else '上一行结果为空或仍在块注释里 → ==不另起一行==，继续接在 `res[-1]` 后面'),
        'while p < len(line)': lambda S, B, r: (f'`p = {S.p}`，还有字符' if S.p < len(S.line) else '这一行扫完了'),
        'if part_flag': lambda S, B, r: ('`part_flag = True`：处于块注释中，字符丢掉' if S.part_flag else '`part_flag = False`：不在块注释中，往下判断'),
        "line[p] == '*' and": lambda S, B, r: (f"`line[{S.p}]` 与下一位是 `*/` → ==块注释结束==" if S.line[S.p] == '*' and S.p + 1 < len(S.line) and S.line[S.p + 1] == '/' else f"`{S.line[S.p]}` 在注释里，不是 `*/` → 丢掉"),
        14: '`part_flag = False`：块注释结束，`*/` 整体跳过',
        "elif line[p] == '/'": lambda S, B, r: (f"`line[{S.p}] = '/'` 且后面还有字符 → 看下一位是 `/` 还是 `*`" if S.line[S.p] == '/' and S.p + 1 < len(S.line) else f"`{S.line[S.p]}` 是普通字符 → 保留"),
        "if line[p + 1] == '/'": lambda S, B, r: ('`//` ==行注释==：直接跳过本行剩余部分' if S.line[S.p + 1] == '/' else '下一位不是 `/`，再看是不是 `*`'),
        "elif line[p + 1] == '*'": lambda S, B, r: ('`/*` ==块注释开始==：`part_flag = True`' if S.line[S.p + 1] == '*' else '只是单独的 `/` → 当普通字符保留'),
        21: '`part_flag = True`：此后字符都丢掉，直到 `*/`',
        'res[-1] += line[p]': '保留字符 `{line[p]}`：`res[-1]` = `{res[-1]!r}`',
        'p += 1': '`p` → {p}',
        'return res': '全部处理完，返回 `{res}`',
    },
    skip=[],
    max_steps=110,
    cards=dict(
        one_liner='用一个标志记住「在不在块注释里」，逐字符扫描',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['`source` 是按行拆分的 C++ 源码，删掉 `//` 行注释和 `/* */` 块注释',
                 '块注释可跨行，删后相邻的代码要拼成一行；结果中不能有空行',
                 '本视频：`["a//b","c/*d","e*/f","g"]` → `["a","cf","g"]`'],
        quote='需要一个变量 flag 表示当前是否处于块注释中，然后遍历数组中的每一行的每个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到 `//`：`break`，跳过本行剩下的字符',
              '遇到 `/*`：`part_flag = True`；遇到 `*/` 再关掉',
              '行首另起一行的条件：`res` 为空，或上一行非空且不在块注释中'],
        summary=['时间 `O(n)`（n 为总字符数），空间 `O(n)`',
                 '块注释跨行时不另起一行，所以 `cf` 才能拼在一起',
                 '`/*` 和 `*/` 都要多跳一位，避免 `/*/` 被当成完整块注释',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
