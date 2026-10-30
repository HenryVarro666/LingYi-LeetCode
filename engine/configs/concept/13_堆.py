def _nums_color(S, i, v):
    if 'cnt' not in S and 'h' in S:
        if v == S.get('x'):
            return 'pink'
        if v in S['h']:
            return 'green'
    if 'cnt' in S and v == S.get('x'):
        return 'pink'
    return None


def _formula(S):
    h = S.get('h')
    if h is None:
        return '堆：`O(log n)` 插入 / 弹出堆顶，`O(1)` 看最小值 `h[0]`'
    k = S['k']
    if 'cnt' in S:
        if len(h) == k:
            return f"堆里是频率最高的 {k} 个；堆顶频率 `{h[0][0]}`（数字 {h[0][1]}）是门槛"
        return f"堆还没满 {k} 个"
    if len(h) == k:
        return f"堆里是目前最大的 {k} 个数，堆顶 `h[0] = {h[0]}` ==就是第 {k} 大=="
    return f"堆还没满 {k} 个，来一个收一个"


CONFIG = dict(
    num=None, title='堆 · 通用思想与模板', author='概念讲解', category='堆',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def kth_largest(nums, k):            # 215. 第 k 大：维护最大的 k 个
    h = []                           # 小根堆，堆顶 = 这 k 个里最小的
    for x in nums:
        if len(h) < k:
            heappush(h, x)           # 不满 k 个，直接进堆
        elif x > h[0]:               # 比第 k 大还大
            heapreplace(h, x)        # 踢掉堆顶，换成 x
    return h[0]                      # 堆顶就是第 k 大

def top_k_frequent(nums, k):         # 347. 前 k 个高频元素
    cnt = Counter(nums)              # 先统计每个数出现几次
    h = []                           # 小根堆，元素是 (频率, 数)
    for x, c in cnt.items():
        if len(h) < k:
            heappush(h, (c, x))
        elif c > h[0][0]:            # 比堆里最低的频率还高
            heapreplace(h, (c, x))
    return sorted(x for _, x in h)
''',
    call='''
a = kth_largest([3, 2, 1, 5, 6, 4], 2)
b = top_k_frequent([1, 1, 1, 2, 2, 3, 4, 4, 4, 4], 2)
(a, b)
''',
    expect=(5, [1, 4]),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums（粉 = 当前的数，绿 = 在堆里）', color=_nums_color, cell=76, h=160),
        dict(type='heap', var='h', label='h', fmt=lambda e: f'{e[1]}出现{e[0]}次' if isinstance(e, tuple) else str(e),
             top_color='yellow', h=120),
        dict(type='map', var='cnt', label='cnt（模板② 先计数）', fmt=lambda a, b: f'{a}: {b}次', font=26, h=110),
    ],
    watch=[('x', 'x', 'pink'), ('c', 'c'), ('k', 'k'), ('h[0]', 'h[0] if h else None', 'yellow')],
    captions={
        'h = []                           # 小根堆，堆顶': '模板①：用 ==小根堆== 存「目前最大的 k 个数」，`k = {k}`',
        'for x in nums': lambda S, B, ret: (f'来了一个数 `x = {S.x}`' if B.get('x') != S.x else '所有数都看完了'),
        'if len(h) < k': lambda S, B, ret: (f'堆里只有 {len(S.h)} 个，不满 {S.k} 个' if len(S.h) < S.k
                                            else f'堆满了，看 `x` 能不能挤进前 {S.k}'),
        'heappush(h, x)': '`{x}` 直接进堆：`h = {h}`',
        'elif x > h[0]': lambda S, B, ret: (f'`{S.x} > 堆顶 {S.h[0]}`：它比当前第 {S.k} 大还大' if S.x > S.h[0]
                                            else f'`{S.x} ≤ 堆顶 {S.h[0]}`：进不了前 {S.k}，==直接丢掉=='),
        'heapreplace(h, x)': lambda S, B, ret: f'踢掉堆顶 `{B.h[0]}`、放入 `{S.x}`：`h = {S.h}`，`O(log k)`',
        'return h[0]': '答案：堆顶 `{ret}` 就是第 `{k}` 大',
        'cnt = Counter': '模板②：先用哈希表统计频率 → 问题变成「频率的 Top-K」',
        'h = []                           # 小根堆，元素是': '小根堆存 `(频率, 数)`：按频率比较',
        'for x, c in cnt': lambda S, B, ret: (f'数字 `{S.x}` 出现了 `{S.c}` 次' if (B.get('x'), B.get('c')) != (S.x, S.c)
                                              else '所有数字都看完了'),
        'heappush(h, (c, x))': '`({c}, {x})` 直接进堆',
        'elif c > h[0][0]': lambda S, B, ret: (f'频率 `{S.c} > 堆顶频率 {S.h[0][0]}` → 挤掉堆顶' if S.c > S.h[0][0]
                                               else f'频率 `{S.c} ≤ 堆顶频率 {S.h[0][0]}` → 进不了前 {S.k}'),
        'heapreplace(h, (c, x))': lambda S, B, ret: f'踢掉 `{B.h[0]}`，放入 `({S.c}, {S.x})`',
        'return sorted': '前 `{k}` 个高频元素：`{ret}`，时间 `O(n log k)`',
    },
    cards=dict(
        one_liner='要反复拿最大 / 最小值，就用堆；Top-K 大用大小为 k 的小根堆',
        complexity='Top-K：时间 `O(n log k)`，空间 `O(k)`',
        problem_heading='什么时候用？',
        problem=['第 k 大 / 前 k 个（Top-K）→ 大小为 k 的小根堆',
                 '数据是 ==流==，要随时取最大、最小或中位数 → 堆',
                 '反复「取出最小的，再放回新的」→ 合并 K 个链表（23）',
                 '只要第 k 个、不需要整体有序 → 快速选择，期望 `O(n)`'],
        before=[dict(heading='核心概念：小根堆维护「最大的 k 个」', lines=[
            '堆：`O(log n)` 插入、弹出堆顶，`O(1)` 看最小值 `h[0]`',
            '维护最大的 k 个用 ==小根堆==：堆顶是这 k 个里最小的 = 第 k 大',
            '新数比堆顶大 → `heapreplace` 踢掉堆顶；否则它进不了前 k',
            'Python 只有小根堆：要最大堆就存相反数 `-x`']),
        ],
        idea_heading='两位作者怎么说',
        quote='维护一个==大小为 k 的小根堆==，key 为元素出现的频率。接下来一趟扫描，对于每个元素，如果其频率大于堆顶元素的频率，那么将堆顶元素弹出，并将当前元素加入到堆中。最后堆中所剩元素即为最后答案。',
        quote_src='—— yiduobo · 347. 前 K 个高频元素',
        idea=['灵神 295 从中位数定义出发：左最大堆 + 右最小堆，==中位数来自两个堆顶==',
              '灵神 215 / 347 给的是 `O(n)` 的快速选择、桶排序；堆是通用的 `O(n log k)`',
              'yiduobo 215：快排分割后，==第 k 大只会在其中一边==，只递归那一边'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`215` 第 K 个最大元素：大小为 k 的小根堆 / 快速选择',
                 '`347` 前 K 个高频元素：先计数，再对频率做 Top-K（或桶排序）',
                 '`295` 数据流的中位数：左最大堆 + 右最小堆，看两个堆顶',
                 '进阶：`23` 合并 K 个升序链表（链表类）也是最小堆',
                 '易错：Top-K 大要用 ==小根堆==；Python 的最大堆要存 `-x`'],
    ),
)
