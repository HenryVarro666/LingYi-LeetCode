N, PRIMES = 6, [2, 3]


def _ugly(n, primes):
    out, seen = [1], {1}
    import heapq as hq
    h = [1]
    while len(out) < n + 1:
        x = hq.heappop(h)
        for p in primes:
            if x * p not in seen:
                seen.add(x * p)
                hq.heappush(h, x * p)
        if x != 1:
            out.append(x)
    return out


UG = _ugly(N, PRIMES)   # UG[k]：第 k+1 个超级丑数（UG[0] = 1）


def _popped(S):
    """已经弹出的超级丑数个数（不含 1）"""
    return S['step'] if 'now' in S else 0   # 第 15 行（for step）被跳过，step 一变就紧跟着 heappop


def _draw_queues(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '候选队列 candidate_list（灰 = 已进过堆，黄框 = 正在堆里，绿 = 刚加入）', 22, T['muted'], bold=True)
    cl = S.get('candidate_list')
    if cl is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    pos = S.get('pos_list') or [0] * len(cl)
    bcl = B.get('candidate_list') or [[] for _ in cl]
    heap_items = set(S.get('heap') or [])
    cell = 74
    for k, q in enumerate(cl):
        y = y0 + 48 + k * 86
        cv.text((x0 + 24, y + 26), f'q{k}（×{PRIMES[k]}）', 24, T['cyan'], anchor='lm', bold=True)
        sx = x0 + 160
        if not q:
            cv.text((sx, y + 26), '空', 22, T['dim'], anchor='lm')
        for t, v in enumerate(q):
            X = sx + t * cell
            if X + cell > x1 - 10:
                cv.text((X, y + 26), '…', 24, T['muted'], anchor='lm')
                break
            new = t >= len(bcl[k])
            in_heap = (v, k) in heap_items
            used = t < pos[k] and not in_heap
            fill = T['green'] if new else ((44, 50, 60) if used else T['panel2'])
            cv.rect((X + 4, y, X + cell - 4, y + 52), fill=fill, r=10,
                    outline=T['yellow'] if in_heap else T['border'], width=4 if in_heap else 1)
            cv.text((X + cell / 2, y + 26), v, 26, T['bg'] if new else (T['dim'] if used else T['text']), anchor='mm', bold=True)


def _draw_seq(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    k = _popped(S)
    cv.text((x0 + 18, y0 + 4), f'超级丑数（按从小到大弹出；要第 n = {N} 个）', 22, T['muted'], bold=True)
    cell = 74
    for t in range(N):
        X = x0 + 24 + t * cell
        known = t <= k
        last = t == k and k > 0 and S['_line'] in (16, 27)
        fill = T['orange'] if last else ((52, 60, 72) if known else T['panel2'])
        cv.rect((X + 4, y0 + 40, X + cell - 4, y0 + 92), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, y0 + 66), UG[t] if known else '?', 26, T['bg'] if last else (T['text'] if known else T['dim']),
                anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 98), f'第{t + 1}个', 16, T['dim'], anchor='mt')


def _cap_pop(S, B, ret):
    return (f'弹出堆顶 `({S.now}, {S.candidate_index})`：==当前最小==的候选就是第 {S.step + 1} 个超级丑数 `{S.now}`'
            f'（来自 q{S.candidate_index}）')


def _cap_if_used(S, B, ret):
    v = S.prime * S.now
    if v in B.used:
        return f'`{S.prime} × {S.now} = {v}` 之前已经生成过 → ==去重==，跳过'
    return f'`{S.prime} × {S.now} = {v}` 是新数'


