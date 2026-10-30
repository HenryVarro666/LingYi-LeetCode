def _draw(cv, S, B, box, T, L_REV, L_SORT):
    x0, y0, x1, y1 = box
    nums, k, m = S['nums'], S['k'], S['m']
    n = len(nums)
    if 'cost' not in S or 'v' not in S:
        cv.text((x0 + 18, y0 + 4), 'nums（先从大到小排序），准备试填每一位', 22, T['muted'], bold=True)
        cell = 100
        sx = x0 + 60 + max(0, ((x1 - x0 - 120) - cell * n) / 2)
        for t, x in enumerate(nums):
            X = sx + t * cell
            cv.rect((X + 4, y0 + 80, X + cell - 4, y0 + 170), fill=T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, y0 + 125), x, 38, T['text'], anchor='mm', bold=True, mono=True)
        if 'p2' in S:
            cv.text((x0 + 18, y0 + 220), '可试的位：p2 = ' + str(S['p2']), 28, T['yellow'], bold=True)
        return
    W = S['p2'][-1].bit_length()
    v = S['v']
    line = S['_line']
    cost, delta = S['cost'], S.get('delta', [0] * n)
    i = S.get('index', -1)
    in_loop = L_REV[0] <= line < L_SORT
    reverted = line >= L_REV[1]
    cell = 70
    sx = x0 + 220
    ys = y0 + 80
    cv.text((x0 + 18, y0 + 4), '每个数 x = nums + cost（已补的位）；试第 v 位：橙 = 这一位原来缺、现在补上', 22, T['muted'], bold=True)
    for b in range(W):
        bit = W - 1 - b
        X = sx + b * cell
        hit = (1 << bit) == v
        cv.text((X + cell / 2, ys - 8), f'v={1 << bit}', 18, T['yellow'] if hit else T['dim'], anchor='mb', mono=True, bold=hit)
    ans = S.get('res', 0)
    for t in range(n):
        y = ys + t * 92
        shown = (t <= i and line < L_SORT) or line >= L_SORT or (line >= 20 and t < i)
        x = nums[t] + cost[t]
        cv.text((sx - 14, y + 31), f'{nums[t]} + {cost[t]} = {x}', 26, T['blue'] if (t == i and in_loop) else T['text'], anchor='rm', bold=True, mono=True)
        for b in range(W):
            bit = W - 1 - b
            X = sx + b * cell
            xb = (x >> bit) & 1
            fill = T['panel2']
            hit = (1 << bit) == v
            if hit and shown:
                if delta[t] and not reverted:
                    fill = T['orange']
                elif xb:
                    fill = T['green']
            elif (ans >> bit) & 1 and xb:
                fill = (46, 90, 60)
            cv.rect((X + 3, y, X + cell - 3, y + 62), fill=fill, r=8, outline=T['yellow'] if (hit and t == i and in_loop) else T['border'], width=4 if (hit and t == i and in_loop) else 1)
            cv.text((X + cell / 2, y + 31), xb, 32, T['bg'] if fill in (T['green'], T['orange']) else T['text'], anchor='mm', bold=True, mono=True)
        if shown and delta[t]:
            cv.text((sx + W * cell + 24, y + 31), ('已撤销 ' if reverted else '') + f'+{delta[t]}', 28, T['dim'] if reverted else T['cyan'], anchor='lm', bold=True, mono=True)
    yb = ys + n * 92 + 10
    if line >= L_SORT:
        sc = S.get('sorted_cost', sorted(cost))
        sm = sum(sc[:m])
        cv.text((x0 + 18, yb), f'sorted_cost = {sc}，前 {m} 小之和 = {sm} ' + ('≤' if sm <= k else '>') + f' k = {k}', 26,
                T['green'] if sm <= k else T['orange'], bold=True)
    cv.text((x0 + 18, yb + 46), f'res = {ans}（二进制 {format(ans, "b")}）', 26, T['green'], bold=True)


_CODE = '''
class Solution(object):
    def maximumAND(self, nums, k, m):
        
        p2 = [1]
        nums.sort(reverse=True)
        s = sum(nums[:m])
        while p2[-1] <= nums[0]:
            p2.append(p2[-1] + p2[-1])
        
        while p2[-1] * m - s <= k:
            p2.append(p2[-1] + p2[-1])

        p2.pop()

        cost = [0] * len(nums)
        res = 0
        for v in p2[::-1]:
            delta = [0] * len(nums)
            for index in range(len(nums)):
                x = nums[index] + cost[index]
                if x & v:
                    continue
                else:
                    delta[index] = v - (x & (v - 1))
                    cost[index] += delta[index]
            
            sorted_cost = sorted(cost)
            if sum(sorted_cost[:m]) <= k:
                res |= v
            else:
                for index in range(len(nums)):
                    cost[index] -= delta[index]
        
        return res
'''
_L = _CODE.lstrip('\n').split('\n')
_SORT = next(n for n, s in enumerate(_L, 1) if 'sorted_cost = sorted' in s)
_REV = next(n for n, s in enumerate(_L, 1) if 'else:' in s and n > _SORT)
_FIDX = next(n for n, s in enumerate(_L, 1) if 'for index in range' in s)

