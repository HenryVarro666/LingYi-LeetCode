Q = [4, 8, 2, 6, 3, 5, 9]
W = [8, 8, 6, 9, 12, 15, 45]
K = 3
PAIRS = sorted(zip(Q, W), key=lambda p: p[1] / p[0])


def _g(x):
    return f'{x:g}' if isinstance(x, float) else str(x)


def _col(S):
    """当前枚举到的工人在 PAIRS 中的下标"""
    if 'q' in S and 'w' in S and (S['q'], S['w']) in PAIRS:
        return PAIRS.index((S['q'], S['w']))
    if 'ans' in S:
        return K - 1
    return None


def _table(S):
    if 'pairs' not in S:
        return None
    return [[q for q, _ in PAIRS], [w for _, w in PAIRS], [_g(round(w / q, 2)) for q, w in PAIRS]]


def _color(S, i, j, v):
    h = S.get('h')
    if h is None:
        return None
    if PAIRS[j][0] in h and j <= (_col(S) if _col(S) is not None else K - 1):
        return 'green'
    c = _col(S)
    if c is not None and j < c:
        return None
    return None


def _formula(S, B):
    if 'ans' not in S:
        if 'sum_q' in S:
            return f"`sum_q = {S['sum_q']}`"
        return '按 `r = wage / quality` 从小到大排好序'
    c = _col(S)
    q, w = PAIRS[c]
    return f"当前基准 `r = {w}/{q} = {_g(round(w / q, 3))}`　堆中 quality 之和 `sum_q = {S['sum_q']}`　`ans = {_g(round(S['ans'], 3))}`"


