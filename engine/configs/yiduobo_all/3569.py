def _isp(v):
    return v > 1 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _eff(S):
    """分割点 0..n-2 当前真实的答案（把祖先的 delta 累加起来，不改动树）"""
    f, dl, n = S.get('f'), S.get('delta'), S.get('n')
    if f is None or dl is None or not n or n < 2:
        return []
    out = [0] * (n - 1)

    def go(p, l, r, add):
        if l == r:
            out[l] = f[p] + dl[p] + add
            return
        m = (l + r) >> 1
        go(p * 2 + 1, l, m, add + dl[p])
        go(p * 2 + 2, m + 1, r, add + dl[p])
    try:
        go(0, 0, n - 2, 0)
    except Exception:
        pass
    return out


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, dl, n = S.get('f'), S.get('delta'), S.get('n')
    cv.text((x0 + 18, y0 + 4), '线段树：f(区间最大，不含自己的 delta) / delta(整段加的量)', 22, T['muted'], bold=True)
    if f is None or dl is None or not n or n < 2 or 'ori' not in S:
        return
    Bf, Bd = B.get('f'), B.get('delta')
    m = n - 1
    pos = {}
    gap = min(100, (y1 - y0 - 110) / max(1, (m - 1).bit_length()))

    def lay(p, l, r, d, lo, hi):
        pos[p] = ((lo + hi) / 2, y0 + 70 + d * gap, l, r, hi - lo)
        if l == r:
            return
        mid = (l + r) >> 1
        c = (lo + hi) / 2
        lay(p * 2 + 1, l, mid, d + 1, lo, c)
        lay(p * 2 + 2, mid + 1, r, d + 1, c, hi)

    lay(0, 0, m - 1, 0, x0 + 10, x1 - 10)
    for p, (cx, cy, l, r, ww) in pos.items():
        for c in (p * 2 + 1, p * 2 + 2):
            if c in pos:
                cv.line([(cx, cy + 28), (pos[c][0], pos[c][1] - 28)], T['border'], 2)
    for p, (cx, cy, l, r, ww) in pos.items():
        ch = Bf is not None and Bd is not None and p < len(Bf) and (Bf[p], Bd[p]) != (f[p], dl[p])
        w = min(140, ww * 0.9)
        cv.rect((cx - w / 2, cy - 28, cx + w / 2, cy + 28), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=8)
        cv.text((cx, cy - 24), f'[{l},{r}]', 16, T['dim'], anchor='mt', mono=True)
        cv.text((cx, cy), f'{f[p]} / {dl[p]}', 22, T['text'], anchor='mt', bold=True, mono=True)


