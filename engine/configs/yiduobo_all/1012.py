def _idx(S):
    return S.get('index')


def _txt(S):
    if 'used' not in S or 'index' not in S:
        return '`f[k][l]` = 用 k 个不同数字排长度 l 的方案数：`f[k][l] = k * f[k-1][l-1]`'
    return f"已用数字 used = =={sorted(S['used'])}==，已经数到的无重复数 `res` = =={S['res']}=="


CONFIG = dict(
    num=1012, title='至少有 1 位重复的数字', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='正难则反 + 排列数 f[k][l] 逐位统计',
    tags=['灵神题单', '动态规划', '难度分 2230'],
    code='''
class Solution(object):
    def numDupDigitsAtMostN(self, N):

        f = [[0] * 11 for _ in range(11)]
        for k in range(1, 11):
            f[k][0] = 1
            for l in range(1, k + 1):
                f[k][l] = k * f[k - 1][l - 1]

        a = []
        l = 0
        tmp = N
        while tmp:
            a.append(tmp % 10)
            tmp //= 10
            l += 1
        
        used = set()
        res = 0
        for index in range(l - 1, 0, -1):
            res += f[10][index] - f[9][index - 1]
        for index in range(l - 1, -1, -1):
            for x in range(a[index]):
                if x in used or (index == l - 1 and x == 0):
                    continue
                res += f[10 - (l - 1 - index) - 1][index]

            if a[index] in used:
                break
            used.add(a[index])
            if index == 0:
                res += 1

        return N - res
''',
    call='Solution().numDupDigitsAtMostN(234)',
    expect=53,
    views=[
        dict(type='array', var='a', label='a = N 的数位（低位在前，蓝 = 当前位 index）', cell=80, h=160,
             pointers={'index': 'blue'}),
        dict(type='set', var='used', label='used：N 前缀已经用过的数字', h=110, fmt=lambda x: str(x)),
        dict(type='text', fn=_txt, size=24, h=90),
        dict(type='text', fn=lambda S: (f"N 位数 `l = {S['l']}`；上一类：位数更短的无重复数共 =={S['res']}==" if 'l' in S and 'index' not in S and S.get('res', 0) else ''), size=22, h=50),
    ],
    watch=[('index', _idx, 'blue'), ('x', lambda S: S.get('x'), 'pink'), ('l', 'l', 'cyan'), ('res', 'res', 'green')],
    skip=['for k in range', 'tmp //= 10', 'for index in range(l - 1, 0, -1)', 'for index in range(l - 1, -1, -1)', 'res = 0', 'f[k][0] = 1', 'a = []', 'l = 0', 'tmp = N', 'l += 1', 'used = set()', 'f[k][l] = k *', 'while tmp', 'for l in range(1, k + 1)', 'f[k][0]'],
    captions={
        'f = [[0] * 11': '预处理 `f[k][l] = k * f[k-1][l-1]`：用 `k` 个不同数字排成长度 `l` 的方案数（第一位有 `k` 种选法，其余是子问题）',
        'a.append': '取出个位 `{a[-1]}`，剩下 `{tmp}` 继续',
        'res += f[10][index] - f[9][index - 1]': '位数更短的无重复数：长度 `{index}` 有 `f[10][p] − f[9][p−1]`（去掉 0 开头）：`f[10][{index}] − f[9][{index-1}] = {f[10][index]} − {f[9][index-1]}` → `res = {res}`',
        'for x in range(a[index])': lambda S, B, ret: (
            f'`x` 都枚举完了（比 `a[{S.index}] = {S.a[S.index]}` 小的数字）' if S.get('x') is not None and B.get('x') == S.x and B.get('index') == S.index and S.x == S.a[S.index] - 1 else
            f'`index = {S.index}`：枚举比 `a[{S.index}] = {S.a[S.index]}` 小的数字 `x`（位数与 N 相同，从最高位逐位处理，前面各位和 N 相同）；轮到 `x = {S.get("x")}`，后面随便排都小于 N'),
        'if x in used or': lambda S, B, ret: (
            f'`x = {S.x}` 已经用过 → 会重复，跳过' if S.x in S.used else
            f'`x = {S.x}` 是最高位，不能为 0，跳过' if S.index == S.l - 1 and S.x == 0 else
            f'`x = {S.x}` 没用过，可以放这一位'),
        'res += f[10 - (l - 1 - index) - 1][index]': '前面已用 `{l - 1 - index}` 个数，加上 `x` 再用 1 个，还剩 `{10 - (l - 1 - index) - 1}` 个数字排 `{index}` 位：`f[{10 - (l - 1 - index) - 1}][{index}]` = {f[10 - (l - 1 - index) - 1][index]} → `res = {res}`',
        'if a[index] in used': lambda S, B, ret: (
            f'`a[{S.index}] = {S.a[S.index]}` 已经用过：N 的前缀自己就重复了，不用再往后看 → break' if S.a[S.index] in S.used else
            f'`a[{S.index}] = {S.a[S.index]}` 没用过：N 的这一位保持不变，继续看下一位'),
        'used.add': '`used` 加入 `{a[index]}`',
        'if index == 0': lambda S, B, ret: ('走到最后一位也没重复：==N 自己==也是无重复数 → `res += 1`' if S.index == 0 else f'`index = {S.index}` 不是最后一位'),
        'res += 1': '`res` + 1（N 本身）→ `{res}`',
        'return N - res': '无重复的数共 `{res}` 个 → 有重复的 = `{N} − {res} = {N - res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='先算 1~N 里没有重复位的数，N 减去它',
        complexity='时间 `O(log²N)`，空间 `O(1)`（预处理 f 为常数）',
        problem=['给正整数 `N`，求 `[1, N]` 中至少有 1 位重复数字的整数个数',
                 '示例：`N=100` → `10`（11、22、…、99、100）',
                 '本视频：`N=234` → `53`'],
        quote='直接遍历求解的话时间复杂度太高，而找规律的话也比较麻烦，那么不妨逆向思维，先求出1到N中没有重复位的数字，设为res，那么最终答案就是N - res。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[k][l] = k * f[k-1][l-1]`：用 k 个不同数字排 l 位，第一位有 k 种选法',
              '位数比 N 少的：长度 `p` 有 `f[10][p] − f[9][p−1]` 个（去掉 0 开头）',
              '位数和 N 相同的：从高位起，某位放比 N 小的 `x`，后面随便排，用 `used` 去重'],
        summary=['时间 `O(log²N)`，空间 `O(1)`',
                 '最高位不能放 0；`a[index]` 已出现过就要 `break`，后面不可能无重复',
                 '最后不要忘了 N 自己：走完所有位还没 break，就 `res += 1`',
                 '原文为 Python 2 写法，`tmp /= 10`（整数除法）已改为 `tmp //= 10`',
                 '对比灵神：灵神用 mask 记忆化数位 DP，yiduobo 用排列数直接组合计数'],
    ),
)
