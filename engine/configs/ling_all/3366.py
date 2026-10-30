K = 3


def _cell(S, r, c, v):
    p, q = S.get('p'), S.get('q')
    if p is None or q is None or S.get('_line', 0) < 7:
        return None
    if (r, c) == (p, q):
        return 'yellow'
    ln = S.get('_line')
    if ln in (8, 9) and (r, c) == (p - 1, q):
        return 'blue'
    if ln in (10, 11) and (r, c) == (p, q - 1):
        return 'pink'
    if ln in (12, 13, 14) and (r, c) == (p - 1, q - 1):
        return 'cyan'
    return None


def _fml(S):
    x = S.get('x')
    if x is None:
        return '`f[p][q]`：前面的数里，至多用 p 次操作 1、q 次操作 2 的最小和'
    p, q = S.get('p'), S.get('q')
    if p is None or q is None:
        return f'当前数 `x = {x}`，`k = {S["k"]}`'
    return f'`x = {x}`：不操作 {x}；操作1 {(x + 1) // 2}；操作2 {x - S["k"] if x >= S["k"] else "不可"}'


CONFIG = dict(
    num=3366, title='最小数组和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='选或不选 · 二维 DP 空间优化',
    tags=['其他线性 DP', '难度分 2040'],
    code='''
class Solution:
    def minArraySum(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        f = [[0] * (op2 + 1) for _ in range(op1 + 1)]
        for x in nums:
            for p in range(op1, -1, -1):
                for q in range(op2, -1, -1):
                    res = f[p][q] + x
                    if p:
                        res = min(res, f[p - 1][q] + (x + 1) // 2)
                    if q and x >= k:
                        res = min(res, f[p][q - 1] + x - k)
                        if p:
                            y = (x + 1) // 2 - k if (x + 1) // 2 >= k else (x - k + 1) // 2
                            res = min(res, f[p - 1][q - 1] + y)
                    f[p][q] = res
        return f[op1][op2]
''',
    call='Solution().minArraySum([2, 8, 3, 19, 3], 3, 1, 1)',
    expect=23,
    skip=['for p in range', 'for q in range'],
    max_steps=60,
    views=[
        dict(type='array', var='nums', label='nums（逐个处理）', h=150, cell=80),
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='table', var='f', label='f[p][q]（行 p = 操作 1 次数，列 q = 操作 2 次数；黄 = 正在算）', h=330, cell=110,
             rows=lambda S: [f'p={i}' for i in range(len(S['f']))], cols=lambda S: [f'q={j}' for j in range(len(S['f'][0]))],
             color=_cell),
    ],
    watch=[('x', 'x', 'yellow'), ('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        3: '`f[p][q]`：处理完已看过的数后，至多 `p` 次操作 1、`q` 次操作 2 的最小和；一开始没有数，全是 0',
        4: lambda S, B, r: ('取下一个数 `x`，对它「选或不选」四种操作' if 'x' in S else ''),
        7: '不操作：`f[{p}][{q}] + {x}` = =={res}==',
        8: lambda S, B, r: (f'`p = {S.p}`，还有操作 1 可用，可对 `{S.x}` 除以 2 上取整' if S.p else f'`p = 0`：操作 1 用完了，跳过'),
        9: '操作 1：`f[{p-1}][{q}] + ceil({x}/2)` = {f[p-1][q] + (x+1)//2}，和 {B.res} 取小 → `res` = =={res}==',
        10: lambda S, B, r: (f'`q = {S.q}`，且 `x = {S.x} >= k = {S.k}`：可以对 `{S.x}` 减 `k`' if S.q and S.x >= S.k else
                             (f'`x = {S.x} < k = {S.k}`：不满足减 k 的条件，跳过' if S.q else '`q = 0`：操作 2 用完了，跳过')),
        11: '操作 2：`f[{p}][{q-1}] + {x} - {k}` = {f[p][q-1] + x - k}，取小 → `res` = =={res}==',
        12: lambda S, B, r: (f'`p = {S.p}`：两个操作都用在 `{S.x}` 上' if S.p else '`p = 0`：不能再除 2，跳过'),
        13: lambda S, B, r: (f'先除再减更优（`ceil(x/2) = {(S.x + 1) // 2} >= k`）→ `y = {S.y}`' if (S.x + 1) // 2 >= S.k
                             else f'`ceil(x/2) < k`，除完就没法减了 → 只能先减再除，`y = {S.y}`'),
        14: '两个都用：`f[{p-1}][{q-1}] + {y}` = {f[p-1][q-1] + y}，取小 → `res` = =={res}==',
        15: '`f[{p}][{q}] = {res}`（倒序遍历，所以读到的 f[p-1]、f[q-1] 还是旧值）',
        16: '至多 `{op1}` 次操作 1、`{op2}` 次操作 2 的最小和 = =={ret}==',
    },
    cards=dict(
        one_liner='对每个数「不操作 / 操作1 / 操作2 / 两个都用」，DP 记剩余次数',
        complexity='时间 `O(n·op1·op2)`，空间 `O(op1·op2)`',
        problem=['操作 1：`nums[i]` 除以 2 上取整，最多 `op1` 次；操作 2：`nums[i] >= k` 时减 `k`，最多 `op2` 次',
                 '每个下标每种操作至多一次，两种可叠加；求最小和',
                 '示例：`[2,8,3,19,3], k=3, op1=1, op2=1` → `23`'],
        quote='动态规划有「选或不选」和「枚举选哪个」两种基本思考方式。……本题用到的是「选或不选」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, op1, op2)`：从右往左考虑 `nums[i]`，四种操作各对应一个子问题',
              '两个操作同用时：能先除再减就先除再减，否则先减再除',
              '记忆化 → 1:1 递推 → 像 0-1 背包一样去掉第一维，次数倒序遍历'],
        summary=['时间 `O(n·op1·op2)`，空间 `O(op1·op2)`',
                 '`y` 的取法是易错点：除完还 `>= k` 才能先除再减',
                 '去掉第一维后，`p`、`q` 必须倒序，否则同一个数被用多次',
                 '题解的方法二是贪心 + 分类讨论（`O(n log n)`），本视频演示方法一的最终空间优化写法'],
    ),
)
