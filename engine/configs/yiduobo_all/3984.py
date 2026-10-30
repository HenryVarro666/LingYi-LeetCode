NUMS = [4, 3, 6]


def _text(S):
    if 'p' not in S:
        if 'hit' in S:
            return f'筛法找出 `nums` 里出现的质因子：`hit` = =={S["hit"]}==（2 总是保留）'
        return '先用筛法找质因子，再逐个当 `k`：倍数 `+v`，非倍数 `−v`，求最大子段和'
    bs = S['best_score']
    return (f'`k = p` = =={S["p"]}==：当前子段和 `s` = =={S["s"]}==，最优 `best_score` = =={"-" if bs is None else bs}==，'
            f'`best_k` = =={S["best_k"]}==')


def _ix(S):
    if 'p' in S and 'v' in S and abs(S['v']) in NUMS:
        return NUMS.index(abs(S['v']))
    return None


def _cap_neg(S, B, ret):
    if S.v % S.p != 0:
        return f'`{S.v} % {S.p} ≠ 0`：不是 `{S.p}` 的倍数，Bob 得分 → 取相反数 `v = {-S.v}`'
    return f'`{S.v} % {S.p} = 0`：是 `{S.p}` 的倍数，Alice 得分，保持 `{S.v}`'


def _cap_best(S, B, ret):
    bs = S.best_score
    if bs is None or bs < S.s:
        return f'`s = {S.s}` 比最优 `{bs}` 更大 → `best_score = {S.s}`，`best_k = {S.p}`'
    return f'`s = {S.s}` 没有超过最优 `{bs}`（相等时保留更小的 `k`）'


CONFIG = dict(
    num=3984, title='可整除游戏', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='筛质因子 + 逐个 k 做最大子段和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1944'],
    code='''
class Solution(object):
    def divisibleGame(self, nums):
        
        best_score = None
        best_k = None

        hit = [2]
        nums_set = set(nums)
        ma = max(nums)

        f = [True] * (ma + 2)
        for x in range(3, ma + 1, 2):
            if f[x]:
                for v in range(x, ma + 1, x):
                    f[v] = False
                    if v in nums_set and hit[-1] != x:
                        hit.append(x)

        for p in hit:
            s = 0
            for v in nums:
                if v % p != 0:
                    v = -v
                
                if s < 0:
                    s = 0
                s += v
                if best_score is None or best_score < s:
                    best_score = s
                    best_k = p
        
        mod = 10 ** 9 + 7
        return best_score * best_k % mod
''',
    call=f'Solution().divisibleGame({NUMS})',
    expect=27,
    skip=['best_score = None', 'best_k = None', 'nums_set = set', 'ma = max', 'f[v] = False', 'for v in range(x'],
    max_steps=110,
    views=[
        dict(type='text', fn=_text, size=24, h=80),
        dict(type='array', var='nums', label='nums（蓝 = 当前 v；绿 = p 的倍数，橙 = 非倍数）', cell=96, h=210,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'v'},
             color=lambda S, i, v: ('blue' if _ix(S) == i else ('green' if 'p' in S and v % S['p'] == 0 else 'orange')) if 'p' in S else None),
        dict(type='array', var='hit', label='hit：要枚举的 k（质因子）', cell=96, h=190),
    ],
    watch=[('x', 'x', 'yellow'), ('p', 'p', 'pink'), ('s', 's', 'blue'), ('best_score', 'best_score', 'green'), ('best_k', 'best_k', 'orange')],
    captions={
        'hit = [2]': '`hit` 存要枚举的 `k`：总是保留 2，顺便处理全 1 的情况',
        'f = [True]': '`f` 是奇数质数筛：`True` 表示还没被划掉',
        'for x in range(3': lambda S, B, r: ('从 3 开始、步长 2，只看奇数 `x`' if 'x' not in B else ('奇数都筛完了，`hit` 就是要枚举的 `k`' if S.x == B.x else f'下一个奇数 `x = {S.x}`')),
        'if f[x]': lambda S, B, r: (f'`f[{S.x}]` 为 {"True，是质数" if S.f[S.x] else "False，已被划掉（合数）"}'),
        'if v in nums_set': lambda S, B, r: (f'`{S.v}` 在 `nums` 里，且质因子 `{S.x}` 还没记录 → 加入 `hit`' if S.v in S.nums_set and S.hit[-1] != S.x else f'`{S.v}` 不在 `nums` 里或 `{S.x}` 已记录，跳过'),
        'hit.append(x)': '`hit` 追加 `{x}` → {hit}',
        'for p in hit': '把 `p = {p}` 当作 `k`：下面做一次最大子段和',
        's = 0': '`s` 清零：这个 `k` 下的当前子段和',
        'if v % p != 0': _cap_neg,
        'v = -v': '`v` 变成 `{v}`',
        'if s < 0': lambda S, B, r: (f'`s = {S.s} < 0`：前面是累赘 → 清零重新开始' if S.s < 0 else f'`s = {S.s}` ≥ 0：保留，继续累加'),
        'if best_score is None': _cap_best,
        's += v': '`s += {v}` → =={s}==',
        'best_score = s': '`best_score` = =={best_score}==',
        'best_k = p': '`best_k` = =={best_k}==',
        'mod = ': '取模常数 `mod = 10^9 + 7`',
        'return best_score': '`best_score × best_k % mod = {best_score} × {best_k}` → =={ret}==',
    },
    cards=dict(
        one_liner='k 只会是质因子：逐个试，每次一趟最大子段和',
        complexity='时间 `O(质因子数 × n + 筛法)`，空间 `O(max(nums))`',
        problem=['Alice 选 `k>1` 和区间 `[l,r]`：`k` 的倍数给 Alice，其余给 Bob',
                 '最大化分数差，并列取最小 `k`，返回 差 × k 取模 `10^9+7`',
                 '本视频：`[4,3,6]` → `27`（`k=3`，差 9）'],
        quote='若k为合数，那么如果改为选择k的某个质因子，那么区间中是老k倍数的元素，必然也是新k的倍数，同时可能出现一些不是老k倍数但是是新k倍数的元素，有机会使得alice的得分更高。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 不是区间内某个数的因子，等于把分全送给 Bob，不优；合数不如它的质因子',
              '所以只试 `nums` 里出现的质因子，用奇数筛法找出来',
              '固定 `k`：倍数保持、其余取相反数，一趟贪心求最大子段和'],
        summary=['时间约 `O(n × 质因子数)`，筛法 `O(U log log U)`',
                 '代码里 `hit` 总带 2：这样全是 1 的情况也自然得到 `k = 2`、差 `-1`',
                 '`best_score < s` 严格小于：并列时保留先试的更小的 `k`',
                 '`best_score` 是负数时取模，Python 的 `%` 结果仍为非负，与题目一致',
                 '对比灵神：灵神预处理每个数的质因子并用前缀和一次扫完；这里按质因子各扫一遍'],
    ),
)
