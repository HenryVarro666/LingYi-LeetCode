CONFIG = dict(
    num=3424, title='将数组变相同的最小代价', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='两种情况取小 · 排序配对',
    tags=['贪心算法', '思维题', '难度分 1503'],
    code='''
class Solution(object):
    def minCost(self, arr, brr, k):
        
        def calc(arr, brr):
            cost = 0
            for a, b in zip(arr, brr):
                cost += abs(a - b)
            return cost

        res = min(calc(arr, brr), k + calc(sorted(arr), sorted(brr)))
        return res
''',
    call='Solution().minCost([-7,9,5], [7,-2,-5], 2)',
    expect=13,
    views=[
        dict(type='array', var='arr', h=200, label='arr（calc 内为传入的数组）', color=lambda S, i, v: 'blue'),
        dict(type='array', var='brr', h=200, label='brr', color=lambda S, i, v: 'pink'),
        dict(type='text', h=130, fn=lambda S: f"`cost` = ==" + str(S['cost']) + '==' if 'cost' in S else '先算不重排的代价，再算排序后重排的代价 `k + calc(...)`，取小'),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('cost', 'cost', 'green'), 'k'],
    captions={
        'def calc': '`calc` 逐位对齐两个数组，累加 `|a − b|`',
        'cost = 0': '`cost = 0`',
        'for a, b in zip': '取对齐的一对：`a = {a}`，`b = {b}`',
        'cost += abs': '`|{a} − {b}| = {abs(a - b)}`，`cost` → =={cost}==',
        'return cost': lambda S, B, r: f'这个对齐方式的总代价 `{r}`',
        'res = min': lambda S, B, r: '两种情况取小：不重排 `calc(arr, brr)`，或花 `k` 重排并让 `sorted` 后的最小对最小',
        'return res': '`min` 的结果 =={res}==：最小总代价',
    },
    cards=dict(
        one_liner='分两种情况：不重排，或花 k 全部拆开排序配对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['操作一：把 `arr` 切成连续段并任意重排，代价 `k`',
                 '操作二：某个元素加减 `x`，代价 `x`',
                 '示例：`arr=[-7,9,5], brr=[7,-2,-5], k=2` → `13`'],
        quote='完全可以将arr分割成若干长度为1的子数组然后重新排列。换言之，实际上就是可以通过k的代价将arr任意排列。……就应该让arr的最小值对上brr的最小值，arr的次小值对上brr的次小值，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['不重排：一趟遍历，代价就是 `Σ|arr[i] − brr[i]|`',
              '重排：切成长度 1 的段，等于花 `k` 任意排列；排序后从小到大配对',
              '两种情况的代价取较小者'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 生成新数组，不改动输入）',
                 '重排只需一次，所以是 `k + calc(sorted…)`，不是乘以次数',
                 '不重排的 `calc(arr, brr)` 里不用排序，和排序版取小',
                 '对比灵神：灵神 `ans2 ≤ k` 时提前返回省排序；yiduobo 每次都算两种情况',
                 '原文为 Python 2 风格，除类型说明外代码无需改动'],
    ),
)
