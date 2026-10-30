def _rect(S):
    """当前被检查的更新矩形 (row1,col1,row2,col2) 或 None（仅在 getValue 扫描中）"""
    if 'index' in S and 'row1' in S and S.get('_line') in (13, 14):
        return S['row1'], S['col1'], S['row2'], S['col2']
    return None


def _cell_color(S, i, j, v):
    r = _rect(S)
    if r is None:
        return None
    inside = r[0] <= i <= r[2] and r[1] <= j <= r[3]
    return 'green' if inside else None


def _txt(S):
    his = S.get('self').update_his if 'self' in S and hasattr(S['self'], 'update_his') else []
    h = '  '.join(f'#{k+1}:[{a},{b},{c},{d}]→{e}' for k, (a, b, c, d, e) in enumerate(his)) or '（空）'
    return f'更新记录 update_his = {h}'


CONFIG = dict(
    num=1476, title='子矩形查询', difficulty='Medium', category='设计',
    author='yiduobo', technique='记录更新历史 · 倒序查找', tags=[],
    code='''
class SubrectangleQueries(object):

    def __init__(self, rectangle):
        self.origin = rectangle[:]
        self.update_his = []

    def updateSubrectangle(self, row1, col1, row2, col2, newValue):
        self.update_his.append([row1, col1, row2, col2, newValue])

    def getValue(self, row, col):
        for index in range(len(self.update_his) - 1, -1, -1):
            row1, col1, row2, col2, value = self.update_his[index]
            if row1 <= row <= row2 and col1 <= col <= col2:
                return value
        
        return self.origin[row][col]
''',
    call='''obj = SubrectangleQueries([[1,2,1],[4,3,4],[3,2,1],[1,1,1]])
out = []
out.append(obj.getValue(0, 2))
obj.updateSubrectangle(0, 0, 3, 2, 5)
out.append(obj.getValue(0, 2))
obj.updateSubrectangle(3, 0, 3, 2, 10)
out.append(obj.getValue(3, 1))
out.append(obj.getValue(0, 2))
out''',
    expect=[1, 5, 10, 5],
    views=[
        dict(type='grid', var='self.origin', label='origin（绿 = 当前检查的更新矩形）', cursors=[('row', 'col', 'yellow', '查询')],
             color=_cell_color, cell=84, h=330),
        dict(type='text', fn=_txt, h=90),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('row', 'row', 'yellow'), ('col', 'col', 'yellow'), 'index', 'value'],
    captions={
        'self.origin = rectangle[:]': '先把原矩阵复制一份存起来，==以后再也不改它==',
        'self.update_his = []': '`update_his` 记录所有更新操作，初始为空',
        'self.update_his.append': '更新不动矩阵，只把 `[{row1},{col1},{row2},{col2},{newValue}]` 记到历史里 → 共 {len(self.update_his)} 条',
        'for index in range': lambda S, B, r: (f'从最新的一条往前扫：`index = {S.index}`（越新的更新优先级越高）' if 'index' in S else '还没有任何更新记录 → 直接去原矩阵里取'),
        'row1, col1, row2, col2, value': '取出第 {index+1} 条更新：行 `{row1}..{row2}`，列 `{col1}..{col2}`，值 `{value}`',
        'if row1 <= row': lambda S, B, r: (f'`({S.row},{S.col})` 在这个矩形里 → 最近一次覆盖它的就是这条' if S.row1 <= S.row <= S.row2 and S.col1 <= S.col <= S.col2
                                           else f'`({S.row},{S.col})` 不在这个矩形里 → 看更早的一条'),
        'return value': '命中最新覆盖它的更新，答案就是 `{ret}`',
        'return self.origin': '没有任何更新覆盖它 → 答案是原值 `{ret}`',
    },
    cards=dict(
        one_liner='不真的改矩阵，只记更新；查询时从最新往前找',
        complexity='更新 `O(1)`，查询 `O(更新次数)`',
        problem=['设计 `SubrectangleQueries`：用矩阵初始化',
                 '`updateSubrectangle(r1,c1,r2,c2,v)`：把子矩形全部改成 `v`',
                 '`getValue(row,col)`：返回当前 `(row,col)` 的值'],
        quote='对于查询操作(x, y)而言，其对应的值应该是最近一次被矩形更新后的值。在这里没有必要针对更新操作修改具体的矩形，而是只需要使用一个list记录下来更新的记录。',
        quote_src='—— yiduobo 题解原文',
        idea=['更新只 `append` 一条记录，不遍历矩形',
              '查询时从列表末尾向前扫：第一个包含 `(x,y)` 的更新就是最新值',
              '都不包含，就取原矩阵里的初始值'],
        summary=['更新 `O(1)`，查询最坏 `O(k)`（k = 更新次数）',
                 '必须==从后往前==扫：后面的更新会覆盖前面的',
                 '`self.origin = rectangle[:]` 是浅拷贝，只读不改，够用',
                 '原文为 Python 2 风格的 `class X(object)`，在 Python 3 下无需修改'],
    ),
)
