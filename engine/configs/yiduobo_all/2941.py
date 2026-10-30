NUMS, K = [6, 3, 9, 12, 4], 2


def _cur(S):
    return S['nums'].index(S['v']) if 'v' in S and S['v'] in S['nums'] else None


def _txt(S):
    if 'v' not in S:
        return f'`f[g] = [和, 长度]`：以当前数结尾、gcd 恰为 `g` 的子数组里，==和最大（也就是最长）==的那个；长度要 `>= k = {S["k"]}`'
    return f'当前数 `v = {S["v"]}`：和旧的每个 `g` 求 gcd，得到新的 `new_g`，再拼进 `tmp`'


_cnt = {'g': 0, 'n': 0}


def _tmp_cap(S, B, ret):
    _cnt['g'] = 0
    return f'先放入只含 `v = {S.v}` 的子数组：gcd = `{S.v}`，和 `{S.v}`，长度 1'


def _for_g(S, B, ret):
    _cnt['g'] += 1
    if _cnt['g'] > len(S.f):
        return f'旧状态 {len(S.f)} 个 gcd 都接过 `v = {S.v}` 了，`tmp` 就是新的状态'
    return f'取旧状态的下一个 gcd：`g = {S.g}`，和 `v = {S.v}` 求 gcd'


def _f_tmp(S, B, ret):
    _cnt['n'] = 0
    return '`f` 换成 `tmp`：gcd 衰减很快，状态数很少，直接遍历'


def _for_n(S, B, ret):
    _cnt['n'] += 1
    if _cnt['n'] > len(S.f):
        return '这个位置的所有 gcd 都检查完了，处理下一个数'
    return f'检查第 {_cnt["n"]} 个状态：`gcd = {S.new_g}`'


def _fmt(k, v):
    return f'gcd={k}：和 {v[0]}，长 {v[1]}'


CONFIG = dict(
    num=2941, title='子数组的最大GCD-Sum', difficulty='Hard', category='位运算',
    author='yiduobo', technique='gcd 衰减 · 以 nums[i] 结尾的哈希表 DP',
    tags=['灵神题单·位运算', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def maxGcdSum(self, nums, k):

        if k == 1:
            res = nums[0] * nums[0]
        else:
            res = 0

        f = {nums[0]: [nums[0], 1]}

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for v in nums[1:]:
            tmp = {v : [v, 1]}
            for g in f:
                new_g = gcd(g, v)
                if new_g not in tmp or tmp[new_g][0] < f[g][0] + v:
                    tmp[new_g] = [f[g][0] + v, f[g][1] + 1]
            
            f = tmp
            for new_g in f:
                if f[new_g][1] >= k:
                    res = max(res, f[new_g][0] * new_g)
        
        return res
''',
    call=f'Solution().maxGcdSum({NUMS}, {K})',
    expect=90,
    views=[
        dict(type='text', h=100, size=27, fn=_txt),
        dict(type='array', var='nums', label='nums', h=170, cell=96, color=lambda S, i, v: 'blue' if _cur(S) == i else None),
        dict(type='map', var='f', label='f（上一个位置的状态）', fmt=_fmt, h=170, font=26),
        dict(type='map', var='tmp', label='tmp（当前位置的新状态）', fmt=_fmt, h=170, font=26),
    ],
    watch=['v', 'g', 'new_g', ('res', 'res', 'green')],
    skip=['while y', 'x, y = y, x % y', 'return x'],
    captions={
        'if k == 1': '`k = {k}`：{"==只取一个数也达标==，答案至少是 nums[0] 的平方" if k == 1 else "单个数长度不够，答案先记 0"}',
        'res = 0': '`k = {k} > 1`：单个数长度不够，先记 `res = 0`',
        'f = {nums[0]:': '初始状态：以 `nums[0] = {nums[0]}` 结尾，gcd 就是它自己，和 `{nums[0]}`，长度 1',
        'tmp = {v': _tmp_cap,
        'for g in f': _for_g,
        'for new_g in f': _for_n,
        'new_g = gcd': '`g = {g}`：把 `v = {v}` 接在这类子数组后面，新的 gcd = `gcd({g}, {v})`',
        'if new_g not in tmp': lambda S, B, ret: (
            f'`new_g = {S.new_g}` 还没出现过 → ==直接放入 tmp==' if S.new_g not in S.tmp
            else f'`new_g = {S.new_g}` 已有，旧和 `{S.tmp[S.new_g][0]}`，新和 `{S.f[S.g][0] + S.v}` → '
                 + ('新的更大，==覆盖==：和大 = 子数组更长' if S.tmp[S.new_g][0] < S.f[S.g][0] + S.v else '旧的更大，保留')),
        'tmp[new_g] =': '`tmp[{new_g}]` = [和 `{f[g][0]} + {v}`，长 `{f[g][1]} + 1`] = =={tmp[new_g]}==',
        'f = tmp': _f_tmp,
        'if f[new_g][1]': '`gcd = {new_g}` 的长度 `{f[new_g][1]}` {">=" if f[new_g][1] >= k else "<"} `k = {k}` → {"达标，可以更新答案" if f[new_g][1] >= k else "不够长，跳过"}',
        'res = max': '`{f[new_g][0]} × {new_g}` = {f[new_g][0] * new_g}，`res = max({B.res}, {f[new_g][0] * new_g})` = =={res}==',
    },
    cards=dict(
        one_liner='gcd 衰减很快，直接用哈希表暴力 DP',
        complexity='时间约 `O(n log U)`，空间 `O(log U)`',
        problem=['给数组 `nums` 和整数 `k`：只看长度至少为 `k` 的子数组。',
                 '子数组的得分 = 元素和 × 元素的最大公约数，求最大得分。',
                 '示例：`[6,3,9,12,4]`、`k=2` → 90。'],
        quote='随着数组长度的扩展，gcd衰减的速度是很快的，因此在这里应该可以直接使用暴力的动态规划。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][g]`：以 `nums[i]` 结尾、gcd 为 `g` 的子数组的 ==最大和及长度==。',
              '转移：把 `nums[i]` 接在旧状态后面，`new_g = gcd(g, nums[i])`。',
              '同一个 gcd 下，和越大就是子数组越长，更容易满足长度 `>= k`。',
              '`k = 1` 时单独一个数也达标，要特殊处理。'],
        summary=['gcd 沿着子数组变长只会不断减小，每次至少减半，所以每个位置的状态很少。',
                 '同 gcd 只保留和最大的一个：右端点固定时，和大 = 更长。',
                 '易错：`k = 1` 时第一个数自己也要算进答案。',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行。'],
    ),
)
