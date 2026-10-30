PR = ('2', '3', '5', '7')


def _ok(S):
    """当前 i 是否满足转移条件（返回 4 个子条件）"""
    i, j, m, n, s = S['i'], S['j'], S['minLength'], S['n'], S['s']
    return (i >= m * j, s[i - 1] not in PR, i + 1 <= n, i + 1 <= n and s[i] in PR)


def _cond_cap(S, B, ret):
    i, j, m, n, s = B['i'], B['j'], B['minLength'], B['n'], B['s']
    a = i >= m * j
    pre = f"`f[{i}]` 先继承 `f[{i-1}] = {B['f'][i-1]}`（前缀累加）；"
    return pre + _why(B)


def _why(B):
    i, j, m, n, s = B['i'], B['j'], B['minLength'], B['n'], B['s']
    a = i >= m * j
    if not a:
        return f"`i = {i}` < `minLength × j = {m*j}`：前 {i} 个字符凑不出 {j} 段 → ==不合法==，`f[{i}]` 只继承前缀"
    b = s[i - 1] not in PR
    if not b:
        return f"`s[{i-1}] = {s[i-1]}` 是质数：这一段不能以它结尾 → ==不合法=="
    if i + 1 > n:
        return f"`i + 1 = {i+1}` > n：后面没有字符了 → 不能当作中间的分割点"
    c = s[i] in PR
    if not c:
        return f"`s[{i}] = {s[i]}` 不是质数：下一段不能以它开头 → ==不合法=="
    return f"`s[{i-1}] = {s[i-1]}` 非质数结尾、`s[{i}] = {s[i]}` 质数开头、长度够 → ==合法分割点=="


def _color(S, i, v):
    if 'i' not in S or S.get('_line') is None:
        return None
    return None


def _formula(S):
    if 'i' not in S or 'g' not in S or 'j' not in S or S.get('_line', 0) < 16:
        return '`f[i]` = 前缀和：到前 `i` 个字符为止，分成 `j` 段的方案数之和；`g` 是上一轮（`j-1` 段）的 `f`'
    i, j, m = S['i'], S['j'], S['minLength']
    if S.get('_line') in (18, 19, 20) and i - m >= 0:
        return f"`f[{i}] += g[{i}-{m}]`：`g[{i-m}]` = {S['g'][i-m]}（前 {i-m} 个字符分成 {j-1} 段的前缀累加）"
    return f"第 `{j}` 轮，正在填 `f[{i}]`"


