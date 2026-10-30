def _cells(S, r, c, v):
    d, m = S.get('d'), S.get('m')
    line = S.get('_line')
    if d is None:
        return None
    if line == 12 and r == m:
        return 'yellow'
    if line == 14 and r == d:
        return 'green' if c == 0 else 'blue'
    return None


def _txt(S):
    d, m = S.get('d'), S.get('m')
    line = S.get('_line')
    if d is None:
        return '`f[m][rem]` = 以当前数位结尾、模 m 余 rem 的子串个数'
    if line == 12:
        return f'模 `{m}`：`nf` = {S["f"][m]}（下标 = 余数，值 = 子串个数）'
    if line == 14:
        return f'末位 `d = {d}`：看 `f[{d}][0]` = ==余数为 0== 的个数 = {S["f"][d][0]}'
    return '每个数位把 m = 1..9 的状态都滚动一遍'


CONFIG = dict(
    num=3448, title='统计可以被最后一个数位整除的子字符串数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子数组 DP · 刷表法 · 枚举模数',
    tags=['灵神题单', '动态规划', '难度分 2387'],
    code='''
class Solution:
    def countSubstrings(self, s: str) -> int:
        ans = 0
        f = [[0] * 9 for _ in range(10)]
        for d in map(int, s):
            for m in range(1, 10):  # 枚举模数 m
                # 滚动数组计算 f
                nf = [0] * m
                nf[d % m] = 1
                for rem in range(m):  # 枚举模 m 的余数 rem
                    nf[(rem * 10 + d) % m] += f[m][rem]  # 刷表法
                f[m] = nf
            # 以 s[i] 结尾的，模 s[i] 余数为 0 的子串个数
            ans += f[d][0]
        return ans
''',
    call='Solution().countSubstrings("129")',
    expect=4,
    skip=['nf = [0] * m', 'nf[d % m] = 1', 'for rem in range', 'for m in range', 'nf[(rem * 10', 'f = [[0] * 9'],
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前末位 d）', h=130, cell=80,
             color=lambda S, i, x: 'blue' if 'd' in S and int(x) == S['d'] else None),
        dict(type='text', size=26, h=60, fn=_txt),
        dict(type='table', var='f', label='f[m][rem]：行 = 模数 m，列 = 余数 rem（黄 = 刚算完的行，绿 = 余数为 0）', h=480, cell=62,
             rows=lambda S: [f'm={k}' for k in range(10)], cols=lambda S: [f'r{k}' for k in range(9)],
             color=_cells),
    ],
    watch=[('d', 'd', 'blue'), ('m', 'm', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加满足条件的子串数',
        'for d in map': '新末位 `d = {d}`：以它结尾的子串 = 旧子串后面接 `d`',
        'f[m] = nf': '模 `{m}`：`d` 单独成串余 `{d} % {m}`，旧串接上 `d` 变 `(rem×10+{d}) % {m}` → `f[{m}] = {nf}`',
        'ans += f[d][0]': '末位是 `{d}`，要整除 `{d}`：取 `f[{d}][0]` = {f[d][0]} 个余数为 0 的子串 → `ans` = =={ans}==',
        'return ans': '所有以非 0 数字结尾、能被末位整除的子串共 =={ret}== 个',
    },
    cards=dict(
        one_liner='每个模数 m 各维护一份余数计数，刷表法滚动',
        complexity='时间 `O(nD^2)`，空间 `O(D^2)`，`D = 9`',
        problem=['数字串 `s`，统计末位不是 0、且能被自己末位整除的子串个数（可有前导 0）',
                 '示例：`s = "12936"` → `11`；`s = "5701283"` → `18`',
                 '视频里用 `s = "129"` 演示，答案 `4`'],
        quote='我们只需要知道以 s[i-1] 结尾的子串的数值模 s[i] 的结果 rem，并不需要知道 val 具体是多少。',
        quote_src='—— 灵茶山艾府题解（公式推导）',
        idea=['末位 `d` 决定模数，所以对 `m = 1..9` 都维护 `f[m][rem]`',
              '子串 + 末位：新数值 `val×10 + d`，余数 `(rem×10 + d) % m`',
              '本题难处理从哪转移来，所以用==刷表法==；`d` 自己单独成串 `nf[d % m] = 1`'],
        summary=['时间 `O(nD^2)`（每位枚举 m 与 rem），空间 `O(D^2)`',
                 '`f[m] = nf` 用滚动数组，每个 m 一行；`f` 第一维开 10 才能直接用 `f[m]`',
                 '末位为 0 的子串不统计：`f[0]` 行始终全 0，所以 `ans += f[0][0]` 加的也是 0',
                 '相似题：3524（本题的简化版）'],
    ),
)
