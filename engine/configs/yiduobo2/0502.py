K, W0 = 4, 0
PROFITS = [3, 1, 8, 2]
CAPITAL = [1, 0, 10, 1]


def _projects(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vl = S.get('value_list')
    sorted_now = 'heap' in S
    cv.text((x0 + 18, y0 + 4), 'value_list：[利润, 启动资金]' + ('（已按启动资金排序）' if sorted_now else ''), 24, T['muted'], bold=True)
    if not vl:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    n = len(vl)
    w = min(190, (x1 - x0 - 60) / n)
    W = S.get('W', W0)
    pos = S.get('pos', 0) if sorted_now else 0
    top = y0 + 50
    h = 96
    left = {}
    for x in S.get('heap') or []:
        left[-x] = left.get(-x, 0) + 1
    state = {}
    for i, (p, c) in enumerate(vl[:pos] if sorted_now else []):
        if left.get(p, 0) > 0:
            left[p] -= 1
            state[i] = 'heap'
        else:
            state[i] = 'done'
    for i, (p, c) in enumerate(vl):
        X = x0 + 30 + i * w
        if state.get(i) == 'heap':
            fill, tc = T['purple'], T['bg']             # 在堆里（候选）
        elif state.get(i) == 'done':
            fill, tc = (40, 45, 53), T['dim']           # 已经做完
        elif sorted_now and c <= W:
            fill, tc = T['green'], T['bg']              # 资金够，下一步会入堆
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X + 6, top, X + w - 6, top + h), fill=fill, r=12, outline=T['border'], width=2)
        cv.text((X + w / 2, top + 28), f'利润 {p}', 24, tc, anchor='mm', bold=True)
        cv.text((X + w / 2, top + 66), f'启动 {c}', 22, tc, anchor='mm')
        if i in state:
            cv.text((X + w / 2, top + h + 8), '在堆中' if state[i] == 'heap' else '已完成 ✓', 19,
                    T['purple'] if state[i] == 'heap' else T['green'], anchor='mt', bold=True)
    if sorted_now:
        X = x0 + 30 + min(pos, n) * w + w / 2
        cv.tri_up(X - (0 if pos < n else w / 2), top + h + 36, 10, T['pink'])
        cv.text((X - (0 if pos < n else w / 2), top + h + 50), 'pos' if pos < n else 'pos（到头）', 22, T['pink'], anchor='mt', bold=True)
        cv.text((x1 - 20, y1 - 10), f'手上资金 W = {W}：启动资金 ≤ {W} 的项目都能做', 22, T['yellow'], anchor='rb', bold=True)


def _while_cap(S, B, ret):
    pos, vl, W = B.pos, B.value_list, B.W
    if pos < len(vl) and W >= vl[pos][1]:
        return f'`W = {W}` ≥ 项目 `{vl[pos]}` 的启动资金 `{vl[pos][1]}` → 能启动，放进候选堆'
    if pos >= len(vl):
        return '所有项目都已经进过堆了'
    return f'`W = {W}` < 下一个项目的启动资金 `{vl[pos][1]}` → 后面的更贵，都启动不了'


def _pop_cap(S, B, ret):
    got = S.W - B.W
    return f'弹出堆顶 `-{got}`：选==利润最大==的项目做，`W` = {B.W} + {got} = =={S.W}=='


CONFIG = dict(
    num=502, title='IPO', difficulty='Hard', category='堆',
    author='yiduobo', technique='按资金排序 + 大根堆选最大利润',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def findMaximizedCapital(self, k, W, Profits, Capital):
        value_list = []
        for index in range(len(Profits)):
            value_list.append([Profits[index], Capital[index]])

        value_list = sorted(value_list, key=lambda d:d[1])

        heap = []
        pos = 0
        for index in range(k):
            while pos < len(value_list) and W >= value_list[pos][1]:
                heapq.heappush(heap, -value_list[pos][0])
                pos += 1
            if not heap:
                break
            W -= heapq.heappop(heap)

        return W
''',
    call=f'Solution().findMaximizedCapital({K}, {W0}, {PROFITS}, {CAPITAL})',
    expect=6,
    views=[
        dict(type='custom', draw=_projects, h=280),
        dict(type='heap', var='heap', label='heap（存 −利润，堆顶 = 利润最大）', h=120),
        dict(type='text', fn=lambda S: (f"第 `{S['index'] + 1}` / {K} 个项目" if 'heap' in S and 'index' in S and isinstance(S['index'], int) and S['index'] < K and S.get('_line', 0) > 10 else
                                        '资金只增不减 → 能启动的项目越来越多（排序后是一段前缀）'), size=26, h=70),
    ],
    watch=[('W', 'W', 'yellow'), ('pos', 'pos', 'pink'), ('heap', 'heap', 'purple')],
    skip=['for index in range(len(Profits))', 'value_list.append', 'pos += 1'],
    captions={
        'value_list = []': '把每个项目整理成 `[利润, 启动资金]`',
        'value_list = sorted': '==按启动资金从小到大排序==：能启动的项目一定是数组的一段前缀',
        'heap = []': '堆维护==当前能启动的项目==的利润（Python 是小根堆，存负数）',
        'pos = 0': '`pos`：下一个还没进堆的项目',
        'for index in range(k)': lambda S, B, ret: (f'选第 `{S.index + 1}` 个项目（最多 {S.k} 个），当前资金 `W = {S.W}`'
                                                   if S.get('index') != B.get('index') or 'index' not in B else '已经做满 k 个项目'),
        'while pos < len': _while_cap,
        'heapq.heappush': '项目 `{value_list[pos]}` 入堆（存 `-{value_list[pos][0]}`），`pos` 后移',
        'if not heap': lambda S, B, ret: ('堆空了：没有能启动的项目 → ==提前结束==' if not S.heap else f'堆里有 {len(S.heap)} 个候选项目'),
        'break': '`break`',
        'W -= heapq.heappop': _pop_cap,
        'return W': '最终资本 =={ret}==',
    },
    cards=dict(
        one_liner='资金只增不减：按启动资金排序，能做的项目进堆，每次做利润最大的',
        complexity='时间 `O(n log n + k log n)`，空间 `O(n)`',
        problem=['初始资本 `w`，最多做 `k` 个项目；项目 `i` 要求资本 ≥ `capital[i]`，完成后得纯利润 `profits[i]`',
                 '求最终能获得的==最大资本==',
                 '示例：`k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]` → `4`',
                 '本视频：`k = 4, w = 0, profits = [3,1,8,2], capital = [1,0,10,1]` → `6`'],
        quote='随着项目的进行，我们手中的启动资金必然是单调递增的……==将项目按启动资金从小到大进行排序，那么每次可选择的项目必然是这个数组的前缀==，而我们需要从中选出收益最大的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次都选==当前能启动的项目中利润最大==的',
              '排序后能启动的项目是前缀；资金增加 → 前缀向右扩展',
              '需要“加入候选集 + 取最大值” → 用堆维护候选集'],
        summary=['排序 `O(n log n)`，每个项目最多入堆、出堆一次',
                 'Python 的 `heapq` 是小根堆：存 `-利润`，所以是 `W -= heappop(heap)`',
                 '易错：堆空时要 `break`，不能再 pop',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
