S0 = '1317'
K0 = 2000


def _cands(S):
    nl, i = S.get('num_list'), S.get('i')
    if nl is None or i is None:
        return ''
    return '本位起的候选数：' + '、'.join(f'`{x}`' for x in nl)


CONFIG = dict(
    num=1416, title='恢复数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='从后往前 DP · 滚动维护候选数',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def numberOfArrays(self, s, k):

        mod = 10 ** 9 + 7

        tmp = k
        l = 0
        p = [1]
        while tmp:
            l += 1
            tmp //= 10
            p.append(p[-1] * 10)
        
        num_list = [0] * l
        f = [1]
        n = len(s)
        for i in range(n - 1, -1, -1):
            for j in range(l - 1, 0, -1):
                num_list[j] = num_list[j - 1] + (ord(s[i]) - 48) * p[j]
            num_list[0] = ord(s[i]) - 48
            f.append(0)

            if num_list[0] > 0:
                for j in range(0, min(l, len(f) - 1)):
                    if num_list[j] >= 1 and num_list[j] <= k:
                        f[-1] += f[-1 - j - 1]
                        f[-1] %= mod

        return f[-1]
''',
    call=f'Solution().numberOfArrays({S0!r}, {K0})',
    expect=8,
    skip=['mod = ', 'tmp = k', 'l = 0', 'p = [1]', 'l += 1', 'p.append', 'f[-1] %= mod', 'tmp //= 10'],
    views=[
        dict(type='string', var='s', label='s（从后往前扫，蓝 = 当前位 i）', h=190, cell=80, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None,
             dim=lambda S, k, v: S.get('i') is not None and k < S['i']),
        dict(type='array', var='num_list', label='num_list[j] = 以当前位开头、长 j+1 位的数', h=190, cell=110,
             pointers={'j': 'pink'}),
        dict(type='array', var='f', label='f[t] = 最后 t 位能恢复出的方案数', h=190, cell=90),
        dict(type='text', fn=_cands, size=26, h=60),
    ],
    watch=[('k', 'k', 'yellow'), 'l', ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'while tmp': '`k = {k}` 有几位，候选数最多就取几位：`l` = ==位数==',
        'num_list = [0] * l': '`num_list` 存当前位开头的 `l = {l}` 个候选数',
        'f = [1]': '`f[0] = 1`：后面没有数字了，空的一种方案',
        'for i in range': '从最后一位往前扫：`i = {i}`，数字 `{s[i]}`',
        'num_list[j] = num_list[j - 1]': '把当前位 `{s[i]}` 接到上轮第 `{j-1}` 个候选前面：`num_list[{j}]` = =={num_list[j]}==',
        'num_list[0] = ': '长度 1 的候选就是当前位本身：`num_list[0]` = =={num_list[0]}==',
        'f.append(0)': '新开 `f[{len(f)-1}]`，先置 0，下面累加',
        'if num_list[0] > 0': lambda S, B, r: ('当前位 `{}` 非 0 → 可以作为一个数的开头'.format(S.num_list[0]) if S.num_list[0] > 0
                                               else '当前位是 ==0==：不能有前导 0 → `f` 保持 0'),
        'for j in range(0, min': '枚举取 1 到 `{min(l, len(f) - 1)}` 位（不超过剩余位数）',
        'if num_list[j] >= 1': lambda S, B, r: (f'`{S.num_list[S.j]}` 在 `1..{S.k}` 内 → ==可以切出这一段==' if 1 <= S.num_list[S.j] <= S.k
                                                else f'`{S.num_list[S.j]}` 超过 `k = {S.k}`（或为 0）→ 这种切法非法'),
        'f[-1] += f[-1 - j - 1]': '切出 `{j+1}` 位，后面还剩 `{len(f)-2-j}` 位 → `f[-1]` += `f[{len(f)-2-j}]`（={f[len(f)-2-j]}）→ =={f[-1]}==',
        'return f[-1]': '整串 `{s}` 有 =={ret}== 种恢复方式',
    },
    cards=dict(
        one_liner='从后往前扫，每位只枚举 k 的位数那么多种切法',
        complexity='时间 `O(n·l)`，空间 `O(n)`（`l` 为 `k` 的位数）',
        problem=['有人把一个数组的数字去掉空格写成字符串 `s`，数组里每个数都在 `[1, k]` 内，且没有前导 0',
                 '求有多少种可能的原数组，对 `10^9+7` 取余',
                 '示例：`s = "1317", k = 2000` → `8`'],
        quote='令f[i]表示字符串中最后i位可以恢复出的数组方案数……若当前位上的数字为0，由于不能出现前导0，因此无论怎么分割得到的都是非法的情况，于是就有f[i] = 0',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：最后 `i` 位的方案数；当前位为 0 → 直接 0',
              '否则枚举从当前位开始的 1 到 `l` 位数，不超过 `k` 就 `f[i] += f[i-j-1]`',
              '候选数不重算：新候选 = 旧候选 + ==当前位 × 10^j==，用 `num_list` 滚动'],
        summary=['时间 `O(n·l)`，空间 `O(n)`',
                 '易错：前导 0 的位置 `f` 必须是 0；候选数要同时 `>= 1` 且 `<= k`',
                 '原文为 Python 2 写法，`tmp /= 10` 已改为 `tmp //= 10`',
                 '`mod` 在每次累加后取，避免溢出（Python 中只是保持数值小）'],
    ),
)
