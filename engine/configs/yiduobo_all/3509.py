def _fmt(k, v):
    return f'{k}: ' + (('{' + ','.join(str(x) for x in sorted(v)) + '}') if isinstance(v, set) else str(v))


CONFIG = dict(
    num=3509, title='最大化交错和为 K 的子序列乘积', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='两个哈希表 · 交错和 → 乘积集合',
    tags=['灵神题单·动态规划', '难度分 2703'],
    setup='import copy',
    code='''
class Solution(object):
    def maxProduct(self, nums, k, limit):
        
        f = {}
        g = {}

        if k < -900 or k > 900:
            return -1

        for v in nums:
            nxt_f = copy.deepcopy(f)
            if v <= limit:
                if v not in nxt_f:
                    nxt_f[v] = set()
                nxt_f[v].add(v)
            nxt_g = copy.deepcopy(g)

            for s in f:
                nxt_s = s - v
                if nxt_s < -900 or nxt_s > 900:
                    continue
                if nxt_s not in nxt_g:
                    nxt_g[nxt_s] = set()
                for m in f[s]:
                    nxt_m = m * v
                    if nxt_m <= limit:    
                        nxt_g[nxt_s].add(nxt_m)
                if v == 0:
                    nxt_g[nxt_s].add(0)

            for s in g:
                nxt_s = s + v
                if nxt_s < -900 or nxt_s > 900:
                    continue
                if nxt_s not in nxt_f:
                    nxt_f[nxt_s] = set()    
                for m in g[s]:
                    nxt_m = m * v
                    if nxt_m <= limit:    
                        nxt_f[nxt_s].add(nxt_m)
                if v == 0:
                    nxt_f[nxt_s].add(0)
        
            f = copy.deepcopy(nxt_f)
            g = copy.deepcopy(nxt_g)

        res = -1
        if k in f and f[k]:
            res = max(res, max(f[k]))

        if k in g and g[k]:
            res = max(res, max(g[k]))
        
        return res
''',
    call='Solution().maxProduct([1, 2, 3], 2, 10)',
    expect=6,
    skip=['if nxt_s < -900', 'continue', 'if nxt_s not in nxt_g', 'if nxt_s not in nxt_f', 'if v not in nxt_f', 'nxt_g[nxt_s] = set()',
          'nxt_f[nxt_s] = set()', 'nxt_f[v] = set()', 'if v == 0', 'f = {}', 'g = {}', 'if k < -900', 'return -1', 'for s in f', 'for s in g',
          'for m in f[s]', 'for m in g[s]', 'nxt_s = s', 'res = -1'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前加入的 v）', cell=64, h=150,
             color=lambda S, i, v: 'blue' if 'v' in S and i == S['nums'].index(S['v']) else None),
        dict(type='map', var='f', label='f：长度为奇数的子序列　交错和 → {乘积集合}', fmt=_fmt, h=190),
        dict(type='map', var='g', label='g：长度为偶数的子序列　交错和 → {乘积集合}', fmt=_fmt, h=170),
        dict(type='map', var=lambda S: S.get('nxt_f'), label='nxt_f：加入 v 之后的奇数长子序列（黄 = 刚改动）', fmt=_fmt, h=170),
        dict(type='map', var=lambda S: S.get('nxt_g'), label='nxt_g：加入 v 之后的偶数长子序列', fmt=_fmt, h=150),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'cyan'), ('m', 'm', 'yellow'), ('nxt_s', 'nxt_s', 'pink'), ('nxt_m', 'nxt_m', 'green')],
    captions={
        'for v in nums': lambda S, B, r: ('`nums` 里的数都处理完了，`f / g` 里是所有可能的子序列' if B.get('v') == S.get('v') and S.get('v') is not None
                                          else f'考虑 `v = {S.v}`：它可以接在已有子序列后面，也可以不选'),
        'nxt_f = copy.deepcopy(f)': '`nxt_f` 先复制 `f`：==不选 v== 时原有子序列都保留',
        'nxt_f[v].add(v)': '`v = {v}` 单独成为一个长度为 1 的子序列：`nxt_f[{v}]` 加入乘积 `{v}`',
        'nxt_g = copy.deepcopy(g)': '`nxt_g` 先复制 `g`，同样先保留不选 `v` 的情况',
        'nxt_m = m * v': lambda S, B, r: (f'`f` 中交错和 `s = {S.s}`、乘积 `m = {S.m}` 的子序列，接上 `v = {S.v}`：乘积 `{S.m} × {S.v} = {S.nxt_m}`' if S.get('_line') == 25
                                          else f'`g` 中交错和 `s = {S.s}`、乘积 `m = {S.m}` 的子序列，接上 `v = {S.v}`：乘积 `{S.m} × {S.v} = {S.nxt_m}`'),
        'nxt_g[nxt_s].add(nxt_m)': '`f` 里是奇数长，接上 `v` 变偶数长，`v` 在交错和里是==负的==：`{s} − {v} = {nxt_s}`，乘积 `{nxt_m} ≤ {limit}`，放进 `nxt_g[{nxt_s}]`',
        'nxt_f[nxt_s].add(nxt_m)': '`g` 里是偶数长，接上 `v` 变奇数长，`v` 在交错和里是==正的==：`{s} + {v} = {nxt_s}`，乘积 `{nxt_m} ≤ {limit}`，放进 `nxt_f[{nxt_s}]`',
        'if nxt_m <= limit': lambda S, B, r: (f'`nxt_m = {S.nxt_m}` ≤ `limit = {S.limit}`，保留' if S.nxt_m <= S.limit else f'`nxt_m = {S.nxt_m}` > `limit = {S.limit}`，超限，丢掉'),
        'f = copy.deepcopy(nxt_f)': '这个数处理完：`f` 更新为 `nxt_f`',
        'g = copy.deepcopy(nxt_g)': '`g` 更新为 `nxt_g`，下一个数继续',
        'if k in f and f[k]': lambda S, B, r: (f'`f[{S.k}] = {sorted(S.f[S.k])}` 非空：取其中最大的乘积' if S.k in S.f and S.f[S.k] else f'`f` 里没有交错和为 `{S.k}` 的子序列'),
        'res = max(res, max(f[k]))': '`res = {res}`',
        'if k in g and g[k]': lambda S, B, r: (f'`g[{S.k}] = {sorted(S.g[S.k])}` 非空：再和 `res` 比' if S.k in S.g and S.g[S.k] else f'`g` 里没有交错和为 `{S.k}` 的子序列'),
        'res = max(res, max(g[k]))': '`res = {res}`',
        'return res': '`f[k]` 与 `g[k]` 中乘积最大者：`{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='用两张哈希表记下所有「交错和 → 可能的乘积」，逐个数滚动更新',
        complexity='状态量不大，时间约 `O(n·S·P)`（S 为交错和个数，P 为乘积个数）',
        problem=['选非空子序列，交错和 = 偶数下标和 − 奇数下标和，要等于 `k`',
                 '乘积不超过 `limit` 且最大；没有则返回 -1',
                 '本视频：`nums=[1,2,3], k=2, limit=10` → `6`'],
        quote='常规的动态规划一般保留的是子状态中的最优解，但是在本题中，子状态的最优解与当前元素相乘后可能超出limit，但是如果子状态中不选择最优解，反而可能可以与当前元素相乘后得到一个更优的解。',
        quote_src='—— yiduobo 题解原文',
        idea=['不能只保留最大乘积，所以 `f / g` 的 value 是乘积的==集合==',
              '`f` 记奇数长、`g` 记偶数长：奇数长接 `v` 变偶数长，交错和 `s − v`；反之 `s + v`',
              '交错和只可能在 `[-900, 900]`，`k` 越界直接 -1；乘积超过 `limit` 的不要'],
        summary=['`nums` 长度 ≤ 150、值 ≤ 12，交错和限制在 ±900，乘积 ≤ `limit`，集合不会太大',
                 '`v = 0` 时乘积变 0，要单独 `add(0)`，否则会被 `m * v` 的集合漏掉',
                 '每轮先 `deepcopy` 再更新，避免边遍历边改字典',
                 '原文为 Python 2 写法，类名后的 `(object)` 在 Python 3 中仍可运行，代码无需修改；使用了 `copy` 模块，已在 setup 里 `import copy`',
                 '对比灵神：他用记忆化 dfs，乘积超限记为 `limit+1`'],
    ),
)
