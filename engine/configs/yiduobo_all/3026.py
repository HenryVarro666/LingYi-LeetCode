def _best(S, d):
    return S['best_prefix'].get(d, None)


def _txt(S):
    if 'v' not in S:
        return '区间和 = 两个前缀和之差：对每个 `v` 找首尾差为 `k`、前缀和最小的开头'
    lo, hi = _best(S, S['v'] - S['k']), _best(S, S['v'] + S['k'])
    f = lambda a: '无' if a is None else str(a)
    return f"`best_prefix[{S['v'] - S['k']}]` = =={f(lo)}==，`best_prefix[{S['v'] + S['k']}]` = =={f(hi)}==，当前 `s` = {S['s']}"


CONFIG = dict(
    num=3026, title='最大好子数组和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 最优前缀哈希表',
    tags=['难度分 1817'],
    code='''
class Solution(object):
    def maximumSubarraySum(self, nums, k):

        best_prefix = {}
        s = 0
        res = None
        for v in nums:
            if v not in best_prefix or best_prefix[v] > s:
                best_prefix[v] = s
            
            s += v
            if v - k in best_prefix and (res is None or res < s - best_prefix[v - k]):
                res = s - best_prefix[v - k]
            
            if v + k in best_prefix and (res is None or res < s - best_prefix[v + k]):
                res = s - best_prefix[v + k]
        
        if res is None:
            res = 0
        return res
''',
    call='Solution().maximumSubarraySum([1,2,3,4,5,6], 2)',
    expect=15,
    views=[
        dict(type='array', var='nums', h=190, label='nums（蓝色 = 当前 v）',
             color=lambda S, i, x: 'blue' if 'v' in S and x == S['v'] else None),
        dict(type='map', var='best_prefix', label='best_prefix：值 v → 以 v 开头的最小前缀和（不含 v 自己）',
             fmt=lambda k, v: f'{k}: {v}', h=230, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        'best_prefix = {}': '`best_prefix[v]`：所有等于 `v` 的 `nums[i]` 里，它们==前面==那段前缀和的最小值',
        's = 0': '`s` 是到上一个数为止的前缀和',
        'res = None': '`res` 用 `None` 表示还没找到好子数组',
        'if v not in best_prefix': lambda S, B, r: (f"此时 `s = {S.s}` 是 `v = {S.v}` 之前的前缀和：" +
                                                   ('`v` 还没登记过 → 记下 `best_prefix[v] = s`' if B.best_prefix.get(S.v) is None
                                                    else (f"已有 `{B.best_prefix[S.v]}`，当前 `{S.s}` 更小 → 更新" if B.best_prefix[S.v] > S.s
                                                          else f"已有 `{B.best_prefix[S.v]}` 不更大，保持不变"))),
        'best_prefix[v] = s': '登记：`best_prefix[{v}] = {s}`',
        's += v': '先登记，再把 `v` 加进前缀和：`s` → {s}（现在 `s` 是含 `v` 的前缀和）',
        'if v - k in best_prefix': lambda S, B, r: (f"开头值 `v−k = {S.v - S.k}` " + ('不在表里，没有这样的开头' if (S.v - S.k) not in S.best_prefix
                                                    else f"在表里，最优前缀 `{S.best_prefix[S.v - S.k]}`：区间和 = `{S.s} − {S.best_prefix[S.v - S.k]}` = =={S.s - S.best_prefix[S.v - S.k]}=="
                                                    + ('，比 res 大 → 更新' if (B.res is None or B.res < S.s - S.best_prefix[S.v - S.k]) else '，不比 res 大'))),
        'res = s - best_prefix[v - k]': '`res` 更新为 =={res}==',
        'if v + k in best_prefix': lambda S, B, r: (f"开头值 `v+k = {S.v + S.k}` " + ('不在表里，没有这样的开头' if (S.v + S.k) not in S.best_prefix
                                                    else f"在表里，最优前缀 `{S.best_prefix[S.v + S.k]}`：区间和 = `{S.s} − {S.best_prefix[S.v + S.k]}` = =={S.s - S.best_prefix[S.v + S.k]}=="
                                                    + ('，比 res 大 → 更新' if (B.res is None or B.res < S.s - S.best_prefix[S.v + S.k]) else '，不比 res 大'))),
        'res = s - best_prefix[v + k]': '`res` 更新为 =={res}==',
        'if res is None': lambda S, B, r: '没找到好子数组 → 返回 0' if S.res is None else '至少找到一个好子数组，保留 `res`',
        'return res': '最大好子数组和 `{res}`',
    },
    cards=dict(
        one_liner='区间和转前缀和：每种开头值只留最小的前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找下标 `(i, j)`，满足 `|nums[i] − nums[j]| = k`，使 `i..j` 的区间和最大',
                 '没有满足条件的子数组则返回 `0`',
                 '本视频：`[1,2,3,4,5,6]`，`k = 2` → `15`（子数组 `[4,5,6]`）'],
        quote='best_prefix[v]储存的是对于所有等于v的nums[i]，其上一轮的前缀和，也就是nums[0] + nums[1] + ... + nums[i - 1]的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和是前缀和之差：`nums[i..j]` = `s[j+1] − s[i]`',
              '遍历到 `v` 时：先把“`v` 作为开头”的前缀和登记，再累加 `s`',
              '用 `s − best_prefix[v−k]` 和 `s − best_prefix[v+k]` 两个候选更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：==顺序是先登记 `best_prefix[v]`、再 `s += v`、最后查表==',
                 '`res` 用 `None` 而不是 0 作初值，因为答案可能是负数',
                 '`k = 0` 时 `v−k` 与 `v+k` 是同一个键（本题 `k` 为正，不会出现）',
                 '代码原文即为 Python 3 可运行写法，未做修改'],
    ),
)
