def _fmt(d):
    return ' '.join(f'{k}:{v}' for k, v in sorted(d.items())) if d else '·'


def _cur(S):
    idx = S.get('index')
    return None if idx is None else idx


def _t(which):
    def fn(S):
        idx = S.get('index')
        if idx is None or 'f' not in S:
            return [[]]
        return [[_fmt(d) for d in row] for row in S['f'][idx + which]]
    return fn


def _hl_src(S, r, c, v):
    if S.get('_line', 0) >= 28 and S.get('x') == r and S.get('state') == c:
        return 'blue'
    return None


def _hl_dst(S, r, c, v):
    if S.get('_line', 0) >= 34 and 'y' in S and 'nxt_state' in S and r == S['x'] + S['y'] and c == S['nxt_state']:
        return 'yellow'
    return None


def _top(S):
    if 'y' in S and 'nxt_state' in S and 'x' in S:
        return (f"再放 `y = {S['y']}` 个下标 `{S['index']}`：低位 `{S.get('nxt_delta', '?')}` 记入 `cnt`，截断后 `state = {S['nxt_state']}`")
    return '`f[index][x][state]`：dict 记录 {低位 1 的个数: 乘积和}；`state` = 幂次和去掉低位'


CONFIG = dict(
    num=3539, title='魔法序列的数组乘积之和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按下标 DP · 截断低位只记 1 的个数',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2694'],
    code='''
class Solution(object):
    def magicalSum(self, m, k, nums):
        
        n = len(nums)
        
        set_bit = [0] * (m + 1)
        for x in range(m + 1):
            tmp = x
            while tmp:
                set_bit[x] += 1
                tmp -= tmp & -tmp

        mod = 10 ** 9 + 7

        inv = [None, 1]
        for x in range(2, m + 1):
            inv.append(-(mod // x) * inv[mod % x] % mod)

        f = [[[{} for _ in range((m >> 1) + 1)] for _ in range(m + 1)] for _ in range(n + 1)]
        f[0][0][0][0] = 1
        for index in range(n):
            for x in range(m + 1):
                for state in range((x >> 1) + 1):
                    v = 1
                    for y in range(m - x + 1):
                        nxt_state = state + y
                        nxt_delta = nxt_state & 1
                        nxt_state >>= 1
                        if y > 0:
                            v = v * (m - x - y + 1) * inv[y] * nums[index] % mod

                        for cnt in f[index][x][state]:
                            nxt_cnt = cnt + nxt_delta
                            if nxt_cnt <= k:
                                f[index + 1][x + y][nxt_state][nxt_cnt] = (f[index + 1][x + y][nxt_state].get(nxt_cnt, 0) + f[index][x][state][cnt] * v % mod) % mod

        res = 0
        for state in range((m >> 1) + 1):
            res += f[-1][-1][state].get(k - set_bit[state], 0)
        
        return res % mod
''',
    call='Solution().magicalSum(2, 2, [5, 4])',
    expect=40,
    skip=[4, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 24, 28, 29, 37],
    max_steps=52,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='table', var=_t(0), label='f[index]（上一轮）：格子里是 {低位1个数: 乘积和}', h=230, cell=120,
             rows=['已选 0', '已选 1', '已选 2'], cols=['s=0', 's=1'], color=_hl_src),
        dict(type='table', var=_t(1), label='f[index+1]（这一轮在累加）', h=230, cell=120,
             rows=['已选 0', '已选 1', '已选 2'], cols=['s=0', 's=1'], color=_hl_dst),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'cyan'), ('state', 'state', 'orange'), ('y', 'y', 'pink'), ('cnt', 'cnt'), ('res', 'res', 'green')],
    captions={
        'f = [[[{}': '`f[index][x][state]` 是 dict：键 = 低位已有 1 的个数 `cnt`，值 = 乘积和',
        'f[0][0][0][0] = 1': '起点：什么都没选，`state = 0`，低位 1 的个数 0 → 方案 1',
        'for index in range(n)': lambda S, B, r: (f'考虑下标 `index = {S.index}`：决定它在序列里出现几次' if S.get('index') != B.get('index') or 'index' not in B else '所有下标都处理完'),
        'for x in range': lambda S, B, r: f'已选 `x = {S.x}` 个下标' if S.get('x') != B.get('x') else '这个下标处理完',
        'for state in range': lambda S, B, r: (f'`state = {S.state}`（幂次和去掉低位后的值，不超过 `x/2`）' if S.get('_line', 0) < 30
                                               else f'最后枚举剩下的 `state = {S.state}`：它自己还含 `{S.set_bit[S.state]}` 个 1'),
        'for y in range': lambda S, B, r: f'再放 `y = {S.y}` 个下标 `{S.index}`（剩余 `m - x = {S.m - S.x}` 个位置）',
        'nxt_state = state + y': '放 `y` 个 `2^index`，截断低位后对 `state` 的贡献就是 `y`：`state + y = {nxt_state}`',
        'nxt_delta = ': '最低位 `nxt_delta = {nxt_delta}`：它会被截掉、记进低位 1 的个数；`state` 右移一位 → `{nxt_state >> 1}`',
        'for cnt in f[index][x][state]': '枚举 dict 里已有的低位 1 个数 `cnt`',
        'nxt_cnt = ': '`nxt_cnt = cnt + nxt_delta = {cnt} + {nxt_delta} = {nxt_cnt}`',
        'if nxt_cnt <= k': lambda S, B, r: (f'`nxt_cnt = {S.nxt_cnt} ≤ k = {S.k}`，还有希望 → 转移' if S.nxt_cnt <= S.k else f'`nxt_cnt = {S.nxt_cnt} > k = {S.k}`：1 太多了 → 丢弃'),
        'f[index + 1][x + y]': lambda S, B, r: f'`f[{S.index + 1}][{S.x + S.y}][{S.nxt_state}][{S.nxt_cnt}]` += `{S.f[S.index][S.x][S.state][S.cnt]}` × `C(m−x, y)·nums[index]^y`(= `{S.v}`) → ==`{S.f[S.index + 1][S.x + S.y][S.nxt_state][S.nxt_cnt]}`=='
        if 'cnt' in S else '累加',
        'res += f[-1][-1]': lambda S, B, r: f'`state = {S.state}` 自带 `{S.set_bit[S.state]}` 个 1，低位还要 `k − {S.set_bit[S.state]} = {S.k - S.set_bit[S.state]}` 个 → `res = {S.res}`',
        'return res % mod': '所有合法序列的乘积和：==`{ret}`==',
    },
    cards=dict(
        one_liner='高位还没定的 1 才需要记，低位的 1 只记个数',
        complexity='时间约 `O(n·m^2·k·m)`，空间 `O(n·m^2)`',
        problem=['选 `m` 个下标（可重复），`Σ 2^seq[i]` 的二进制==恰有 `k` 个 1==',
                 '序列乘积为 `nums` 对应元素之积，求所有合法序列乘积之和（模 `10^9+7`）',
                 '本视频：`m=2, k=2, nums=[5,4]` → `40`'],
        quote='随着index的遍历，其对应的2^index也是越来越大的，对state二进制表示的0到index - 1这些数位不会产生任何影响，因此对于这些数位，只需要记录其中1的数目cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['按下标从小到大，`f[index][x][state]`：已选 `x` 个，`state` = 幂次和去掉低位',
              '放 `y` 个下标 `index`：`state += y`，最低位记入 `cnt`，再右移一位',
              '位置选法 `C(m-x, y)` 乘 `nums[index]^y`，用上一个 `y` 的结果乘一个系数递推出来'],
        summary=['`state` 不超过 `x/2`，所以状态不会爆炸',
                 '最后要加上 `state` 自己的 1：`k - set_bit(state)` 才是低位还需要的 1 的个数',
                 '`f` 的最内层用 dict，只存 `cnt ≤ k` 的状态；超过 `k` 直接丢',
                 '逆元 `inv` 用线性递推 `-(mod//x) * inv[mod % x]`，不需要 `pow`',
                 '对比灵神：灵神倒着做记忆化，用 `left_k` 倒扣；这里正着递推，用 `cnt` 正着累加'],
    ),
)
