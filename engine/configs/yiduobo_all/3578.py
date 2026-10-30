def _cur(S):
    idx = len(S['f']) - (1 if S.get('_line', 0) >= 28 else 0)
    return min(idx, len(S['nums']) - 1)


def _w(S):
    if 'p' not in S or 'f' not in S:
        return ''
    nums, p = S['nums'], S['p']
    r = _cur(S)
    seg = nums[p:r + 1]
    if not seg:
        return ''
    return f'窗口 `nums[{p}..{r}]`：最大 `{max(seg)}` 最小 `{min(seg)}`（k = {S["k"]}）'


CONFIG = dict(
    num=3578, title='统计极差最大为 K 的分割方式数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分 DP + 前缀和 + 双堆懒删除',
    tags=['灵神题单·动态规划', '难度分 2033'],
    code='''
class Solution(object):
    def countPartitions(self, nums, k):
        
        f = [1]
        sf = [1, 2]
        ma_heap = [-nums[0]]
        mi_heap = [nums[0]]
        p = 0
        ma_remove = {}
        mi_remove = {}

        mod = 10 ** 9 + 7
        for v in nums[1:]:
            while (ma_heap and -ma_heap[0] - v > k) or (mi_heap and v - mi_heap[0] > k):
                ma_remove[nums[p]] = ma_remove.get(nums[p], 0) + 1
                mi_remove[nums[p]] = mi_remove.get(nums[p], 0) + 1
                p += 1
                while ma_heap and ma_remove.get(-ma_heap[0], 0) > 0:
                    ma_remove[-ma_heap[0]] -= 1
                    heapq.heappop(ma_heap)
                while mi_heap and mi_remove.get(mi_heap[0], 0) > 0:
                    mi_remove[mi_heap[0]] -= 1
                    heapq.heappop(mi_heap)

            heapq.heappush(ma_heap, -v)
            heapq.heappush(mi_heap, v)
            if p == 0:
                f.append(sf[-1])
            else:
                f.append((sf[-1] - sf[p - 1] + mod) % mod)
                
            sf.append(f[-1] + sf[-1])
            if sf[-1] >= mod:
                sf[-1] %= mod

        return f[-1]
''',
    call='Solution().countPartitions([9,4,1,3,7], 4)',
    expect=6,
    skip=['ma_remove = {}', 'mi_remove = {}', 'mod = 10', 'ma_remove[nums[p]]', 'mi_remove[nums[p]]', 'ma_remove[-ma_heap[0]] -= 1', 'mi_remove[mi_heap[0]] -= 1',
          'ma_heap = [', 'mi_heap = ['],
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 窗口，p = 最小合法左边界）', h=225, cell=80,
             pointers={'p': 'blue', 'min(len(f) - (_line >= 28), len(nums) - 1)': 'pink'}, pointer_labels={'min(len(f) - (_line >= 28), len(nums) - 1)': '右端点'}, window=('p', 'min(len(f) - (_line >= 28), len(nums) - 1)'),
             dim=lambda S, j, v: 'p' in S and 'f' in S and not (S['p'] <= j <= _cur(S))),
        dict(type='array', var='f', label='f（f[idx] = 前 idx+1 个数的合法分割数）', h=120, cell=70),
        dict(type='array', var='sf', label='sf（前缀和，sf[t] = 1 + f[0] + … + f[t-1]）', h=120, cell=70),
        dict(type='heap', var='ma_heap', label='ma_heap（存 −值，堆顶 = −最大值）', h=110, fmt=lambda x: f'{x}'),
        dict(type='heap', var='mi_heap', label='mi_heap（堆顶 = 最小值）', h=110, fmt=lambda x: f'{x}'),
    ],
    watch=[('v', 'v', 'pink'), ('p', 'p', 'blue'), ('k', 'k'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：只有 `nums[0]` 一个数，只有一种分法',
        'sf = [1, 2]': '`sf` 是前缀和：`sf[0] = 1`（空前缀算 1 种），`sf[1] = 1 + f[0] = 2`，后面区间求和用它',
        'p = 0': '`p` = 最小的合法左边界，右边界右移时 p 只增不减（变长滑动窗口）',
        'for v in nums[1:]': '新元素 `v = {v}` 作为右边界，要先把窗口收缩到合法',
        'while (ma_heap': lambda S, B, r: (f'最大 `{-S.ma_heap[0]}` − `v = {S.v}` = {-S.ma_heap[0] - S.v}，`v` − 最小 `{S.mi_heap[0]}` = {S.v - S.mi_heap[0]}，有一个 > k = {S.k} → ==窗口不合法，左边界要右移=='
                                           if (S.ma_heap and -S.ma_heap[0] - S.v > S.k) or (S.mi_heap and S.v - S.mi_heap[0] > S.k)
                                           else f'加入 `v = {S.v}` 后极差 ≤ k = {S.k} → 窗口合法，不用再收缩'),
        'p += 1': '`nums[p]` 离开窗口（在两个堆里做==懒删除==标记），`p` → {p}',
        'while ma_heap and ma_remove': lambda S, B, r: ('`ma_heap` 堆顶已被标记删除 → 真正弹出' if S.ma_heap and S.ma_remove.get(-S.ma_heap[0], 0) > 0 else '`ma_heap` 堆顶还在窗口里，停止清理'),
        'while mi_heap and mi_remove': lambda S, B, r: ('`mi_heap` 堆顶已被标记删除 → 真正弹出' if S.mi_heap and S.mi_remove.get(S.mi_heap[0], 0) > 0 else '`mi_heap` 堆顶还在窗口里，停止清理'),
        'heapq.heappop(ma_heap)': '弹出 `ma_heap` 堆顶（已过期的最大值）',
        'heapq.heappop(mi_heap)': '弹出 `mi_heap` 堆顶（已过期的最小值）',
        'heapq.heappush(ma_heap': '`v = {v}` 入两个堆（`ma_heap` 里存 `-v`）',
        'heapq.heappush(mi_heap': '`mi_heap` 同步加入 `{v}`',
        'if p == 0': lambda S, B, r: ('`p = 0`：左边界可以是 0，整段 `[0..idx]` 合法，`f[idx] = sf[-1]`（全部 f 之和）' if S.p == 0
                                    else f'`p = {S.p} > 0`：左边界 ≥ p，不能用 `f[0..p-2]` → 需要减去前缀 `sf[{S.p - 1}]`'),
        'f.append(sf[-1])': '`f[idx] = sf[-1]` = =={f[-1]}==',
        'f.append((sf[-1] - sf[p - 1]': '`f[idx] = sf[-1] − sf[p-1]` = `{B.sf[-1]} − {B.sf[p-1]}` = =={f[-1]}==（区间和，O(1)）',
        'sf.append(f[-1] + sf[-1])': '`sf` 追加 `f[-1] + sf[-1]` = {sf[-1]}，保持前缀和',
        'sf[-1] %= mod': '前缀和超过 `mod`，取模',
        'return f[-1]': '`f[-1]` = =={ret}== 种合法分割',
    },
    cards=dict(
        one_liner='右边界右移，左边界只增不减；转移是区间和，用前缀和 O(1)',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干连续非空子段，每段 ==最大值 − 最小值 ≤ k==，求方案数（模 `10^9+7`）',
                 '示例：`nums = [9,4,1,3,7], k = 4` → `6`',
                 '`nums` 长度可达 5×10^4，朴素 O(n^2) 不行'],
        quote='固定了子数组的右边界 index 后，对于某个合法的左边界 p，任意大于 p 的左边界 q 也是合法的……转移方程就变成 f[index] = f[p - 1] + f[p - 2] + ... + f[index - 1]。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举分割点 p：`nums[p..index]` 极差 ≤ k 就累加 `f[p-1]`',
              '合法左边界连续 → 变长滑动窗口，转移变成区间和 → ==前缀和==',
              '窗口最值：这份代码用==两个堆 + 懒删除==（也可用单调队列）'],
        summary=['时间 `O(n log n)`（堆），空间 `O(n)`；用单调队列可到 `O(n)`',
                 '易错：`p == 0` 时没有前缀可减，直接取 `sf[-1]`',
                 '易错：堆里最大值存的是 `-v`；删除用计数字典做懒删除',
                 '对比灵神：灵神用两个单调队列、`sum_f` 维护窗口和；这里是双堆 + 前缀和数组 `sf`'],
    ),
)
