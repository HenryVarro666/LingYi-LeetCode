_L = lambda S: S['_inner'].get('level') if 'level' in S['_inner'] and 'cnt' in S['_inner'] else None


def _state(S):
    I = S['_inner']
    if 'level' in I and 'cnt' in I:
        st = '==等于 n 的前缀==' if I['state'] else '已经 ==小于 n 的前缀=='
        return f"`calc(level={I['level']}, cnt={I['cnt']}, state={I['state']})`：已放 {I['cnt']} 个 1（目标恰好 {S['x']} 个），{st}"
    if 'x' in S and 'f' in S:
        return f"当前 `x = {S['x']}`，`f[x] = {S['f'][S['x']]}`，需要 `f[x] == k − 1 = {S['k'] - 1}`"
    return '先预处理 f（1..50 的深度），再对符合条件的 x 数「恰好 x 个 1」'


CONFIG = dict(
    num=3621, title='位计数深度为 K 的整数数目 I', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='预处理 f[1..50] + 数位 DP（state 表示是否贴着 n）',
    tags=['灵神题单', '动态规划', '难度分 3352'],
    code='''
class Solution(object):
    def popcountDepth(self, n, k):
        
        if k == 0:
            return 1

        f = [None] * 51
        f[1] = 0
        for v in range(2, 51):
            x = v
            step = 0
            while f[x] is None:
                cnt = 0
                while x:
                    if x % 2 == 1:
                        cnt += 1
                    x //= 2
                x = cnt
                step += 1
            f[v] = step + f[x]
        
        bound = []
        while n:
            bound.append(n % 2)
            n //= 2
        bound.reverse()
        
        def calc(level, cnt, state, g):
            if level == len(bound):
                if cnt == x:
                    return 1
                else:
                    return 0
            
            if g[level][cnt][state] is None:
                g[level][cnt][state] = 0
                start = 0
                end = 1
                if state == 1 and bound[level] == 0:
                    end = 0

                for d in range(start, end + 1):
                    nxt_cnt = cnt + d
                    if state == 1 and d == bound[level]:
                        nxt_state = 1
                    else:
                        nxt_state = 0
                    
                    if nxt_cnt <= x:
                        g[level][cnt][state] += calc(level + 1, nxt_cnt, nxt_state, g)
            
            return g[level][cnt][state]

        res = 0
        for x in range(1, 51):
            if f[x] == k - 1:
                g = [[[None] * 2 for _ in range(x + 1)] for _ in range(len(bound))]
                res += calc(0, 0, 1, g)
                if x == 1:
                    res -= 1
        
        return res
''',
    call='Solution().popcountDepth(3, 2)',
    expect=1,
    skip=['f = [None]', 'f[1] = 0', 'for v in range', 'x = v', 'step = 0', 'while f[x] is None', 'cnt = 0', 'while x:',
          'if x % 2 == 1', 'cnt += 1', 'x //= 2', 'x = cnt', 'step += 1', 'f[v] = step', 'if k == 0', 'return 1',
          'n //= 2', 'bound.append', 'bound.reverse', 'while n:', 'start = 0', 'end = 1', 'end = 0',
          'g[level][cnt][state] = 0', 'nxt_cnt = cnt + d', 'nxt_state = ', 'for x in range(1, 51)', 'if f[x] == k - 1',
          'if state == 1 and bound[level] == 0', 'else:', 'res = 0', 'if x == 1', 'res -= 1', 'bound = []',
          'for d in range'],
    views=[
        dict(type='array', var=lambda S: [('-' if v is None else v) for v in S['f'][:9]],
             label='f[x]：x 的位计数深度（只显示 0..8，x≤50 都已算好）', cell=70, h=170),
        dict(type='array', var='bound', label='bound = n 的二进制（蓝箭头 = 正在填第 level 位）', cell=70, h=210,
             pointers={_L: 'blue'}, pointer_labels={_L: 'level'},
             color=lambda S, i, v: 'blue' if i == _L(S) else None),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=200, hide=('g',)),
    ],
    watch=[('x', lambda S: S.get('x', '-'), 'cyan'),
           ('level', lambda S: S['_inner'].get('level', '-'), 'blue'),
           ('cnt', lambda S: S['_inner'].get('cnt', '-'), 'yellow'),
           ('state', lambda S: S['_inner'].get('state', '-'), 'pink'),
           ('res', lambda S: S.get('res', '-'), 'green')],
    captions={
        'g = [[[': lambda S, B, r: f"`f[{S.x}] = {S.f[S.x]} = k − 1`：这样的 `x` 一次操作后再 {S.k - 1} 次变成 1。数 `[1, n]` 里==恰好有 {S.x} 个 1==的数，给它建备忘录 `g`",
        'res += calc': '从最高位开始填，`state = 1`（还贴着 n 的前缀）：`calc(0, 0, 1)`，结果累计进 `res`',
        'if level == len(bound)': lambda S, B, r: (f"填满 {len(S.bound)} 位：`cnt = {S['_inner']['cnt']}`，目标 `x = {S.x}` → " +
                                                   ('==恰好相等，算 1 种==' if S['_inner']['cnt'] == S.x else '个数不对，算 0 种'))
                                                  if S['_inner']['level'] == len(S.bound) else f"`level = {S['_inner']['level']}`，还没填满",
        'if cnt == x': lambda S, B, r: ('`cnt == x`：1 的个数恰好是 x → 返回 1' if S['_inner']['cnt'] == S.x else '`cnt != x` → 返回 0'),
        'if g[level][cnt][state] is None': '备忘录：没算过才往下算（这里的 `g` 是每个 `x` 重新建的）',
        'if nxt_cnt <= x': '放完这一位 1 的个数是 `{nxt_cnt}`，目标恰好 `{x}` 个：==超过 x 就不用再往下算==',
        'if state == 1 and d == bound': '`state = {state}`，`d = {d}`，`bound[{level}] = {bound[level]}`：只有「还贴着 n 且 d 和 n 这一位相同」，下一位才继续受 n 约束',
        'g[level][cnt][state] += calc': '这一位填 `d`：`state` 保持 1 只有当「贴着 n 且 d 等于 n 的这一位」，其余都变成 0，交给下一位',
        'return g[level]': '这个状态的方案数 ==`{ret}`==',
        'return res': '答案 ==`{res}`==',
    },
    max_steps=46,
    cards=dict(
        one_liner='n 不到 2^50，先预处理 1..50 的深度，再数「恰好 x 个 1」',
        complexity='时间约 `O(log³ n)`，空间 `O(log² n)`',
        problem=['`popcount-depth`：不断取二进制 1 的个数，直到变成 1 所需的最少次数',
                 '数出 `[1, n]` 中深度==恰好==等于 `k` 的整数个数',
                 '本视频：`n=3, k=2` → `1`（只有 3）'],
        quote='10^15刚好小于2^50，也就是说在对于1到n之间的任意整数x，在一次操作后，其对应的p[1] <= 50。基于这一点，就可以先预处理出1到50的位计数深度',
        quote_src='—— yiduobo 题解原文',
        idea=['`x ≤ 10^15 < 2^50`：一次操作后一定落在 `1..50`',
              '`f[x] == k − 1` 的 `x`：数恰好有 x 个 1 的数',
              '`calc` 里 `state = 1` 表示前缀还和 `n` 相同'],
        before=[dict(heading='预处理（视频中略过）', lines=['`f[v]`：反复取 popcount 直到碰到已算出的数', '`f[1] = 0`，其余 `f[v] = step + f[x]`', '1..50 的结果在开头已经算好'])],
        summary=['时间约 `O(log³ n)`，空间 `O(log² n)`',
                 '`k = 0` 只有 `x = 1`；`k = 1` 时 `x = 1` 的 `f` 也等于 0，但不应计入，所以 `res -= 1`',
                 '`cnt` 超过 `x` 时剪枝，`g` 对每个 `x` 重建',
                 '原文已是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神用 `bit_count` 和 `@cache`，只枚举到 n 的位数；yiduobo 直接预处理到 50'],
    ),
)
