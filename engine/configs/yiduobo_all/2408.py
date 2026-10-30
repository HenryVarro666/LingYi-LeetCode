def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tabs = S.get('self.tables') or {}
    cv.text((x0 + 18, y0 + 4), 'self.tables：表名 → Table（rows 按插入顺序存；被删的行只记进 removed，不真删）', 22, T['muted'], bold=True)
    sel_name, sel_r, sel_c = S.get('name'), S.get('rowId'), S.get('columnId')
    line = S.get('_line')
    y = y0 + 56
    for tn, t in tabs.items():
        rows, rem = getattr(t, 'rows', []), getattr(t, 'removed', set())
        active = tn == sel_name
        cv.text((x0 + 24, y + 4), f'"{tn}"', 28, T['blue'] if active else T['text'], bold=True, mono=True)
        cv.text((x0 + 24, y + 40), f'removed = {sorted(rem)}', 22, T['red'] if rem else T['dim'], mono=True)
        ncol = max([len(r) for r in rows] + [1])
        cw = min(150, (x1 - x0 - 330) / ncol)
        rh = 44
        sx = x0 + 250
        if not rows:
            cv.text((sx, y + 18), '（空表，rows = []）', 22, T['dim'])
            y += 100
            continue
        for ri, row in enumerate(rows):
            rid = ri + 1
            dead = rid in rem
            Y = y + ri * (rh + 8)
            cv.text((sx - 12, Y + rh / 2), f'行{rid}', 22, T['red'] if dead else T['muted'], anchor='rm', mono=True)
            for ci, v in enumerate(row):
                X = sx + ci * cw
                hot = active and rid == sel_r and ci + 1 == sel_c and 'rowId' in S and line is not None and line >= 33
                fill = (60, 40, 46) if dead else T['panel2']
                if hot:
                    fill = T['yellow']
                cv.rect((X + 2, Y, X + cw - 2, Y + rh), fill=fill, r=8, outline=T['border'])
                cv.text((X + cw / 2, Y + rh / 2), str(v), 22, T['bg'] if hot else (T['dim'] if dead else T['text']), anchor='mm', bold=hot)
            if dead:
                cv.line([(sx + 4, Y + rh / 2), (sx + len(row) * cw - 4, Y + rh / 2)], T['red'], 3)
        y += len(rows) * (rh + 8) + 56


CONFIG = dict(
    num=2408, title='设计SQL', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表 + 列表 + 集合（惰性删除）',
    tags=[],
    code='''
class Table(object):

    def __init__(self):
        self.rows = []
        self.removed = set()

class SQL(object):

    def __init__(self, names, columns):
        self.tables = {}
        for name in names:
            self.tables[name] = Table()

    def insertRow(self, name, row):
        t = self.tables[name]
        t.rows.append(row)

    def deleteRow(self, name, rowId):
        t = self.tables[name]
        t.removed.add(rowId)

    def selectCell(self, name, rowId, columnId):
        if name not in self.tables:
            return ""
            
        t = self.tables[name]
        if rowId in t.removed or rowId > len(t.rows):
            return ""

        if columnId > len(t.rows[rowId - 1]):
            return ""
        
        return t.rows[rowId - 1][columnId - 1]
''',
    call='''sql = SQL(["one", "two"], [2, 3])
sql.insertRow("two", ["first", "second", "third"])
sql.insertRow("two", ["fourth", "fifth", "sixth"])
out = [sql.selectCell("two", 1, 3)]
sql.deleteRow("two", 1)
out.append(sql.selectCell("two", 1, 2))
out.append(sql.selectCell("two", 2, 2))
out''',
    expect=['third', '', 'fifth'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('name', 'name', 'blue'), ('rowId', 'rowId', 'pink'), ('columnId', 'columnId', 'orange')],
    skip=['self.rows = []', 'self.removed = set()'],
    captions={
        'self.tables = {}': '哈希表 `tables`：表名 → 表，`O(1)` 通过表名找到表',
        'self.tables[name] = Table()': '为 `{name!r}` 建一张空表：`rows` 列表存行，`removed` 集合记被删的行号',
        't = self.tables[name]': lambda S, B, ret: f'先通过表名 `{S.name!r}` 找到对应的表',
        't.rows.append(row)': '只在==末尾==插入，所以用 list：这一行的行号 = `len(rows)` = `{len(t.rows)}`',
        't.removed.add(rowId)': '删除后==后面的行号不会前移==，所以不真删：只把 `{rowId}` 记进 `removed`',
        'if name not in self.tables': lambda S, B, ret: ('表不存在 → 返回空串' if S.name not in S['self.tables'] else f'表 `{S.name!r}` 存在'),
        'if rowId in t.removed': lambda S, B, ret: (
            f'行 `{S.rowId}` 已被删除 → 返回 `""`' if S.rowId in S.t.removed
            else (f'行号 `{S.rowId}` 超过行数 `{len(S.t.rows)}` → 返回 `""`' if S.rowId > len(S.t.rows)
                  else f'行 `{S.rowId}` 没被删、也没越界，继续检查列')),
        'if columnId > len': lambda S, B, ret: (
            f'列号 `{S.columnId}` 超过这行的列数 → 返回 `""`' if S.columnId > len(S.t.rows[S.rowId - 1])
            else f'列号 `{S.columnId}` 没越界'),
        'return t.rows[rowId - 1]': '行号、列号从 1 开始，所以下标要减一：`rows[{rowId} - 1][{columnId} - 1]` = =={ret!r}==',
        'return ""': '返回空字符串：这个单元格不存在',
    },
    cards=dict(
        one_liner='表名找表，列表存行，集合记录被删的行号',
        complexity='插入、删除、查询均为 `O(1)`',
        problem=['实现 `SQL(names, columns)`：`insertRow`、`deleteRow`、`selectCell`',
                 '行号从 1 自增，==删除后后面的行号不变==；单元格不存在时 `selectCell` 返回 `""`',
                 '本视频：建表 `two`，插两行，查 (1,3)，删第 1 行，再查 (1,2)、(2,2)'],
        quote='题目中的删除操作执行后，后续行的行数并不会向前移动，因此在这里可以不执行真正的删除，而是记录下哪些行被删去就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['表名 → 表：用哈希表 `tables`',
              '只在末尾插入：每张表用 `list` 存行，行号就是下标 + 1',
              '删除：用 `set` 记下被删的行号，查询时先看行号在不在里面'],
        summary=['插入、删除、查询都是 `O(1)`',
                 '易错：行号、列号从 1 开始，访问列表要减一',
                 '查询要依次判断：表是否存在、行是否被删或越界、列是否越界',
                 '题目保证 `columns` 与每行的列数一致，所以这份代码没有用到 `columns` 参数'],
    ),
)
