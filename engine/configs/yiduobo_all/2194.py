CONFIG = dict(
    num=2194, title='Excel 表中某个范围内的单元格', difficulty='Easy', category='模拟',
    author='yiduobo', technique='先列后行双重循环',
    code='''
class Solution(object):
    def cellsInRange(self, s):

        c1 = ord(s[0])
        c2 = ord(s[3])
        r1 = int(s[1])
        r2 = int(s[4])
        res = []
        for c in range(c1, c2 + 1):
            for r in range(r1, r2 + 1):        
                res.append(chr(c) + str(r))
        
        return res
''',
    call='Solution().cellsInRange("B2:D3")',
    expect=['B2','B3','C2','C3','D2','D3'],
    views=[
        dict(type='string', var='s', label='s', h=150),
        dict(type='grid', var="[[chr(c) + str(r) for c in range(ord(s[0]), ord(s[3]) + 1)] for r in range(int(s[1]), int(s[4]) + 1)]",
             h=260, label='范围内的单元格（绿 = 已加入 res，黄 = 当前）',
             color=lambda S, i, j, v: ('yellow' if 'c' in S and 'r' in S and v == chr(S['c']) + str(S['r']) else 'green' if v in S.get('res', []) else None)),
        dict(type='array', var='res', label='res', h=120, cell=70),
    ],
    watch=['c1', 'c2', 'r1', 'r2', 'c', 'r'],
    captions={
        'c1 = ord': '起始列 `{s[0]}` 的编码 `c1 = {c1}`',
        'c2 = ord': '结束列 `{s[3]}` 的编码 `c2 = {c2}`',
        'r1 = int': '起始行 `r1 = {r1}`',
        'r2 = int': '结束行 `r2 = {r2}`',
        'for c in range': '外层枚举列（字母编码相连，所以能 `range`）：`c = {c}`，即 `{chr(c)}`',
        'for r in range': '内层枚举行：`r = {r}`（先列后行，保证输出顺序）',
        'res.append': '拼出单元格 `chr({c}) + str({r}) = "{chr(c)}{r}"`，加入 `res`',
        'return res': '先列后行遍历完，共 `{len(res)}` 个单元格',
    },
    cards=dict(
        one_liner='字母可以转编码做循环，先列后行拼字符串',
        complexity='时间 `O(列数 × 行数)`，空间 `O(1)`（不计答案）',
        problem=['单元格写作 `"<列字母><行号>"`，给定范围 `"c1r1:c2r2"`',
                 '按先列后行的顺序，返回范围内所有单元格字符串',
                 '示例：`"K1:L2"` → `["K1","K2","L1","L2"]`；本视频用 `"B2:D3"`'],
        quote='比较基础的题目，直接按先列后行的顺序进行遍历，将列和行拼起来填充到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`ord` 把字母变成编码，列就能像数字一样 `range`',
              '外层列、内层行，正好满足「先按列、再按行」的排序要求',
              '`chr(c) + str(r)` 把编码和行号拼回字符串'],
        summary=['时间 `O(列数 × 行数)`，空间 `O(1)`（不计答案）',
                 '`range(c1, c2 + 1)` 要加一，两端都包含',
                 '外层必须是列，否则输出顺序错',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
