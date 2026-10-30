def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'values 压扁存储；这里按 26 列折回二维显示（只画 A~F 列，黄框 = 刚算出的下标）', 22, T['muted'], bold=True)
    vals = S.get('self.values')
    if vals is None:
        return
    rows = len(vals) // 26
    cw, ch = 96, 64
    X0, Y0 = x0 + 90, y0 + 90
    cur = S.get('index')
    for j in range(6):
        cv.text((X0 + j * cw + cw / 2, Y0 - 12), chr(65 + j), 24, T['muted'], anchor='mb', bold=True)
    for r in range(rows):
        cv.text((X0 - 12, Y0 + r * ch + ch / 2), f'行{r + 1}', 22, T['muted'], anchor='rm', bold=True)
        for j in range(6):
            v = vals[r * 26 + j]
            hot = cur == r * 26 + j
            cv.rect((X0 + j * cw + 2, Y0 + r * ch + 2, X0 + (j + 1) * cw - 2, Y0 + (r + 1) * ch - 2),
                    fill=T['yellow'] if hot else ((40, 110, 70) if v else (36, 42, 52)), r=6)
            cv.text((X0 + j * cw + cw / 2, Y0 + r * ch + ch / 2), v, 28, T['bg'] if hot else T['text'], anchor='mm', bold=True)
            cv.text((X0 + (j + 1) * cw - 8, Y0 + r * ch + 6), r * 26 + j, 15, T['dim'], anchor='rt', mono=True)


CONFIG = dict(
    num=3484, title='设计电子表格', difficulty='Medium', category='设计',
    author='yiduobo', technique='直接模拟 · 压扁成一维数组',
    code='''
class Spreadsheet(object):

    def __init__(self, rows):

        self.values = [0] * (rows * 26)

    def getIndex(self, cell):
        row = int(cell[1:]) - 1
        return row * 26 + ord(cell[0]) - 65

    def setCell(self, cell, value):
        
        index = self.getIndex(cell)
        self.values[index] = value

    def resetCell(self, cell):
        
        self.setCell(cell, 0)

    def getValue(self, formula):
        
        exp_list = formula[1:].split('+')
        res = 0
        for exp in exp_list:
            if exp.isdigit():
                res += int(exp)
            else:
                res += self.values[self.getIndex(exp)]
        
        return res
''',
    call="""s = Spreadsheet(2)
out = [s.getValue("=5+7")]
s.setCell("A1", 10)
out.append(s.getValue("=A1+6"))
s.setCell("B2", 15)
out.append(s.getValue("=A1+B2"))
s.resetCell("A1")
out.append(s.getValue("=A1+B2"))
out""",
    expect=[12, 16, 25, 15],
    views=[
        dict(type='custom', draw=_draw, h=240),
        dict(type='text', h=70, fn=lambda S: (f"`{S['cell']}` → 行 `{int(S['cell'][1:]) - 1}`，列 `{ord(S['cell'][0]) - 65}` → 下标 `{int(S['cell'][1:]) - 1} × 26 + {ord(S['cell'][0]) - 65}` = =={(int(S['cell'][1:]) - 1) * 26 + ord(S['cell'][0]) - 65}==" if isinstance(S.get('cell'), str) and S['cell'][1:].isdigit() else '')),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['cell', 'value', 'index', 'formula', 'exp', ('res', 'res', 'green')],
    captions={
        'self.values = [0]': '二维表不用二维数组，==压扁成一维==：`rows × 26` 个 0（共 {len(self.values)} 格）',
        'row = int(cell[1:])': '数字部分是行号，从 1 开始，减 1 变成 0 起始：`row = {row}`',
        'return row * 26': '列字符 `ord(cell[0]) - 65`（`A`→0）；下标 = `row × 26 + col` = =={ret}==',
        'index = self.getIndex': '先把 `{cell}` 换算成一维下标：`{index}`',
        'self.values[index] = value': '`values[{index}] = {value}`，单元格写好了',
        'self.setCell(cell, 0)': '`resetCell` 直接复用 `setCell(cell, 0)`，不用重复写换算',
        'exp_list = ': '去掉 `=`，按 `+` 拆成两项：`{exp_list}`',
        'res = 0': '累加器 `res = 0`',
        'for exp in exp_list': '逐项检查 `exp`',
        'if exp.isdigit()': lambda S, B, r: (f'`{S.exp}` 全是数字 → 是常数' if S.exp.isdigit() else f'`{S.exp}` 不是数字 → 是单元格引用'),
        'res += int(exp)': '常数直接累加：`res` = =={res}==',
        'res += self.values[': '单元格引用：换算下标后取 `values` 对应位置，累加得 `res` = =={res}==',
        'return res': '公式的值 = ==`{res}`==',
    },
    cards=dict(
        one_liner='操作都很直观：直接模拟，二维表压扁成一维',
        complexity='初始化 `O(rows)`，其余 `O(L)`',
        problem=['26 列（A~Z）、`rows` 行的电子表格，格子初始都是 0',
                 '`setCell` 设值，`resetCell` 置 0，`getValue("=X+Y")` 求和',
                 '示例：设 A1=10、B2=15 后，`=A1+B2` → 25'],
        quote='在具体实现上，我没有使用二维数组，而是将其压扁成一个rows * 26的一维数组，然后通过row * 26 + col来计算在二维数组中位于(row, col)的元素在这个一维数组中的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`getIndex`：首字母 → 列，数字部分 → 行，换算成下标',
              '`resetCell` 就是 `setCell(cell, 0)`',
              '`getValue`：按 `+` 拆开，首字符是数字就累加数值，否则查表'],
        summary=['初始化 `O(rows)`，其余 `O(L)`；空间 `O(rows × 26)`',
                 '行号从 1 开始，别忘了减 1；列用 `ord(c) - 65`',
                 '原文为 Python 2 风格，代码无需改动（类继承 `object` 照旧）',
                 '对比灵神：灵神用哈希表，rows 完全用不上；yiduobo 用数组，按格子数开空间'],
    ),
)
