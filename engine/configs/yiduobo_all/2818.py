def _info(S):
    if 'freq' in S:
        return f"当前取 `{S['v']}`：可用 `freq = {S['freq']}` 次，剩余操作次数 `k = {S['k']}`"
    if 'left' in S:
        return '第二趟（从右往左）：左边界取 `cnt >= `，保证并列时只算最左的'
    if 'right' in S:
        return '第一趟（从左往右）：遇到质因子更多的数，栈顶的 right 就定下来'
    return '先给每个不同的数算质因子个数 `cnt[v]`'


CONFIG = dict(
    num=2818, title='操作使得分最大', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='质因数分解 + 单调栈 + 排序贪心',
    tags=['灵神题单', '单调栈', '难度分 2397'],
    code='''
class Solution(object):
    def maximumScore(self, nums, k):

        p = list(range(400))
        x = 2
        while x * x <= 400:
            if p[x] == x:
                for y in range(x + x, 400, x):
                    p[y] = x
            
            if x == 2:
                x += 1
            else:
                x += 2

        prime_list = []
        for x in range(2, 400):
            if p[x] == x:
                prime_list.append(x)

        cnt = {}
        for v in nums:
            if v not in cnt:
                x = v
                cnt[v] = 0
                for y in prime_list:
                    if y > x:
                        break
                    if x % y == 0:
                        while x % y == 0:
                            x //= y
                        cnt[v] += 1

                if x > 1:
                    cnt[v] += 1
                

        n = len(nums)
        right = [n] * n
        stack = []
        for index in range(n):
            v = nums[index]
            while stack and cnt[nums[stack[-1]]] < cnt[v]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        left = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            while stack and cnt[nums[stack[-1]]] <= cnt[v]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        mod = 10 ** 9 + 7
        res = 1
        
        def quickPow(base, x):
            if x == 1:
                return base
            
            tmp = quickPow(base, x // 2)
            tmp *= tmp
            tmp %= mod

            if x % 2 == 1:
                tmp *= base
                tmp %= mod
            
            return tmp

        for v, freq in sorted([[nums[index], (right[index] - index) * (index - left[index])] for index in range(n)], reverse=True):
            if k > freq:
                res *= quickPow(v, freq)
                res %= mod
                k -= freq
            else:
                res *= quickPow(v, k)
                res %= mod
                break
            
        return res
''',
    call='Solution().maximumScore([2, 6, 3, 6], 8)',
    expect=1679616,
    max_steps=100,
    skip=list(range(4, 20)) + ['n = len(nums)', 'right = [n] * n', 'left = [-1] * n', 'stack = []', 'mod = 10', 'res = 1', 'def quickPow', 'tmp *= tmp', 'tmp %= mod', 'res %= mod', 'if x == 1', 'return base', 'tmp = quickPow', 'return tmp', 'if x % 2 == 1', 'tmp *= base', 'break', 'v = nums[index]', 'for y in prime_list', 'if y > x', 'cnt[v] = 0', 'if v not in cnt', 'x = v'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=70, h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='map', var='cnt', label='cnt：每个数的质因子个数', h=120, font=24),
        dict(type='stack', var='stack', label='stack（下标，底→顶）', h=100, font=24),
        dict(type='array', var='right', label='right：右边 cnt 更大的最近下标', cell=64, h=100, index=False),
        dict(type='array', var='left', label='left：左边 cnt >= 的最近下标', cell=64, h=100, index=False),
        dict(type='text', fn=_info, size=22, h=50),
    ],
    watch=[('v', 'v', 'yellow'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'for v in nums': lambda S, B, r: (f'看 `{S.v}`：之前算过就跳过' if S.v in S.cnt else f'`{S.v}` 还没算过，分解质因数'),
        'if v not in cnt': lambda S, B, r: ('没算过 → 分解' if S.v not in S.cnt else '算过了，直接跳过'),
        'cnt[v] = 0': '`cnt[{v}]` 记录不同质因子的个数，先置 `0`',
        'for y in prime_list': lambda S, B, r: f'试除质数 `{S.y}`',
        'if y > x': lambda S, B, r: (f'质数 `{S.y}` > 剩余 `{S.x}`：不用再试了' if S.y > S.x else f'`{S.y}` 不大于剩余 `{S.x}`，继续'),
        'if x % y == 0': lambda S, B, r: (f'`{S.x} % {S.y} == 0`：`{S.y}` 是质因子' if S.x % S.y == 0 else f'`{S.x} % {S.y} != 0`：不是质因子'),
        'while x % y == 0': lambda S, B, r: (f'`{S.x}` 还能被 `{S.y}` 整除 → 除掉' if S.x % S.y == 0 else f'除干净了，剩余 `{S.x}`'),
        'x //= y': '除去一个 `{y}`，剩余 `x = {x}`',
        'cnt[v] += 1': '`{y}` 算一个不同的质因子 → `cnt[{v}] = {cnt[v]}`',
        'if x > 1': lambda S, B, r: (f'剩下 `{S.x} > 1`：是个大于 400 的质数，还要再算一个' if S.x > 1 else '剩下 `1`，分解完了'),
        'while stack and cnt[nums[stack[-1]]] < cnt[v]': lambda S, B, r: (
            f'栈顶 `{S.nums[S.stack[-1]]}` 的 cnt `{S.cnt[S.nums[S.stack[-1]]]}` < 当前 `{S.cnt[S.v]}`：右边第一个更多的就是当前 → 定下 right'
            if S.stack and S.cnt[S.nums[S.stack[-1]]] < S.cnt[S.v] else '栈空或栈顶 cnt 不小于当前，停'),
        'right[stack[-1]] = index': '栈顶的 `right` = `{index}`',
        'stack.append(index)': '`{index}` 入栈',
        'while stack and cnt[nums[stack[-1]]] <= cnt[v]': lambda S, B, r: (
            f'栈顶 `{S.nums[S.stack[-1]]}` 的 cnt `{S.cnt[S.nums[S.stack[-1]]]}` <= 当前 `{S.cnt[S.v]}`：左边第一个 `>=` 的就是当前 → 定下 left（并列也算）'
            if S.stack and S.cnt[S.nums[S.stack[-1]]] <= S.cnt[S.v] else '栈空或栈顶 cnt 更大，停'),
        'left[stack[-1]] = index': '栈顶的 `left` = `{index}`',
        'for v, freq in sorted': '按数值从大到小：`{v}` 可用 `freq = {freq}` 次，剩余 `k = {k}`',
        'if k > freq': lambda S, B, r: (f'`k = {S.k} > freq = {S.freq}`：用满 `freq` 次，还有剩' if S.k > S.freq else f'`k = {S.k} <= freq = {S.freq}`：只需 `k` 次，做完就结束'),
        'res *= quickPow(v, freq)': '`res` 乘上 `{v}^{freq}`（快速幂：指数折半递归，每层平方）',
        'k -= freq': '用掉 `freq` 次，剩余 `k = {k}`',
        'res *= quickPow(v, k)': '最后 `k = {k}` 次：`res` 乘上 `{v}^{k}`，取模后返回 `res`',
        'return res': '最大分数 =={ret}==',
    },
    cards=dict(
        one_liner='先算每个数的质因子数，再看每个数能用几次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次选没选过的子数组，分数乘以其中质因子数最多的数（并列取最左）',
                 '至多操作 `k` 次，求最大分数 mod `10^9+7`',
                 '示例：`[19,12,14,6,10,18]`，`k = 3` → `4788`',
                 '本视频：`[2,6,3,6]`，`k = 8` → `6^8 = 1679616`'],
        quote='题目的描述比较复杂，不妨从结果出发一步步反推。',
        quote_src='—— yiduobo 题解原文',
        idea=['数都是正的，应该优先用大的数；每个位置的使用次数有上限',
              '位置 `index` 能用几次 = 以它为质因子数最多者的子数组个数，用单调栈求左右边界',
              '`cnt` 左 `>=`、右 `>`：并列只取最左；数值和次数打包，从大到小排序用快速幂'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：分解后剩下大于 1 的数，必是大质数，要再加 1',
                 '易错：左边界用 `>=`，右边界用 `>`',
                 '原文为 Python 2 写法，已改为：`p = range(400)` → `list(range(400))`，`x /= y` → `x //= y`，`x / 2` → `x // 2`',
                 '前 16 行是用筛法求 400 以内的质数，为节省时间直接跳过，视频里不逐步演示'],
        before=[dict(heading='先备好质数表', lines=['用筛法求出 `400` 以内的所有质数 `prime_list`', '因为 `v <= 10^5`，分解只需试除到 `sqrt(10^5)`', '分解后若还剩大于 1 的数，它一定是一个大质数'])],
    ),
)
