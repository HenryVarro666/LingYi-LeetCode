S0 = '101101'


def _ok(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    return S['s'][j:i + 1] in S['pow5_str']


def _sc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if j is not None and S.get('_line') in (15, 16) and j <= k <= i:
        return 'green' if _ok(S) and S['f'][j] != -1 else 'yellow'
    return 'blue' if k == i else None


def _fc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if k == len(S['f']) - 1 and k > 0:
        return 'yellow'
    if j is not None and k == j and S.get('_line') in (15, 16) and _ok(S):
        return 'green' if v != -1 else 'pink'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return '`f[i]` = 前 `i` 个字符最少切几段，`-1` = 切不了；`f[0] = 0`'
    if j is not None and S.get('_line') in (15, 16):
        sub = S['s'][j:i + 1]
        if sub not in S['pow5_str']:
            return f'`s[{j}:{i + 1}] = "{sub}"` 不是 5 的幂的二进制'
        fj = S['f'][j]
        if fj == -1:
            return f'`"{sub}"` 是 5 的幂，但前面 `f[{j}] = -1` 切不了 → 不能用'
        return f'`"{sub}"` 是 5 的幂，前面 `f[{j}] = {fj}` → 候选 `{fj} + 1` = =={fj + 1}=='
    return f'求 `f[{i + 1}]`：枚举最后一段的起点 `j`，先设成 `-1`（还没找到）'


CONFIG = dict(
    num=2767, title='将字符串分割为最少的美丽子字符串', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP：枚举最后一段起点',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1865'],
    code='''
class Solution(object):
    def minimumBeautifulSubstrings(self, s):
        pow5_str = set(['1'])
        pow5 = 1
        while True:
            pow5 *= 5
            b = bin(pow5)[2:]
            if len(b) > len(s):
                break
            pow5_str.add(b)
        f = [0]
        for i in range(len(s)):
            f.append(-1)
            for j in range(i + 1):
                if s[j : i + 1] in pow5_str and f[j] != -1 and (f[-1] == -1 or f[-1] > f[j] + 1):
                    f[-1] = f[j] + 1
        return f[-1]
''',
    call=f'Solution().minimumBeautifulSubstrings({S0!r})',
    expect=2,
    skip=['for j in range', 'pow5 = 1', 'pow5 *= 5'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = s[i]，黄/绿 = 正在检查的 s[j..i]）', h=190, cell=70, pointers={'j': 'pink', 'i': 'blue'}, color=_sc),
        dict(type='set', var='pow5_str', label='pow5_str：长度不超过 s 的 5 的幂（二进制）', h=100),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f[k]：前 k 个字符最少切几段（-1 = 不行；黄 = 正在算的 f[-1]）', h=170, cell=70, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'pow5_str = set': '先造表：把 5 的幂的二进制串收进集合，从 `"1"`（即 5^0）开始',
        'b = bin(pow5)': '`5` 的下一个幂的二进制：`{b}`',
        'if len(b) > len(s)': lambda S, B, r: (f'`{S.b}` 比 `s` 还长（{len(S.b)} > {len(S.s)}），放不进任何前缀 → 不用再往后算' if len(S.b) > len(S.s)
                                              else f'`{S.b}` 长 {len(S.b)} ≤ {len(S.s)}，可能用得上，收进集合'),
        'pow5_str.add': '`{b}` 加入 `pow5_str`',
        'f = [0]': '`f[0] = 0`：空串不用切，0 段',
        'for i in range(len(s))': lambda S, B, r: (f'枚举 `i = {S.i}`：算前 `{S.i+1}` 个字符的 `f[{S.i+1}]`' if S.get('i') != B.get('i')
                                                  else '所有前缀都算完了'),
        'f.append(-1)': '先追加 `-1`：`f[{i+1}]` 暂时「还没找到切法」',
        'if s[j : i + 1] in pow5_str': lambda S, B, r: (
            (f'`s[{S.j}:{S.i+1}] = "{S.s[S.j:S.i+1]}"` 不是 5 的幂' if S.s[S.j:S.i+1] not in S.pow5_str else
             f'`"{S.s[S.j:S.i+1]}"` 是 5 的幂，但 `f[{S.j}] = -1`：前面切不了 → 不能用' if S.f[S.j] == -1 else
             f'`"{S.s[S.j:S.i+1]}"` 是 5 的幂，`f[{S.j}] = {S.f[S.j]}` 可行；现在 `f[-1] = {S.f[-1]}`：{"还没有切法" if S.f[-1] == -1 else "比一比谁更小"}')),
        'f[-1] = f[j] + 1': '把最后一段切成 `s[{j}:{i+1}]`：`f[{i+1}] = f[{j}] + 1` = =={f[-1]}==',
        'return f[-1]': '`f[-1]` = =={ret}==；若是 `-1` 就表示切不了',
    },
    cards=dict(
        one_liner='先造 5 的幂的二进制表，再枚举最后一段',
        complexity='时间 `O(n^3)`（切片比较），空间 `O(n)`',
        problem=['把二进制串 `s` 切成若干段，每段是「美丽」的：无前导 0，且是 5 的幂的二进制',
                 '求最少切几段；切不了返回 `-1`',
                 '示例：`"1011"` → `2`（`"101"`、`"1"`）；视频用 `"101101"` → `2`'],
        quote='可以先将所有长度不超过s的5的幂的二进制表示先计算好，接下来就是常规的动态规划了。',
        quote_src='—— yiduobo 题解',
        idea=['`pow5_str` 存所有不超过 `len(s)` 位的 5 的幂的二进制串',
              '`f[i]` = 前 `i` 个字符的最少段数；枚举最后一段的起点 `j`',
              '`s[j:i+1]` 在表里、且 `f[j]` 切得了，就用 `f[j] + 1` 更新'],
        summary=['时间：`i`、`j` 两层循环 + 切片比较，`O(n^3)`，`n ≤ 15` 足够',
                 '易错：用 `-1` 表示「切不了」，所以要判断 `f[j] != -1`，更新时也要先看 `f[-1] == -1`',
                 '前导 0 不用单独判断：5 的幂的二进制都以 `1` 开头，表里没有 `0` 开头的串',
                 '原文代码无需修改即可在 Python 3 运行，仅删去了多余空行'],
    ),
)
