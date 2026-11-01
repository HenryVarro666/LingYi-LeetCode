CODE = r"""
class Solution(object):
    def composeCube(self, shapes):

        '''
                       ___________9____________
                      /|                      /|
                     / |                     / |
                   11  |                    8  |
                   /   |                   /   |  
                  /   10                  /    7
                 /_____|______5__________/     |
                 |     |                 |     |
                 |     |                 |     |
                 |     |___________2_____|_____|
                 |     /                 |     / 
                 6    /                  4    /
                 |   3                   |   1
                 |  /                    |  /
                 | /                     | /
                 |/___________0__________|/

                ori:                rev:
                   <----               <----
                     2                   0
               |            ^      |            ^
               | 3        1 |      | 3'       1'|
               v            |      v            |
                     0                   2
                   ---->               ----> 
        '''

        #6个面的枚举顺序，以及影响到的棱
        target_list = [[0, 1, 2, 3], [0, 4, 5, 6], [1, 7, 8, 4], [2, 7, 9, 10], [3, 10, 11, 6], [5, 8, 9, 11]]

        #编码顺序冲突的棱，检验时需要一方反向编码
        reverst_list = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]]
        
        n = len(shapes[0])
        state_without_corner = (1 << (n - 1)) - 2
        edge_list = []
        one_cnt = 0
        for s in shapes:
            edge_list.append([[0, 0, 0, 0], [0, 0, 0, 0]])
            for index in range(n):
                #按下、右、上、左的顺序逆时针编码
                edge_list[-1][0][0] += edge_list[-1][0][0] + int(s[n - 1][index])
                edge_list[-1][0][1] += edge_list[-1][0][1] + int(s[n - 1 - index][n - 1])
                edge_list[-1][0][2] += edge_list[-1][0][2] + int(s[0][n - 1 - index])
                edge_list[-1][0][3] += edge_list[-1][0][3] + int(s[index][0])

                #顺时针编码
                edge_list[-1][1][0] += edge_list[-1][1][0] + int(s[n - 1][n - 1 - index])
                edge_list[-1][1][1] += edge_list[-1][1][1] + int(s[index][n - 1])
                edge_list[-1][1][2] += edge_list[-1][1][2] + int(s[0][index])
                edge_list[-1][1][3] += edge_list[-1][1][3] + int(s[n - 1 - index][0])
        
                #统计1的数量
                one_cnt += int(s[0][index]) + int(s[n - 1][index]) + int(s[index][0]) + int(s[index][n - 1])
            
            #减去四个角重复计算的1
            one_cnt -= int(s[0][0]) + int(s[0][n - 1]) + int(s[n - 1][n - 1]) + int(s[n - 1][0])

        #判断1的数量是否合法
        if one_cnt != n * 12 - 16:
            return False

        #8种板子的放置方式
        candidate_list = [[[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]], 
                     [[0, 3, 2, 1], [1, 0, 3, 2], [2, 1, 0, 3], [3, 2, 1, 0]]]

        def dfs(level, choose, used):
            if level == 6:
                return True
            
            for edge in range(6):
                if not used[edge]:
                    #对于没有用过的板子，枚举所有可能的放置方法
                    for d in range(2):
                        for candidate in candidate_list[d]:
                            #放置后4条边对应的编码
                            #当前编码方式d与reverst_list异或，表示对于冲突棱的校验需要按当前编码方式进行反向编码
                            tmp = [edge_list[edge][d ^ reverst_list[level][index]][candidate[index]] for index in range(4)]
                            flag = True
                            fill_cnt = 0
                            for index in range(4):
                                #对于已经填充过的棱，需要检验重叠以及中间部分填充
                                if target_list[level][index] < len(choose):
                                    now = tmp[index]
                                    filled = choose[target_list[level][index]]
                                    if (now & filled) != 0 or (now | filled) < state_without_corner:
                                        flag = False
                                        break
                                else:
                                    fill_cnt += 1
                            
                            if flag:
                                #检验通过，按当前枚举的方式放置板子，然后继续处理下一个面
                                for index in range(4):
                                    if target_list[level][index] < len(choose):
                                        continue
                                    choose.append(tmp[index])
                                used[edge] = True
                                if dfs(level + 1, choose, used):
                                    return True
                                used[edge] = False
                                for index in range(fill_cnt):
                                    choose.pop()
            
            return False

        #板子0作为底面
        choose = [edge_list[0][0][0], edge_list[0][0][1], edge_list[0][0][2], edge_list[0][0][3]]
        used = [False] * 6
        used[0] = True
        if dfs(1, choose, used):
            return True

        #板子0翻转后作为底面
        choose = [edge_list[0][1][0], edge_list[0][1][3], edge_list[0][1][2], edge_list[0][1][1]]
        if dfs(1, choose, used):
            return True
        
        return False
"""


