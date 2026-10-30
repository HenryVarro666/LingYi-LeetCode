N, K, M = 3, 2, 3
TIME = [2, 5, 8]
MUL = [1.0, 1.5, 0.75]
U = 1 << N

CODE = '''
class Solution:
    def minTime(self, n: int, k: int, m: int, time: List[int], mul: List[float]) -> float:
        u = 1 << n
        # 预处理每个 time 子集的最大值
        max_time = [0] * u
        for i, t in enumerate(time):
            high_bit = 1 << i
            for mask in range(high_bit):
                max_time[high_bit | mask] = max(max_time[mask], t)

        # 预处理每个集合的大小 <= k 的非空子集
        sub_masks = [[] for _ in range(u)]
        for i in range(u):
            sub = i
            while sub:
                if sub.bit_count() <= k:
                    sub_masks[i].append(sub)
                sub = (sub - 1) & i

        dis = [[[inf, inf] for _ in range(u)] for _ in range(m)]
        h = []

        def push(d: float, stage: int, mask: int, direction: int) -> None:
            if d < dis[stage][mask][direction]:
                dis[stage][mask][direction] = d
                heappush(h, (d, stage, mask, direction))

        push(0, 0, u - 1, 0)  # 起点

        while h:
            d, stage, left, direction = heappop(h)  # left 是剩余没有过河的人
            if left == 0:  # 所有人都过河了
                return d
            if d > dis[stage][left][direction]:
                continue
            if direction == 0:
                # 枚举 sub 这群人坐一艘船过河
                for sub in sub_masks[left]:
                    cost = max_time[sub] * mul[stage]
                    push(d + cost, (stage + floor(cost)) % m, left ^ sub, 1)
            else:
                # 枚举回来的人
                s = (u - 1) ^ left
                while s:
                    lb = s & -s
                    cost = max_time[lb] * mul[stage]
                    push(d + cost, (stage + floor(cost)) % m, left ^ lb, 0)
                    s ^= lb

        return -1
'''
_L = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    ids = [i + 1 for i, l in enumerate(_L) if sub in l]
    return ids[nth]


POP_LINE = _ln('heappop(h)')
FOR_SUB = _ln('for sub in sub_masks[left]')
S_LINE = _ln('s = (u - 1) ^ left')
LB_LINE = _ln('lb = s & -s')
RET_LINE = _ln('return d')
CALL_LINES = {_ln('push(d + cost, (stage + floor(cost)) % m, left ^ sub, 1)'), _ln('push(d + cost, (stage + floor(cost)) % m, left ^ lb, 0)')}


def _isp(S):
    inn = S.get('_inner') or {}
    return 'mask' in inn and 'u' not in inn


def _src(S, B):
    return B if _isp(S) else S


def _cur(S, B):
    line = S.get('_line') or 0
    src = _src(S, B)
    if not all(k in src for k in ('left', 'stage', 'direction', 'd')):
        return None
    return src


def _boat(S, B, src, line):
    if src is None:
        return None
    dr = src['direction']
    if dr == 0 and line >= FOR_SUB and line < S_LINE and 'sub' in src:
        return src['sub']
    if dr == 1 and line >= LB_LINE and 'lb' in src:
        return src['lb']
    return None


