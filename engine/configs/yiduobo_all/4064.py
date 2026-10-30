def _txt(S):
    if S['_line'] < 27 or 'rv' not in S or 's' not in S:
        return ''
    rs = (S['s'] - S['rv'] * 2) % S['k']
    return (f"取反 `v={S['rv']}`：`rs = (s − 2v) % k = {rs}`，"
            f"`first_s[rs] = {S['first_s'].get(rs, '无')}`，`last_v[v] = {S['last_v'][S['rv']]}`")


CONFIG = dict(
    num=4064, title='至多一次取反能被 K 整除的最长子数组 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和取模 + last_v 检测取反元素',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def longestSubarray(self, nums, k):
        
        first_s = {}
        last_s = {}

        first_s[0] = -1
        last_s[0] = -1

        s = 0
        for index, v in enumerate(nums):
            v %= k
            s += v
            s %= k

            if s not in first_s:
                first_s[s] = index
            
            last_s[s] = index

        last_v = {}
        s = 0
        res = 0
        for index, v in enumerate(nums):
            v %= k
            s += v
            s %= k

            res = max(res, index - first_s[s])
            last_v[v] = index

            if last_s[s] != index:
                continue

            for rv in last_v:
                rs = (s - rv * 2) % k
                if rs in first_s and first_s[rs] < last_v[rv]:
                    res = max(res, index - first_s[rs])

        return res
''',
    call='Solution().longestSubarray([4,1,2], 3)',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=190, label='nums',
             window=(lambda S: (S['first_s'][S['rs']] + 1) if S['_line'] >= 36 and 'rs' in S and S['rs'] in S['first_s'] else None, 'index')),
        dict(type='map', var='first_s', fmt=lambda k, v: f'模 {k} 首次在 {v}', h=150, font=24, label='first_s'),
        dict(type='map', var='last_s', fmt=lambda k, v: f'模 {k} 最后在 {v}', h=150, font=24, label='last_s'),
        dict(type='map', var='last_v', fmt=lambda k, v: f'v={k} 最近在 {v}', h=150, font=24, label='last_v'),
        dict(type='text', size=24, h=80, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'cyan'), ('rv', 'rv', 'pink'), ('res', 'res', 'green')],
    captions={
        'first_s = {}': '`first_s[s]`：前缀和模 k 为 s 时==首次==出现的下标（左边界越靠左越长）',
        'last_s = {}': '`last_s[s]`：前缀和模 k 为 s 时==最后==出现的下标',
        'first_s[0] = -1': '空前缀：模 k 为 0，下标 `-1`',
        'last_s[0] = -1': '`last_s[0] = -1`',
        'v %= k': '先把元素模 k：`v = {v}`',
        's += v': '`s += {v}`',
        's %= k': '前缀和模 k：`s = {s}`',
        'if s not in first_s': lambda S, B, r: (f'`s = {S.s}` 第一次出现 → 记下首次位置' if S.s not in S.first_s else f'`s = {S.s}` 已出现过 → 保留更靠左的首次位置'),
        'first_s[s] = index': '`first_s[{s}] = {index}`',
        'last_s[s] = index': '`last_s[{s}] = {index}`：不断覆盖，最后留下最靠右的',
        'last_v = {}': '第二趟：`last_v[v]` 记录元素 v 最后一次出现的位置，用来判断取反的元素是否在区间内',
        10: '`s` 是前缀和模 k',
        22: '前缀和重新从 0 累计',
        23: '`res` 是答案',
        'res = max(res, index - first_s[s])': '不取反：`s` 与首次位置同余 → 长度 `{index} − {first_s[s]}`，`res` = =={res}==',
        'last_v[v] = index': '`last_v[{v}] = {index}`',
        'if last_s[s] != index': lambda S, B, r: (f'`last_s[{S.s}] = {S.last_s[S.s]} ≠ {S.index}`：同余的右端点更靠右的更优 → 跳过' if S.last_s[S.s] != S.index else f'`last_s[{S.s}] = {S.index}`：这是该余数最后一次出现，检查取反'),
        'for rv in last_v': '枚举可能取反的元素值 `rv = {rv}`',
        'rs = (s - rv * 2) % k': '取反 `v` 后和变化 `−2v`：要左边前缀模 k = `({s} − 2×{rv}) % {k} = {rs}`',
        'if rs in first_s and': lambda S, B, r: ((f'`first_s[{S.rs}] = {S.first_s[S.rs]} < last_v[{S.rv}] = {S.last_v[S.rv]}`：v 出现在区间内 → 取反它即合法' if S.first_s[S.rs] < S.last_v[S.rv] else f'`first_s[{S.rs}] = {S.first_s[S.rs]} ≥ last_v[{S.rv}] = {S.last_v[S.rv]}`：v 在区间左侧 → 不行') if S.rs in S.first_s else f'`rs = {S.rs}` 没出现过 → 不行'),
        'res = max(res, index - first_s[rs])': '长度 `{index} − ({first_s[rs]})`，`res` = =={res}==',
        'return res': '最长有效长度 `{res}`',
    },
    cards=dict(
        one_liner='先模 k，再对每个右端点检查「哪个元素取反能凑成同余」',
        complexity='时间 `O(n + min(n,k)^2)`，空间 `O(min(n,k))`',
        problem=['子数组和能被 `k` 整除，或取反其中一个元素后能被 `k` 整除，就是有效',
                 '求最长有效子数组长度，没有则 0；本题 `k ≤ 3000`',
                 '本视频：`nums=[4,1,2], k=3` → `3`'],
        quote='在这里只需要满足first[(s - v * 2) % k] + 1到当前下标index之间，存在至少一个v，就说明将这个v取反后可以使得这个子数组合法。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素先模 k，前缀和也模 k；不取反就是同余的最长区间',
              '取反 `v`，和变化 `−2v`：左端前缀要等于 `(s − 2v) % k`',
              '只检查 `last_s` 的右端点，只用 `last_v[v]` 判断 v 是否在区间里'],
        summary=['时间 `O(n + min(n,k)^2)`，空间 `O(min(n,k))`',
                 '不同的 `v` 和不同的右端点各 ≤ `min(n,k)` 个，所以二重循环可过',
                 '`first_s[rs] < last_v[rv]`：区间是 `(first, index]`，v 的位置必须落在其中',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行',
                 '对比灵神：灵神枚举 `s[l]%k`，用 `last_x2` 记 `2x%k`；yiduobo 枚举被取反的 v'],
    ),
)
