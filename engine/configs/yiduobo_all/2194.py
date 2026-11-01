
def _sheet(S):
    s = S['s']
    return [[chr(c) + str(r) for c in range(ord(s[0]), ord(s[3]) + 1)] for r in range(int(s[1]), int(s[4]) + 1)]


def _col(S, i, j, v):
    if 'res' not in S:
        return None
    if 'r' in S and 'c' in S and v == chr(S['c']) + str(S['r']):
        return 'yellow' if v in S['res'] else 'blue'
    return 'green' if v in S['res'] else None


CONFIG = dict(
    num=2194, title='Excel 表中某个范围内的单元格', difficulty='Easy', category='模拟',
    author='yiduobo', technique='先列后行遍历 + 拼接',
    tags=[],
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
    expect=['B2', 'B3', 'C2', 'C3', 'D2', 'D3'],
    views=[
        dict(type='text', fn=lambda S: (f"列 `c = '{chr(S['c'])}'`，行 `r = {S['r']}`" if 'r' in S and 'c' in S else f"范围 `{S['s']}`"), size=30),
        dict(type='grid', var=_sheet, label='表格（绿 = 已加入结果，蓝 = 正在加入）', cell=110, h=260,
             rows=lambda S: [str(r) for r in range(int(S['s'][1]), int(S['s'][4]) + 1)],
             cols=lambda S: [chr(c) for c in range(ord(S['s'][0]), ord(S['s'][3]) + 1)], color=_col),
        dict(type='array', var='res', label='res', cell=90, h=140),
    ],
    watch=[('c', 'chr(c) if "c" in S else None', 'blue'), ('r', 'r', 'pink'), ('c1,c2', '(c1, c2)'), ('r1,r2', '(r1, r2)')],
    captions={
        'c1 = ord': '起始列字母转成编码：`c1 = {c1}`（`"{s[0]}"`）',
        'c2 = ord': '结束列：`c2 = {c2}`（`"{s[3]}"`）',
        'r1 = int': '起始行：`r1 = {r1}`',
        'r2 = int': '结束行：`r2 = {r2}`',
        'res = []': '`res` 存结果，要按先列后行',
        'for c in range': lambda S, B, ret: (f"外层按列：`c = '{chr(S.c)}'`" if 'c' in S and S.c != B.get('c') else '所有列处理完了'),
        'for r in range': lambda S, B, ret: (f"内层按行：`r = {S.r}`" if S.get('r') != B.get('r') else '这一列的行走完了，换下一列'),
        'res.append': '列 + 行拼起来：`"{chr(c)}{r}"`，`res` 共 {len(res)} 个',
        'return res': '先列后行，结果天然有序：`{res}`',
    },
    cards=dict(
        one_liner='直接按先列后行遍历，把列字母和行号拼起来',
        complexity='时间 `O(列数 × 行数)`，空间 `O(1)`（不计答案）',
        problem=['单元格写成 `"<列字母><行号>"`，给定区间 `"c1r1:c2r2"`',
                 '按先列后行返回区间内所有单元格',
                 '本视频：`"B2:D3"` → `["B2","B3","C2","C3","D2","D3"]`'],
        quote='比较基础的题目，直接按先列后行的顺序进行遍历，将列和行拼起来填充到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先取出四个端点：列用 `ord` 转编码，行用 `int` 转数字', '外层 `c` 从起始列到结束列，内层 `r` 从起始行到结束行',
              '`chr(c) + str(r)` 拼出单元格'],
        summary=['时间 `O(列数 × 行数)`',
                 '`range` 右端点要 `+1`，否则丢掉最后一列/行',
                 '列要用 `chr` 转回字母，行要用 `str` 转成字符串才能拼接'],
    ),
)
