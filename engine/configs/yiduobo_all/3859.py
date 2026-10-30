def _info(S):
    if 'p1' not in S:
        return ''
    s = f"`index = {S.get('index', '-')}`：p1 = {S['p1']}（最远右端）　p2 = {S['p2']}（刚够 k 个好整数的最近右端）"
    if S.get('cnt') is not None:
        s += f"　好整数 `cnt = {S['cnt']}`"
    return s


CONFIG = dict(
    num=3859, title='统计包含 K 个不同整数的子数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左端点 · 双窗口 p1/p2 夹出合法右端区间',
    tags=['难度分 2302'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, k, m):
        
        freq1 = {}
        freq2 = {}
        cnt = 0
        p1 = 0
        p2 = 0
        res = 0

        n = len(nums)
        for index, v in enumerate(nums):
            while p1 < n and (len(freq1) < k or (len(freq1) == k and nums[p1] in freq1)):
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1
            
            while p2 < p1 and cnt < k:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                if freq2[nums[p2]] == m:
                    cnt += 1
                p2 += 1
            
            if cnt == k:
                res += p1 - p2 + 1

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            
            freq2[v] -= 1
            if freq2[v] == m - 1:
                cnt -= 1
            
        return res
''',
    call='Solution().countSubarrays([1,2,1,2,2], 2, 2)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 左端 index，粉 = p1，绿 = p2；p1/p2 是开区间右端）',
             pointers={'index': 'blue', 'p2': 'green', 'p1': 'pink'}, h=240, cell=100),
        dict(type='map', var='freq1', label='freq1（index..p1-1：种类 ≤ k）', fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
        dict(type='map', var='freq2', label='freq2（index..p2-1：统计好整数）', fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
        dict(type='text', h=90, size=26, fn=_info),
    ],
    watch=[('index', 'index', 'blue'), ('p1', 'p1', 'pink'), ('p2', 'p2', 'green'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'freq1 = {}': '两个哈希表：`freq1` 管“种类不超过 k 的最远右端 p1”，`freq2` 管“好整数够 k 个的最近右端 p2”',
        'cnt = 0': '`cnt`：`freq2` 窗口里出现 ≥ m 次的整数个数',
        'while p1 < n and': lambda S, B, r: ((f'`freq1` 只有 {len(S.freq1)} 种，没满 k={S.k} → 纳入 `nums[{S.p1}] = {S.nums[S.p1]}`，`p1` 右移' if len(S.freq1) < S.k else f'`freq1` 已满 k={S.k} 种，但 `{S.nums[S.p1]}` 已在窗口里，不增加种类 → 纳入，`p1` 右移')
                                              if S.p1 < S.n and (len(S.freq1) < S.k or (len(S.freq1) == S.k and S.nums[S.p1] in S.freq1))
                                              else f'`p1 = {S.p1}`：再扩就会超过 k 种（或到末尾），停。`index..p1-1` 是最长的合法种类窗口'),
        'p1 += 1': '`p1` → {p1}',
        'while p2 < p1 and cnt < k': lambda S, B, r: (f'好整数 `cnt = {S.cnt}` < k={S.k}：`p2` 继续右移' if S.p2 < S.p1 and S.cnt < S.k
                                                      else f'`p2 = {S.p2}`：好整数已够 k 个（或没法再扩），停'),
        'freq2[nums[p2]] = freq2.get': '`nums[{p2}]` 加入 `freq2`：`{freq2}`',
        'if freq2[nums[p2]] == m': lambda S, B, r: (f'`freq2[{S.nums[S.p2]}] = {S.m}`：刚好出现 m 次，成为好整数 → `cnt` +1（{S.cnt + 1}）' if S.freq2[S.nums[S.p2]] == S.m
                                                    else f'`freq2[{S.nums[S.p2]}] = {S.freq2[S.nums[S.p2]]}` ≠ m，`cnt` 不变'),
        'cnt += 1': '`cnt = {cnt}`',
        'p2 += 1': '`p2` → {p2}',
        'if cnt == k': lambda S, B, r: (f'`cnt = k = {S.k}`：右端在 `p2-1` 到 `p1-1` 之间都合法' if S.cnt == S.k
                                        else f'`cnt = {S.cnt}` < k：以 `index` 为左端没有合法子数组'),
        'res += p1 - p2 + 1': '合法右端下标 `p2-1 .. p1-1`，共 `{p1} − {p2} + 1` = =={p1 - p2 + 1}== 个，`res` → {res}',
        'freq1[v] -= 1': '左端点 `{v}` 移出：`freq1` → `{freq1}`',
        'if freq1[v] == 0': lambda S, B, r: (f'左端点 `{S.v}` 移出 `freq1` 后次数为 0：窗口里没有它了，弹出' if S.freq1[S.v] == 0 else f'左端点 `{S.v}` 移出 `freq1`，次数剩 {S.freq1[S.v]}，保留'),
        'freq1.pop': '`freq1` → `{freq1}`',
        'freq2[v] -= 1': '`freq2` 也移出 `{v}` → `{freq2}`',
        'if freq2[v] == m - 1': lambda S, B, r: (f'左端点 `{S.v}` 也移出 `freq2`：`freq2[{S.v}] = {S.m - 1}`，次数从 m 掉到 m−1，不再是好整数 → `cnt` −1（{S.cnt - 1}）' if S.freq2[S.v] == S.m - 1
                                                 else f'左端点 `{S.v}` 也移出 `freq2`：次数 {S.freq2[S.v]}，好整数个数不变'),
        'cnt -= 1': '`cnt = {cnt}`',
        'return res': '一共 `{res}` 个',
    },
    skip=['freq1[nums[p1]]', 'freq2[nums[p2]] = freq2.get', 'freq1[v] -= 1', 'freq2[v] -= 1', 'freq2 = {}', 'cnt = 0', 'p1 = 0', 'p2 = 0', 'n = len', 'p1 += 1', 'p2 += 1', 'cnt += 1', 'cnt -= 1', 'freq1.pop'],
    max_steps=110,
    cards=dict(
        one_liner='固定左端点，合法右端点夹在 p2 和 p1 之间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 与整数 `k`、`m`',
                 '求子数组个数：恰好 `k` 种不同整数，且每种==至少出现 `m` 次==',
                 '示例：`[1,2,1,2,2], k = 2, m = 2` → `2`'],
        quote='首先找出最大的右边界p1，满足index到p1 - 1这一段中恰好出现了k个不同的整数；接下来在index到p1之间，找出最小的右边界p2，满足index到p2 - 1这一段中出现至少m次的整数有k个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p1`：种类不超过 `k` 的最远右端，用 `freq1` 做变长窗口',
              '`p2`：刚好攒够 `k` 个好整数的最近右端，用 `freq2` 和 `cnt` 做变长窗口',
              '`p2..p1` 之间再加元素也只会是已有的 k 种，仍然合法，共 `p1 − p2 + 1` 个',
              '左端点右移时两个窗口各自去掉 `nums[index]`'],
        summary=['时间 `O(n)`：`index`、`p1`、`p2` 只增不减',
                 '易错：`freq2` 减一后等于 `m-1`，才说明少了一个好整数',
                 '易错：`p2` 不能超过 `p1`，且要 `cnt == k` 才累加',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神用两次“至少”相减；yiduobo 直接数合法右端区间'],
    ),
)