CONFIG = dict(
    num=2478, title='完美分割的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP · 前缀和 + 滚动数组',
    tags=['灵神题单', '动态规划', '难度分 2344'],
    code='''
class Solution(object):
    def beautifulPartitions(self, s, k, minLength):

        prime_set = set(['2', '3', '5', '7'])
        if s[0] not in prime_set or s[-1] in prime_set:
            return 0
        
        mod = 10 ** 9 + 7
        n = len(s)
        if minLength * k > n:
            return 0
        
        f = [1] * (n + 1)

        for j in range(1, k + 1):
            g = f[:]
            f = [0]
            for i in range(1, n + 1):
                f.append(f[-1])
                if i >= minLength * j and s[i - 1] not in prime_set and i + 1 <= n and s[i] in prime_set:
                    f[i] += g[i - minLength]
                    if f[i] >= mod:
                        f[i] -= mod

        return g[n - minLength]
''',
    call='Solution().beautifulPartitions("2354218", 2, 2)',
    expect=1,
    views=[
        dict(type='string', var='s', label='s（绿 = 质数数字；黄 = 当前 i 的结尾字符 s[i-1]）', h=170, cell=80,
             color=lambda S, k, v: ('yellow' if 'i' in S and S.get('_line', 0) >= 17 and k == S['i'] - 1 else ('green' if v in PR else None))),
        dict(type='array', var='g', label='g：上一轮（分成 j-1 段）的前缀累加', h=170, cell=80,
             pointers={'i': 'blue'}),
        dict(type='array', var='f', label='f：这一轮（分成 j 段）的前缀累加，边走边追加', h=170, cell=80,
             pointers={'i': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
    ],
    watch=['j', 'i', ('minLength', 'minLength', 'blue'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'prime_set = ': '质数数字集合 `{2,3,5,7}`',
        'if s[0] not in': '首字符 `{s[0]}` 必须是质数、尾字符 `{s[-1]}` 必须不是质数，否则一份都分不出来 → 通过',
        'mod = ': '答案取模 `10^9+7`',
        'if minLength * k': '`minLength × k = {minLength*k}` ≤ `n = {n}`，长度够分',
        'f = [1]': '`f[i]` 是前缀累加和；第 0 轮只有「空串」这一种方案，累加起来每个位置都是 ==1==',
        'for j in range': lambda S, B, ret: ('`j` 轮次结束，答案是上一轮的 `g[n - minLength]`' if B.get('j') == S['j'] else f"第 =={S['j']}== 轮：把字符串分成 {S['j']} 段"),
        'g = f[:]': '`g` 保存上一轮的结果，`f` 马上重置为 `[0]` 重新累加（只依赖上一轮，所以滚动）',
        'for i in range': lambda S, B, ret: ('这一轮 `f` 填完了' if B.get('i') == S['i'] else f"考虑前 =={S['i']}== 个字符，最后一段以 `s[{S['i']-1}] = {S['s'][S['i']-1]}` 结尾"),
        'f.append(f[-1])': '`f[{i}]` 先继承 `f[{i-1}] = {f[-1]}`：因为 `f` 是前缀累加，自身就含有之前所有位置的方案',
        'if i >= minLength': _cond_cap,
        'f[i] += g[i - minLength]': '`f[{i}] += g[{i}-{minLength}]` = `g[{i-minLength}]` = {g[i-minLength]} → `f[{i}]` 变为 =={f[i]}==：上一轮前 `{i-minLength}` 个字符的所有切法都能接上',
        'if f[i] >= mod': '`f[{i}] = {f[i]}` 没超过 `mod`，不用减',
        'return g[n - minLength]': '最后一段必然结束在 `n`：只要前 `k-1` 段的累加取到 `g[n-minLength]` = ==`{g[n-minLength]}`==（作者强调：不是 `g[n]`）',
    },
    skip=['mod = ', 'f[i] -= mod', 'f = [0]', 'f.append(f[-1])', 'if f[i] >= mod'],
    max_steps=70,
    cards=dict(
        one_liner='把「前缀和」直接当 DP 状态，转移只剩一次加法',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['数字串 `s` 切成 `k` 段，每段长度 `≥ minLength`，首字符是质数 `2357`，尾字符不是质数',
                 '返回方案数，对 `10^9+7` 取模',
                 '本视频：`s="2354218"`，`k=2`，`minLength=2` → `1`'],
        quote='注意到转移的复杂度主要集中在情况3，且这是一个非常典型的前缀和的式子，那么可以令f[i][j]表示h[0][j] + h[1][j] + ... + h[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写二维：`h[i][j]` = 前 `i` 个字符切成 `j` 段；不合法的位置直接置 0',
              '转移是 `h[i-minLength-1][j-1] + … + h[0][j-1]`，一个前缀和 → 令 `f` 存前缀累加',
              '于是 `f[i] = f[i-1]`，合法时再 `+= g[i-minLength]`；`h` 数组可以直接扔掉，再按轮滚动'],
        summary=['时间 `O(nk)`，空间 `O(n)`',
                 '`f` 是累加值，答案是 `g[n - minLength]`（最后一段结尾固定在 `n`），不是 `g[n]`',
                 '不合法位置（质数结尾、非质数开头、长度不够）只继承前缀，不加新值',
                 '原文为 Python 2 风格，本题代码在 Python 3 可直接运行，无需修改',
                 '对比灵神：灵神直接记录分割点的方案数，用 sum 双指针累加；yiduobo 把前缀和变成状态本身'],
    ),
)
