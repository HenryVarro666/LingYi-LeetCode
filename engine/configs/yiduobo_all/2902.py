def _cap_g(S, B, ret):
    idx, v = S.index, S.v
    c = S.cnt[v]
    return f'`g[{idx}] += g[{idx - v}]`：并上「本轮已含」`g[{idx - v}]`，相当于多选一个 `{v}` → `{S.g[idx]}`（还没限制个数）'


def _cap_lim(S, B, ret):
    idx, v = S.index, S.v
    c = S.cnt[v]
    return f'`{idx} ≥ (cnt+1)·v = {(c + 1) * v}`：选了 {c + 1} 个 `{v}` 的方案多算了，减去 `f[{idx - (c + 1) * v}]` → `{S.g[idx]}`'


CONFIG = dict(
    num=2902, title='和带限制的子多重集合的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='多重背包 · 递推式相减去重',
    tags=['灵神题单', '动态规划', '难度分 2759'],
    code='''
class Solution(object):
    def countSubMultisets(self, nums, l, r):

        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        f = [0] * (r + 1)
        f[0] = 1
        mod = 10 ** 9 + 7

        for v in cnt:
            if v == 0:
                continue
            
            g = f[:]
            for index in range(v, r + 1):
                g[index] += g[index - v]
                if g[index] >= mod:
                    g[index] -= mod
                if index >= (cnt[v] + 1) * v:
                    g[index] -= f[index - (cnt[v] + 1) * v]
                    if g[index] < 0:
                        g[index] += mod
            
            f = g[:]
        
        res = 0
        for index in range(l, r + 1):
            res += f[index]
            if res >= mod:
                res -= mod
        
        return res * (cnt.get(0, 0) + 1) % mod
''',
    call='Solution().countSubMultisets([0,2,1,1], 2, 4)',
    expect=8,
    views=[
        dict(type='map', var='cnt', label='cnt：每种数的个数', h=150, fmt=lambda k, v: f'{k}×{v}'),
        dict(type='array', var='f', label='f：上一种物品后，和为 j 的方案数', h=190, cell=70),
        dict(type='array', var='g', label='g：本轮正在算的新数组', h=210, cell=70, pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: (f"当前物品 `v = {S['v']}`，共 `{S['cnt'][S['v']]}` 个" if 'v' in S and 'cnt' in S and S['v'] in S['cnt'] else '0 不影响和，最后统一乘 `cnt[0]+1`'), size=26, h=60),
    ],
    watch=['v', 'index', 'l', 'r', ('res', 'res', 'green')],
    captions={
        'cnt[v] = cnt.get': '数一数：`{v}` 出现 `{cnt[v]}` 次',
        'f = [0] * (r + 1)': '`f[j]`：和恰好为 `j` 的方案数，长度到 `r`',
        'f[0] = 1': '什么都不选，和为 0，有 1 种',
        'if v == 0': '`v = {v}`：{"0 先跳过，最后乘上 cnt[0]+1" if v == 0 else "不是 0，要处理"}',
        'g = f[:]': '`g` 先拷贝上一轮的 `f`：`f[j]` 保持不动，`g` 里累加；不能单数组倒序，因为要用本轮新算的 `g[j-v]`',
        'g[index] += g[index - v]': _cap_g,
        'if index >= (cnt[v] + 1)': '`index = {index}`，`(cnt+1)·v = {(cnt[v] + 1) * v}`：{"够大，要减去多算的一项" if index >= (cnt[v] + 1) * v else "还不够大，没有多算的项"}',
        'g[index] -= f[': _cap_lim,
        'f = g[:]': '这一种物品处理完，`g` 变成新的 `f`',
        'res += f[index]': '把和为 `{index}` 的方案数加入答案：`res = {res}`',
        'return res': '`res = {res}` 再乘 `cnt[0] + 1 = {cnt.get(0, 0) + 1}` → ==`{ret}`==',
    },
    skip=['if res >= mod', 'res -= mod', 'if g[index] >= mod', 'g[index] -= mod', 'if g[index] < 0', 'g[index] += mod'],
    cards=dict(
        one_liner='f[i][j] 减去 f[i][j-v] 的重复段，一步算出新状态',
        complexity='时间 `O(r·√s)`，空间 `O(r)`',
        problem=['`nums` 中选子多重集合（每个值出现次数不超过原数组，无序）', '求元素和在 `[l, r]` 的方案数，取模 `10^9+7`',
                 '示例：`[1,2,2,3], l=6, r=6` → `1`；视频用 `[0,2,1,1], l=2, r=4`'],
        quote='可以发现，其中f[i - 1][j - v]到f[i - 1][j - cnt[v] * v]这一段是重复的，更进一步的，就有f[i][j] = f[i - 1][v] + f[i][j - 1] - f[i - 1][j - (cnt[v] + 1) * v]',
        quote_src='—— yiduobo 题解原文',
        idea=['同一种物品选 `0..cnt` 个，转移方程是一串求和', '把 `f[i][j-v]` 也展开，两式中间一大段重复，作差只剩头尾两项',
              '`j` 不够大时没有减项；0 单独处理，最后乘 `cnt[0]+1`'],
        summary=['时间 `O(r·√s)`：不同的数至多约 `√(2s)` 种',
                 '易错：不能单数组倒序，转移用到本轮新算的 `g[j-v]`，所以用 `f` 和 `g` 两个数组',
                 '加减后手动判断 `mod`，避免取模运算；`0` 不进 DP，最后乘 `cnt[0]+1`',
                 '原文就是 Python 3 可运行的写法，未做修改；题文说「令 f[i-1][v]」属原文笔误，代码以 `g[index-v]` 为准',
                 '对比灵神：灵神把 `f[0]` 初始为 `cnt[0]+1`，并把 `r` 压到总和'],
    ),
)
