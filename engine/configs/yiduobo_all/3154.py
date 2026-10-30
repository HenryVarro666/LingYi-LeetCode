K = 6


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 26:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i - 1, j), (i - 1, j - 1)):
        return 'blue'
    return None


def _txt(S):
    if 'd' not in S:
        return f'`k = {S["k"]}`：先确定操作二的次数 `jump`，再算操作一的次数 `d`'
    jp, d = S['jump'], S['d']
    return f'`jump = {jp}`，`d = 2^{jp} − {S["k"]} = {d}`：在 `{jp + 1}` 个空隙里选 `{d}` 个 → `C({jp + 1}, {d})`'


CONFIG = dict(
    num=3154, title='到达第 K 级台阶的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='组合数 + 杨辉三角 DP',
    tags=['数学算法', '难度分 2071'],
    code='''
class Solution(object):
    def waysToReachStair(self, k):

        if k == 0:
            return 2
        
        if k == 1:
            return 4
        
        if k == 2:
            return 4

        if k == 4:
            return 2
        
        jump = len(bin(k - 1)) - 2
        d = (1 << jump) - k

        if d > jump + 1:
            return 0

        c = [[0] * (d + 1) for _ in range(jump + 2)]
        for i in range(jump + 2):
            c[i][0] = 1
            for j in range(1, min(i, d) + 1):
                c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
        
        return c[jump + 1][d]
''',
    call=f'Solution().waysToReachStair({K})',
    expect=6,
    skip=['for j in range', 'c[i][0] = 1'],
    views=[
        dict(type='text', size=28, h=70, fn=_txt),
        dict(type='table', var='c', label='c[i][j] = C(i, j)（黄 = 正在算，蓝 = 它依赖的两格）', h=420, cell=96,
             cursors=[], color=_cell),
    ],
    watch=[('k', 'k', 'blue'), ('jump', 'jump', 'pink'), ('d', 'd', 'cyan'), ('i', 'i', 'yellow'), ('j', 'j', 'yellow')],
    captions={
        'if k == 0': '先处理特殊的 k：0、1、2、4 要考虑多跳一次再用大量操作一回填，答案固定',
        'if k == 1': '`k = 1` 不是 0，继续看下一个特殊值',
        'if k == 2': '`k = 2` 也不是特殊值，继续',
        'if k == 4': '`k = 4` 也不是特殊值：`k = {k}` 属于“jump 唯一”的普通情况',
        'jump = len(bin': '最小的 `jump` 满足 `2^jump >= k`，就是 `k - 1` 的二进制位数：`bin({k - 1})` → `jump = {jump}`',
        'd = (1 << jump)': '走完 `jump` 次操作二共 `2^jump − 1` 级，`1 + 2^jump − 1 − d = k` → `d = {1 << jump} − {k} = {d}`',
        'if d > jump + 1': lambda S, B, r: (f'`d = {S.d} > jump + 1 = {S.jump + 1}`：操作一不能连续，放不下 → 返回 0' if S.d > S.jump + 1
                                            else f'`d = {S.d} ≤ jump + 1 = {S.jump + 1}`：{S.jump + 1} 个空隙放得下 {S.d} 个操作一'),
        'c = [[0]': '建杨辉三角表：`jump + 2 = {jump + 2}` 行、`d + 1 = {d + 1}` 列，只算到第 `d` 列就够了',
        'for i in range': lambda S, B, r: ('杨辉三角算完，目标格 `c[{0}][{1}]` 已就绪'.format(S.jump + 1, S.d) if S.get('i') == B.get('i')
                                           else f'第 `i = {S.i}` 行，先写 `c[{S.i}][0] = 1`：一个都不选只有 1 种'),
        'c[i][j] = c[i - 1][j]': '`C({i}, {j}) = C({i - 1}, {j}) + C({i - 1}, {j - 1})` = `{c[i - 1][j]} + {c[i - 1][j - 1]}` = =={c[i][j]}==',
        'return c[jump + 1][d]': '`C({jump + 1}, {d})` = =={ret}==：在 {jump + 1} 个空隙中选 {d} 个放操作一',
    },
    cards=dict(
        one_liner='jump 取最小值，d 由 jump 决定，再用杨辉三角求 C(jump+1, d)',
        complexity='时间 `O(log^2 k)`，空间 `O(log^2 k)`',
        problem=['无限台阶，从第 `1` 级出发，到第 `k` 级有几种走法',
                 '操作一：下走一级，不能连续；操作二：上走 `2^jump` 级且 `jump` 加 1',
                 '可以先到 `k` 再走回 `k`；本视频演示 `k = 6` → `6`'],
        quote='第二种操作执行jump次后，走过的台阶数一共是2^0 + 2^1 + ... + 2^(jump - 1) = 2^jump - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['设操作一 `d` 次：`1 + 2^jump − 1 − d = k`，`d` 增长是线性的、`jump` 是指数的',
              '操作一不能连续，最多插进 `jump + 1` 个空隙：`d <= jump + 1`，所以 jump 要尽量小',
              '`jump` 唯一时方案数 `C(jump+1, d)`；只有 `k = 0/1/2/4` 要多考虑几种 jump，直接返回答案'],
        summary=['特殊值：`k = 0、1、2、4` 的答案分别是 2、4、4、2',
                 '`d > jump + 1` 时无解；原文文字写“返回 -1”，但代码返回 0，与题目一致',
                 '组合数用 `C(m, n) = C(m-1, n) + C(m-1, n-1)` 递推，列数只开到 `d`',
                 '对比灵神：灵神枚举 j 累加，不需要特判；yiduobo 证明只有 4 个 k 要特判'],
    ),
)
