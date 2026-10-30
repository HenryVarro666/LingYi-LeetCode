NUMS = [3, 7, 5]


def _cand(S, i, v):
    if 'right' not in S:
        return None
    if v < S['left']:
        return 'red'
    if v > S['right']:
        return 'green'
    return None


def _ops(S):
    if 'mid' not in S or 'cnt' not in S or S['_line'] not in (13, 14, 15, 17):
        return []
    m = S['mid']
    upto = len(NUMS) if S['_line'] == 17 else NUMS.index(S['v']) + 1
    return [x // m + (1 if x % m else 0) if j < upto else '?' for j, x in enumerate(NUMS)]


def _top(S):
    if 'right' not in S:
        return 'k 越大，操作次数越少、`k²` 越大 → ==二分答案=='
    if 'mid' in S and 'cnt' in S and S['_line'] in (13, 14, 15, 17):
        m = S['mid']
        return f"`k = mid = {m}`：已累计操作 `cnt = {S['cnt']}` 次，要求 `≤ mid² = {m * m}`"
    if S['left'] < S['right']:
        return f"答案在 `[{S['left']}, {S['right']}]` 里"
    return f"`left == right = {S['left']}`：最小的 k"


def _if(S, B, ret):
    m = S.mid
    if S.cnt <= m * m:
        return f'`cnt = {S.cnt} ≤ {m}² = {m * m}`：k = {m} 满足 → ==修正上界== `right = mid`'
    return f'`cnt = {S.cnt} > {m}² = {m * m}`：k = {m} 不满足 → ==修正下界== `left = mid + 1`'


CONFIG = dict(
    num=3824, title='减小数组使其满足条件的最小 K 值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 一趟遍历计数',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1531'],
    code='''
class Solution(object):
    def minimumK(self, nums):
        
        n = len(nums)
        ma = max(nums)

        left = 1
        right = max(ma, int(n ** 0.5) + 1)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            for v in nums:
                cnt += v // mid
                if v % mid != 0:
                    cnt += 1
            
            if cnt <= mid * mid:
                right = mid
            else:
                left = mid + 1
    
        return left
''',
    call=f'Solution().minimumK({NUMS})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(1, max(NUMS) + 1)),
             label='候选 k（红 = 确认不满足，绿 = 确认满足但更大，灰 = 待定）', cell=84, index=False, color=_cand,
             pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, h=240),
        dict(type='array', var='nums', label='nums（黄 = 当前 v）', cell=110, h=170,
             color=lambda S, i, v: 'yellow' if 'v' in S and S['_line'] in (13, 14, 15) and S['nums'].index(S['v']) == i else None),
        dict(type='array', var=_ops, label='每个数要减几次 mid：v // mid，有余数再 +1（向上取整）', cell=110, index=False, h=170,
             color=lambda S, i, v: 'cyan' if isinstance(v, int) else None),
    ],
    watch=['n', 'ma', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'green'), 'v'],
    skip=['for v in'],
    captions={
        'n = len': '`n = {n}`',
        'ma = max': '`ma = max(nums) = {ma}`：k = ma 时每个数都只要减一次',
        'left = 1': '下界 `left = 1`',
        'right = max': '上界 `max(ma, int(sqrt(n)) + 1) = {right}`：k = ma 时 `k² ≥ n` ==未必成立==，所以要和 sqrt(n) 取大',
        'while left < right': lambda S, B, r: (f'`[{S.left}, {S.right}]` 不为空，继续二分' if S.left < S.right
                                                else f'`left == right = {S.left}`，结束'),
        'mid = (left': '`mid = ({left} + {right}) // 2 = {mid}`',
        'cnt = 0': '一趟遍历，计算 `nonPositive(nums, {mid})`',
        'cnt += v // mid': '`{v} // {mid} = {v // mid}` → `cnt = {cnt}`',
        'if v % mid != 0': lambda S, B, r: (f'`{S.v} % {S.mid} = {S.v % S.mid} ≠ 0`：还剩一点 → ==再减一次==' if S.v % S.mid
                                             else f'`{S.v} % {S.mid} = 0`：正好减到 0'),
        'cnt += 1': '`cnt = {cnt}`',
        'if cnt <= mid * mid': _if,
        'right = mid': '`right = {right}`',
        'left = mid + 1': '`left = {left}`',
        'return left': '满足 `nonPositive ≤ k²` 的最小 k =={ret}==',
    },
    cards=dict(
        one_liner='操作次数随 k 变少、k² 随 k 变大：二分答案找最小 k',
        complexity='时间 `O(n log(max(nums)))`，空间 `O(1)`',
        problem=['正整数数组 `nums`，一次操作把某个 `nums[i]` 减去 `k`',
                 '`nonPositive(nums, k)`：所有数都变为非正的最少操作次数',
                 '求满足 `nonPositive(nums, k) ≤ k²` 的==最小== k；示例 `[3,7,5]` → `3`'],
        quote='在这种情况下，nonPositive(nums, k)恰好就等于nums的长度n，但是此时的==k^2并不一定大于等于n==。……于是这里二分的上界就应该取max(max(nums), sqrt(n)向上取整)。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数要操作 `nums[i] / k` 向上取整次',
              'k 越大 nonPositive 越小、k² 越大 → 满足的可能越大 → 二分',
              '上界不能只取 `max(nums)`：还要保证 `k² ≥ n`'],
        summary=['时间 `O(n log(max(nums)))`，空间 `O(1)`',
                 '易错：上界只取 `max(nums)` 会漏掉 `n > max(nums)²` 的情况',
                 '向上取整写成 `v // mid`，有余数再 `+1`',
                 '对比灵神：灵神用 `(x−1)//k + 1`，并用 `cbrt(S)` 把下界再夹紧'],
    ),
)
