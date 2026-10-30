def _col(S, i, v):
    nums = S['nums']
    if v == max(nums):
        return 'pink'
    if v == min(nums):
        return 'blue'
    return None


def _info(S):
    if 'other_diff' in S:
        return f"`tot_diff = {S['tot_diff']}`（全变 ma），`min_diff = {S['min_diff']}`，`other_diff = {S['other_diff']}`"
    if 'tot_diff' in S:
        return f"`tot_diff` = 全变成最大值 `ma = {S['ma']}` 总共要加几次 1：{S['tot_diff']}"
    if 'ma' in S:
        return f"最小 `mi = {S['mi']}`，最大 `ma = {S['ma']}`"
    return '看全变成最大值要几次，再看能不能用更大的目标省钱'


def _branch(S):
    if 'sp' not in S:
        return ''
    return f"先花 `res = {S['res']}`，落单的 `sp = {S['sp']}` 次留到最后处理"


CONFIG = dict(
    num=3139, title='使数组中所有元素相等的最小开销', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='分类讨论 · 最小值是否落单',
    tags=['灵神题单', '贪心与思维', '难度分 2666'],
    code='''
class Solution(object):
    def minCostToEqualizeArray(self, nums, cost1, cost2):

        mod = 10 ** 9 + 7

        freq = Counter(nums)
        n = len(nums)

        ma = max(freq.keys())
        mi = min(freq.keys())

        tot_diff = 0
        for v, f in freq.items():
            tot_diff += (ma - v) * f

        min_diff = (ma - mi) * freq[mi]
        other_diff = tot_diff - min_diff

        if cost1 + cost1 <= cost2:
            return tot_diff * cost1 % mod

        if freq[mi] > 1 or min_diff <= other_diff:
            res = tot_diff // 2 * cost2 % mod
            sp = tot_diff % 2
        elif n > 2 and (n - 1) * cost2 < (n - 2) * cost1:
            res = (other_diff * cost2 + (min_diff - other_diff) // (n - 2) * (n - 1) * cost2) % mod
            sp = (min_diff - other_diff) % (n - 2)
        else:
            res = ((min_diff - other_diff) * cost1 + other_diff * cost2) % mod
            sp = 0

        sp_cost = sp * cost1
        if sp > 0 and n > 2:
            if (sp + n) % 2 == 0:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2)
            elif sp % 2 == 0:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2 + cost1, (sp + n + n) // 2 * cost2)
            else:
                sp_cost = min(sp_cost, (sp + n) // 2 * cost2 + cost1)

        res = (res + sp_cost) % mod
        return res
''',
    call='Solution().minCostToEqualizeArray([1,3,4,4], 9, 5)',
    expect=20,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='bars', var='nums', color=_col, h=330, label='nums（蓝 = 最小 mi，粉 = 最大 ma）'),
        dict(type='text', fn=_branch, h=70),
    ],
    watch=['tot_diff', 'min_diff', 'other_diff', ('res', 'res', 'green'), 'sp', 'sp_cost'],
    captions={
        'mod =': '答案对 `10^9 + 7` 取余',
        'freq = Counter': '`freq` 统计每个值出现几次：`{freq}`',
        'n = len': '`n = {n}` 个数',
        'for v, f in freq.items()': lambda S, B, r: ('每种值都算完了' if ('v' in B and B['v'] == S.v) else f'看值 `{S.v}`，出现 `{S.f}` 次'),
        'ma = max': '`ma = {ma}`：最大值，目标起码是它',
        'mi = min': '`mi = {mi}`：最小值',
        'tot_diff = 0': '`tot_diff` 累计「全变成 ma」要加的次数',
        'tot_diff += ': '值 `{v}` 有 {f} 个，每个差 `{ma} − {v}` → `tot_diff` = {tot_diff}',
        'min_diff =': '最小值要补 `min_diff = ({ma} − {mi}) × {freq[mi]}` = =={min_diff}==',
        'other_diff =': '其他数一共 `other_diff = {tot_diff} − {min_diff}` = =={other_diff}==',
        'if cost1 + cost1 <= cost2': lambda S, B, r: ('`cost1 + cost1 ≤ cost2`：两次操作一不比一次操作二贵 → 只用操作一，答案 `tot_diff × cost1`' if S.cost1 + S.cost1 <= S.cost2
                                                       else f'`{S.cost1 * 2} > {S.cost2}`：操作二更划算，继续往下分情况'),
        'return tot_diff * cost1': '只用操作一',
        'if freq[mi] > 1 or': lambda S, B, r: (f'最小值 `{S.mi}` 出现 `{S.freq[S.mi]}` 次，`min_diff = {S.min_diff}` ≤ `other_diff = {S.other_diff}` → 操作二够用，先尽量配对' if (S.freq[S.mi] > 1 or S.min_diff <= S.other_diff)
                                                  else f'最小值 `{S.mi}` 只有 1 个，且 `min_diff = {S.min_diff}` > `other_diff = {S.other_diff}` → 最小值落单，操作二会不够用'),
        'res = tot_diff // 2 * cost2': '操作二够用：`res = {tot_diff} // 2 × {cost2}` = =={res}==，`sp = {tot_diff} % 2` = {sp}',
        'elif n > 2 and': lambda S, B, r: (f'`(n−1)×cost2 = {(S.n - 1) * S.cost2}` < `(n−2)×cost1 = {(S.n - 2) * S.cost1}`：用 n−1 次操作二顶替 n−2 次操作一更划算' if (S.n > 2 and (S.n - 1) * S.cost2 < (S.n - 2) * S.cost1)
                                           else f'`(n−1)×cost2 = {(S.n - 1) * S.cost2}` ≥ `(n−2)×cost1 = {(S.n - 2) * S.cost1}`：顶替不划算 → 落单的全靠操作一'),
        'res = (other_diff * cost2': '其他数先和最小值配 `other_diff` 次；剩下的最小值每 `n−2` 次缺口用 `n−1` 次操作二顶替：`res` = =={res}==',
        'sp = (min_diff - other_diff)': '用不完的缺口 `sp = ({min_diff} − {other_diff}) % ({n} − 2)` = =={sp}==',
        'res = ((min_diff': '顶替也不划算：配完后剩下的全用操作一：`res` = =={res}==，`sp = 0`',
        'sp = 0': '没有落单，`sp = 0`',
        'sp_cost = sp * cost1': '落单的 `sp` 先按全用操作一估价：`sp_cost = {sp} × {cost1}` = =={sp_cost}==',
        'if sp > 0 and n > 2': lambda S, B, r: (f'`sp = {S.sp} > 0` 且 `n > 2`：可以再试试放大目标，用操作二补' if (S.sp > 0 and S.n > 2)
                                                 else '`sp = 0`（或 n ≤ 2）：没有落单的，不用再试'),
        'if (sp + n) % 2 == 0': '`sp + n` 是偶数：选 `sp+1` 个其他数配最小值，剩下的两两配 → `(sp+n)//2` 次操作二',
        'elif sp % 2 == 0': '`sp` 偶、`n` 奇：多出一个落单，用一次操作一补，或把目标再加 1',
        'sp_cost = min': '`sp_cost` 取各方案里最小：=={sp_cost}==',
        'res = (res + sp_cost) % mod': '`res` = res + sp_cost = =={res}==（取余后）',
        'return res': '最小开销 =={res}==',
    },
    cards=dict(
        one_liner='最小值落单时，操作二会不够用，要把目标抬高',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['操作一：一个数 `+1`，花 `cost1`；操作二：两个不同的数各 `+1`，花 `cost2`',
                 '求让所有数相等的最小总开销，结果对 `10^9+7` 取余',
                 '示例：`[4,1], 5, 2` → `15`；本视频：`[1,3,4,4], 9, 5` → `20`'],
        quote='若cost1 * 2 <= cost2，那么就没有使用cost2的意义了，因为所有的cost2操作都可以使用两次cost1操作来替代，所需的代价只会更小。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cost1×2 ≤ cost2`：全用操作一，`tot_diff × cost1`',
              '否则尽量用操作二：最小值多于一个、或补得不比其他数多时，`tot_diff // 2` 次操作二就够',
              '最小值落单且缺口大：用 `n−1` 次操作二顶替 `n−2` 次操作一；剩下的 `sp` 再分奇偶讨论'],
        summary=['时间 `O(n)`，空间 `O(n)`（`Counter`）',
                 '最容易错的是最小值落单时「操作二够不够用」的判断',
                 '`sp` 落单要么全用操作一，要么多抬高目标用操作二，取更便宜者',
                 '对比灵神：灵神证明只需枚举 4 个目标值；yiduobo 按落单情况逐类讨论'],
    ),
)
