def _set(mask, n):
    return '{' + ','.join(str(i) for i in range(n) if mask >> i & 1) + '}'


def _vs(v):
    return '?' if v is None else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['lists'])
    u = 1 << n
    length, median, f = S.get('length'), S.get('median'), S.get('f')
    cv.text((x0 + 18, y0 + 4), '每个下标集合 state：合并后长度 length · 中位数 median · 最小成本 f（? = 还没算）', 21, T['muted'], bold=True)
    rowh = min(52, (y1 - y0 - 100) / (u - 1))
    y = y0 + 56
    cols = [x0 + 20, x0 + 260, x0 + 460, x0 + 660]
    for h_, cx in zip(('state', 'length', 'median', 'f'), cols):
        cv.text((cx, y - 4), h_, 20, T['dim'], bold=True)
    y += 28
    st, sub = S.get('state'), S.get('sub')
    line = S.get('_line')
    for m in range(1, u):
        row = y + (m - 1) * rowh
        tag = None
        if st == m:
            tag = T['yellow']
        elif sub is not None and line in (22, 23, 24) and m == sub:
            tag = T['cyan']
        elif sub is not None and line in (22, 23, 24) and st is not None and m == st ^ sub:
            tag = T['pink']
        if tag:
            cv.rect((x0 + 8, row - 3, x1 - 8, row + rowh - 6), fill=tag, alpha=45, r=8, outline=tag, width=2)
        cy = row + rowh / 2 - 4
        cv.text((cols[0], cy), _set(m, n), 22, T['text'], anchor='lm', mono=True)
        for c, arr, color in ((1, length, T['text']), (2, median, T['purple']), (3, f, T['green'])):
            v = arr[m] if arr else None
            cv.text((cols[c], cy), _vs(v), 22, color if v is not None else T['dim'], anchor='lm', mono=True, bold=True)


