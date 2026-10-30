K0, X0 = 7, 2
W = ((K0 + 1) << X0).bit_length()   # 6 位


def _bits(S):
    if 'num' not in S:
        return None
    return [str(S['num'] >> j & 1) for j in range(W - 1, -1, -1)]


def _pos(S):
    return W - 1 - S['i'] if 'i' in S else None


def _fml(S):
    if 'cnt' not in S or 'i' not in S:
        return '从高位到低位试填：这一位填 1，会让 1 到 num-1 的价值和增加 `cnt`'
    i, x = S['i'], X0
    return (f'填 1 的增量 `cnt` = `pre1 × 2^{i}` + `{i}//{x} × 2^{max(i - 1, 0)}` = '
            f'{S["pre1"]} × {1 << i} + {i // x} × {(1 << i) >> 1} = =={S["cnt"]}==')


CONFIG = dict(
    num=3007, title='价值和小于等于 K 的最大数字', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='试填法（逐位构造）',
    tags=['位运算', '难度分 2258'],
    code='''
class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        num = pre1 = 0
        for i in range(((k + 1) << x).bit_length() - 1, -1, -1):
            cnt = (pre1 << i) + (i // x << i >> 1)
            if cnt <= k:
                k -= cnt
                num |= 1 << i
                pre1 += (i + 1) % x == 0
        return num - 1
''',
    call=f'Solution().findMaximumNumber({K0}, {X0})',
    expect=9,
    skip=['num = pre1 = 0'],
    views=[
        dict(type='text', fn=_fml, size=26, h=100),
        dict(type='array', var=_bits, index=False, label='num 的二进制（左高右低；蓝色 = 正在试填的第 i 位，绿色 = 已填 1，暗 = 还没试）',
             cell=100, h=300,
             dim=lambda S, i, v: 'i' in S and i > W - 1 - S['i'],
             color=lambda S, i, v: ('blue' if i == W - 1 - S['i'] else 'green' if v == '1' else None) if 'i' in S else None),
        dict(type='text', fn=lambda S: (f'剩余预算 `k` = =={S["k"]}==；已填的 1 里，位置（从 1 数）是 x 的倍数的有 `pre1` = =={S["pre1"]}== 个'
                                         if 'pre1' in S else ''), size=24, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'orange'), ('k', 'k', 'yellow'), ('pre1', 'pre1', 'purple'), ('num', 'num', 'green')],
    captions={
        'for i in range': lambda S, B, r: (
            f'上界 `(k+1)<<x` = {(K0 + 1) << X0}，二进制 {W} 位 → 从第 `{S["i"]}` 位开始试填（再高的位一定填不下）'
            if S.get('i') == W - 1 and B.get('i') is None else
            (f'第 `{S["i"]}` 位（从低到高、从 0 数）：试着填 1' if 'i' in S and S.get('i') != B.get('i') else '所有位都试完了')),
        'cnt = (pre1 << i)': ('第 `{i}` 位填 1，多出 `2^{i}` 个更小的数：每个数在高位都有 `pre1 = {pre1}` 个有效 1 → `{pre1} × 2^{i}`；'
                              '低位有 `{i}//{x} = {i // x}` 个有效位，各有 `2^{max(i-1,0)}` 个 1 → cnt = =={cnt}=='),
        'if cnt <= k': lambda S, B, r: (
            f'`cnt = {S["cnt"]}` ≤ `k = {S["k"]}`：预算够 → 这位==填 1==（高位尽量大，答案才最大）'
            if S['cnt'] <= S['k'] else f'`cnt = {S["cnt"]}` > `k = {S["k"]}`：预算不够，这位只能==填 0=='),
        'k -= cnt': '花掉预算：`k` = {B.k} − {cnt} = =={k}==',
        'num |= 1 << i': '第 `{i}` 位填 1：`num` = =={num}==（二进制 `{num:b}`）',
        'pre1 += (i + 1) % x == 0': lambda S, B, r: (
            f'编号 `i+1 = {S["i"] + 1}` 是 `x = {X0}` 的倍数 → `pre1` 加一，以后更低的位都会多算它'
            if (S['i'] + 1) % X0 == 0 else f'编号 `i+1 = {S["i"] + 1}` 不是 `x = {X0}` 的倍数 → `pre1` 不变'),
        'return num - 1': '循环里算的是==小于 num==的价值和，所以合法的最大数是 `num - 1` = =={num - 1}=='
    },
    cards=dict(
        one_liner='从高位到低位试填：能填 1 就填 1，预算 k 扣掉新增价值',
        complexity='时间 `O(x + log k)`，空间 `O(1)`',
        problem=['`num` 的价值 = 二进制里第 `x, 2x, 3x…` 位（从低位数起，从 1 计）上 1 的个数',
                 '累加价值 = 从 1 到 num 的价值之和；要求累加价值 ≤ `k`，求最大的 `num`',
                 '示例：`k = 7, x = 2` → `9`'],
        quote='如果 cnt ≤ k，那么这个比特位可以填 1。由于我们是从高到低考虑的，能填 1 就填 1，这会让答案尽量大。然后把 k 减少 cnt。',
        quote_src='—— 灵茶山艾府题解（方法三 试填法）',
        idea=['`num` 越大价值和越大，所以从最高位开始贪心地试填',
              '第 i 位填 1 会多出 `2^i` 个更小的数：高位已有 `pre1` 个有效 1，加上低位的有效位贡献',
              '上界取 `(k+1)<<x`：它的价值和一定 ≥ k+1，不会填过头'],
        summary=['时间 `O(x + log k)`：只枚举二进制位，没有二分',
                 '易错：算的是小于 num 的价值和，返回要 `num - 1`',
                 '易错：比特位编号从 0 开始，所以 `pre1` 判断的是 `(i + 1) % x == 0`',
                 '另外两种写法：方法一 二分答案 + 数位 DP，方法二 二分答案 + 数学公式，复杂度更高但更直观'],
    ),
)
