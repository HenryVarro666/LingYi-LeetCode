def _sheet(S):
    s = S['s']
    return [[chr(c) + chr(r) for c in range(ord(s[0]), ord(s[3]) + 1)] for r in range(ord(s[1]), ord(s[4]) + 1)]


def _col(S, i, j, v):
    if 'ans' not in S:
        return None
    if 'i' in S and 'j' in S and v == chr(S['i']) + chr(S['j']):
        return 'yellow' if v in S['ans'] else 'blue'
    return 'green' if v in S['ans'] else None


CONFIG = dict(
    num=2194, title='Excel 表中某个范围内的单元格', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='双重循环枚举列、行（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def cellsInRange(self, s: str) -> List[str]:
        ans = []
        for i in range(ord(s[0]), ord(s[3]) + 1):
            for j in range(ord(s[1]), ord(s[4]) + 1):
                ans.append(chr(i) + chr(j))
        return ans
''',
    call='Solution().cellsInRange("B2:D3")',
    expect=['B2', 'B3', 'C2', 'C3', 'D2', 'D3'],
    views=[
        dict(type='text', fn=lambda S: (f"列 `i = '{chr(S['i'])}'`，行 `j = '{chr(S['j'])}'`" if 'j' in S else
                                        (f"当前列 `i = '{chr(S['i'])}'`" if 'i' in S else f"范围 `{S['s']}`")), size=30),
        dict(type='grid', var=_sheet, label='表格（绿 = 已加入答案，蓝 = 正在加入）', cell=110, h=260,
             rows=lambda S: [chr(r) for r in range(ord(S['s'][1]), ord(S['s'][4]) + 1)],
             cols=lambda S: [chr(c) for c in range(ord(S['s'][0]), ord(S['s'][3]) + 1)], color=_col),
        dict(type='array', var='ans', label='ans', cell=90, h=140),
    ],
    watch=[('i', 'chr(i)', 'blue'), ('j', 'chr(j)', 'pink'), ('len(ans)', 'len(ans)', 'green')],
    captions={
        'ans = []': '`ans` 收集结果，顺序要先按列、再按行',
        'for i in range': lambda S, B, ret: (f"外层枚举列：`i = '{chr(S.i)}'`" if 'i' not in B or S.i != B.i else '所有列都枚举完了'),
        'for j in range': lambda S, B, ret: (f"内层枚举行：`j = '{chr(S.j)}'`" if 'j' in S and S.get('j') != B.get('j') else
                                              f"这一列的行都枚举完了，换下一列"),
        'ans.append': '拼出单元格 `"{chr(i)}{chr(j)}"` 加入答案，共 {len(ans)} 个',
        'return ans': '外层是列、内层是行，答案天然有序：`{ans}`',
    },
    cards=dict(
        one_liner='外层枚举列，内层枚举行，拼成单元格',
        complexity='时间 `O(列数 × 行数)`，空间 `O(1)`（不计答案）',
        problem=['单元格写成 `"<列字母><行号>"`，给定区间 `"c1r1:c2r2"`',
                 '按先列后行的顺序返回区间内所有单元格',
                 '示例：`"K1:L2"` → `["K1","K2","L1","L2"]`'],
        quote='for i := s[0]; i <= s[3]; i++ { for j := s[1]; j <= s[4]; j++ { ans = append(ans, string(i)+string(j)) } }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['Go 里字符串下标得到的是字节，字节可以直接做循环变量', 'Python 转写时用 `ord` 取编码、`chr` 还原字符',
              '列在外层、行在内层，正好满足“先列后行”'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（字节循环 → `ord/chr`；Go 里预分配容量的 `make` 去掉了容量参数）',
                 '时间 `O(列数 × 行数)`',
                 '易错：循环嵌套顺序反了会变成先行后列',
                 '行号只有一位（1~9），所以字符加一就是下一行'],
    ),
)