CONFIG = dict(
    num=3801, title='合并有序列表的最小成本', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 二分套二分求中位数',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2399'],
    code='''
class Solution(object):
    def minMergeCost(self, lists):
        
        n = len(lists)
        max_state = (1 << n)

        length = [None] * max_state
        median = [None] * max_state

        f = [None] * max_state
        for index in range(n):
            state = (1 << index)
            f[state] = 0
            length[state] = len(lists[index])
            median[state] = lists[index][(len(lists[index]) - 1) // 2]

        for state in range(1, max_state):
            if f[state] is None:
                sub = state & (state - 1)
                length[state] = length[sub] + length[state ^ sub]

                while sub > (state ^ sub):
                    cost = f[sub] + f[state ^ sub] + abs(median[sub] - median[state ^ sub])
                    if f[state] is None or f[state] > cost:
                        f[state] = cost
                    sub = (sub - 1) & state
                
                f[state] += length[state]

                lo = None
                hi = None
                ll = []
                for index in range(n):
                    if state & (1 << index):
                        ll.append(index)
                        if lo is None or lo > lists[index][0]:
                            lo = lists[index][0]
                        if hi is None or hi < lists[index][-1]:
                            hi = lists[index][-1]
                
                k = (length[state] + 1) // 2
                while lo < hi:
                    v = (lo + hi) // 2
                    cnt = 0
                    for index in ll:
                        if v < lists[index][0]:
                            continue

                        left = 0
                        right = len(lists[index]) - 1
                        while left < right:
                            mid = (left + right + 1) // 2
                            if lists[index][mid] <= v:
                                left = mid
                            else:
                                right = mid - 1

                        cnt += left + 1
                        if cnt >= k:
                            break
                    
                    if cnt >= k:
                        hi = v
                    else:
                        lo = v + 1
                
                median[state] = lo
        
        return f[-1]
''',
    call='Solution().minMergeCost([[1,3,5],[2,4],[6,7,8]])',
    expect=18,
    views=[
        dict(type='text', size=28, h=60, fn=lambda S: '`lists` ' + '  '.join(f'#{i}`{a}`' for i, a in enumerate(S['lists']))),
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', size=27, h=70, fn=lambda S: (
            f"二分中位数：`lo = {S['lo']}`，`hi = {S['hi']}`，试 `v = {S['v']}`：不超过 v 的有 `{S['cnt']}` 个，要 `{S['k']}` 个"
            if all(x in S for x in ('lo', 'hi', 'v', 'cnt', 'k')) and S.get('_line') in (63, 65) else '')),
    ],
    watch=[('state', "bin(state)[2:]", 'yellow'), ('sub', "bin(sub)[2:]", 'cyan'), ('lo', 'lo', 'blue'), ('hi', 'hi', 'pink'), ('k', 'k', 'orange')],
    skip=[20, 25, 47, 4, 5, 7, 8, 10, 11, 12, 13, 14, 18, 19, 22, 24, 26, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 44, 45, 46,
          49, 50, 51, 52, 53, 54, 56, 58, 59, 60, 62],
    captions={
        15: lambda S, B, r: f'单个列表 `#{S.index}` 就是 `state = {_set(S.state, len(S.lists))}`：`f = 0`，长度 `{S.length[S.state]}`，中位数 `{S.median[S.state]}`（下标 `(len-1)//2`，偶数取左中间）',
        17: lambda S, B, r: ('所有 `state` 都算完了' if S.state & (S.state - 1) and S.f[S.state] is not None else f'`state = {_set(S.state, len(S.lists))}`：' + ('单个列表，已有答案 → 跳过' if S.f[S.state] is not None else '多个列表：最后一步拆成两个子集合并')),
        20: lambda S, B, r: f'长度 `length[{_set(S.state, len(S.lists))}] = length[{_set(S.sub, len(S.lists))}] + length[{_set(S.state ^ S.sub, len(S.lists))}] = {S.length[S.state]}`；`sub` 从最大的真子集开始枚举',
        23: lambda S, B, r: f'拆成 `{_set(S.sub, len(S.lists))}`（f={S.f[S.sub]}，中位数 {S.median[S.sub]}）和 `{_set(S.state ^ S.sub, len(S.lists))}`（f={S.f[S.state ^ S.sub]}，中位数 {S.median[S.state ^ S.sub]}）：`{S.f[S.sub]} + {S.f[S.state ^ S.sub]} + |{S.median[S.sub]} − {S.median[S.state ^ S.sub]}|` = ==成本 {S.cost}==',
        25: lambda S, B, r: f'`f[{_set(S.state, len(S.lists))}]` 取更小的：{_vs(B.f[S.state])} → =={S.f[S.state]}==',
        28: lambda S, B, r: f'所有拆法里最小的是 `{B.f[S.state]}`，再加上合并后的长度 `length = {S.length[S.state]}`（每种拆法都一样）→ `f` 变成 =={S.f[S.state]}==',
        41: lambda S, B, r: f'`median[state]` 没法直接拿：合并后的数组没存。第 `k = {S.k}` 小（左中位数）就是答案，在 `[{S.lo}, {S.hi}]` 里二分这个值',
        63: lambda S, B, r: f'试 `v = {S.v}`：各列表里 ≤ v 的元素个数累计 `{S.cnt}` ≥ `k = {S.k}` → v 够大，`hi` 变成 =={S.hi}==',
        65: lambda S, B, r: f'试 `v = {S.v}`：累计只有 `{S.cnt}` < `k = {S.k}` → v 太小，`lo` 变成 =={S.lo}==',
        67: lambda S, B, r: f'`lo == hi`：第 `{S.k}` 小就是 `{S.lo}` → `median[{_set(S.state, len(S.lists))}] = {S.lo}`',
        'return f[-1]': '`f[-1]` 是全部列表：最小总成本 =={ret}==',
    },
    max_steps=140,
    cards=dict(
        one_liner='f[state] 状压 DP；中位数没法存数组，就二分套二分去算',
        complexity='时间 `O(3^n + 2^n·n·log U·log ℓ)`，空间 `O(2^n)`',
        problem=['`lists` 是若干非递减数组，每次选两个合并成一个有序数组',
                 '成本 = `len(a) + len(b) + |median(a) − median(b)|`，偶数长度取左中位数',
                 '本视频：`[[1,3,5],[2,4],[6,7,8]]` → `18`'],
        quote='非常标准的状态压缩动态规划问题。令f[state]表示将状态表示为state的列表合并到一起的最小成本。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 的每一位表示一个原始列表；2 的幂 = 单个列表 → `f = 0`',
              '否则枚举子状态 `sub`：`f[sub] + f[state^sub]` 加上两边中位数之差，最后统一加 `length[state]`',
              '`length` 好算（子状态相加）；`median` 不能存合并后的数组，只能==二分中位数 v，再在每个原始列表里二分 ≤ v 的个数=='],
        summary=['时间 `O(3^n)` 的子集枚举 + 每个状态一次二分套二分求中位数',
                 '`while sub > (state ^ sub)` 只枚举一半（`sub` 与 `state^sub` 对称）',
                 '中位数取左中间：`k = (length + 1) // 2`，找最小的 `v` 使得 ≤ v 的元素数 ≥ k',
                 '代码本身兼容 Python 3，未做修改',
                 '对比灵神：灵神直接把每个子集的数组合并排好；yiduobo 不存数组，用二分算中位数省空间']
    ),
)
