GRID = ["S.C", "#.P"]
NAMES = {0: '空', 1: '障', 2: '魔', 3: '城'}
COLS = {0: None, 1: 'orange', 2: 'pink', 3: 'blue'}


def _state(S, i, j, v):
    return None


def _board(S):
    return [list(r) for r in S['grid']]


def _bcolor(S, i, j, v):
    return {'S': 'pink', 'C': 'blue', 'P': 'purple', '#': 'orange'}.get(v)


def _f(S):
    """f[i] 的 16 个 state，只画已经填过的列：行 = 列号 i，列 = state"""
    if 'f' not in S:
        return None
    return [['' if x is None else x for x in row] for row in S['f']]


def _fcolor(S, i, j, v):
    if v == '':
        return None
    if S.get('i') == i and S.get('state') == j:
        return 'yellow'
    if S.get('i') is not None and i == S['i'] - 1 and j == S.get('prev_state'):
        return 'blue'
    return 'green'


def _cand(S):
    if 'first_candidate' not in S or 'second_candidate' not in S:
        return ''
    return f'上格候选 [状态,代价]：`{S["first_candidate"]}`　下格候选：`{S["second_candidate"]}`'


def _txt(S):
    if 'mapping' not in S:
        return ''
    P = '城堡' if S['mapping'].get('P') == 3 else '恶魔'
    t = f'这一轮：传送门 `P` 当作==' + P + '=='
    if 'first' in S and 'second' in S:
        t += f'　　当前列：first=`{S["first"]}`，second=`{S["second"]}`'
    if 'prev_state' in S and 'i' in S:
        t += f'　　prev_state=`{S["prev_state"]}`'
    return t


