def _idx(S):
    if 'v' in S and S['v'] in S['nums']:
        return S['nums'].index(S['v'])
    return None


def _bcolor(S, i, v):
    if 's' in S and i == S['s'] and 'v' in S:
        return 'yellow'
    return None


def _text(S):
    if 'v' not in S or 's' not in S:
        return '`res` = 当前前缀删完后的最小和；`best[s]` = 模 k 余 s 的前缀里最小的 res'
    return f"当前 `v = {S['v']}`，前缀和模 k 得 ==s {S['s']}==；`best[{S['s']}]` 就是余数相同的最优前缀"


CONFIG = dict(
    num=3654, title='删除可整除和后的最小数组和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前缀和余数 + best 数组',
    tags=['灵神题单', '动态规划', '难度分 2039'],
    code='''
class Solution(object):
    def minArraySum(self, nums, k):
        
        best = [None] * k
        best[0] = 0
        f = [0]
        s = 0
        res = 0
        for v in nums:
            res += v
            s += v
            s %= k
            if best[s] is not None:
                res = min(res, best[s])
            
            if best[s] is None or best[s] > res:
                best[s] = res
        
        return res
''',
    call='Solution().minArraySum([3,1,4,2,5], 4)',
    expect=3,
    skip=['f = [0]'],
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var='nums', pointers={'nums.index(v)': 'blue'}, label='nums', h=190,
             color=lambda S, i, v: 'blue' if _idx(S) == i else None,
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S)),
        dict(type='array', var='best', label='best[s]：余数 s 对应的最优 res（None = 没出现过）', h=190,
             pointers={'s': 'pink'}, color=_bcolor),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'pink'), ('res', 'res', 'green')],
    captions={
        'best = [None]': '`best` 长 `k = {k}`：记录每种前缀余数的最优值，None 表示还没见过',
        'best[0] = 0': '空前缀的余数是 0，最小和是 0',
        's = 0': '`s` 是前缀和，`res` 是保留当前元素时的最小和',
        'res = 0': '`s` 是前缀和，`res` 是保留当前元素时的最小和',
        'for v in nums': lambda S, B, r: ('数组处理完了，退出循环' if B.get('v') == S.get('v') else f"处理 `v = {S['v']}`"),
        'res += v': '先假设保留 `v`：`res` = {B.res} + {v} = =={res}==',
        's += v': '前缀和加上 `v`',
        's %= k': '只关心模 k 的余数：`s` = =={s}==',
        'if best[s] is not None': lambda S, B, r: (f"`best[{S.s}] = {S.best[S.s]}`：以前出现过同余前缀，中间那段和是 k 的倍数，可以整段删掉" if S.best[S.s] is not None else f"`best[{S.s}]` 为 None：没有同余的前缀，删不了"),
        'res = min(res, best[s])': '删掉那一段：`res = min({B.res}, {best[s]})` = =={res}==',
        'if best[s] is None or': lambda S, B, r: (f"`best[{S.s}]` 还是 None → 记下 `{S.res}`" if S.best[S.s] is None else (f"`best[{S.s}] = {S.best[S.s]} > res = {S.res}` → 更新为更小的" if S.best[S.s] > S.res else f"`best[{S.s}] = {S.best[S.s]}` 已经不大于 `res = {S.res}`，保持")),
        'best[s] = res': '`best[{s}]` 更新为 =={res}==',
        'return res': '最小可能和 `{res}`',
    },
    cards=dict(
        one_liner='区间和是 k 的倍数，等价于两端前缀和模 k 相等',
        complexity='时间 `O(n + k)`，空间 `O(k)`',
        problem=['可多次删除和为 `k` 的倍数的连续子数组，删后元素补齐',
                 '求删除后数组和的最小值',
                 '本视频：`[3,1,4,2,5], k=4` → `3`'],
        quote='对于上面的区间和模k等于0的这一条件，可以转化为前缀和模k是否相等，也就是说对于f[index]，不妨设当前的前缀和为s[index]，那么在这里就只需要找出所有满足s[p - 1] % k等于s[index] % k的下标p。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]`：保留当前元素就是 `f[index-1]`，删除就从同余前缀的 `f` 取最小',
              '用数组 `best` 记每种余数的最优 `f`，直接取 `best[s]`',
              '`f` 和前缀和都只依赖上一轮，所以只留一个 `res` 变量'],
        summary=['时间 `O(n + k)`，空间 `O(k)`',
                 '`best[s]` 为 None 表示余数还没出现过，不能删',
                 '先用 `best[s]` 更新 `res`，再用 `res` 反过来更新 `best[s]`',
                 '代码里 `f = [0]` 没有用到，是原文留下的',
                 '对比灵神：灵神用 `inf` 初始化 `min_f`，yiduobo 用 None 并显式判断'],
    ),
)