CONFIG = dict(
    num=313, title='超级丑数', difficulty='Medium', category='堆',
    author='yiduobo', technique='多路队列 + 堆取最小',
    tags=['字节30天'],
    code='''
class Solution(object):

    def nthSuperUglyNumber(self, n, primes):
        if n == 1:
            return 1

        heap = []
        for index, prime in enumerate(primes):
            heappush(heap, (prime, index))

        candidate_list = [[] for _ in range(len(primes))]
        pos_list = [0] * len(primes)
        used = set()

        for step in range(1, n):
            now, candidate_index = heappop(heap)
            for index, prime in enumerate(primes):
                next_candidate = prime * now
                if next_candidate not in used:
                    used.add(next_candidate)
                    candidate_list[index].append(next_candidate)

            if pos_list[candidate_index] < len(candidate_list[index]):
                heappush(heap, (candidate_list[candidate_index][pos_list[candidate_index]], candidate_index))
                pos_list[candidate_index] += 1

        return now
''',
    call=f'Solution().nthSuperUglyNumber({N}, {PRIMES})',
    expect=8,
    skip=['for index, prime in enumerate', 'next_candidate = prime * now', 'used.add', 'pos_list[candidate_index] += 1',
          'for step in range', 'pos_list = [0]', 'used = set()'],
    views=[
        dict(type='heap', var='heap', label='heap（每个队列的队首：值, 队列号）', fmt=lambda t: f'{t[0]}, q{t[1]}', h=118),
        dict(type='custom', draw=_draw_queues, h=230),
        dict(type='custom', draw=_draw_seq, h=140),
        dict(type='set', var='used', label='used（生成过的数，用来去重）', h=100),
    ],
    watch=[('step', 'step'), ('now', 'now', 'orange'), ('candidate_index', 'candidate_index', 'cyan'), ('pos_list', 'pos_list')],
    captions={
        'if n == 1': '`n = {n}`，不是 1（第 1 个超级丑数就是 1）',
        'heappush(heap, (prime, index))': '质数 `{prime}` 本身作为 q{index} 的第一个候选放进堆（它就是 `{prime} × 1`）',
        'heap = []': '堆里只放每个队列的==队首==：`(值, 队列下标)`',
        'candidate_list = ': '每个质数一个候选队列：q0 存 `2 × 丑数`，q1 存 `3 × 丑数`…（`pos_list` 记每个队列进堆到第几个，`used` 去重）',
        'now, candidate_index = heappop': _cap_pop,
        'if next_candidate not in used': _cap_if_used,
        'candidate_list[index].append': lambda S, B, r: (f'`{S.next_candidate}` 加入 q{S.index} 队尾'
                                                         + ('（队列内部天然递增）' if sum(map(len, S.candidate_list)) == 1 else '')),
        'if pos_list[candidate_index] <': lambda S, B, r: (f'q{S.candidate_index} 还有下一个候选吗？'
                                                           + ('（实测这个判断总成立）' if S.step == 1 else '')),
        'heappush(heap, (candidate_list': lambda S, B, r: (f'把 q{S.candidate_index} 的下一个 `{S.candidate_list[S.candidate_index][B.pos_list[S.candidate_index]]}` '
                                                          f'推进堆，补上它的队首'),
        'return now': '第 {n} 个超级丑数是 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='每次取出最小的丑数，乘上每个质数放进对应队列，堆里比较各队列的队首',
        complexity='时间 `O(nk)`（每轮 k 次乘法；取最小用堆是 `O(log k)`），空间 `O(nk)`',
        problem=['超级丑数：质因数==全部==出自数组 `primes` 的正整数（1 也算）',
                 '求第 `n` 个超级丑数',
                 '示例：`n = 12, primes = [2,7,13,19]` → `32`',
                 '本视频：`n = 6, primes = [2,3]` → 序列 `1,2,3,4,6,8`，答案 `8`'],
        quote='每次取出当前最小的丑数，然后分别与primes中的元素相乘，得到的结果==去重后分别加入对应的队列==，然后从各个队列的队首选取最小的一个重复上述步骤直到产生出第n个超级丑数为止。',
        quote_src='—— yiduobo 题解原文（沿用 264 丑数 II 的做法）',
        idea=['大丑数 = 某个小丑数 × 某个质数，所以按从小到大的顺序「生成」',
              '每个质数一个队列，队列内部天然递增 → 全局最小一定在==某个队首==',
              '堆里只放各队首：弹出最小值，再把同一队列的下一个补进堆'],
        summary=['时间 `O(nk)`，空间 `O(nk)`',
                 '易错：`6 = 2×3 = 3×2` 会被生成两次，必须用 `used` 去重',
                 '读代码注意：判断里的 `candidate_list[index]` 用的是内层循环残留的 `index`；实测这个条件总成立，不影响结果',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