def _people(cv, T, x, y, w, mask, boat, title, col):
    cv.text((x + w / 2, y), title, 22, T['muted'], anchor='mt', bold=True)
    ids = [i for i in range(N) if mask >> i & 1]
    cw, ch = min(130, (w - 10) / max(1, min(len(ids), 2)) - 8), 46
    for k, i in enumerate(ids):
        cx = x + 5 + (k % 2) * (cw + 8)
        cy = y + 40 + (k // 2) * (ch + 8)
        on = boat is not None and (boat >> i & 1)
        cv.rect((cx, cy, cx + cw, cy + ch), fill=T['yellow'] if on else T['panel2'], outline=T['border'], r=10, width=2)
        cv.text((cx + cw / 2, cy + ch / 2), f'{i}号 t={TIME[i]}', 22, T['bg'] if on else T['text'], anchor='mm', bold=True)


def _river(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line') or 0
    src = _cur(S, B)
    cv.text((x0 + 18, y0 + 4), '营地（未过河） ⇄ 河对岸（已过河）', 22, T['muted'], bold=True)
    w = x1 - x0
    bank = w * 0.36
    cv.rect((x0 + 14, y0 + 40, x0 + 14 + bank, y1 - 6), outline=T['border'], r=12, width=2)
    cv.rect((x1 - 14 - bank, y0 + 40, x1 - 14, y1 - 6), outline=T['border'], r=12, width=2)
    cv.rect((x0 + 24 + bank, y0 + 60, x1 - 24 - bank, y1 - 26), fill=T['panel2'], r=10)
    if src is None:
        left = U - 1 if line < POP_LINE else None
        boat = None
        if left is None:
            return
        _people(cv, T, x0 + 22, y0 + 46, bank - 16, left, None, '营地', T['text'])
        return
    left, dr = src['left'], src['direction']
    boat = _boat(S, B, src, line)
    _people(cv, T, x0 + 22, y0 + 46, bank - 16, left, boat if dr == 0 else None, f'营地 {left:0{N}b}', T['text'])
    _people(cv, T, x1 - 14 - bank + 8, y0 + 46, bank - 16, (U - 1) ^ left, boat if dr == 1 else None, f'对岸 {(U - 1) ^ left:0{N}b}', T['text'])
    mx = (x0 + x1) / 2
    cv.text((mx, y0 + 64), f"阶段 {src['stage']}  ×{MUL[src['stage']]}", 22, T['cyan'], anchor='mt', bold=True)
    cv.text((mx, y0 + 92), f"用时 {src['d']:g}", 22, T['green'], anchor='mt', bold=True)
    ay = y0 + 132
    if dr == 0:
        cv.arrow((mx - 60, ay), (mx + 60, ay), T['yellow'] if boat else T['dim'], 6, 20)
        cv.text((mx, ay + 14), '一群人过河' + (f' {boat:0{N}b}' if boat else ''), 20, T['muted'], anchor='mt')
    else:
        cv.arrow((mx + 60, ay), (mx - 60, ay), T['yellow'] if boat else T['dim'], 6, 20)
        cv.text((mx, ay + 14), '一个人划回' + (f' {boat:0{N}b}' if boat else ''), 20, T['muted'], anchor='mt')


def _fmtv(v):
    return '∞' if v == inf else f'{v:g}'


def _table(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'dis[阶段][left][方向]（列 = left：还在营地的人；行 = 阶段+方向）', 22, T['muted'], bold=True)
    dis = S.get('dis')
    if dis is None:
        return
    rows = [(st, dr) for st in range(M) for dr in (0, 1)]
    cw = min(96, (x1 - x0 - 150) / U)
    rh = min(46, (y1 - y0 - 100) / len(rows))
    sx, sy = x0 + 120, y0 + 76
    src = _cur(S, B)
    inner = S.get('_inner') or {}
    new = (inner['stage'], inner['mask'], inner['direction']) if _isp(S) else None
    for c in range(U):
        cv.text((sx + c * cw + cw / 2, sy - 6), f'{c:0{N}b}', 18, T['muted'], anchor='mb', mono=True)
    for r, (st, dr) in enumerate(rows):
        cv.text((sx - 8, sy + r * rh + rh / 2), f'阶段{st} ' + ('过河' if dr == 0 else '返回'), 18, T['muted'], anchor='rm')
        for c in range(U):
            v = dis[st][c][dr]
            cur = src is not None and (src['stage'], src['left'], src['direction']) == (st, c, dr)
            isnew = new == (st, c, dr)
            fill = T['blue'] if cur else (T['orange'] if v != inf else T['panel2'])
            cv.rect((sx + c * cw + 2, sy + r * rh + 2, sx + (c + 1) * cw - 2, sy + (r + 1) * rh - 2), fill=fill,
                    outline=T['yellow'] if isnew else T['border'], width=4 if isnew else 1, r=6)
            cv.text((sx + c * cw + cw / 2, sy + r * rh + rh / 2), _fmtv(v), 20, T['bg'] if fill != T['panel2'] else T['dim'], anchor='mm', bold=True)


def _text(S, B):
    src = _cur(S, B)
    if src is None:
        return '节点 = (阶段, 还没过河的集合, 方向)：方向 0 = 一群人过河，1 = 一个人划回'
    what = '要派一群人过河' if src['direction'] == 0 else '要派一个人划回营地'
    return f"当前：阶段 `{src['stage']}`，营地还有 `{src['left']:0{N}b}`，{what}，已用 `{src['d']:g}`"


def _fmth(t):
    return f'{t[0]:g}|s{t[1]}|{t[2]:0{N}b}|{"回" if t[3] else "去"}'


_V = {}


def _forsub(S, B, r):
    k = (S.d, S.stage, S.left, S.direction)
    c = _V.get(k, 0)
    nb = S.sub_masks[S.left]
    if c >= len(nb):
        _V.pop(k, None)
        return f'`{S.left:0{N}b}` 的子集都枚举完了，处理堆里的下一个状态'
    _V[k] = c + 1
    return f'枚举过河的人群 `sub = {nb[c]:0{N}b}`（大小 ≤ k，不一定坐满：小倍率阶段再运大个子更划算）'


def _pushcap(S, B, r):
    # S: inside push (new state); B: caller env
    c = B.cost
    old = B.dis[S.stage][S.mask][S.direction]
    tail = f'`dis` 原为 {_fmtv(old)}，' + ('新值更小 → ==更新并入堆==' if S.d < old else '不比它小 → 不更新')
    return (f'新状态：阶段 `({B.stage}+floor({c:g}))%{B.m}` = ==`{S.stage}`==，营地剩 `{S.mask:0{N}b}`，'
            f'用时 `{B.d:g}+{c:g}` = ==`{S.d:g}`==；{tail}')


CONFIG = dict(
    num=3594, title='所有人渡河所需的最短时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 Dijkstra（状压）',
    tags=['灵神题单·动态规划', '灵神题单·图论算法', '难度分 2604'],
    code=CODE,
    setup='from math import floor',
    call=f'Solution().minTime({N}, {K}, {M}, {TIME}, {MUL})',
    expect=14.5,
    skip=['for i, t in enumerate(time)', 'high_bit = 1 << i', 'for mask in range(high_bit)', 'max_time[high_bit | mask]',
          'for i in range(u)', 'sub = i', 'while sub:', 'sub.bit_count()', 'sub_masks[i].append', 'sub = (sub - 1) & i',
          'if d < dis[stage][mask][direction]', 'dis[stage][mask][direction] = d', 'heappush(h, (d, stage, mask, direction))', 's ^= lb'],
    max_steps=50,
    views=[
        dict(type='text', fn=_text, h=50, size=22),
        dict(type='custom', draw=_river, h=225),
        dict(type='custom', draw=_table, h=320),
        dict(type='heap', var='h', label='h：(用时|阶段|营地|去/回)', h=100, fmt=_fmth),
    ],
    watch=[('d', 'd', 'green'), ('stage', 'stage', 'cyan'), ('left', 'left', 'blue'), ('direction', 'direction', 'orange'), ('cost', 'cost', 'yellow')],
    captions={
        'u = 1 << n': '用二进制表示集合：`u = 1 << {n}` = {u}，共 `2^{n}` 种「营地里还剩谁」',
        'max_time = [0] * u': '预处理：`max_time[S]` = 集合 S 里 time 的最大值（这群人的过河耗时由最慢的人决定）',
        'sub_masks = [[] for': '预处理：`sub_masks[S]` = S 的所有大小 `<= k` 的非空子集（船坐得下的人群）',
        'dis = [[[inf, inf]': '`dis[阶段][left][方向]` = 到这个节点的最短用时，节点 = (阶段, 营地里剩的人, 方向)',
        'h = []': '堆里存 `(用时, 阶段, left, 方向)`',
        'push(0, 0, u - 1, 0)': '起点：阶段 0，所有人都在营地（`left = {u-1:0{n}b}`），方向 0 = 先送一群人过河',
        'while h': lambda S, B, r: '堆非空，取用时最短的状态' if S.h else '堆空了：不可能所有人过河',
        'd, stage, left, direction = heappop': '弹出：用时 `{d:g}`，阶段 `{stage}`，营地还剩 `{left:0{n}b}`，' + '方向 `{direction}`',
        'if left == 0': lambda S, B, r: '营地没人了 → ==所有人都过河==' if S.left == 0 else f'营地还剩 `{S.left:0{N}b}`，没渡完',
        'return d': '==第一次弹出 left = 0 的状态==，Dijkstra 保证用时最小：`{d:g}`',
        'if d > dis[stage][left][direction]': lambda S, B, r: (f'`{S.d:g} > dis = {S.dis[S.stage][S.left][S.direction]:g}` → 成立：堆里的旧记录' if S.d > S.dis[S.stage][S.left][S.direction] else f'`{S.d:g} = dis` → 不成立：这是最新记录，继续扩展'),
        'continue': '旧记录，==跳过==',
        'if direction == 0': lambda S, B, r: '方向 0：船在营地，==派一群人过河==' if S.direction == 0 else '方向 1：船在对岸，==派一个人划回==',
        'for sub in sub_masks[left]': _forsub,
        'cost = max_time[sub] * mul[stage]': '过河耗时：最慢的人 `{max_time[sub]}` × 当前倍率 `{mul[stage]}` = =={cost:g}==',
        'push(d + cost, (stage + floor(cost)) % m, left ^ sub, 1)': _pushcap,
        's = (u - 1) ^ left': '已经过河的人 `s = {s:0{n}b}`：谁都可能划回来（不只是刚过河的那几个）',
        'lb = s & -s': '取出 `s` 的最低位：一个划回的人 `{lb:0{n}b}`',
        'cost = max_time[lb] * mul[stage]': '划回耗时：`time = {max_time[lb]}` × 倍率 `{mul[stage]}` = =={cost:g}==',
        'push(d + cost, (stage + floor(cost)) % m, left ^ lb, 0)': _pushcap,
        'return -1': '堆空了 → ==无法让所有人过河==，返回 -1',
    },
    cards=dict(
        one_liner='(阶段, 还没过河的集合, 方向) 当节点，跑 Dijkstra',
        complexity='时间 `O(M log M)`，`M = m·3^n`，空间 `O(M)`',
        problem=['`n` 个人用一艘最多坐 `k` 人的船过河，每个阶段有速度倍率 `mul[j]`',
                 '过河耗时 = 组内最大 `time` × 倍率，之后阶段前进 `floor(耗时) % m`，每趟需有人划回',
                 '本视频：`time=[2,5,8]`，`mul=[1.0,1.5,0.75]`，`k=2` → `14.5`'],
        quote='由于存在来来回回过河的情况，计算过程中可能会形成环，所以 DP（记忆化搜索）不太合适。改成在这个有向图上跑 Dijkstra 最短路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['阶段会循环，状态有环 → 不能 DP，改成最短路',
              '写法二加方向维度：先「送一群人」，再「回一个人」，回来的人在对岸集合里枚举',
              '子集可以小于 `k`，回来的人也不一定是刚过河的，都是为了把握倍率小的阶段'],
        after=[dict(heading='写法一：合并成一步', lines=[
            '节点只有 `(阶段, 集合)`，过河和划回在同一步里枚举',
            '时间复杂度 `O(nm3^n log)`，比状态机多一个 `n` 的重复枚举',
            '状态机把「过河后」拆成独立节点，省掉重复枚举'])],
        summary=['时间 `O(m·3^n log)`：枚举「集合的子集」总共 `3^n`',
                 '易错：划回的人可以是之前过河的任何人，不能贪心选最快的',
                 '易错：阶段只在过河/划回之后才推进，不能原地等',
                 '`bit_count()` 需要 Python 3.10+；灵神另给了合并写法（写法一）'],
    ),
)