CONFIG = dict(
    num='LCP 38', title='守卫城堡', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP（列 DP，4 进制状态）',
    tags=['灵神题单·图论算法', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def guardCastle(self, grid):

        n = len(grid[0])

        def check():
            f = [[None] * 16 for _ in range(n)]
            for i in range(n):
                first = mapping[grid[0][i]]
                second = mapping[grid[1][i]]
                if first + second == 5:
                    return n * 2 + 1

                if i == 0:
                    max_prev_state = 0
                else:
                    max_prev_state = 15
                for prev_state in range(max_prev_state + 1):
                    prev_first = prev_state // 4
                    prev_second = prev_state % 4
                    if prev_first + first == 5 or prev_second + second == 5:
                        continue

                    if i > 0 and f[i - 1][prev_state] is None:
                        continue
                    
                    if i == 0:
                        last_w = 0
                    else:
                        last_w = f[i - 1][prev_state]

                    first_candidate = []
                    second_candidate = []

                    if first == 0:
                        if prev_first == 0 or prev_first == 1:
                            first_candidate.append([0, 0])    
                        else:
                            first_candidate.append([prev_first, 0])
                        first_candidate.append([1, 1])
                    else:
                        first_candidate.append([first, 0])
                    
                    if second == 0:
                        if prev_second == 0 or prev_second == 1:
                            second_candidate.append([0, 0])
                        else:
                            second_candidate.append([prev_second, 0])
                        second_candidate.append([1, 1])
                    else:
                        second_candidate.append([second, 0])

                    for first_state, first_cost in first_candidate:
                        for second_state, second_cost in second_candidate:
                            if first_state + second_state == 5:
                                continue
                            if first_state == 0 and second_state >= 2:
                                state = second_state * 4 + second_state
                            elif second_state == 0 and first_state >= 2:
                                state = first_state * 4 + first_state
                            else:
                                state = first_state * 4 + second_state
                            
                            if f[i][state] is None or f[i][state] > last_w + first_cost + second_cost:
                                f[i][state] = last_w + first_cost + second_cost

            res = n * 2 + 1
            for state in range(16):
                if f[-1][state] is not None:
                    res = min(res, f[-1][state])
            
            return res

        res = n * 2 + 1
        mapping = {}
        mapping['.']=  0
        mapping['#'] = 1
        mapping['S'] = 2
        mapping['C'] = 3
        mapping['P'] = 2
        res = min(res, check())
        mapping['P'] = 3
        res = min(res, check())
        
        if res == n * 2 + 1:
            res = -1
        return res
''',
    call=f'Solution().guardCastle({GRID})',
    expect=1,
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='grid', var=_board, label='地图（粉 S 恶魔，蓝 C 城堡，紫 P 传送门，橙 # 障碍；黄框 = 当前列）', cell=76, h=210,
             color=_bcolor, cursors=[(lambda S: None if S.get('i') is None else 0, 'i', 'yellow'),
                                     (lambda S: None if S.get('i') is None else 1, 'i', 'yellow')]),
        dict(type='text', fn=_cand, h=50),
        dict(type='table', var=_f, label='f[列][state]（state = 上×4+下；黄 = 新写，蓝 = 来源）', cell=60, h=250,
             rows=lambda S: [f'列{k}' for k in range(S['n'])] if 'n' in S else None,
             cols=list(range(16)), color=_fcolor),
    ],
    watch=[('i', 'i', 'blue'), ('prev_state', 'prev_state', 'pink'), ('state', 'state', 'yellow'), ('res', 'res', 'green')],
    skip=[74, 75, 76, 77, 78, 79, 'first = mapping', 'if i == 0', 'max_prev_state', 'for prev_state', 'prev_first = ',
          'prev_second = ', 'if prev_first + first', 'if i > 0 and f[i - 1]', 'continue', 'first_candidate = []',
          'second_candidate = []', 'if first == 0', 'if second == 0', 'if prev_first == 0', 'if prev_second == 0',
          'for first_state', 'for second_state', 'if first_state == 0 and', 'second_state == 0 and first_state >= 2',
          'for state in range(16)', 'for i in range(n)', 'if first + second == 5', 'res = min(res, check())', 'if first_state + second_state == 5', 'if f[i][state] is None or', 'second_candidate.append', 'if f[-1][state] is not None', 'f = [[None]'],
    captions={
        'n = len(grid[0])': '两行 `n = {n}` 列，按列 DP；每格 4 种状态，一列 16 种 state',
        "mapping['P'] = 2": '方针一：==放弃传送门==，所有 `P` 当作恶魔，只守城堡',
        "mapping['P'] = 3": '方针二：==防守传送门==，所有 `P` 当作城堡',
        'res = min(res, check())': lambda S, B, r: ('跑一轮 DP，传送门当作' + ('城堡' if B.mapping['P'] == 3 else '恶魔') + '，返回这轮的最少障碍数'),
        'second = mapping': '处理第 `{i}` 列：上 `{grid[0][i]}` → =={first}==，下 `{grid[1][i]}` → =={second}==（0 空 1 障 2 魔 3 城）',
        'if first + second == 5': lambda S, B, r: ('`first + second = 5`：一魔一城同列相邻，恶魔直接到达城堡，这个方针==无解==' if S.first + S.second == 5
                                                   else f'`first + second = {S.first + S.second}`，不是一魔一城同列，可以继续'),
        'return n * 2 + 1': '`first + second = 5`：第 `{i}` 列一魔一城同列相邻，恶魔直接到达城堡 → 这个方针==无解==，返回 `n * 2 + 1 = {n * 2 + 1}`（表示不可能）',
        'last_w = ': '接上一列状态 `{prev_state}`（上 {prev_state // 4}，下 {prev_state % 4}），已付 `{last_w}`',
        'first_candidate.append([0, 0])': '上格空地且左边无魔/城：保持空地，代价 0',
        'first_candidate.append([prev_first, 0])': '上一列上格是 `{prev_first}`（魔/城）：沿空地蔓延，状态沿袭，代价 0',
        'first_candidate.append([1, 1])': '空地也可放障碍：代价 1（下格同理）',
        'first_candidate.append([first, 0])': '上格不是空地，只能保持 `{first}`，代价 0（下格同理）',
        'state = second_state * 4 + second_state': '上格空、下格是 `{second_state}`：空格也算 `{second_state}` → `state = {state}`',
        'state = first_state * 4 + first_state': '下格空、上格是 `{first_state}`：空格也算 `{first_state}` → `state = {state}`',
        'state = first_state * 4 + second_state': '编码 `上×4+下 = {first_state}×4+{second_state}` → `state = {state}`',
        'f[i][state] = last_w': lambda S, B, r: (f'`f[{S.i}][{S.state}]`（原 {"空" if B.f[S.i][S.state] is None else B.f[S.i][S.state]}）= `{S.last_w}` + `{S.first_cost}` + `{S.second_cost}` = =={S.f[S.i][S.state]}==，取较小值'),
        'res = n * 2 + 1': '`res` 先设成 `n * 2 + 1`（表示无解），再对最后一列所有合法状态取最小',
        'res = min(res, f[-1][state])': '最后一列的合法状态 `{state}`，代价 `{f[-1][state]}` → `res = {res}`',
        'if res == n * 2 + 1': lambda S, B, r: (f'两轮取小得 `res = {S.res}`，不等于 `n * 2 + 1`，有解' if S.res != S.n * 2 + 1 else '仍是 `n * 2 + 1`，两个方针都无解 → 返回 -1'),
        'return res': lambda S, B, r: (f'这一轮最少障碍数 `{S.res}`' if 'f' in S._inner or 'mapping' not in S._inner else f'两种方针中较小的答案：最少放 `{S.res}` 个障碍'),
    },
    max_steps=110,
    cards=dict(
        one_liner='传送门全连通：要么当城堡守住，要么当恶魔放弃；再按列状压 DP',
        complexity='时间 `O(n · 16 · 4)`，空间 `O(16n)`',
        problem=['2 行 `n` 列地图：`S` 恶魔，`C` 城堡，`P` 传送门，`#` 障碍，`.` 空地',
                 '恶魔可在空地上下左右走；传送门彼此连通，恶魔进入任一传送门就能到达所有传送门',
                 '可以把空地改成障碍，求最少改几个，使恶魔到不了城堡和传送门（无解返回 -1）',
                 '本视频：`["S.C", "#.P"]` → `1`'],
        quote='由于所有传送门都连通，那么一旦有一座传送门失守，相当于所有传送门都沦陷了，于是在一开始就可以决定一个大方针，即防守城堡以及所有传送门，或者仅防守城堡。',
        quote_src='—— yiduobo 题解原文',
        idea=['传送门全连通 → 两种大方针：`P` 当恶魔（只守城堡），或 `P` 当城堡（全守）',
              '`f[i][state]`：前 `i` 列、末列两格状态为 `state` 且恶魔到不了城堡的最少障碍；状态 0 空 1 障 2 魔 3 城',
              '只有空地能操作：放障碍代价 1，不放就沿袭相邻的魔/城状态；一魔一城相邻即非法'],
        summary=['时间 `O(n)`（常数 16×4），两轮方针取小，都无解才返回 -1',
                 '空地一侧是恶魔/城堡时，空地也要当作同类编码，否则会漏掉蔓延',
                 '本例：当恶魔时 `P` 紧贴 `C`（同列相邻）→ 无解；当城堡时放一个障碍就够',
                 '原文为 Python 2 写法，整数除法 `prev_state / 4` 已改为 `//`，其余代码未改'],
    ),
)
