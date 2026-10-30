import heapq as _hq

TASKS = ["A", "A", "A", "B", "B", "B"]
N = 2


def _rounds(tasks, n):
    """按原文算法预先模拟出每一轮执行了哪些任务（只用来画已完成的轮）"""
    d = {}
    for t in tasks:
        d[t] = d.get(t, 0) + 1
    h = [[-c, t] for t, c in d.items()]
    _hq.heapify(h)
    out = []
    while True:
        rt = []
        for _ in range(n + 1):
            if h:
                rt.append(_hq.heappop(h))
                rt[-1][0] += 1
        out.append([t for _, t in rt])
        for c, t in rt:
            if c < 0:
                _hq.heappush(h, [c, t])
        if not h:
            return out


ROUNDS = _rounds(TASKS, N)
SLOT_COLOR = {'A': 'blue', 'B': 'pink', 'C': 'purple', 'D': 'cyan'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    k = N + 1
    cv.text((x0 + 18, y0 + 4), f'时间线（每轮最多 n + 1 = {k} 个时间单位；虚线框 = 待命）', 24, T['muted'], bold=True)
    if 'res' not in S:
        return
    ln = S.get('_line', 0)
    cur = S['res'] // k              # 当前是第几轮（从 0 开始）
    finished = ln == 27              # return 那一步：最后一轮也结束了
    rt = S.get('round_task') or []
    sw, sh = 120, 56
    sx = x0 + 150
    for r in range(len(ROUNDS)):
        y = y0 + 50 + r * (sh + 18)
        if r > cur:
            break
        names = ROUNDS[r] if r < cur else [t for _, t in rt]
        last_round = r == len(ROUNDS) - 1
        cv.text((sx - 20, y + sh / 2), f'第 {r + 1} 轮', 22, T['yellow'] if r == cur and not finished else T['muted'],
                anchor='rm', bold=True)
        picking = r == cur and ln in (14, 17, 18)
        for s in range(k):
            X = sx + s * (sw + 8)
            if s < len(names):
                c = T[SLOT_COLOR.get(names[s], 'blue')]
                cv.rect((X, y, X + sw, y + sh), fill=c, r=10)
                cv.text((X + sw / 2, y + sh / 2), names[s], 28, T['bg'], anchor='mm', bold=True)
            elif not picking:
                if last_round and (r < cur or finished or not S.get('heap')):
                    cv.dashed((X, y + sh / 2), (X + sw, y + sh / 2), T['dim'], 2, 6, 6)
                    cv.text((X + sw / 2, y + sh / 2 - 14), '不用等', 18, T['dim'], anchor='mm')
                else:
                    for a, b in (((X, y), (X + sw, y)), ((X + sw, y), (X + sw, y + sh)),
                                 ((X + sw, y + sh), (X, y + sh)), ((X, y + sh), (X, y))):
                        cv.dashed(a, b, T['muted'], 2, 8, 6)
                    cv.text((X + sw / 2, y + sh / 2), '待命', 22, T['muted'], anchor='mm')
    total = S['res'] + (len(rt) if finished else 0)
    cv.text((x1 - 30, y0 + 50), f'res = {total}', 30, T['green'], anchor='ra', bold=True, mono=True)


def _fmt(x):
    return f'{x[1]}:{-x[0]}'


def _pop(S, B, ret):
    cnt, t = S.round_task[-1]
    if S.res == 0:
        return f'弹出堆顶 `{t}`（还剩 {-cnt} 个）：==优先做堆积最多的=='
    return f'弹出堆顶 `{t}`（还剩 {-cnt} 个）'


def _inc(S, B, ret):
    cnt, t = S.round_task[-1]
    return f'执行一次 `{t}`：`cnt` 加 1（存的是负数）→ 还剩 `{-cnt}` 个'


def _ifcnt(S, B, ret):
    if S.cnt < 0:
        return f'`{S.task}` 还剩 {-S.cnt} 个 → 放回堆里，下一轮再做'
    return f'`{S.task}` 已经做完 → 不再放回'


def _ifheap(S, B, ret):
    if S.heap:
        idle = N + 1 - len(S.round_task)
        tail = f'（其中 {idle} 个待命）' if idle else ''
        return f'堆里还有任务 → 这一轮占满 `n + 1 = {N + 1}` 个时间单位{tail}'
    return '堆空了 → ==这是最后一轮=='


CONFIG = dict(
    num=621, title='任务调度器', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按轮调度 · 每轮 n+1 个不同任务 + 大根堆',
    tags=['热题173'],
    code='''
import heapq

class Solution(object):
    def leastInterval(self, tasks, n):
        task_dict = {}
        for task in tasks:
            task_dict[task] = task_dict.get(task, 0) + 1

        heap = [[-cnt, task] for task, cnt in task_dict.items()]
        heapq.heapify(heap)

        res = 0
        while True:
            round_task = []
            for index in range(n + 1):
                if heap:
                    round_task.append(heapq.heappop(heap))
                    round_task[-1][0] += 1

            for cnt, task in round_task:
                if cnt < 0:
                    heapq.heappush(heap, [cnt, task])

            if heap:
                res += n + 1
            else:
                return res + len(round_task)
''',
    call=f'Solution().leastInterval({TASKS}, {N})',
    expect=8,
    skip=[6, 7, 'while True', 'for index in range', 16, 'for cnt, task in', 'heapq.heappush'],
    views=[
        dict(type='map', var='task_dict', label='task_dict（每种任务的个数）', h=100),
        dict(type='heap', var='heap', label='heap（任务:剩余个数）', fmt=_fmt, h=110),
        dict(type='queue', var='round_task', label='round_task（本轮选中的任务）', fmt=_fmt, h=110),
        dict(type='custom', draw=_draw, h=300),
    ],
    watch=[('n', 'n'), ('res', 'res', 'green')],
    captions={
        'task_dict = {}': '先数每种任务有几个',
        'heap = [[-cnt': '统计好了：`{task_dict}`；存 `[-cnt, task]` → 小根堆当==大根堆==用，堆顶剩得最多',
        'heapq.heapify': '建堆',
        'res = 0': '`res` 累计用掉的时间',
        'round_task = []': lambda S, B, r: (
            f'新的一轮：最多挑 `n + 1 = {S.n + 1}` 个==不同==的任务，轮与轮之间同一任务不会冲突' if S.res == 0
            else f'第 {S.res // (S.n + 1) + 1} 轮：再从堆顶挑至多 {S.n + 1} 个'),
        'round_task.append(heapq.heappop': _pop,
        'round_task[-1][0] += 1': _inc,
        'if cnt < 0': _ifcnt,
        'if heap:': _ifheap,
        'res += n + 1': '`res += n + 1` → `{res}`',
        'return res + len(round_task)': '最后一轮==不用补待命==，只算实际任务数：`{res} + {len(round_task)}` = =={ret}==',
    },
    cards=dict(
        one_liner='把调度粒度从“一个一个”变成“一组一组”：每轮 n+1 个不同任务',
        complexity='时间 `O(m log k)`，空间 `O(k)`（m 个任务，k ≤ 26 种）',
        problem=['`tasks` 是 CPU 要执行的任务（`A`–`Z`），每个时间单位完成一个任务或==待命==',
                 '两个==相同==任务之间至少间隔 `n` 个时间单位，求完成所有任务的最短时间',
                 '示例：`["A","A","A","B","B","B"], n = 2` → `8`',
                 '`A → B → 待命 → A → B → 待命 → A → B`'],
        quote='我们可以将执行任务的粒度由一个一个变成一组一组，即对于冷却时间n，==我们每轮选择执行n + 1个不同的任务==，那么组与组之间相同的任务就不存在冷却时间的问题。',
        quote_src='—— yiduobo 题解',
        idea=['只用堆按堆积数挑任务，会撞上冷却：刚做完的 A 可能还是最多的',
              '每轮从堆顶弹出至多 `n + 1` 个不同任务执行，次数减一后==统一放回==',
              '每轮耗时 `n + 1`；==最后一轮耗时是剩余的任务数=='],
        result='返回 `8` ✓：`AB待命 | AB待命 | AB`',
        summary=['时间 `O(m log k)`：每次弹堆执行一个任务；`k ≤ 26`，空间 `O(k)`',
                 '易错：本轮任务先全部弹出、做完再放回，否则同一轮可能选到同一个任务',
                 '易错：最后一轮不需要补满 `n + 1`，返回 `res + len(round_task)`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
