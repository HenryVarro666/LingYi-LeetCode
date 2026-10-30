def _txt(S):
    ln = S.get('_line', 0)
    if ln >= 36 and 'num' in S:
        pc = S.get('prime_cnt', [])
        return f'`num = {S["num"]}`，质因子次数 `{pc}`：`delta` = 各 `c[次数]` 相乘；`res` 累计 = ==结尾 1 的 1 种 + 其余=='
    if ln >= 22 and 'now' in S:
        return f'筛法：`f[i]` 记录 `i` 的一个质因子；现在 `now = {S["now"]}`'
    if ln >= 7:
        return '递推杨辉三角一行 `f`：`C(i, j) = C(i-1, j-1) + C(i-1, j)`；`i ≥ n` 时取 `c[k] = C(n+k-1, k)`'
    return '先算组合数 `c[k]`，再筛质因子，最后对每个结尾 `num` 累加'


CONFIG = dict(
    num=2338, title='统计理想数组的数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='指数序列 + 插板法',
    tags=['数论', '组合数学', '难度分 2615'],
    code='''
class Solution(object):
    def idealArrays(self, n, maxValue):
        
        mod = 10 ** 9 + 7

        f = [0] * 14
        c = [1]
        for i in range(1, n + 13):
            g = f[:]
            f = []
            for j in range(min(i + 1, 14)):
                if j == 0 or j == i:
                    f.append(1)
                else:
                    f.append(g[j - 1] + g[j])
                    if f[-1] >= mod:
                        f[-1] -= mod

            if i >= n:
                c.append(f[i - n + 1])

        f = list(range(maxValue + 1))
        now = 2
        while now * now <= maxValue:
            if f[now] == now:
                for index in range(now + now, maxValue + 1, now):
                    if f[index] == index:
                        f[index] = now
            now += 1

        res = 1
        for num in range(2, maxValue + 1):
            now = num
            prime_cnt = []
            last_prime = None

            while now != 1:
                if f[now] == last_prime:
                    prime_cnt[-1] += 1
                else:
                    prime_cnt.append(1)
                    last_prime = f[now]
                
                now //= f[now]
            
            delta = 1
            for cnt in prime_cnt:
                delta = delta * c[cnt] % mod
            
            res = (res + delta) % mod
        
        return res
''',
    call='Solution().idealArrays(3, 4)',
    expect=13,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='f', label='f（先是杨辉三角的一行，后是 f[i] = i 的一个质因子）', cell=64, h=130,
             color=lambda S, i, v: 'blue' if 'now' in S and S.get('_line', 0) >= 22 and i == S['now'] else None),
        dict(type='array', var='c', label='c[k] = C(n+k-1, k)：k 个质因子放进 n 个位置的方案数', cell=84, h=130,
             color=lambda S, i, v: 'cyan' if 'prime_cnt' in S and S.get('_line', 0) >= 36 and i in S['prime_cnt'] else None),
        dict(type='array', var=lambda S: S['prime_cnt'] if 'prime_cnt' in S else [], label='prime_cnt（当前 num 的各质因子次数）', cell=84, h=130),
    ],
    watch=['n', 'maxValue', 'i', ('num', 'num', 'blue'), 'delta', ('res', 'res', 'green')],
    skip=['g = f[:]', 'f = []', 'for j in range', 'if j == 0 or j == i', 'if f[-1] >= mod', 'f[-1] -= mod', 'now += 1', 'for index in range', 'if f[index] == index', 'mod = 10', 'last_prime = None', 'for i in range(1, n + 13)', 'f.append(1)', 'f.append(g[j - 1] + g[j])', 'if i >= n', 'prime_cnt = []', 'now = num', 'last_prime = f[now]', 'for cnt in prime_cnt'],
    max_steps=80,
    captions={
        'f = [0] * 14': '`f` 保存杨辉三角当前行，最多用到 14 列（`2^14 > 10000`，指数最大 13）',
        'c = [1]': '`c[k]`：以 `k` 结尾的递增指数序列数；`c[0] = 1`',
        'for i in range(1, n + 13)': '递推到第 `i = {i}` 行（只需到 `n + 12`）',
        'f.append(1)': '边界 `C(i, 0) = C(i, i) = 1`',
        'f.append(g[j - 1] + g[j])': '`C({i}, {j}) = C({i-1}, {j-1}) + C({i-1}, {j}) = {f[-1]}`',
        'if i >= n': lambda S, B, r: (f'`i = {S.i} ≥ n = {S.n}`：这一行的第 `i-n+1` 项就是 `C(n+k-1, k)`' if S.i >= S.n else f'`i = {S.i} < n = {S.n}`，还没到需要的行'),
        'c.append': '杨辉三角推到第 `i = {i}` 行：`c[{len(c)-1}] = C({i}, {i-n+1}) = {c[-1]}`',
        'f = list(range': '`f[i] = i`：先认为每个数的质因子是自己（原文 `f = range(...)`，Python 3 需转成 list）',
        'now = 2': '从 `now = 2` 开始做一遍筛法',
        'while now * now <= maxValue': lambda S, B, r: (f'`{S.now}² = {S.now ** 2} ≤ {S.maxValue}`，继续' if S.now ** 2 <= S.maxValue else '筛完了：`f[i]` 是 `i` 的最小质因数'),
        'if f[now] == now': lambda S, B, r: (f'`f[{S.now}] = {S.now}`：==质数==，筛它的倍数' if S.f[S.now] == S.now else f'`f[{S.now}] = {S.f[S.now]}`：合数，跳过'),
        'f[index] = now': '`f[{index}] = {now}`：`{index}` 第一次被筛到，最小质因数记为 `{now}`',
        'res = 1': '`res` 初值 1：以 1 结尾的数组只有「全是 1」这一种',
        'for num in range': lambda S, B, r: ('结尾 `2..maxValue` 都枚举完了' if 'num' in B and B.num == S.num else f'枚举结尾 `num = {S.num}`'),
        'now = num': '`now` 从 `num = {num}` 开始，不断除以最小质因数',
        'prime_cnt = []': '`prime_cnt` 记录每个质因子的次数',
        'while now != 1': lambda S, B, r: (f'`now = {S.now} ≠ 1`，还有质因子' if S.now != 1 else f'`now = 1`：分解完，次数 `{S.prime_cnt}`'),
        'if f[now] == last_prime': lambda S, B, r: (f'`f[{S.now}] = {S.f[S.now]}` 与上一个质因子相同 → 次数 +1' if S.f[S.now] == S.last_prime else f'`f[{S.now}] = {S.f[S.now]}` 是新的质因子 → 开一项'),
        'prime_cnt[-1] += 1': '这个质因子次数变成 `{prime_cnt[-1]}`',
        'prime_cnt.append(1)': '新质因子，次数 1：`{prime_cnt}`',
        'now //= f[now]': '`now` 除掉 `{B.f[B.now]}` → {now}（原文 `/=`，Python 3 改为 `//=`）',
        'delta = 1': '`delta` = 以 `{num}` 结尾的方案数，各质因子独立相乘',
        'for cnt in prime_cnt': '取次数 `cnt = {cnt}`',
        'delta = delta * c[cnt]': '这个质因子次数 `{cnt}`：`delta` × `c[{cnt}] = {c[cnt]}` → {delta}',
        'res = (res + delta)': '以 `{num}` 结尾共 `{delta}` 个 → `res = {res}`',
        'return res': '把所有结尾的方案数加起来：`{ret}`',
    },
    cards=dict(
        one_liner='把每个数写成质因数的指数，每个质因子的指数序列单调递增，用插板法数',
        complexity='时间 `O((n+13)·14 + maxValue·log)`，空间 `O(maxValue)`',
        problem=['长为 `n` 的数组，每个数在 `1..maxValue`，==每个数被前一个数整除==',
                 '求不同理想数组的个数，对 `10^9+7` 取余',
                 '示例：`n = 2, maxValue = 5` → `10`',
                 '本视频：`n = 3, maxValue = 4` → `13`'],
        quote='可以发现，不同质因子的指数是互不影响的……问题实际上就转化成了有多少个长度为i，且最后一个元素为……的递增数组的数目。',
        quote_src='—— yiduobo 题解原文（节选）',
        idea=['`dp[i][j]` 太大：改从质因数入手，`j = p0^k0 · p1^k1 …`',
              '每个质因子的指数从左到右非递减，最后一个等于 `k` → 插板法 `C(i+k-1, k)`',
              '不同质因子互不影响：相乘得到以 `j` 结尾的方案数',
              '递推杨辉三角求 `c`（不用逆元），再筛法求最小质因数分解每个 `j`'],
        summary=['以 `1` 结尾只有 1 种，所以 `res` 初值 1，从 `num = 2` 枚举',
                 '`c[k]` 只需 `k ≤ 13`（`2^13 ≤ 10000 < 2^14`），杨辉三角只算 14 列',
                 '原文为 Python 2 写法，已改为：`f = range(...)` → `list(range(...))`，`now /= f[now]` → `now //= f[now]`',
                 '易错：`i ≥ n` 才取 `f[i-n+1]` 作为 `c`；`f` 变量先后存了两种东西',
                 '对比灵神：灵神把「商分」看作放球，直接按 `C(n+e-1, e)` 乘起来'],
    ),
)
