IMG = [[5, 6, 7, 10], [8, 9, 10, 10], [11, 12, 13, 10]]


def _center(S):
    if 'x' in S and 'y' in S and 11 <= S['_line'] <= 25:
        return S['x'], S['y']
    if S['_line'] in (27, 28, 29) and 'i' in S and 'j' in S:
        return S['i'], S['j']
    return None


def _win(S, r, c, v):
    ct = _center(S)
    return 'blue' if ct and abs(r - ct[0]) <= 1 and abs(c - ct[1]) <= 1 else None


def _cnt_col(S, r, c, v):
    return 'green' if v > 0 else None


def _info(S):
    if 'cnt' not in S:
        return ''
    ln = S['_line']
    ct = _center(S)
    if ct and ln >= 11 and 'tot' in S:
        return f"区域中心 `({ct[0]},{ct[1]})`，数值和 `tot` = =={S['tot']}=="
    if ln >= 35 and 'res' in S:
        return f"res = `{S['res']}`"
    return ''


def _cap_down(S, B, r):
    v = B.image[B.x + B.i][B.y + B.j]
    if B.i >= 1:
        return f'`image[{B.x+B.i}][{B.y+B.j}]={v}` 在区域最后一行，没有区域内的下邻居，跳过'
    d = abs(v - B.image[B.x + B.i + 1][B.y + B.j])
    tail = ' → ==超过 threshold，不是区域，直接 return==' if d > B.threshold else ' → 不超过'
    return f'看 `{v}` 与下邻居 `{B.image[B.x+B.i+1][B.y+B.j]}`：差 `{d}`' + tail


def _cap_right(S, B, r):
    v = B.image[B.x + B.i][B.y + B.j]
    if B.j >= 1:
        return f'`image[{B.x+B.i}][{B.y+B.j}]={v}` 在区域最后一列，没有区域内的右邻居，跳过'
    d = abs(v - B.image[B.x + B.i][B.y + B.j + 1])
    tail = ' → ==超过 threshold，不是区域，直接 return==' if d > B.threshold else ' → 不超过'
    return f'看 `{v}` 与右邻居 `{B.image[B.x+B.i][B.y+B.j+1]}`：差 `{d}`' + tail


CONFIG = dict(
    num=3030, title='找出网格的区域平均强度', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举区域中心 + s/cnt 累加',
    tags=[],
    code='''
class Solution(object):
    def resultGrid(self, image, threshold):

        m = len(image)
        n = len(image[0])

        s = [[0] * n for _ in range(m)]
        cnt = [[0] * n for _ in range(m)]

        def update(x, y):
            tot = 0
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if i < 1 and abs(image[x + i][y + j] - image[x + i + 1][y + j]) > threshold:
                        return
                    if j < 1 and abs(image[x + i][y + j] - image[x + i][y + j + 1]) > threshold:
                        return
                    
                    tot += image[x + i][y + j]
            
            tot //= 9
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    s[x + i][y + j] += tot
                    cnt[x + i][y + j] += 1

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                update(i, j)
        
        res = []
        for i in range(m):
            res.append([])
            for j in range(n):
                if cnt[i][j] == 0:
                    res[-1].append(image[i][j])
                else:
                    res[-1].append(s[i][j] // cnt[i][j])
        
        return res
''',
    call=f'Solution().resultGrid({IMG}, 3)',
    expect=[[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9]],
    skip=[4, 5, 7, 8, 11, 12, 13, 19, 22, 23, 25, 28, 31, 32, 33, 34, 35, 27, 29],
    max_steps=130,
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='grid', var='image', label='image（蓝 = 当前 3×3 区域，黄框 = 正在看的格子）', cell=70, h=230, color=_win,
             cursors=[('x + i if 14 <= _line <= 24 else None', 'y + j', 'yellow')]),
        dict(type='grid', var='s', label='s（各区域平均强度之和）', cell=70, h=230,
             cursors=[('x + i if _line == 24 else (i if _line >= 35 else None)', 'y + j if _line == 24 else j', 'yellow')]),
        dict(type='grid', var='cnt', label='cnt（属于几个区域）', cell=70, h=230, color=_cnt_col),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'blue'), 'tot', 'threshold'],
    captions={
        'if i < 1 and': _cap_down,
        'if j < 1 and': _cap_right,
        'tot += image': '顺便累加数值：`tot = {tot}`',
        'tot //= 9': '9 个格子都合格：区域平均强度 `tot = 数值和 // 9` = =={tot}==',
        's[x + i][y + j] += tot': '`s[{x+i}][{y+j}]` 加上这个区域的平均强度 → `{s[x+i][y+j]}`，`cnt` 同时 +1',
        'update(i, j)': '以 `({i},{j})` 为中心检查 3×3 区域',
        'for i in range(1, m - 1)': '区域中心不能在边界上，所以行从 1 到 m-2：`i = {i}`',
        'res[-1].append(image[i][j])': '`cnt = 0`，不属于任何区域，保持原值 `{image[i][j]}`',
        'res[-1].append(s[i][j]': '`res({i},{j}) = s // cnt = {s[i][j]} // {cnt[i][j]}` = =={res[-1][-1]}==',
        'return res': '全部算完，返回 `res`',
    },
    cards=dict(
        one_liner='枚举区域中心，合法就把平均强度加进 s，cnt 记次数',
        complexity='时间 `O(9mn)`，空间 `O(mn)`',
        problem=['3×3 网格内所有相邻像素的差 ≤ `threshold`，才叫区域',
                 '像素结果 = 所属各区域平均强度的平均，向下取整；不在任何区域则不变',
                 '示例：`[[5,6,7,10],[8,9,10,10],[11,12,13,10]]`，`threshold = 3` → 全是 `9`'],
        quote='接下来枚举所有区域的中心位置，也就是原始image中除开边界的这一圈之外的其他所有单元格，接下来对于一个区域中心，按上下左右偏移量都为1来划分出其作为中心位置对应的3*3网格。',
        quote_src='—— yiduobo 题解原文',
        idea=['需要两个单元格粒度的数组：`s` 存平均强度之和，`cnt` 存所属区域数',
              '对每个中心，遍历区域上方两行、左侧两列，检查相邻差，同时累加数值和',
              '合法就用数值和除以 9 得到区域平均，更新区域内 9 个格子的 `s` 和 `cnt`'],
        summary=['时间 `O(9mn)`，空间 `O(mn)`',
                 '易错：区域平均先取整，再对所属区域做第二次平均',
                 '易错：只检查 `i < 1`、`j < 1` 的偏移，才不会越出 3×3 区域',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`tot //= 9` 与 `s // cnt`）'],
    ),
)
