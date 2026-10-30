Q = [4, 8, 2, 6, 3, 5, 9]
W = [8, 8, 6, 9, 12, 15, 45]
K = 3
PAIRS = sorted(zip(Q, W), key=lambda d: d[1] * 1.0 / d[0])


def _g(x):
    return f'{x:g}' if isinstance(x, float) else str(x)


def _table(S):
    if 'heap' not in S:
        return None
    return [[q for q, _ in PAIRS], [w for _, w in PAIRS], [_g(round(w / q, 2)) for q, w in PAIRS]]


def _color(S, i, j, v):
    h = S.get('heap')
    if h is None:
        return None
    if -PAIRS[j][0] in h:
        return 'green'
    return None


def _idx(S):
    return S.get('index')


def _formula(S, B):
    if 'index' not in S:
        return '按 `w / q`（单位质量的价格）从小到大排序后依次遍历'
    q, w = S['q'], S['w']
    r = S.get('res')
    rs = '尚无' if r is None else _g(round(r, 3))
    return f"当前工人 `w/q = {w}/{q} = {_g(round(w / q, 3))}` 作为工资标准　`sum_q = {S['sum_q']}`　`res = {rs}`"


def _cap_if(S, B, ret):
    i, q, w = S.index, S.q, S.w
    cost = w * 1.0 / q * S.sum_q
    if i < K - 1:
        return (f'`index = {i} < K − 1`：还凑不够 {K} 个人 → 不更新答案'
                + ('（补上的 `res is not None` 防止 Python 3 里 None 和数比较报错）' if i == 0 else ''))
    if B.res is None:
        return f'第一次凑够 {K} 人：`res` 为空 → 直接记录 `{_g(round(cost, 3))}`'
    if B.res > cost:
        return f'`{w}/{q} × {S.sum_q} = {_g(round(cost, 3))} < res = {_g(round(B.res, 3))}` → ==更新=='
    return f'`{w}/{q} × {S.sum_q} = {_g(round(cost, 3))} ≥ res = {_g(round(B.res, 3))}` → 不更新'


CONFIG = dict(
    num=857, title='雇佣 K 名工人的最低成本', difficulty='Hard', category='堆',
    author='yiduobo', technique='按 w/q 排序 · 取相反数的小根堆做 topK',
    tags=['字节30天'],
    code='''
class Solution(object):
    def mincostToHireWorkers(self, quality, wage, K):
        heap = []
        sum_q = 0
        res = None
        for index, (q, w) in enumerate(sorted(zip(quality, wage), key=lambda d:d[1]* 1.0 / d[0])):
            sum_q += q
            if len(heap) == K:
                sum_q += heapq.heappop(heap)
            if index >= K - 1 and res is None or res is not None and res > w * 1.0 / q * sum_q:
                res = w * 1.0 / q * sum_q
            heapq.heappush(heap, -q)

        return res
''',
    call=f'Solution().mincostToHireWorkers({Q}, {W}, {K})',
    expect=33.0,
    result_fn=lambda x: round(x, 5),
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var=_table, label='工人按 w/q 排序（绿 = 在堆里的工人；黄框 = 当前工人 index）',
             rows=['q', 'w', 'w/q'], cell=92, h=330, color=_color,
             cursors=[(lambda S: 0, _idx, 'yellow'), (lambda S: 1, _idx, 'yellow'), (lambda S: 2, _idx, 'yellow')]),
        dict(type='heap', var='heap', label='heap：存 -q 的小根堆（堆顶 = q 最大的工人）', h=120),
    ],
    watch=[('index', 'index', 'yellow'), ('sum_q', 'sum_q', 'green'),
           ('res', lambda S: (round(S['res'], 4) if S.get('res') is not None else None) if 'res' in S else '·', 'orange')],
    captions={
        'heap = []': '`heap`：已遍历工人里 q 最小的那些（存相反数，模拟大根堆）',
        'sum_q = 0': '`sum_q`：当前选中工人的 q 之和',
        'res = None': '`res = None`：还没有答案',
        'for index, (q, w)': lambda S, B, ret: (f'第 `{S.index}` 位工人 `(q={S.q}, w={S.w})`：前面的人都按他的 `w/q` 换算工资'
                                                if S.get('index') is not None and S.index != B.get('index') else '遍历结束'),
        'sum_q += q': '1、`sum_q` 加上当前工人的 `q` → `{sum_q}`',
        'if len(heap) == K': lambda S, B, ret: (f'2、堆里已有 `K = {K}` 人，加上当前工人超过 K 位 → 要踢掉一个'
                                                if len(S.heap) == K else f'2、堆里只有 `{len(S.heap)}` 人，不用踢人'),
        'sum_q += heapq.heappop(heap)': lambda S, B, ret: (f'弹出 q 最大的工人 `{-B.heap[0]}`（堆里存的是 `{B.heap[0]}`）：'
                                                           f'`sum_q += {B.heap[0]}` → `{S.sum_q}`'),
        'if index >= K - 1': _cap_if,
        'res = w * 1.0': lambda S, B, ret: f'3、用 `w[index] / q[index] × sum_q` 更新答案：`res = {_g(round(S.res, 3))}`',
        'heapq.heappush(heap, -q)': '4、把当前工人的 `-q = {-q}` 加入堆',
        'return res': lambda S, B, ret: f'最低成本 =={_g(round(ret, 5))}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='按单位质量价格排序，用堆从前面的人里选 q 最小的 K 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 名工人，`quality[i]` 是工作质量，`wage[i]` 是最低期望工资；雇 `K` 名',
                 '规则：工资==按质量比例==支付，且每人至少拿到自己的最低期望工资；求最小总金额',
                 '示例：`quality = [10,20,5]`，`wage = [70,50,30]`，`K = 2` → `105`'],
        quote='需要将==单位工作质量价格最高的工人作为工资标准==……就是 max(w_per_q) * sumq。……这里就出现了一个topK的问题，可以使用堆来解决。',
        quote_src='—— yiduobo 题解',
        idea=['一组工人的总工资 = `max(w/q) × sumq`',
              '按 `w/q` 排序后，第 index 位工人是前 index+1 人的工资标准',
              '再从中选 q 最小的 K 位让 `sumq` 最小 → topK，用堆'],
        result='运行结束：返回 `33` ✓',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先把当前工人算进 `sum_q`，再从==之前的 K 人==里踢掉 q 最大的：当前工人是工资标准，必须留下',
                 'Python 只有小根堆：存 `-q` 就得到 q 的大根堆，弹出后 `sum_q += 负数` 即减去它',
                 '原文依赖 Python 2 的 `None > 数` 为 False，这里补上 `res is not None and`；并删去 docstring',
                 '对比灵神：灵神先放入前 K 人再比较堆顶，yiduobo 每人都入堆再弹出'],
    ),
)
