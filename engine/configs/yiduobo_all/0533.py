PIC = [['B', 'W', 'B', 'W'],
       ['B', 'W', 'B', 'W'],
       ['W', 'B', 'W', 'B'],
       ['W', 'B', 'W', 'W']]
TARGET = 2


def _phase(S):
    ln = S['_line']
    return 1 if ln <= 14 else 2 if ln <= 22 else 3


def _color(S, i, j, v):
    if 'same' not in S:
        return None
    ph = _phase(S)
    if ph == 1 and 'k' in S:
        if i == S['i']:
            return 'blue'
        if i == S['j']:
            return 'pink'
    if ph == 3 and 'j' in S and j == S['j']:
        if v == 'B':
            return 'blue'
    return None


def _top(S):
    if 'res' in S:
        return f"第三步：逐列检查，数量对、行相同才加 `target`；`res = {S['res']}`"
    if 'col' in S:
        return '第二步：`row[i]` 是第 i 行黑像素数，`col[j]` 记录第 j 列哪些行是黑像素'
    return '第一步：枚举每两行，预处理 `same[i][j]`：第 i 行和第 j 行是否完全一样'


CONFIG = dict(
    num=533, title='孤独像素 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='预处理行是否相同 · 逐列检查',
    code='''
class Solution(object):
    def findBlackPixel(self, picture, target):

        m = len(picture)
        n = len(picture[0])

        same = [[True] * m for _ in range(m)]

        for i in range(m - 1):
            for j in range(i + 1, m):
                for k in range(n):
                    if picture[i][k] != picture[j][k]:
                        same[i][j] = same[j][i] = False
                        break

        row = [0] * m
        col = [[] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B':
                    row[i] += 1
                    col[j].append(i)
        
        res = 0
        for j in range(n):
            if len(col[j]) == target:
                first = col[j][0]
                if row[first] == target:
                    flag = True
                    for other in col[j][1:]:
                        if not same[first][other]:
                            flag = False
                            break
                    
                    if flag:
                        res += target
        
        return res
''',
    call=f'Solution().findBlackPixel({PIC}, {TARGET})',
    expect=4,
    skip=['m = len', 'n = len', 'for k in range', 'for i in range', 'for j in range', 'if picture[i][k]', "if picture[i][j] == 'B'", 'break'],
    max_steps=110,
    views=[
        dict(type='text', size=24, fn=_top, h=90),
        dict(type='grid', var='picture', label='picture（蓝/粉 = 正在比较的两行；第三步蓝 = 当前列的黑像素）', cell=84, h=300, color=_color),
        dict(type='grid', var='same', label='same[i][j]（两行是否相同）', cell=56, h=230),
        dict(type='array', var='row', label='row（每行黑像素数）', cell=70, h=140),
        dict(type='text', size=26, h=70, fn=lambda S: ('`col` = ' + ' ， '.join(f'列{j}:{c}' for j, c in enumerate(S['col']))) if 'col' in S else ''),
    ],
    watch=[('target', 'target'), ('j', 'j', 'blue'), ('first', 'first', 'orange'), ('flag', 'flag'), ('res', 'res', 'green')],
    captions={
        'same = [[True]': '`same[i][j]` 先全设为 `True`，随后把不同的两行改成 `False`',
        'same[i][j] = same[j][i] = False': '第 `{i}` 行和第 `{j}` 行在第 `{k}` 列不同 → `same` 记为 ==False==，不用再比后面的列',
        'row = [0] * m': '`row[i]`：第 i 行的黑像素数',
        'col = [[] for': '`col[j]`：第 j 列里==哪些行==是黑像素（方便后面判断行是否相同）',
        'row[i] += 1': '`picture[{i}][{j}]` 是黑像素：第 `{i}` 行黑像素数 `row[{i}]` → {row[i]}',
        'col[j].append(i)': '第 `{j}` 列的黑像素记下行号 `{i}`：`col[{j}] = {col[j]}`',
        'res = 0': '预处理完成，开始逐列检查，`target = {target}`',
        'for j in range(n)': lambda S, B, r: f'检查第 `{S.j}` 列：黑像素所在行 `{S.col[S.j]}`',
        'if len(col[j]) == target': lambda S, B, r: (f'`len(col[{S.j}]) = {len(S.col[S.j])}`，`target = {S.target}`' + (' → 数量刚好' if len(S.col[S.j]) == S.target else ' → 不相等，这列不可能有孤独像素')),
        'first = col[j][0]': '取这列第一个黑像素所在的行作基准行：`first = {first}`',
        'if row[first] == target': lambda S, B, r: (f'第 `{S.first}` 行黑像素数 `{S.row[S.first]}`，`target = {S.target}`' + (' → 行也刚好' if S.row[S.first] == S.target else ' → 不相等，行里黑像素太多或太少')),
        'flag = True': '先假设这列的黑像素行都与基准行相同',
        'for other in col[j][1:]': '取这列的另一个黑像素行 `other = {other}`',
        'if not same[first][other]': lambda S, B, r: (f'`same[{S.first}][{S.other}] = {S.same[S.first][S.other]}` → ' + ('这两行不同，这列没有孤独像素' if not S.same[S.first][S.other] else '两行完全一样，继续')),
        'flag = False': '行不一致，`flag = False`，不再检查',
        'if flag': lambda S, B, r: ('每一行都相同，这一列所有黑像素都是孤独像素' if S.flag else '`flag = False`，这一列不计入'),
        'res += target': '这一列的 `{target}` 个黑像素都是孤独像素 → `res = {res}`',
        'return res': '一共 `{res}` 个孤独像素',
    },
    cards=dict(
        one_liner='先预处理哪些行相同，再逐列检查是否满足 target 与行一致',
        complexity='时间 `O(m²n)`，空间 `O(m²+mn)`',
        problem=['`m × n` 的图片，`B` 黑 `W` 白，整数 `target`',
                 '黑色孤独像素 `(r, c)` 须满足：',
                 '行 `r` 和列 `c` 都恰有 `target` 个黑像素，',
                 '且==列 `c` 中所有黑像素所在的行完全一致==',
                 '本视频：4×4，`target = 2` → 答案 `4`'],
        quote='在这里就需要有方法可以高效地判断两行是否相同。……我在这里采用的是暴力法，这一步预处理的时间复杂度为O(n^3)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`same[i][j]`：两两枚举所有行，一趟比较得到两行是否相同',
              '`row[i]` 数每行黑像素；`col[j]` 记录每列哪些行是黑像素',
              '列里黑像素数 `== target`，第一行黑像素数 `== target`，其余行都与它相同 → 答案加 `target`'],
        summary=['时间 `O(m²n)`，空间 `O(m²+mn)`',
                 '行相同 + 行里黑像素数 `== target`，加上列里数量 `== target`，三个条件缺一不可',
                 '易错：按列累计答案，一列满足就加 `target`，不要逐格重复加',
                 '作者说用哈希判断行相同更好，原文采用暴力法',
                 '这是会员题，题面按 LeetCode 原题整理；原文代码已是 Python 3 写法，未改动'],
    ),
)
