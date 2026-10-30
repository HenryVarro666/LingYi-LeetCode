CONFIG = dict(
    num=2462, title='雇佣 K 位工人的总代价', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='两个最小堆模拟',
    tags=['堆（优先队列）', '难度分 1764'],
    code='''
class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
        n = len(costs)
        if candidates * 2 + k > n:
            # 也可以 sum(nsmallest(k, costs))，但效率不如直接排序
            costs.sort()
            return sum(costs[:k])

        pre = costs[:candidates]
        suf = costs[-candidates:]
        heapify(pre)
        heapify(suf)

        ans = 0
        i = candidates
        j = n - 1 - candidates
        for _ in range(k):
            if pre[0] <= suf[0]:
                ans += heapreplace(pre, costs[i])
                i += 1
            else:
                ans += heapreplace(suf, costs[j])
                j -= 1
        return ans
''',
    call='Solution().totalCost([17,12,10,2,7,2,11,20,8,5,9], 3, 3)',
    expect=22,
    views=[
        dict(type='text', fn=lambda S: (f"前堆堆顶 `{S['pre'][0]}`　后堆堆顶 `{S['suf'][0]}`　已雇总代价 =={S.get('ans', 0)}==" if 'suf' in S and S['pre'] and S['suf'] else '')),
        dict(type='array', var='costs', pointers={'i': 'blue', 'j': 'pink'}, h=220, label='costs（i = 前面下一个入堆，j = 后面下一个入堆）'),
        dict(type='heap', var='pre', h=140, label='pre：最前面 candidates 个'),
        dict(type='heap', var='suf', h=140, label='suf：最后面 candidates 个'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green'), ('k', 'k', 'purple')],
    captions={
        'if candidates * 2 + k > n': '`{candidates}×2 + {k} = {candidates*2+k}` 与 `n = {n}` 比较：不大于 n → 前后候选区不会重叠，走堆模拟',
        'pre = costs[:candidates]': '前 `candidates` 个工人先放进 `pre`',
        'suf = costs[-candidates:]': '后 `candidates` 个工人先放进 `suf`',
        'heapify(pre)': '`pre` 原地建成最小堆',
        'heapify(suf)': '`suf` 原地建成最小堆',
        'i = candidates': '`i = {i}`：前面下一个要补进堆的下标',
        'j = n - 1': '`j = {j}`：后面下一个要补进堆的下标',
        'for _ in range(k)': '雇佣一轮（共 `{k}` 轮）',
        'if pre[0] <= suf[0]': lambda S, B, r: (f'`pre[0] = {S.pre[0]} <= suf[0] = {S.suf[0]}` → 成立：前面更便宜（相等取下标小的，即前面）' if S.pre[0] <= S.suf[0]
                                                else f'`pre[0] = {S.pre[0]} > suf[0] = {S.suf[0]}` → 后面严格更便宜'),
        'ans += heapreplace(pre': lambda S, B, r: f'弹出前堆顶 `{S.ans - B.ans}` 雇佣，同时把 `costs[{B.i}] = {S.costs[B.i]}` 补入前堆：`ans = {S.ans}`',
        'i += 1': '`i` 右移到 {i}',
        'ans += heapreplace(suf': lambda S, B, r: f'弹出后堆顶 `{S.ans - B.ans}` 雇佣，同时把 `costs[{B.j}] = {S.costs[B.j]}` 补入后堆：`ans = {S.ans}`',
        'j -= 1': '`j` 左移到 {j}',
        'return ans': '雇佣完 `k` 人，总代价 `{ans}`',
    },
    cards=dict(
        one_liner='前后各一个最小堆，每轮取更便宜的一边并补位',
        complexity='时间 `O((c+k) log (c+k))`，空间 `O(c)`',
        problem=['共 `k` 轮，每轮从最前 `candidates` 和最后 `candidates` 个工人里选代价最小的（并列取下标小的）',
                 '示例：`costs=[17,12,10,2,7,2,11,20,8]`，`k=3`，`candidates=4` → `11`',
                 '本视频：`[17,12,10,2,7,2,11,20,8,5,9]`，`k=3`，`candidates=3` → `22`'],
        quote='雇佣过程可以用两个最小堆来模拟，一个负责维护 costs 剩余数字的最前面 candidates 个数的最小值，另一个负责维护最后面 candidates 个数的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pre` 管前 `c` 个，`suf` 管后 `c` 个',
              '每轮比两个堆顶：`pre[0] <= suf[0]` 取前面（并列取下标小的）',
              '用 `heapreplace` 弹出堆顶并补入下一个，`i`、`j` 向中间靠拢'],
        summary=['时间 `O((c+k) log (c+k))`，空间 `O(c)`',
                 '易错点：`candidates*2 + k > n` 时前后会重叠，直接排序取前 k 小',
                 '易错点：比较用 `<=`，并列时前面下标更小',
                 '这个判断保证 `i` 与 `j` 不会交叉，补位不会重复'],
    ),
)
