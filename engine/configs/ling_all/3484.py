CONFIG = dict(
    num=3484, title='设计电子表格', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='哈希表 · cell 字符串直接当键',
    code='''
class Spreadsheet:
    def __init__(self, _):
        self.data = {}

    def setCell(self, cell: str, value: int) -> None:
        self.data[cell] = value

    def resetCell(self, cell: str) -> None:
        self.data.pop(cell, None)

    def getValue(self, formula: str) -> int:
        ans = 0
        for cell in formula[1:].split("+"):
            # 注：如果用 defaultdict(int)，访问 self.data[cell] 也会把 cell 插入哈希表，增加空间复杂度
            ans += self.data.get(cell, 0) if cell[0].isupper() else int(cell)
        return ans
''',
    call="""s = Spreadsheet(3)
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
        dict(type='map', var='self.data', label='data（cell → 值；没有的键就是 0）', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='text', h=70, fn=lambda S: (f"公式 `{S['formula']}` → 拆成 `{S['formula'][1:].split('+')}`" if 'formula' in S else '')),
        dict(type='text', h=70, fn=lambda S: (f"这一项 `{S['cell']}`：{'首字母大写 → 当单元格，查哈希表' if S['cell'][0].isupper() else '是数字，直接转 int'}" if 'cell' in S and isinstance(S.get('cell'), str) and 'formula' in S else '')),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['cell', 'value', 'formula', ('ans', 'ans', 'green')],
    captions={
        'self.data = {}': '用一个空字典存「被设置过的单元格」，没出现的格子默认就是 0',
        'self.data[cell] = value': '`setCell`：直接把 `{cell}` 整个字符串当键，不用解析行列 → `data[{cell!r}] = {value}`',
        'self.data.pop(cell': '`resetCell`：重置为 0 等于==删掉这个键==（取不到就是 0），还能省空间',
        'ans = 0': '`getValue` 开始：累加器 `ans = 0`',
        'for cell in formula': '去掉开头的 `=`，按 `+` 拆成两项：`{formula[1:].split("+")}`，逐项处理',
        'ans += self.data.get': lambda S, B, r: (
            f"`{S.cell}` 首字母是大写 → 是单元格：用 `get(cell, 0)` 查表，没设置过就是 0，取到 `{S.self.data.get(S.cell, 0)}`，`ans` = =={S.ans}=="
            if S.cell[0].isupper() else f"`{S.cell}` 首字符不是大写字母 → 是数字，`int` 转换后累加，`ans` = =={S.ans}=="),
        'return ans': '公式的值 = ==`{ans}`==',
    },
    cards=dict(
        one_liner='cell 字符串直接当哈希表的键，不用解析行列',
        complexity='初始化 `O(1)`，其余 `O(L)`（L 为字符串长度）',
        problem=['26 列（A~Z）、`rows` 行的电子表格，格子初始都是 0',
                 '`setCell` 设值，`resetCell` 置 0，`getValue("=X+Y")` 求和，X、Y 是单元格或数字',
                 '示例：`=5+7` → 12；设 A1=10 后 `=A1+6` → 16'],
        quote='创建一个哈希表，直接把整个 cell 字符串作为哈希表的键，无需解析行号列号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`setCell` 插入键值对，`resetCell` 删除键',
              '`getValue`：去掉 `=`，按 `+` 拆开，大写字母开头就查表，否则转 int',
              '表的大小只和 setCell 次数有关，和 rows 无关'],
        summary=['时间：初始化 `O(1)`，其余 `O(L)`；空间 `O(qL)`，q 为 setCell 次数',
                 '`rows` 根本用不上，所以 `__init__` 的参数写成 `_`',
                 '读取要用 `get(cell, 0)`：若用 `defaultdict(int)`，读取也会把键插进表里，浪费空间',
                 'resetCell 用 `pop(cell, None)`，键不存在也不会报错'],
    ),
)