CONFIG = dict(
    num=857, title='雇佣 K 名工人的最低成本', difficulty='Hard', category='堆',
    author='灵茶山艾府', technique='按 r 排序 + 最大堆维护最小的 k 个 quality',
    tags=['字节30天'],
    code='''
class Solution:
    def mincostToHireWorkers(self, quality: List[int], wage: List[int], k: int) -> float:
        pairs = sorted(zip(quality, wage), key=lambda p: p[1] / p[0])  # 按照 r 值排序

        h = [q for q, _ in pairs[:k]]  # 最大堆
        heapify_max(h)

        sum_q = sum(h)
        ans = sum_q * pairs[k - 1][1] / pairs[k - 1][0]  # 选 r 值最小的 k 名工人
        for q, w in pairs[k:]:  # 后面的工人 r 值更大
            if q < h[0]:  # 但是 sum_q 可以变小，从而可能得到更优的答案
                sum_q -= heapreplace_max(h, q) - q  # 更新堆顶和 sum_q
                ans = min(ans, sum_q * w / q)
        return ans
''',
    # heapify_max / heapreplace_max 是 Python 3.14 新增的公开函数；这里的 Python 3.13 用 heapq 里同名的内部实现代替
    setup='heapify_max = heapq._heapify_max\nheapreplace_max = heapq._heapreplace_max',
    call=f'Solution().mincostToHireWorkers({Q}, {W}, {K})',
    expect=33.0,
    result_fn=lambda x: round(x, 5),
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var=_table, label='工人按 r 排序（绿 = 在堆里，即当前选中的 k 人；黄框 = 当前枚举的 r 基准）',
             rows=['q', 'w', 'r'], cell=92, h=330, color=_color,
             cursors=[(lambda S: 0, _col, 'yellow'), (lambda S: 1, _col, 'yellow'), (lambda S: 2, _col, 'yellow')]),
        dict(type='heap', var='h', label='h：最大堆（存 quality，堆顶最大）', h=120),
    ],
    watch=[('sum_q', 'sum_q', 'green'), ('ans', lambda S: round(S['ans'], 4) if 'ans' in S else None, 'orange')],
    captions={
        'pairs = sorted': '按照 `r = wage / quality` 排序：r 不超过基准的工人==都可以随意雇佣==',
        'h = [q for q': '先选 r 值最小的 `k = {k}` 名工人，把 quality 放进堆',
        'heapify_max(h)': '建==最大堆==：堆顶 `{h[0]}` 是选中的人里 quality 最大的',
        'sum_q = sum(h)': '`sum_q = {sum_q}`',
        'ans = sum_q * pairs': lambda S, B, ret: (f'以第 `k` 人的 `r = {PAIRS[K - 1][1]}/{PAIRS[K - 1][0]}` 为基准：'
                                                  f'`ans = {S.sum_q} × {_g(round(PAIRS[K - 1][1] / PAIRS[K - 1][0], 3))} = {_g(round(S.ans, 3))}`'),
        'for q, w in pairs[k:]': lambda S, B, ret: (f'枚举下一个工人 `(q={S.q}, w={S.w})` 作为 r 基准（r 值更大）'
                                                    if S.get('q') is not None and (S.q, S.w) != (B.get('q'), B.get('w')) else '枚举结束'),
        'if q < h[0]': lambda S, B, ret: (f'`q = {S.q} < 堆顶 {S.h[0]}`：换掉堆顶，==sum_q 可以变小== → 可能更优'
                                          if S.q < S.h[0] else f'`q = {S.q} ≥ 堆顶 {S.h[0]}`：换进来 sum_q 只会变大，r 也更大 → 跳过'),
        'sum_q -= heapreplace_max': lambda S, B, ret: (f'弹出堆顶 `{B.h[0]}`、放入 `{S.q}`：`sum_q -= {B.h[0]} − {S.q}` → `{S.sum_q}`'),
        'ans = min(ans': lambda S, B, ret: (f'`sum_q × r = {S.sum_q} × {S.w}/{S.q} = {_g(round(S.sum_q * S.w / S.q, 3))}` → '
                                            f'`ans = {_g(round(S.ans, 3))}`' + ('（==更新==）' if S.ans < B.ans else '')),
        'return ans': lambda S, B, ret: f'最低成本 =={_g(round(ret, 5))}==',
    },
    cards=dict(
        one_liner='枚举谁拿最低工资（r 基准），堆里留 quality 最小的 k 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 名工人，`quality[i]` 是工作质量，`wage[i]` 是最低期望工资；雇 `k` 名',
                 '规则：工资==按质量比例==支付，且每人至少拿到自己的最低期望工资；求最小总金额',
                 '示例：`quality = [10,20,5]`，`wage = [70,50,30]`，`k = 2` → `105`'],
        before=[dict(heading='一步步提示', lines=[
            '定理：最优方案里==至少有一人恰好拿到最低期望工资==（否则可以全体下调）',
            '设 `r = wage / quality`；以某人的 r 为基准，r 不超过它的工人都满足规则 2',
            '总工资 = `sum_q × r`：r 固定时，要让 `sum_q` 尽量小',
        ])],
        quote='按照 r 从小到大的顺序遍历工人，当堆中有 k 个元素时，==如果 quality_i 比堆顶小，则可以弹出堆顶，将 quality_i 入堆==，从而得到一个更小的 sumQ。',
        quote_src='—— 灵茶山艾府题解（提示 5）',
        idea=['按 r 从小到大枚举基准，前面的人都能雇',
              '用==最大堆==维护当前最小的 k 个 quality：比堆顶小就替换',
              '每次替换后用 `sum_q × r` 更新答案'],
        result='运行结束：返回 `33` ✓（雇 q = 2、5、4 三人，以 r = 3 为基准）',
        summary=['时间 `O(n log n)`（排序），堆操作 `O(n log k)`；空间 `O(n)`',
                 '`heapify_max` / `heapreplace_max` 是 Python 3.14 新增函数，本视频环境用 heapq 内部同名实现代替',
                 '`q ≥ 堆顶` 时可以直接跳过：sum_q 不会变小，r 又更大',
                 '易错：答案是浮点数，`p[1] / p[0]` 用真除法'],
    ),
)