def _ln(sub, k=0):
    ls = [i for i, l in enumerate(CODE.strip("\n").split("\n"), 1) if sub in l]
    return ls[k]


SHAPES = [["110","011","000"],["000","010","111"],["000","110","000"],["011","010","000"],["110","011","110"],["011","111","011"]]

FACE = ['底面', '前面', '右面', '后面', '左面', '上面']
TARGET = [[0, 1, 2, 3], [0, 4, 5, 6], [1, 7, 8, 4], [2, 7, 9, 10], [3, 10, 11, 6], [5, 8, 9, 11]]
L_FOR_EDGE = _ln('for edge in range(6)')
L_TMP = _ln('tmp = [')
L_CALL = _ln('if dfs(level + 1')


def _bits(v, n):
    return format(v, f'0{n}b')


def _bad(S, index):
    """第 index 条边与已填充的棱是否冲突（复刻代码里的判断）"""
    k = TARGET[S['level']][index]
    if k >= len(S['choose']):
        return None
    now, filled = S['tmp'][index], S['choose'][k]
    return (now & filled) != 0 or (now | filled) < S['state_without_corner']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    shapes = S.get('shapes') or SHAPES
    n = len(shapes[0])
    line = S.get('_line') or 0
    in_dfs = 'level' in S and 'choose' in S and 'used' in S
    level = S['level'] if in_dfs else 0
    inner = S.get('_inner') or {}
    cand = in_dfs and 'edge' in inner and line >= L_FOR_EDGE and line <= L_CALL
    # ---- 积木一排
    cv.text((x0 + 14, y0 + 2), '6 块板子（黄 = 正在试，蓝 = 已放好）', 21, T['muted'], bold=True)
    pc = min(18, (x1 - x0 - 40) / (6 * (n + 1.4)))
    px0 = x0 + 20
    used = S.get('used') or [False] * 6
    for k, sh in enumerate(shapes):
        X = px0 + k * (n + 1.4) * pc
        iscand = cand and S['edge'] == k and not used[k]
        col = T['yellow'] if iscand else (T['blue'] if (in_dfs and used[k]) else T['text'])
        for i in range(n):
            for j in range(n):
                on = sh[i][j] == '1'
                cv.rect((X + j * pc + 1, y0 + 40 + i * pc + 1, X + (j + 1) * pc - 1, y0 + 40 + (i + 1) * pc - 1),
                        fill=col if on else T['panel2'], alpha=255 if on else 120, r=3)
        cv.text((X + n * pc / 2, y0 + 44 + n * pc), f'板子 {k}', 18, col, anchor='mt', bold=True)
    # ---- 12 条棱
    ty = y0 + 40 + n * pc + 78
    cv.text((x0 + 14, ty - 34), '12 条棱（上一行 = 已占用，下一行 = 正在试的编码；高位在前）', 19, T['muted'], bold=True)
    cw = 24
    sw = (x1 - x0 - 30) / 4
    tmp = S.get('tmp') if (in_dfs and line >= L_TMP and line <= L_CALL and 'tmp' in inner) else None
    trial = {}
    if tmp is not None:
        for index in range(4):
            trial[TARGET[level][index]] = index
    choose = S.get('choose') or []
    for k in range(12):
        col_, row_ = k % 4, k // 4
        X = x0 + 20 + col_ * sw
        Y = ty + row_ * 112
        cv.text((X, Y), f'棱 {k}', 18, T['dim'], bold=True)
        for i in range(n):
            ch = _bits(choose[k], n)[i] if k < len(choose) else None
            fill = (T['blue'] if ch == '1' else T['panel2']) if ch is not None else None
            cv.rect((X + i * (cw + 3), Y + 26, X + i * (cw + 3) + cw, Y + 26 + cw), fill=fill, outline=T['border'], width=1 if ch is not None else 2, r=4)
            if ch is None:
                cv.text((X + i * (cw + 3) + cw / 2, Y + 26 + cw / 2), '·', 16, T['dim'], anchor='mm')
        if k in trial:
            idx = trial[k]
            b = _bad(S, idx)
            for i in range(n):
                ch = _bits(tmp[idx], n)[i]
                cv.rect((X + i * (cw + 3), Y + 58, X + i * (cw + 3) + cw, Y + 58 + cw), fill=(T['yellow'] if ch == '1' else T['panel2']),
                        outline=T['red'] if b else T['border'], width=3 if b else 1, r=4)
            if b is not None:
                cv.text((X + n * (cw + 3) + 6, Y + 70), '冲突' if b else '吻合', 17, T['red'] if b else T['green'], anchor='lm', bold=True)
    # ---- 说明
    ym = ty + 3 * 112 + 4
    if cand and 'd' in S and 'candidate' in S and line >= _ln('for candidate'):
        cv.text((x0 + 20, ym), f'第 {level} 个面（{FACE[level]}）← 板子 {S["edge"]}，{"原样" if S["d"] == 0 else "翻面"}，4 条边按 {S["candidate"]} 的顺序对应', 19, T['yellow'], bold=True)
    elif in_dfs:
        cv.text((x0 + 20, ym), f'第 {level} 个面（{FACE[level]}）：影响的棱 {TARGET[level] if level < 6 else ""}', 19, T['text'], bold=True)