CONFIG = dict(
    num=3569, title='分割数组后不同质数的最大数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='差分建初值 + 懒更新线段树 + 双堆维护最左/最右',
    tags=['灵神题单', '常用数据结构', '难度分 2697'],
    code='''
class Solution(object):
    def maximumCount(self, nums, queries):
        
        ma = 10
        prime = [True] * (ma + 1)
        prime[1] = False

        for v in range(2, ma + 1):
            if prime[v]:
                for x in range(v + v, ma + 1, v):
                    prime[x] = False

        first = {}
        last = {}
        n = len(nums)
        for index, v in enumerate(nums):
            if prime[v]:
                if v not in first:
                    first[v] = [index]
                    last[v] = [-index]
                else:
                    heapq.heappush(first[v], index)
                    heapq.heappush(last[v], -index)

        d = [0] * n
        for v in first:
            d[first[v][0]] += 1
            d[-last[v][0]] -= 1

        cnt = len(first)
        f = [0] * (n * 4)
        delta = [0] * (n * 4)
        ori = [0] * n

        def build(now, left, right):
            if left == right:
                f[now] = ori[left]
                return
            
            mid = (left + right) >> 1
            left_child = now + now + 1
            right_child = now + now + 2
            build(left_child, left, mid)
            build(right_child, mid + 1, right)
            f[now] = max(f[left_child], f[right_child])

        def update(now, left, right, start, end, v):
            if left == start and right == end:
                delta[now] += v
                return
            
            left_child = now + now + 1
            right_child = now + now + 2

            mid = (left + right) >> 1
            if end <= mid:
                update(left_child, left, mid, start, end, v)
            elif start > mid:
                update(right_child, mid + 1, right, start, end, v)
            else:
                update(left_child, left, mid, start, mid, v)
                update(right_child, mid + 1, right, mid + 1, end, v)
            
            f[now] = max(f[left_child] + delta[left_child], f[right_child] + delta[right_child])

        
        for index in range(n - 1):
            cnt += d[index]
            ori[index] = cnt

        build(0, 0, n - 2)
        
        res = []
        for index, v in queries:
            if nums[index] == v:
                res.append(f[0] + delta[0])
                continue
            
            rm_v = nums[index]
            if prime[rm_v]:
                while first[rm_v] and (nums[first[rm_v][0]] != rm_v or first[rm_v][0] == index):
                    heapq.heappop(first[rm_v])
                while last[rm_v] and (nums[-last[rm_v][0]] != rm_v or -last[rm_v][0] == index):
                    heapq.heappop(last[rm_v])

                if not first[rm_v]:
                    update(0, 0, n - 2, 0, n - 2, -1)
                elif index < first[rm_v][0]:
                    update(0, 0, n - 2, index, first[rm_v][0] - 1, -1)
                elif index > -last[rm_v][0]:
                    update(0, 0, n - 2, -last[rm_v][0], index - 1, -1)
            
            if prime[v]:
                if v not in first:
                    first[v] = []
                    last[v] = []

                while first[v] and nums[first[v][0]] != v:
                    heapq.heappop(first[v])
                while last[v] and nums[-last[v][0]] != v:
                    heapq.heappop(last[v])
                
                if not first[v]:
                    update(0, 0, n - 2, 0, n - 2, 1)
                elif index < first[v][0]:
                    update(0, 0, n - 2, index, first[v][0] - 1, 1)
                elif index > -last[v][0]:
                    update(0, 0, n - 2, -last[v][0], index - 1, 1)
                
                heapq.heappush(first[v], index)
                heapq.heappush(last[v], -index)
            
            nums[index] = v
            res.append(f[0] + delta[0])
        
        return res
''',
    call='Solution().maximumCount([3, 2, 1, 3], [[2, 3], [0, 1]])',
    expect=[3, 3],
    views=[
        dict(type='array', var='nums', label='nums（橙 = 质数）', h=190, cell=80, pointers={'index': 'blue'},
             color=lambda S, i, v: 'orange' if _isp(v) else None),
        dict(type='array', var=_eff, label='每个分割点 k 当前的答案（线段树维护，取最大）', h=190, cell=80),
        dict(type='map', var='first', label='first：质数 → 下标小根堆（堆顶 = 最左）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='map', var='last', label='last：质数 → 负下标小根堆（堆顶取负 = 最右）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='custom', draw=_draw_tree, h=290),
    ],
    watch=['index', 'v', 'rm_v', 'cnt', ('res', 'res', 'green')],
    skip=['ma = ', 'prime = [True]', 'prime[1] = False', 'for v in range(2, ma + 1)', 9, 36, 38, 'for x in range(v + v', 'prime[x] = False',
          'def build', 'def update', 'first = {}', 'last = {}', 'n = len(nums)', 'd = [0] * n', 'f = [0] * (n * 4)', 'delta = [0] * (n * 4)', 'ori = [0] * n',
          'left_child = now', 'right_child = now', 'mid = (left + right)', 'res = []', 'heapq.heappush(last[v], -index)', 'last[v] = [-index]',
          'for index, v in enumerate(nums)', 'if v not in first:', 'else:', 'f[now] = ori[left]', 'build(left_child', 'build(right_child', 'f[now] = max(f[left_child], f[right_child])'],
    max_steps=60,
    captions={
        'first[v] = [index]': '质数 `{v}` 第一次出现：`first[{v}] = [{index}]`，`last` 同时记 `-{index}`',
        17: lambda S, B, r: (f'`nums[{S.index}] = {S.v}` 是质数 → 记下它的下标' if S.prime[S.v] else f'`{S.v}` 不是质数，不用记'),
        'heapq.heappush(first[v], index)': lambda S, B, r: f'记下质数 `{S.v}` 的下标 `{S.index}`：`first` 是小根堆，堆顶 = 最左出现位置',
        'd[first[v][0]] += 1': '质数 `{v}` 的最左出现位置 `{first[v][0]}`：这里开始一条线段，差分 `+1`',
        'd[-last[v][0]] -= 1': '最右出现位置 `{-last[v][0]}`：线段在这里结束，差分 `-1`（只出现一次时两步抵消）',
        'cnt = len(first)': '每种出现过的质数至少被计 1 次：`cnt = {cnt}`',
        'cnt += d[index]': '分割点 `{index}` 被几条线段盖住，就多算几次 → `cnt` = {cnt}',
        'ori[index] = cnt': '分割点 `{index}` 的初始答案 = =={cnt}==',
        'build(0, 0, n - 2)': '用 `ori` 建线段树：区间最大值 = 当前最优答案（分割点只有 `0..n-2`）',
        'if nums[index] == v': lambda S, B, r: ('新旧值相同：答案不变，直接复用' if S.nums[S.index] == S.v else f'`nums[{S.index}]` 要从 `{S.nums[S.index]}` 改成 `{S.v}`，要处理'),
        'rm_v = nums[index]': '先看被换掉的旧值 `rm_v = {rm_v}`',
        'if prime[rm_v]': lambda S, B, r: (f'`{S.rm_v}` 是质数：它的最左/最右出现位置可能变' if S.prime[S.rm_v] else f'`{S.rm_v}` 不是质数：不影响答案，跳过'),
        'while first[rm_v] and': '懒删除：堆顶如果已被改掉（值不对，或就是这次要改的下标）就弹出',
        'while last[rm_v] and': '`last` 同理：弹到堆顶是真正的最右出现位置',
        'update(0, 0, n - 2, 0, n - 2, -1)': '`{rm_v}` 一次都不剩了：它至少计的那 1 次要去掉 → 整个区间 `-1`',
        'update(0, 0, n - 2, index, first[rm_v][0] - 1, -1)': '删掉的是最左的：线段缩短了，`[{index}, {first[rm_v][0] - 1}]` 不再被盖住 → `-1`',
        'update(0, 0, n - 2, -last[rm_v][0], index - 1, -1)': '删掉的是最右的：`[{-last[rm_v][0]}, {index - 1}]` 不再被盖住 → `-1`',
        93: lambda S, B, r: (f'新值 `{S.v}` 是质数：看它加进来后线段怎么变' if S.prime[S.v] else f'新值 `{S.v}` 不是质数：不影响答案'),
        'while first[v] and': '先清掉堆顶的失效下标（懒删除）',
        'while last[v] and': '`last` 同理',
        'if not first[v]:': lambda S, B, r: ('`first[v]` 空了：这个质数是第一次出现，要加 1' if not S.first[S.v] else f'`first[{S.v}] = {S.first[S.v]}`：这个质数以前出现过'),
        'update(0, 0, n - 2, 0, n - 2, 1)': '新出现一种质数：每个分割点都多算 1 → 整个区间 `+1`',
        'update(0, 0, n - 2, index, first[v][0] - 1, 1)': '新下标在最左边：线段向左延长，`[{index}, {first[v][0] - 1}]` 多盖住 → `+1`',
        'update(0, 0, n - 2, -last[v][0], index - 1, 1)': '新下标在最右边：线段向右延长，`[{-last[v][0]}, {index - 1}]` 多盖住 → `+1`',
        'nums[index] = v': '修改落地：`nums[{index}] = {v}`',
        'res.append(f[0] + delta[0])': '根节点的最大值（`f[0] + delta[0]`）就是本次答案 =={f[0] + delta[0]}==',
        'f[now] = max(f[left_child] + delta': '回溯：`f` = 两个儿子 `f + delta` 的较大值，自己的 `delta` 不用往下推',
        'delta[now] += v': '整段命中：只在这个节点记 `delta += {v}`，不往下推',
    },
    cards=dict(
        one_liner='每种质数至少计 1 次，切点夹在它最左最右之间再多计 1 次',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['`nums` 被依次修改，每次修改后选一个切点，把数组分成前后两段',
                 '求两段「不同质数个数」之和的最大值，每次修改后各答一个',
                 '本视频：`[3,2,1,3]`，查询 `[[2,3],[0,1]]` → `[3,3]`'],
        quote='对于特定的划分点c，不同质数之间相互不会产生影响，因此在这里可以从每种质数的角度出发来考虑……若v出现了多次：此时只有当v同时被划分到两个部分中才会计入答案两次，否则同样也只会计入答案恰好1次。',
        quote_src='—— yiduobo 题解原文',
        idea=['质数 `v` 只出现 1 次，不管怎么切都恰好计 1 次；出现多次且切点在最左和最右之间，就计 2 次',
              '先用差分数组算出每个切点的初始答案，建一棵区间最大值的线段树',
              '用两个堆（`first` 取最左、`last` 存负数取最右）加懒删除，改动时只给变化的那一段区间 ±1'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '堆用懒删除：堆顶的下标已失效（值变了）才弹出，所以可以随时取最左/最右',
                 '只有「最左/最右」变化，或者这个质数新增/消失时才需要改线段树，中间位置的修改不用管',
                 '为了演示，质数筛的上界 `ma` 从 `100000` 改成了 `10`（示例数值都不超过 10），筛本身的逻辑不变',
                 '原文是 Python 2 风格写法，在 Python 3 中可直接运行，其余未改动',
                 '对比灵神：灵神用有序集合 + Lazy 线段树；yiduobo 用堆懒删除 + 差分初值，思路相同'],
    ),
)
