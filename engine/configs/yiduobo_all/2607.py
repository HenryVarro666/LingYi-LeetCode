CONFIG = dict(
    num=2607, title='使子数组元素和相等', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='gcd 分组 + 中位数', tags=['灵神题单', '数学算法', '难度分 2071'],
    code='''
class Solution(object):
    def makeSubKSumEqual(self, arr, k):
        n = len(arr)
        x, y = n, k
        while y:
            x, y = y, x % y

        g = x

        num_list = [[] for _ in range(g)]
        for index, v in enumerate(arr):
            num_list[index % g].append(v)

        res = 0
        for r in range(g):
            num_list[r].sort()
            mid = num_list[r][len(num_list[r]) // 2]
            for v in num_list[r]:
                if v < mid:
                    res += mid - v
                else:
                    res += v - mid

        return res
''',
    call='Solution().makeSubKSumEqual([1,9,4,2,7,3,5,8], 6)',
    expect=19,
    views=[
        dict(type='array', var='arr', h=170, label='arr',
             color=lambda S, i, v: ('blue' if i % S['g'] == S['r'] else None) if 'r' in S and 'g' in S else None),
        dict(type='table', var='num_list', h=230, label='num_list（按下标模 g 分组）', cell=60),
        dict(type='text', h=90, fn=lambda S: f"`g` = =={S['g']}==" + (f"，当前组 `r = {S['r']}`" if 'r' in S else '') if 'g' in S else f"求 `gcd({S['n']}, {S['k']})`，`x, y = {S['x']}, {S['y']}`" if 'x' in S else ''),
    ],
    watch=['x', 'y', 'g', 'r', 'mid', ('res', 'res', 'green')],
    captions={
        'x, y = n, k': '用辗转相除求 `n` 与 `k` 的最大公约数：`x, y = {x}, {y}`',
        'x, y = y': '`x, y = {x}, {y}`',
        'g = x': '`gcd` 求出：`g = {g}`。下标之差是 `g` 的倍数的两个数必须相等',
        'num_list = [[]': '准备 `{g}` 个分组，下标模 `g` 相同的数放一起',
        'num_list[index % g]': '`arr[{index}] = {v}` 放入第 `{index % g}` 组',
        'num_list[r].sort()': '第 `{r}` 组排序：`{num_list[r]}`',
        'mid = ': '中位数是最优目标：`mid = {mid}`',
        'if v < mid': lambda S, B, r: f'`{S.v}` 与中位数 `{S.mid}` 比较，差值 `{abs(S.v - S.mid)}` 就是这个数的操作次数',
        'res += mid - v': '`v < mid`，要加 `{mid - v}` 次：`res = {res}`',
        'res += v - mid': '`v ≥ mid`，要减 `{v - mid}` 次：`res = {res}`',
        'return res': '全部分组累加，最少操作 =={ret}==',
    },
    cards=dict(
        one_liner='下标差是 gcd(n,k) 的倍数的数必须相等，按组取中位数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['循环数组 `arr`，每次可让一个元素 `+1` 或 `-1`',
                 '使每个长为 `k` 的子数组之和都相等，求最少操作次数',
                 '示例：`[1,4,1,3]`, `k=2` → `1`'],
        quote='那么i和j只要满足下标之差为g的倍数，那么这两个下标上的数就必须相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻子数组和相等，去掉公共部分后得 `a[i] = a[i+k]`',
              '循环数组还可能 `i + a*k = j + b*n`，推出 `j - i = (a*p - b*q)*g`',
              '`p`、`q` 互质，系数能取任意整数 → 下标差为 `g` 的倍数就要相等',
              '分组后每组取中位数，是经典的最少 ±1 问题'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`len(num_list[r]) / 2` 已改为 `//`',
                 '这版手写辗转相除求 gcd，再分组排序',
                 '对比灵神：同样的结论，灵神用裴蜀定理证明周期，yiduobo 用方程推导'],
    ),
)
