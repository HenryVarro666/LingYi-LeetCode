N, K, M = 3, 2, 3
TIME = [2, 5, 8]
MUL = [1.0, 1.5, 0.75]
FULL = (1 << N) - 1

CODE = '''
class Solution(object):
    def minTime(self, n, k, m, time, mul):

        max_state = (1 << n) - 1
        sub_contain = {}
        sub_cost = {}

        for state in range(1, max_state + 1):
            contain = []
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    contain.append(index)

            sub_contain[state] = contain[:]
            if len(contain) <= k:
                sub_cost[state] = max([time[index] for index in contain])


        heap = [(0, 0, 0)]
        f = [[None] * m for _ in range(max_state + 1)]
        f[0][0] = 0.0
        while heap:
            cost, state, step = heapq.heappop(heap)
            if cost > f[state][step]:
                continue
            if state == max_state:
                return cost
            for sub in sub_cost:
                if state & sub == 0:
                    nxt_state = state | sub
                    d = sub_cost[sub] * mul[step]
                    nxt_step = (step + int(d)) % m

                    if nxt_state == max_state:
                        if f[nxt_state][nxt_step] is None or f[nxt_state][nxt_step] > cost + d:
                            f[nxt_state][nxt_step] = cost + d
                            heapq.heappush(heap, (cost + d, nxt_state, nxt_step))
                    else:
                        for rt in sub_contain[nxt_state]:
                            state_with_rt = nxt_state ^ (1 << rt)
                            rt_d = time[rt] * mul[nxt_step]
                            step_with_rt = (nxt_step + int(rt_d)) % m

                            if f[state_with_rt][step_with_rt] is None or f[state_with_rt][step_with_rt] > cost + d + rt_d:
                                f[state_with_rt][step_with_rt] = cost + d + rt_d
                                heapq.heappush(heap, (cost + d + rt_d, state_with_rt, step_with_rt))

        return -1
'''
_L = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    return [i + 1 for i, l in enumerate(_L) if sub in l][nth]


POP_LINE = _ln('heappop')
FOR_SUB = _ln('for sub in sub_cost')
NXT_STATE = _ln('nxt_state = state | sub')
NXT_STEP = _ln('nxt_step = (step')
RT_FOR = _ln('for rt in sub_contain')
SWR = _ln('state_with_rt = nxt_state')
STWR = _ln('step_with_rt = (nxt_step')
RET_LINE = _ln('return cost')


def _cur(S):
    line = S.get('_line') or 0
    if line >= POP_LINE and all(k in S for k in ('cost', 'state', 'step', 'f')) and line < RET_LINE + 200:
        return S
    return None


def _boat(S, line):
    if 'sub' in S and line >= NXT_STATE and line < RT_FOR:
        return ('go', S['sub'])
    if 'rt' in S and line >= SWR:
        return ('back', 1 << S['rt'])
    return None


