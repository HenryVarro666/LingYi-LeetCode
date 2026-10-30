def _head(S, key, n=6):
    v = S.get(key)
    return list(v[:n]) if v else None


def _top(S):
    I = S.get('_inner', {})
    if 'x' in I and 'p' in I:
        return f"`calc({I['x']})`：操作数数组前 {I['x']} 项之和，当前 `p = {I['p']}`，`res = {I['res']}`"
    if 'tot_cost' in I:
        return f"区间和 `tot_cost = {I['tot_cost']}`，右端点自己需要 `max_cost = {I.get('max_cost', '?')}` 次"
    return '操作数数组：`1×3, 2×12, 3×48, ...`（`4^k ~ 4^(k+1)-1` 的数各需 `k+1` 次）'


CONFIG = dict(
    num=3495, title='使数组元素都变为零的最少操作次数', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='操作数前缀和 · 最大值与总和取舍',
    tags=['灵神题单', '贪心与思维', '难度分 2206'],
    code='''
class Solution(object):
    def minOperations(self, queries):
        
        p4 = [1]
        cost = [0]

        while p4[-1] < 10 ** 9:
            p4.append(p4[-1] * 4)
            cost.append(3 * p4[-2] * len(cost))
        
        def calc(x):
            p = 1
            res = 0
            while x >= p4[p]:
                res += cost[p]
                p += 1

            res += (x - p4[p - 1] + 1) * p
            return res

        def get_single(x):
            res = 0
            while x:
                res += 1
                x //= 4
            
            return res

        res = 0
        for left, right in queries:
            tot_cost = calc(right) - calc(left - 1)
            max_cost = get_single(right)
            if max_cost * 2 > tot_cost:
                res += max_cost
            else:
                res += (tot_cost + 1) // 2
        
        return res
''',
    call='Solution().minOperations([[1,2],[2,6]])',
    expect=5,
    skip=['while p4[-1]', 'p4.append', 'cost.append'],
    max_steps=80,
    views=[
        dict(type='text', fn=_top, h=80),
        dict(type='array', var='queries', label='queries', h=190, cell=110),
        dict(type='array', var=lambda S: _head(S, 'p4'), label='p4：4 的幂（只显示前几项）', h=170, cell=90),
        dict(type='array', var=lambda S: _head(S, 'cost'), label='cost[k]：操作数为 k 的那些数，操作数之和 = 3×4^(k-1)×k', h=170, cell=90),
    ],
    watch=[('res', 'res', 'green'), 'left', 'right', 'tot_cost', 'max_cost'],
    captions={
        'p4 = [1]': '`p4` 存 4 的幂：`4^k` 之前（不含）的数都至多需要 `k` 次',
        'cost = [0]': '`cost[k]` 存「操作数恰为 k 的数的总操作数」：这类数有 `3×4^(k-1)` 个，各要 k 次',
        'while p4[-1] < 10 ** 9': '`p4`、`cost` 循环生成到 `4^15 > 10^9` 为止（下面右侧是前几项）',
        'p = 1': '从 `p = 1` 开始，一段一段累加',
        13: '`res` 累计前缀和，从 0 开始',
        22: '`res` 统计除了几次，从 0 开始',
        29: '`res` 是所有询问的答案之和，从 0 开始',
        'while x >= p4[p]': lambda S, B, r: (f'`x = {S.x} ≥ p4[{S.p}] = {S.p4[S.p]}`：第 {S.p} 段（操作数为 {S.p}）整段都在范围内 → 整段加上' if S.x >= S.p4[S.p]
                                              else f'`x = {S.x} < p4[{S.p}] = {S.p4[S.p]}`：第 {S.p} 段只到一半，不能整段加'),
        'res += cost[p]': '加上整段 `cost[{p - 0}]`：`res` → {res}',
        'p += 1': '`p` → {p}',
        'res += (x - p4[p - 1] + 1) * p': '最后一段只有 `x - p4[{p - 1}] + 1 = {x - p4[p - 1] + 1}` 个数，每个 `{p}` 次 → `res` = =={res}==',
        19: '`calc({x})` = =={ret}==：操作数数组前 {x} 项之和',
        27: '`x` 除到 0 一共 =={ret}== 次：这个数的操作数',
        38: '所有询问加起来：最少 =={ret}== 次操作',
        'def get_single': '`get_single(x)`：把单个数 x 除以 4 到 0 要几次，即 x 自己的操作数',
        'while x:': lambda S, B, r: (f'`x = {S.x}` > 0 → 还没除到 0，再除一次 4' if S.x else '`x = 0` → 除到 0 了，循环结束'),
        'res += 1': '又除了一次，`res` → {res}',
        'x //= 4': '`x` → {x}（除以 4 一次）',
        'for left, right in queries': lambda S, B, r: ('询问都处理完了，循环结束' if ('left' in B and (B['left'], B['right']) == (S.left, S.right)) else f"取下一个询问 `[{S.left}, {S.right}]`"),
        'tot_cost = calc(right)': '区间 `[{left}, {right}]` 的操作数之和 = `calc({right}) - calc({left} - 1)`（前缀和相减）',
        'max_cost = get_single': '最大的数 `{right}` 自己需要几次？它是整个区间的瓶颈',
        'if max_cost * 2 > tot_cost': lambda S, B, r: (f'`max_cost × 2 = {S.max_cost * 2}` > `tot_cost = {S.tot_cost}`：最大值比其余之和还大 → 被它卡住' if S.max_cost * 2 > S.tot_cost
                                                       else f'`max_cost × 2 = {S.max_cost * 2}` ≤ `tot_cost = {S.tot_cost}`：最大值不超过其余之和 → 可以均衡消减'),
        'res += max_cost': '答案取最大值：`res` = {B.res} + {max_cost} = =={res}==',
        'res += (tot_cost + 1) // 2': '答案取总和的一半向上取整：`({tot_cost} + 1) // 2` → `res` = =={res}==',
    },
    cards=dict(
        one_liner='把区间变成操作数数组：最大值若不超过其余之和，答案就是总和的一半',
        complexity='时间 `O(q log U)`，空间 `O(log U)`',
        problem=['对每个 `[l, r]`，数组是 `l, l+1, ..., r`；每次选两个数 `a, b`，都换成 `a // 4`、`b // 4`',
                 '求全部变 0 的最少操作次数，所有询问的结果相加',
                 '示例：`[[1,2],[2,4]]` → `3`；本视频：`[[1,2],[2,6]]` → `5`'],
        quote='处于4^k到4^(k + 1) - 1之间的元素，需要k + 1次操作才能变为0。……每次都应该选择数组中最大的两个元素执行减1操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个数变成操作数：`[0,1,1,1,2,2,...]`，一次操作 = 两个正数各减 1',
              '最大值大于其余之和 → 答案是最大值；否则 → 总和 // 2 向上取整',
              '区间和用前缀和：4 的幂分段，每段 k 的个数是 `3 × 4^(k-1)`'],
        summary=['时间 `O(q log U)`，空间 `O(log U)`',
                 '区间 `[l, r]` 里最大值一定是 `r` 的操作数，所以 `get_single(right)` 就是 `max_cost`',
                 '判断 `max_cost × 2 > tot_cost` 等价于「最大值 > 其余之和」',
                 '对比灵神：灵神证明了连续整数的最大值不会卡住，直接用 `ceil(tot / 2)`；yiduobo 保留了最大值的分支做保险'],
    ),
)
