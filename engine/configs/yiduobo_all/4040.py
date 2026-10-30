def _fv(v):
    return '凑不出' if v == -1 else str(v)


def _usage(S):
    u = S.get('usage')
    if u is None:
        return ''
    if not u:
        return '本轮可用变换 `usage`：（空）'
    return '本轮可用变换（体积, 代价）：' + '  '.join(f'==`({a},{b})`==' for a, b in u)


def _fcolor(S, k, v):
    s = S.get('s')
    if s is None or S.get('_line', 0) < 31:
        return None
    if k == s:
        return 'yellow'
    x = S.get('x')
    if x is not None and k == s - x and S.get('_line') in (34, 35):
        return 'blue'
    return None


def _upd(S, B, r):
    s, x, c = S.s, S.x, S.cost
    old = B.f[s]
    return (f'`f[{s - x}] = {_fv(B.f[s - x])}` 能凑出 → 用变换 `({x},{c})`：`f[{s}]` 由 {_fv(old)} 更新为 =={S.f[s]}==')


CONFIG = dict(
    num=4040, title='构造子集和的最少操作次数 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='先枚举变换 + 分组背包',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums, sum):
        
        f = [-1] * (sum + 1)
        f[0] = 0
        for v in nums:
            usage = []
            x = v
            cost = 0
            while x > 1:
                x >>= 1
                cost += 1
                usage.append((x, cost))
            
            usage.reverse()

            x = v
            cost = 0
            while x <= sum:
                usage.append((x, cost))
                x <<= 1
                cost += 1
            
            for s in range(sum, -1, -1):
                for x, cost in usage:
                    if s < x:
                        break
                    if f[s - x] != -1 and (f[s] == -1 or f[s] > f[s - x] + cost):
                        f[s] = f[s - x] + cost
            

        return f[-1]
''',
    call='Solution().minOperations([5, 6], 4)',
    expect=3,
    skip=['f[0] = 0', 'usage = []', 'x = v', 'cost = 0', 'x >>= 1', 'x <<= 1', 'cost += 1', 'usage.reverse', 'for x, cost in usage', 'break'],
    max_steps=100,
    views=[
        dict(type='array', var='nums', label='nums', h=130, cell=90, color=lambda S, k, v: 'blue' if S.get('v') == v else None),
        dict(type='text', fn=_usage, size=26, h=60),
        dict(type='array', var='f', label='f[s]：恰好凑出 s 的最少操作数（-1 = 凑不出）', h=240, cell=96,
             pointers={'s': 'pink'}, color=_fcolor),
    ],
    watch=['v', ('s', 's', 'pink'), 'x', 'cost'],
    captions={
        'f = [-1]': '`f[s]` = 凑出和恰为 `s` 的最少操作数，-1 表示凑不出；`f[0] = 0`（空集）',
        'for v in nums': lambda S, B, r: ('所有数都处理完了' if B.get('v') == S.v else f'处理 `v = {S.v}`：先列出它所有可用的变换'),
        'while x > 1': lambda S, B, r: (f'`x = {S.x} > 1`：还能再除一次' if S.x > 1 else f'`x = {S.x}`：再除就成 0 了，除法变换列完'),
        'usage.append((x, cost))': lambda S, B, r: (f'记录变换：除 `{S.cost}` 次得到 `{S.x}`，代价 `{S.cost}` → `usage` = `{S.usage}`' if S.get('_line') == 13 else f'记录变换：乘 `{S.cost}` 次得到 `{S.x}`，代价 `{S.cost}` → `usage` = `{S.usage}`'),
        'while x <= sum': lambda S, B, r: (f'`x = {S.x} <= sum = {S.sum}`：乘 `{S.cost}` 次后还没超过 sum，可用' if S.x <= S.sum else f'`x = {S.x} > sum = {S.sum}`：乘多了不能选，乘法变换列完'),
        'for s in range': lambda S, B, r: (f'容量 `s = {S.s}`（倒序，保证每个数至多用一个变换）' if S.s >= 0 and B.get('s') != S.s else '这个数处理完了'),
        'if s < x': lambda S, B, r: (f'变换体积 `x = {S.x}` > `s = {S.s}`：放不下，==break== 跳出内层（usage 按体积从小到大排好，后面的更大）' if S.s < S.x else f'变换体积 `x = {S.x}` ≤ `s = {S.s}`：放得下，看 `f[{S.s - S.x}]`'),
        'if f[s - x] != -1': lambda S, B, r: (f'`f[{S.s - S.x}] = {_fv(S.f[S.s - S.x])}`：' + ('凑不出，这个变换不能用' if S.f[S.s - S.x] == -1 else (f'`f[{S.s}]` 还是凑不出，或 {_fv(S.f[S.s])} > {S.f[S.s - S.x]} + {S.cost}，更优 → 更新' if (S.f[S.s] == -1 or S.f[S.s] > S.f[S.s - S.x] + S.cost) else f'`f[{S.s}] = {S.f[S.s]}` 已经不比 {S.f[S.s - S.x]} + {S.cost} 差，不更新'))),
        'f[s] = f[s - x] + cost': lambda S, B, r: f'`f[{S.s}]` 更新为 `f[{S.s - S.x}] + {S.cost}` = =={S.f[S.s]}==',
        'return f[-1]': lambda S, B, r: (f'`f[{S.sum}] = {S.f[-1]}`：最少 =={S.f[-1]}== 次操作' if S.f[-1] != -1 else '`f[sum] = -1`：凑不出'),
    },
    cards=dict(
        one_liner='乘除互相抵消，只剩一种方向：先列变换，再背包',
        complexity='时间 `O(n·sum·log)`，空间 `O(sum)`',
        problem=['一次操作把某元素 `x` 变成 `x * 2` 或 `x // 2`，且每个元素的乘法都在除法之前',
                 '求最少操作数，使某个子集和恰好为 `sum`；做不到返回 -1',
                 '示例：`[10,2], sum=13` → `3`；本视频：`[5,6], sum=4` → `3`'],
        quote='最后一次乘法操作与第一次除法操作就是相邻执行的，可以发现，这两个操作实际上完全抵消掉了。……是一个非常标准的背包问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘除相邻就抵消 → 每个数要么不动，要么只乘 `k` 次，要么只除 `k` 次',
              '乘法结果 `x << k` 不能超过 `sum`；除法结果 `x >> k` 不能为 0',
              '把这些 `(结果, 代价)` 存进 `usage`，用它们倒序更新 `f`，每个数至多选一个'],
        summary=['时间 `O(n·sum·(log sum + log U))`，空间 `O(sum)`',
                 '`f[s] = -1` 表示凑不出：判断时要先看 `f[s - x] != -1`',
                 '`usage` 先放除法（`reverse` 后体积从小到大），再放乘法，所以 `s < x` 可以直接 `break`',
                 '`s` 倒序是关键：不然同一个数会被用多次',
                 '原文已是 Python 3 可运行写法，无需改动；对比灵神：灵神直接在背包里枚举 `x<<a`、`x>>a`，这里先建 `usage` 表'],
    ),
)
