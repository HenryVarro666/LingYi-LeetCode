NUMS = [6, 10, 3, 9, 5]


def _txt(S):
    if 'best' in S and 'f' in S and 'index' in S and S['index'] < len(NUMS):
        i = S['index']
        ps = sorted(S['prime_set_map'].get(NUMS[i], []))
        return f"`nums[{i}] = {NUMS[i]}` 的质因子：{'、'.join(map(str, ps))}；`best[p]` = 含因子 p 的位置里最小的 `f[x-1]`"
    if 'prime_set_map' in S:
        return '给每个数分解质因数：`prime[x]` 是 `x` 的最大质因子，反复 `x //= prime[x]`'
    if 'prime' in S:
        return '筛法：把每个数标上它的最大质因子 `prime[x]`（质数自己标自己）'
    return ''


def _sieve(S):
    return S.get('prime') if isinstance(S.get('prime'), list) else None


CONFIG = dict(
    num='LCP 14', title='切分数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='DP + 质因子最小值 best[p]',
    tags=[],
    code='''
class Solution(object):
    def splitArray(self, nums):

        max_num = max(nums)
        prime = list(range(max_num + 1))
        now = 2
        while now * now <= max_num:
            if prime[now] == now:
                tmp = now + now
                while tmp <= max_num:
                    prime[tmp] = now
                    tmp += now
            now += 1

        prime_set_map = {}
        for num in nums:
            if num not in prime_set_map:
                prime_set_map[num] = set()
                now = num
                while now != 1:
                    prime_set_map[num].add(prime[now])
                    now //= prime[now]
        
        best = {}
        f = []
        for index in range(len(nums)):
            if index == 0:
                f.append(1)
            else:
                f.append(f[-1] + 1)

            for p in prime_set_map[nums[index]]:
                if index == 0:
                    best[p] = 0
                else:
                    if p not in best or best[p] > f[index - 1]:
                        best[p] = f[index - 1]
                    f[-1] = min(f[-1], best[p] + 1)
        
        return f[-1]
''',
    call='Solution().splitArray([6, 10, 3, 9, 5])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=60),
        dict(type='array', var='prime', label='prime[x]：x 的最大质因子（筛出来的）', h=150, color=lambda S, i, v: ('green' if i == v and i >= 2 else None)),
        dict(type='array', var='nums', label='nums', h=200, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f[i]：nums[0..i] 最少切成几个子数组', h=150),
        dict(type='map', var='best', label='best[p]：含质因子 p 的位置里，最小的 f[x-1]', h=170, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'blue'), 'p'],
    captions={
        'max_num = max': '最大值 `max_num = {max_num}`：筛法只需处理到它',
        'prime = list': '`prime[x]` 先设成 `x` 自己，表示「还没被更小的质数标过」',
        'while now * now': '`now = {now}`：只需筛到 `√{max_num}`，更大的合数一定有更小的质因子',
        'if prime[now] == now': lambda S, B, r: (f'`prime[{S.now}] == {S.now}`：{S.now} 是质数 → 把它的倍数都标成 {S.now}（后标的覆盖先标的，留下的是最大质因子）'
                                                 if S.prime[S.now] == S.now else f'`prime[{S.now}] = {S.prime[S.now]}`：已被标过，不是质数，跳过'),
        'now += 1': '倍数标完了，看上面的 `prime` 数组；`now` → {now}',
        'prime_set_map = {}': '`prime_set_map[x]`：`x` 的质因子集合，之后 DP 直接用',
        'for num in nums': lambda S, B, r: ('所有数都分解完了' if B.get('num') == S.num and S.num == S.nums[-1] else f'分解 `{S.num}`'),
        'prime_set_map[num].add': '`prime[{now}] = {prime[now]}` 是 `{now}` 的最大质因子 → 记下，然后 `now //= {prime[now]}` 继续分解',
        'for index in range': lambda S, B, r: ('所有位置都算完了' if B.get('index') == S.index and len(S.f) == len(S.nums) else f'处理 `nums[{S.index}] = {S.nums[S.index]}`'),
        'f.append(1)': '`index = 0`：第一个数自己成一个子数组，`f[0] = 1`',
        'f.append(f[-1] + 1)': '先假设 `nums[{index}]` 自己单独成段（`gcd(x, x) = x > 1`）：`f[{index}] = f[{index - 1}] + 1 = {f[-1]}`',
        'best[p] = 0': '`index = 0`：质因子 `{p}` 第一次出现，`best[{p}] = 0`（前面没有数，段数 0）',
        'if p not in best': lambda S, B, r: (f'质因子 `{S.p}`：' + ('还没记录' if S.p not in S.best else f'`best[{S.p}] = {S.best[S.p]}` > `f[{S.index - 1}] = {S.f[S.index - 1]}`') + f' → 用 `f[{S.index - 1}]` 更新 `best`'
                                             if S.p not in S.best or S.best[S.p] > S.f[S.index - 1] else
                                             f'质因子 `{S.p}`：`best[{S.p}] = {S.best[S.p]}` 已经不比 `f[{S.index - 1}] = {S.f[S.index - 1]}` 大 → 不更新'),
        'best[p] = f[index - 1]': '`best[{p}] = f[{index - 1}] = {best[p]}`：含因子 {p} 的位置里，最小的前缀段数',
        'f[-1] = min': '`f[{index}] = min({B.f[-1]}, best[{p}] + 1 = {best[p] + 1})` = =={f[-1]}==：从含公共质因子 `{p}` 的最优位置切一刀',
        'return f[-1]': '`f[-1]` = =={f[-1]}==：最少切成的子数组个数',
    },
    skip=['tmp = now + now', 'while tmp <= max_num', 'prime[tmp] = now', 'tmp += now', 'now = num', 'prime_set_map[num] = set()', 'if num not in prime_set_map', 'while now != 1', 'now //= prime[now]',
          'best = {}', 'f = []', 'if index == 0', 'for p in prime_set_map'],
    max_steps=100,
    cards=dict(
        one_liner='f 只从「共享质因子」的最优位置转移：best[p] 记下每个质因子的最小 f',
        complexity='时间 `O(n log A + A log log A)`，空间 `O(A + n)`',
        problem=['把 `nums` 切成若干连续子数组，每个子数组的 ==第一个和最后一个数的最大公约数 > 1==',
                 '求最少切成几个子数组',
                 '本视频：`[6,10,3,9,5]` → `2`（`[6,10,3,9]` + `[5]`）'],
        quote='对于f[i]，不妨设0到i之间有两个位置j和k，满足nums[j]、nums[k]以及nums[i]都有某个大于1的约数p……best[p]表示当前已知的具有因子p的nums[x]中，f[x - 1]的最小值是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP：`f[i] = min(f[j-1] + 1)`，`j` 是和 `nums[i]` 不互质的位置，`O(n²)`',
              '不互质 = 有公共质因子 `p`。对同一个 `p`，只需要 `f[j-1]` ==最小== 的那个位置',
              '用 `best[p]` 维护，转移时只枚举 `nums[i]` 的质因子：先用 `f[i-1]` 更新 `best[p]`，再用 `best[p] + 1` 更新 `f[i]`'],
        summary=['时间 `O(n log A + A log log A)`，空间 `O(A + n)`，`A = max(nums)`',
                 '`f[i]` 先取 `f[i-1] + 1`（自己单独成段，`gcd(x,x) = x > 1`）',
                 '`best[p]` 要先用 `f[index-1]` 更新，再拿来转移',
                 '原文为 Python 2 写法，已把 `prime = range(max_num + 1)` 改为 `list(range(max_num + 1))`，整数除法 `now /= prime[now]` 改为 `now //= prime[now]`',
                 '题面库里缺失，题意按 LeetCode LCP 14 补写'],
    ),
)