CONFIG = dict(
    num=3806, title='增加操作后最大按位与的结果', difficulty='Hard', category='位运算',
    author='yiduobo', technique='从高位到低位贪心 · 累计 cost',
    tags=['灵神题单·位运算', '难度分 2259'],
    code=_CODE,
    call='Solution().maximumAND([3,1,2], 8, 2)',
    expect=6,
    skip=['x = nums[index] + cost[index]', 'cost[index] += delta[index]', 'delta = [0]', 'continue', 'cost = [0]', 'p2 = [1]', 's = sum', 'p2.pop()'],
    max_steps=80,
    views=[dict(type='custom', draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T, (_FIDX, _REV), _SORT), h=560)],
    watch=[('v', 'v', 'yellow'), ('index', 'index', 'blue'), ('res', 'res', 'green'), ('cost', 'cost', 'cyan'), ('k', 'k'), ('m', 'm')],
    captions={
        'nums.sort(reverse=True)': '先从大到小排序：`nums = {nums}`，最大的 `m` 个数在最前面',
        'while p2[-1] <= nums[0]': lambda S, B, r: (f'`p2[-1] = {S.p2[-1]}` ≤ 最大值 `{S.nums[0]}`：2 的幂还没超过最大数 → 继续翻倍'
                                                    if S.p2[-1] <= S.nums[0] else f'`p2[-1] = {S.p2[-1]}` 已经大于最大值 `{S.nums[0]}`，停'),
        'while p2[-1] * m - s <= k': lambda S, B, r: (
            f'把 `m` 个最大数都补到 `{S.p2[-1]}` 的总代价 = `{S.p2[-1]}×{S.m} − {S.s}` = `{S.p2[-1] * S.m - S.s}` ≤ `k = {S.k}`：还补得起 → 继续往更高位试'
            if S.p2[-1] * S.m - S.s <= S.k else
            f'补到 `{S.p2[-1]}` 要 `{S.p2[-1] * S.m - S.s}` > `k = {S.k}`：补不起，最高位找到了'),
        'p2.append': '候选位增加：`p2 = {p2}`（每个都是 2 的幂）',
        'res = 0': '`p2 = {p2}`（最高位已确定）。`cost[i]` 记录每个数为了满足已填的高位已经花了多少；`res = 0`',
        'for v in p2[::-1]': lambda S, B, r: ('所有位都试完了' if B.get('v') == S.v and 'v' in B else
                                             f'试第 `v = {S.v}`（二进制 `{bin(S.v)[2:]}`）这一位，从高到低'),
        'if x & v': lambda S, B, r: (f'当前 `x = nums[{S.index}] + cost[{S.index}] = {S.nums[S.index]} + {S.cost[S.index]} = {S.x}`（保留了之前补高位花的）；`{S.x} & {S.v}` ≠ 0：这一位已经是 1 → 不用花钱'
                                     if S.x & S.v else f'当前 `x = {S.nums[S.index]} + {S.cost[S.index]} = {S.x}`；`{S.x} & {S.v}` = 0：这一位是 0 → 要补'),
        'delta[index] = ': lambda S, B, r: (f'补成 `v`：保留 `x` 的低位 `x & (v-1) = {S.x & (S.v - 1)}`，再加到 `v`：花 `{S.v} − {S.x & (S.v - 1)}` = =={S.delta[S.index]}==；`cost[{S.index}]` 累计为 `{S.cost[S.index] + S.delta[S.index]}`'),
        'sorted_cost = sorted': '`cost` 排序：`{sorted_cost}`，贪心选花钱最少的 `m` 个数',
        'if sum(sorted_cost[:m]) <= k': lambda S, B, r: (
            f'前 `{S.m}` 小之和 `{sum(S.sorted_cost[:S.m])}` ≤ `k = {S.k}` → ==这一位可以填 1=='
            if sum(S.sorted_cost[:S.m]) <= S.k else f'前 `{S.m}` 小之和 `{sum(S.sorted_cost[:S.m])}` > `k = {S.k}` → ==这一位填不了=='),
        'res |= v': '`res |= {v}` → `res = {res}`（二进制 `{bin(res)[2:]}`）',
        'cost[index] -= delta[index]': lambda S, B, r: f'填不了：把这一轮 `delta` 撤销，`cost[{S.index}]` 回到 `{S.cost[S.index]}`',
        19: lambda S, B, r: ('这一轮每个数都算过了' if B.get('index') == S.index and 'index' in B else f'看第 `{S.index}` 个数'),
        31: lambda S, B, r: ('撤销完毕' if B.get('index') == S.index and 'index' in B else f'看第 `{S.index}` 个数'),
        'return res': '每一位都试完：最大按位与 `res = {res}`',
    },
    cards=dict(
        one_liner='从高位往低位，算每个数把这一位补成 1 的代价，前 m 小之和够不够',
        complexity='时间 `O(n log n log U)`，空间 `O(n)`',
        problem=['最多 `k` 次操作，每次把某个 `nums[i]` 加 1；选出 `m` 个数，求它们按位与的最大值',
                 '示例：`[3,1,2]`，`k=8`，`m=2` → `6`'],
        quote='计算将数组中的每个元素的这一位变为1所需的代价，若前m小的代价之和小于等于k，那么答案的这一位就为1，否则为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先定最高位：`p2` 是 2 的幂，把最大的 `m` 个数补到 `p` 的代价是 `p×m − 最大 m 个数之和`，补得起就继续翻倍',
              '低位变 1 是在高位已变 1 的基础上：用 `cost` 累计，每轮先算 `x = nums + cost`',
              '这一位成功就保留 `delta`，失败就从 `cost` 里把 `delta` 减回去'],
        summary=['时间 `O(n log n log U)`，每位排序一次；空间 `O(n)`',
                 '易错：低位的“代价”要在已经补过高位的数上算，所以必须记 `cost`；失败时要撤销本轮的 `delta`',
                 '原文就是 Python 2/3 通用写法，未做改动',
                 '对比灵神：灵神每轮直接用 `target = ans | bit` 重新算每个数的代价，不用累计 cost 和撤销'],
    ),
)
