def _txt(S):
    if 'last_v' not in S:
        return '第一遍：记录每种前缀和模 `k` 的首次 / 最后一次下标'
    return f"`last_v` = {S['last_v']}，当前前缀 `s` = =={S['s']}==，`res` = =={S['res']}=="


CONFIG = dict(
    num=4063, title='至多一次取反能被 K 整除的最长子数组 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和模 k · 首尾位置哈希表',
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
    skip=[5, 10, 22, 23],
    call='Solution().longestSubarray([2,2,5], 6)',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=240, label='nums（蓝 = 当前右端点 index）'),
        dict(type='map', var='first_s', label='first_s：前缀和 % k → 首次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var=lambda S: S['last_s'] if 'last_s' in S else {}, label='last_s：前缀和 % k → 最后一次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='map', var=lambda S: S['last_v'] if 'last_v' in S else {}, label='last_v：元素值 % k → 最后一次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='text', h=80, size=26, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('s', 's', 'pink'), ('res', 'res', 'green')],
    captions={
        'first_s = {}': '第一遍：`first_s` / `last_s` 记下每种前缀和余数首次 / 最后一次出现的下标',
        'last_v = {}': '第二遍：`last_v` 记录每种元素值（模 k）最后一次出现的下标，`s`、`res` 重新开始',
        'first_s[0] = -1': '空前缀的余数是 `0`，位置记为 `-1`：`first_s[0] = -1`',
        'last_s[0] = -1': '`last_s[0] = -1`，同理',
        'v %= k': '先把元素对 `k` 取模：`v = {v}`',
        's += v': '前缀和累加：`s = {s}`',
        's %= k': '前缀和也取模：`s = {s}`（只关心余数）',
        'if s not in first_s': lambda S, B, r: (f"余数 `{S.s}` 之前没出现过 → 记为首次位置" if S.s not in B.first_s else f"余数 `{S.s}` 已有首次位置 `{S.first_s[S.s]}`，不动"),
        'first_s[s] = index': '`first_s[{s}] = {index}`：这个余数首次出现的位置',
        'last_s[s] = index': '`last_s[{s}] = {index}`：不断覆盖，最后留下的是最后一次出现',
        'res = max(res, index - first_s[s])': '不取反：以 `index` 结尾、左端点在首次位置之后，和能被 `k` 整除 → 长度 `{index} − {first_s[s]}`，`res = {res}`',
        'last_v[v] = index': '`last_v[{v}] = {index}`：值 `{v}` 最后出现在 `index` 之前或当前',
        'if last_s[s] != index': lambda S, B, r: ('这个余数之后还会再出现 → 右端点交给后面更靠右的那个，跳过' if S.last_s[S.s] != S.index else '这是该余数最后一次出现 → 需要检测取反的情况'),
        'rs = (s - rv * 2)': '取反 `{rv}` 后，前缀和余数变为 `(s − 2·rv) % k = {rs}`，需要左边界余数为它',
        'if rs in first_s': lambda S, B, r: (f"`first_s[{S.rs}]` = {S.first_s.get(S.rs, '无')}，值 `{S.rv}` 最后出现在 `{S.last_v[S.rv]}`："
                                               + ('取反点落在 `(first_s[rs], index]` 内 → 这段合法' if (S.rs in S.first_s and S.first_s[S.rs] < S.last_v[S.rv]) else '没有取反点落在区间内 → 不合法')),
        'res = max(res, index - first_s[rs])': '取反后的合法子数组长度 `{index} − {first_s[rs]}`：`res = {res}`',
        'return res': '最长有效子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='取反 v 等于前缀余数少 2v：只看每个余数的最优端点和最后一个 v',
        complexity='时间 `O(n + min(n,k)^2)`，空间 `O(min(n,k))`',
        problem=['子数组和能被 `k` 整除，或取反其中一个元素后能被 `k` 整除，就是“有效”的',
                 '求最长有效子数组的长度，没有则返回 `0`',
                 '本视频：`nums=[2,2,5]`，`k=6` → `2`'],
        quote='若在 index 左侧 v 最后一次出现的位置大于 first[(s - v * 2) % k]，那么就说明将这个 v 取反后可以使得这个子数组合法。',
        quote_src='—— yiduobo 题解原文（大意）',
        idea=['先对元素取模；不取反时就是“前缀余数相同”的最长区间，左端点取首次出现',
              '取反 `v`：区间和从 `s − s_l` 变成 `s − s_l − 2v`，所以需要 `(s − 2v) % k` 等于左端点余数',
              '同一个余数只需检测最后一次出现的右端点；`v` 只需看最后出现的位置，是否落在区间内'],
        summary=['时间 `O(n + min(n,k)^2)`，空间 `O(min(n,k))`',
                 '易错点：条件是 `first_s[rs] < last_v[rv]`，取反点必须在 `(左端点, index]` 内',
                 '第一遍只建 `first_s` / `last_s`，第二遍才一边更新 `last_v` 一边检测',
                 '这份写法同时适用 4064（`n` 到 `10^5`、`k ≤ 3000`）',
                 '代码原文即为 Python 3 可运行写法，未做修改'],
    ),
)