def _people(cv, T, x, y, w, mask, boat, title):
    cv.text((x + w / 2, y), title, 22, T['muted'], anchor='mt', bold=True)
    ids = [i for i in range(N) if mask >> i & 1]
    cw, ch = min(130, (w - 10) / 2 - 8), 46
    for k, i in enumerate(ids):
        cx = x + 5 + (k % 2) * (cw + 8)
        cy = y + 40 + (k // 2) * (ch + 8)
        on = boat is not None and (boat >> i & 1)
        cv.rect((cx, cy, cx + cw, cy + ch), fill=T['yellow'] if on else T['panel2'], outline=T['border'], r=10, width=2)
        cv.text((cx + cw / 2, cy + ch / 2), f'{i}号 t={TIME[i]}', 22, T['bg'] if on else T['text'], anchor='mm', bold=True)


def _river(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line') or 0
    S0 = _cur(S)
    cv.text((x0 + 18, y0 + 4), '营地（还没过河） ⇄ 河对岸（已过河）', 22, T['muted'], bold=True)
    w = x1 - x0
    bank = w * 0.36
    cv.rect((x0 + 14, y0 + 40, x0 + 14 + bank, y1 - 6), outline=T['border'], r=12, width=2)
    cv.rect((x1 - 14 - bank, y0 + 40, x1 - 14, y1 - 6), outline=T['border'], r=12, width=2)
    cv.rect((x0 + 24 + bank, y0 + 60, x1 - 24 - bank, y1 - 26), fill=T['panel2'], r=10)
    state = S0['state'] if S0 else 0
    boat = _boat(S0, line) if S0 else None
    camp, far = FULL ^ state, state
    if boat and boat[0] == 'go':
        camp_b, far_b = boat[1], None
    elif boat:
        camp_b, far_b = None, boat[1]
    else:
        camp_b = far_b = None
    # 过河的人在营地里高亮；划回的人在对岸里高亮
    if boat and boat[0] == 'go':
        camp_show, far_show = camp, far
    elif boat:
        camp_show, far_show = camp, far
    else:
        camp_show, far_show = camp, far
    if boat and boat[0] == 'back':
        # 过河后的状态：nxt_state 里 rt 在对岸
        far_show = S0.get('nxt_state', far)
        camp_show = FULL ^ far_show
    _people(cv, T, x0 + 22, y0 + 46, bank - 16, camp_show, camp_b, f'营地 {camp_show:0{N}b}')
    _people(cv, T, x1 - 14 - bank + 8, y0 + 46, bank - 16, far_show, far_b, f'对岸 {far_show:0{N}b}')
    if S0 is None:
        return
    mx = (x0 + x1) / 2
    cv.text((mx, y0 + 64), f"阶段 {S0['step']}  ×{MUL[S0['step']]}", 22, T['cyan'], anchor='mt', bold=True)
    cv.text((mx, y0 + 92), f"用时 {S0['cost']:g}", 22, T['green'], anchor='mt', bold=True)
    ay = y0 + 132
    if boat and boat[0] == 'go':
        cv.arrow((mx - 60, ay), (mx + 60, ay), T['yellow'], 6, 20)
        cv.text((mx, ay + 14), f'过河 {boat[1]:0{N}b}', 20, T['muted'], anchor='mt')
    elif boat:
        cv.arrow((mx + 60, ay), (mx - 60, ay), T['yellow'], 6, 20)
        cv.text((mx, ay + 14), f'划回 {boat[1]:0{N}b}', 20, T['muted'], anchor='mt')


def _fmtv(v):
    return '·' if v is None else f'{v:g}'


def _table(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'f[state][step]（列 = state：已过河的人；行 = 阶段 step）', 22, T['muted'], bold=True)
    f = S.get('f')
    if f is None:
        return
    line = S.get('_line') or 0
    U = FULL + 1
    cw = min(96, (x1 - x0 - 150) / U)
    rh = min(58, (y1 - y0 - 100) / M)
    sx, sy = x0 + 120, y0 + 80
    S0 = _cur(S)
    new = None
    if S0 is not None:
        if line >= STWR and 'state_with_rt' in S and 'step_with_rt' in S and 'rt' in S:
            new = (S['step_with_rt'], S['state_with_rt'])
        elif line >= NXT_STEP and line < RT_FOR and 'nxt_state' in S and S['nxt_state'] == FULL:
            new = (S['nxt_step'], S['nxt_state'])
    for c in range(U):
        cv.text((sx + c * cw + cw / 2, sy - 6), f'{c:0{N}b}', 18, T['muted'], anchor='mb', mono=True)
    for st in range(M):
        cv.text((sx - 8, sy + st * rh + rh / 2), f'阶段 {st}', 18, T['muted'], anchor='rm')
        for c in range(U):
            v = f[c][st]
            cur = S0 is not None and (S0['step'], S0['state']) == (st, c)
            isnew = new == (st, c)
            fill = T['blue'] if cur else (T['orange'] if v is not None else T['panel2'])
            cv.rect((sx + c * cw + 2, sy + st * rh + 2, sx + (c + 1) * cw - 2, sy + (st + 1) * rh - 2), fill=fill,
                    outline=T['yellow'] if isnew else T['border'], width=4 if isnew else 1, r=6)
            cv.text((sx + c * cw + cw / 2, sy + st * rh + rh / 2), _fmtv(v), 20, T['bg'] if fill != T['panel2'] else T['dim'], anchor='mm', bold=True)


def _text(S, B):
    S0 = _cur(S)
    if S0 is None:
        return '节点 = (已过河的人 state, 阶段 step)：每次「去一群人 + 回一个人」算一条边'
    return f"当前：已过河 `{S0['state']:0{N}b}`，阶段 `{S0['step']}`，已用 `{S0['cost']:g}`"


def _fmth(t):
    return f'{t[0]:g}|{t[1]:0{N}b}|s{t[2]}'


_V = {}


def _forsub(S, B, r):
    k = (S.cost, S.state, S.step)
    c = _V.get(k, 0)
    keys = list(S.sub_cost)
    if c >= len(keys):
        _V.pop(k, None)
        return f'`sub_cost` 里的人群都试过了，处理堆里的下一个状态'
    _V[k] = c + 1
    return f'试 `sub = {keys[c]:0{N}b}` 这群人'


_V2 = {}


def _forrt(S, B, r):
    k = (S.cost, S.state, S.step, S.sub)
    c = _V2.get(k, 0)
    nb = S.sub_contain[S.nxt_state]
    if c >= len(nb):
        _V2.pop(k, None)
        return '对岸的人都试过当划回者了'
    _V2[k] = c + 1
    return f'试对岸第 `{nb[c]}` 号当划回的人'


def _cmp_end(S, B, r):
    old = B.f[S.nxt_state][S.nxt_step]
    return (f'`f[{S.nxt_state:0{N}b}][{S.nxt_step}] = {_fmtv(old)}`，新值 `{S.cost:g}+{S.d:g}` = `{B.cost + S.d:g}` → ' +
            ('==更优，更新=='if old is None or old > B.cost + S.d else '不更优，跳过'))


def _cmp_rt(S, B, r):
    new = S.cost + S.d + S.rt_d
    old = S.f[S.state_with_rt][S.step_with_rt]
    return (f'`f[{S.state_with_rt:0{N}b}][{S.step_with_rt}] = {_fmtv(old)}`，新值 `{S.cost:g}+{S.d:g}+{S.rt_d:g}` = `{new:g}` → ' +
            ('==更优，更新=='if old is None or old > new else '不更优，跳过'))


CONFIG = dict(
    num=3594, title='所有人渡河所需的最短时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 + 最短路（去一群、回一人）',
    tags=['灵神题单·动态规划', '灵神题单·图论算法', '难度分 2604'],
    code=CODE,
    call=f'Solution().minTime({N}, {K}, {M}, {TIME}, {MUL})',
    expect=14.5,
    skip=['for state in range(1, max_state + 1)', 'contain = []', 'for index in range(n)', 'if state & (1 << index)', 'contain.append', 'sub_cost = {}',
          'sub_contain[state] = contain[:]', 'if len(contain) <= k', 'sub_cost[state] =',
          'heapq.heappush', 'state_with_rt = nxt_state', 'step_with_rt = (nxt_step', 'f[nxt_state][nxt_step] = cost + d',
          'f[state_with_rt][step_with_rt] = cost'],
    max_steps=52,
    views=[
        dict(type='text', fn=_text, h=50, size=22),
        dict(type='custom', draw=_river, h=225),
        dict(type='custom', draw=_table, h=240),
        dict(type='heap', var='heap', label='heap：(用时|已过河|阶段)', h=100, fmt=_fmth),
    ],
    watch=[('cost', 'cost', 'green'), ('state', 'state', 'blue'), ('step', 'step', 'cyan'), ('d', 'd', 'yellow'), ('rt_d', 'rt_d', 'orange')],
    captions={
        'max_state = ': '`max_state = {max_state}`：全部人都过河的状态（`n` 位全是 1）',
        'sub_contain = {}': '预处理：`sub_contain[S]` = S 里有哪些人；`sub_cost[S]` = 坐满一艘船（人数 `<= k`）时 S 的最慢耗时',
        'heap = [(0, 0, 0)]': '堆存 `(用时, 已过河的人, 阶段)`：起点没人过河，阶段 0',
        'f = [[None]': '`f[state][step]`：已过河 state、阶段 step 时的最小用时，`None` = 没到过',
        'f[0][0] = 0.0': '起点用时 0',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了：没有可行方案 → 返回 -1',
        'heapq.heappop': '弹出用时最小的状态：已过河 `{state:0{n}b}`，阶段 `{step}`，用时 `{cost:g}`',
        'if cost > f[state][step]': lambda S, B, r: (f'`{S.cost:g} > f = {S.f[S.state][S.step]:g}` → 成立：旧记录' if S.cost > S.f[S.state][S.step] else f'`{S.cost:g}` 就是 `f` 里的值 → 不成立，往下扩展'),
        'continue': '旧记录，==跳过==',
        'if state == max_state': lambda S, B, r: '所有人都过河了 → ==成立==' if S.state == S.max_state else f'已过河 `{S.state:0{N}b}`，还有人在营地',
        'return cost': '==第一次弹出全员过河的状态==：最小用时 `{cost:g}`',
        'for sub in sub_cost': _forsub,
        'if state & sub == 0': lambda S, B, r: (f'`{S.state:0{N}b} & {S.sub:0{N}b} == 0` → ==这群人都还在营地==，可以出发' if S.state & S.sub == 0 else f'`{S.state:0{N}b} & {S.sub:0{N}b} != 0` → 有人已经过河了，换一群'),
        'nxt_state = state | sub': '这群人过河后，已过河 `{state:0{n}b} | {sub:0{n}b}` = =={nxt_state:0{n}b}==',
        'd = sub_cost[sub] * mul[step]': '过河耗时：最慢的人 `{sub_cost[sub]}` × 倍率 `{mul[step]}` = =={d:g}==',
        'nxt_step = (step + int(d)) % m': '阶段推进 `int({d:g}) = {int(d)}` 步：`({step}+{int(d)}) % {m}` = =={nxt_step}==',
        'if nxt_state == max_state': lambda S, B, r: ('所有人都过去了：不用再划回去' if S.nxt_state == S.max_state else '还有人在营地：需要对岸有一个人划回来'),
        'if f[nxt_state][nxt_step] is None': _cmp_end,
        'for rt in sub_contain[nxt_state]': _forrt,
        'rt_d = time[rt] * mul[nxt_step]': '划回耗时：`time[{rt}] = {time[rt]}` × 新阶段倍率 `{mul[nxt_step]}` = =={rt_d:g}==',
        'if f[state_with_rt][step_with_rt] is None': _cmp_rt,
        'return -1': '堆空了：==没有可行方案==，返回 -1',
    },
    cards=dict(
        one_liner='「去一群 + 回一人」合成一条边：状态是（已过河的人，阶段）',
        complexity='时间 `O(m·3^n·n·log)`（常数大），空间 `O(m·2^n)`',
        problem=['`n` 个人用一艘最多坐 `k` 人的船过河，阶段 `j` 的倍率是 `mul[j]`',
                 '过河耗时 = 组内最慢 `time` × 倍率，阶段前进 `int(耗时) % m`；有人没过河就要一人划回',
                 '本视频：`time=[2,5,8]`，`mul=[1.0,1.5,0.75]`，`k=2` → `14.5`'],
        quote='直观看来，应该让最快的人当摆渡人，每次带最慢的几个人过河，但是这个策略明显是有问题的……在这里很难找到通用的贪心策略。不过本题中需要过河的人数n较小，因此可以使用状态压缩来处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心不行（例：`[1,2,9,10]` 先送 1、2 再回 2 更省）→ 状压 + 最短路',
              '阶段循环，没有固定的 DP 顺序 → 用堆按用时从小到大扩展',
              '一次扩展：枚举过河的人群 `sub`，再枚举对岸谁划回，直接回到「营地侧」状态'],
        summary=['状态 `(state, step)` 共 `m·2^n` 个，每个枚举 `sub` 和划回者',
                 '易错：划回者从「过河后的 `nxt_state`」里选，所以可以是之前过河的人',
                 '易错：划回耗时用「过河后的新阶段」的倍率，不是出发阶段的',
                 '原文常数卡得紧，所以预处理出每个 `sub` 的人和最慢耗时；Python 3 下无需改写'],
    ),
)