def _end(S, B, name):
    return name in B['_inner'] and B['_inner'][name] == S['_inner'].get(name)


def _chk(S, B, ret):
    k = TARGET[S.level][S._inner.get('index', 0)]
    now, filled = S.now, S.filled
    ov = (now & filled) != 0
    gap = (now | filled) < S.state_without_corner
    n = len(S.shapes[0])
    s = f'棱 `{k}`：新 `{now:0{n}b}`，已有 `{filled:0{n}b}`'
    if ov:
        return s + ' → 有格子重叠（与运算不为 0）→ ==冲突=='
    if gap:
        return s + f' → 中间没填满（或运算小于 `{S.state_without_corner:0{n}b}`）→ ==冲突=='
    return s + ' → 不重叠、中间填满 → 吻合'


_PRE = _ln('for s in shapes')
_END_PRE = _ln('one_cnt -= ')

CONFIG = dict(
    num='LCP 58', title='积木拼接', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举摆放 + 棱编码位运算',
    tags=['链表树与回溯'],
    code=CODE,
    call='Solution().composeCube(SHAPES)',
    setup='SHAPES = ' + repr(SHAPES),
    expect=True,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('level', 'level', 'yellow'), ('edge', 'edge', 'blue'), ('d', 'd', 'cyan'), ('candidate', 'candidate', 'pink')],
    skip=list(range(_ln('edge_list = []'), _END_PRE + 1)) + [_ln('candidate_list = ') + 1, _ln('for edge in range(6)'), _ln('for candidate in candidate_list'), _ln('flag = False'), _ln('used = [False]'), _ln('used[0] = True'), _ln('return True', 2), _ln('for d in range(2)'), _ln('if not used[edge]'), _ln('if level == 6'), _ln('flag = True'), _ln('fill_cnt = 0'),
          _ln('for index in range(4)', 1), _ln('if target_list[level][index] < len(choose)', 0), _ln('now = tmp[index]'), _ln('filled = choose[target_list'),
          _ln('break'), _ln('fill_cnt += 1'), _ln('for index in range(4)', 2), _ln('if target_list[level][index] < len(choose)', 1), _ln('continue'),
          _ln('choose.append'), _ln('return True', 1), _ln('for index in range(fill_cnt)'), _ln('choose.pop()'), 'candidate_list', 'target_list = ', 'reverst_list = '],
    max_steps=80,
    captions={
        'n = len(shapes[0])': '每块板子是 `{n} × {n}` 的方阵',
        'state_without_corner = (1': '`state_without_corner = {state_without_corner:0{n}b}`：棱去掉两端顶角后，中间的位必须被填满',
        'edge_list = []': '`edge_list` 预处理每块板子的逆时针 / 顺时针 4 条边编码',
        'one_cnt != n * 12 - 16': '板子四边的 1 一共 `{one_cnt}` 个；12 条棱共 `12n − 16 = {n * 12 - 16}` 格 → ' + '==数量必须相等==',
        'choose = [edge_list[0][0][0]': '板子 0 当底面（只需考虑翻不翻）：它 4 条边先占住棱 0–3：`choose` = `{choose}`；`used` 标记板子 0 已用',
                'if dfs(1, choose, used)': '先试板子 0 原样当底面：从第 1 个面（前面）开始搜索',
        'tmp = [': lambda S, B, r: f'第 `{S.level}` 个面试板子 `{S.edge}`：{"原样" if S.d == 0 else "翻面"}，边按 `{S.candidate}` 的顺序对应。4 条边编码：' + '，'.join(f'`{x:0{len(S.shapes[0])}b}`' for x in S.tmp) + f'（对应棱 {TARGET[S.level]}）',
        'if (now & filled) != 0': _chk,
        'if flag:': lambda S, B, r: ('4 条边都检验通过' if S.flag else '有冲突，试下一种放法'),
        'used[edge] = True': '放上板子 `{edge}`（新占的棱已追加到 `choose`）：`choose` = `{choose}`',
        'if dfs(level + 1': '递归：去放第 `{B.level + 1}` 个面',
        'used[edge] = False': '后面放不下 → 回溯：释放板子 `{edge}`，并弹出刚追加的棱',
        'return True': '6 个面都放好了 → 返回 ==True==',
        'return False': '第 `{level}` 个面怎么放都不行 → 返回 False，上一层换个放法',
    },
    cards=dict(
        one_liner='把板子四条边编成二进制，按面的顺序枚举放法，用与/或检查棱',
        complexity='时间 `O(6! × 8^5)`（有剪枝，实际很小），空间 `O(1)`',
        problem=['6 块 `n × n` 的板子，中间都是实心，只有边上有空缺',
                 '板子可旋转、翻面，问能否围成正方体，每块恰好一个面',
                 '本视频：6 块 `3 × 3` 板子（示例 1 的顺序做了调整），答案 `true`'],
        quote='题目给出的6块板子中间都是实心的，意思就是说这六块板子的四条边拼起来，能否刚刚好构成正方体的十二条棱。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数 1：12 条棱共 `12n − 16` 格，板子四边的 1 总数不对就直接 False',
              '板子 0 当底面，其余按 前、右、后、左、上 的顺序逐个枚举，每块 8 种放法（4 旋转 × 翻面）',
              '检验：已占用的棱，新边与旧边 `&` 必须为 0，`|` 必须填满中间（`>= (1 << (n-1)) - 2`）'],
        summary=['时间 `O(6! × 8^5)`，棱长不超过 10，位运算判断一次 `O(1)`',
                 '先数 1 的个数是个便宜的剪枝；中间填满的检查可以提前砍掉非法分支',
                 '部分棱在两个面里编码方向相反，用 `reverst_list` 对其中一方反向编码',
                 '原文为 Python 2 风格，但在 Python 3 下可直接运行，代码未改动；视频里把示例 1 的 6 块板子换了顺序，搜索更快找到解'],
    ),
)
