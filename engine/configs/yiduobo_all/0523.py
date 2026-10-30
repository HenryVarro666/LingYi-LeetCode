NUMS, K = [23, 2, 6, 4, 7], 6


def _done(S):
    # 已经算好“前缀和 % k”的最后一个下标
    if 'now' not in S:
        return -1
    if 'index' not in S:
        return 0
    return S['index'] - 1 if S.get('_line') in (18, 19) else S['index']


def _rems(S):
    d = _done(S)
    out, s = [], 0
    for j, x in enumerate(NUMS):
        s += x
        out.append(s % K if j <= d else '·')
    return out


def _hit(S):
    # 当前余数在 dict 里出现过：返回 (上次位置, 当前位置)
    if S.get('_line') not in (21, 22, 23) or 'index' not in S:
        return None
    p = S['sum_dict'].get(S['now'])
    return (p, S['index']) if p is not None and p != S['index'] else None


def _rem_color(S, i, v):
    h = _hit(S)
    if h and i in h:
        return 'green' if h[1] - h[0] >= 2 else 'orange'
    return 'yellow' if i == _done(S) and v != '·' else None


def _formula(S):
    h = _hit(S)
    if h:
        p, i = h
        sub = NUMS[p + 1:i + 1]
        tail = '长度 ≥ 2 → ==找到==' if i - p >= 2 else '长度只有 1 → 不算'
        return (f"余数 `{S['now']}` 在位置 `{p}` 出现过 → `nums[{p + 1}..{i}]` 的和 "
                f"`{sum(sub)}` 是 {K} 的倍数，{tail}")
    return '`prefix_sum[r] − prefix_sum[l − 1] = n × k` ⇔ 两个前缀和 ==对 k 取模的余数相同=='


CONFIG = dict(
    num=523, title='连续的子数组和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和取模 · dict 记余数首次位置',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def checkSubarraySum(self, nums, k):

        if len(nums) < 2:
            return False

        if k == 0:
            for index in range(1, len(nums)):
                if nums[index] == 0 and nums[index - 1] == 0:
                    return True
            return False

        sum_dict = {0: -1}
        now = nums[0] % k
        if now not in sum_dict:
            sum_dict[now] = 0

        for index in range(1, len(nums)):
            now += nums[index]
            now %= k
            if now in sum_dict:
                if index - sum_dict[now] >= 2:
                    return True
            else:
                sum_dict[now] = index

        return False
''',
    call=f'Solution().checkSubarraySum({NUMS}, {K})',
    expect=True,
    views=[
        dict(type='text', fn=_formula, h=100, size=26),
        dict(type='array', var='nums', label=f'nums（k = {K}）', pointers={'index': 'blue'},
             window=(lambda S: _hit(S)[0] + 1 if _hit(S) else None, lambda S: _hit(S)[1] if _hit(S) else None),
             h=210),
        dict(type='array', var=_rems, label='前缀和 % k（黄 = 刚算出；绿/橙 = 余数相同的两个位置）',
             color=_rem_color, h=150),
        dict(type='map', var='sum_dict', label='sum_dict（余数 → 首次出现的位置）', fmt=lambda k, v: f'{k}: {v}',
             h=130, font=30),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'yellow')],
    captions={
        'if len(nums) < 2': '长度不到 2 不可能有解；这里 `len = {len(nums)}`，继续',
        'if k == 0': '`k = {k} ≠ 0`，可以对 k 取模（k = 0 要单独判断）',
        'sum_dict = {0: -1}': '`{{0: -1}}`：空前缀的和是 0，记在==位置 -1==，从下标 0 开始的子数组也能被找到',
        'now = nums[0] % k': '`now`：前缀和对 k 的余数。`prefix_sum[0] % {k} = {nums[0]} % {k} = {now}`',
        'if now not in sum_dict': lambda S, B, r: (f'余数 `{S.now}` 第一次出现' if S.now not in B.sum_dict
                                                   else f'余数 `{S.now}` 已经在 dict 里'),
        'sum_dict[now] = 0': '记下余数 `{now}` 首次出现在位置 `0`',
        'for index in range': lambda S, B, r: (f'扫描 `index = {S.index}`' if 'index' not in B or B.index != S.index
                                               else '扫描结束'),
        'now += nums[index]': '加上 `nums[{index}] = {nums[index]}`：`now = {B.now} + {nums[index]} = {now}`',
        'now %= k': '对 k 取模：`now = {B.now} % {k}` = =={now}==（只需要余数）',
        'if now in sum_dict': lambda S, B, r: (
            f'余数 `{S.now}` ==出现过==（位置 {S.sum_dict[S.now]}）→ 这两个前缀和之差是 {S.k} 的倍数'
            if S.now in S.sum_dict else f'余数 `{S.now}` 没出现过'),
        'if index - sum_dict[now] >= 2': lambda S, B, r: (
            f'间隔 `{S.index} − {S.sum_dict[S.now] if S.sum_dict[S.now] >= 0 else "(-1)"} = {S.index - S.sum_dict[S.now]} ≥ 2`：子数组至少 2 个元素 → ==满足=='
            if S.index - S.sum_dict[S.now] >= 2 else
            f'间隔 `{S.index} − {S.sum_dict[S.now]} = 1 < 2`：子数组只有 `[{S.nums[S.index]}]` 一个元素，==不算=='),
        'return True': '返回 `True`：`nums[{sum_dict[now] + 1}..{index}]` 的和 `{sum(nums[sum_dict[now] + 1:index + 1])}` 是 {k} 的倍数',
        'sum_dict[now] = index': '余数 `{now}` 首次出现，记下位置 `{index}`；==以后不覆盖==，保证间隔尽量大',
        'return False': '没有找到，返回 `False`',
    },
    cards=dict(
        one_liner='子数组和是 k 的倍数 ⇔ 两个前缀和模 k 同余；dict 记余数首次出现的位置',
        complexity='时间 `O(n)`，空间 `O(min(n, k))`',
        problem=['给整数数组 `nums` 和整数 `k`，判断是否存在==长度至少为 2==、',
                 '且元素和为 `k` 的倍数的连续子数组（`0` 也算 k 的倍数）',
                 '示例：`nums = [23,2,4,6,7], k = 6` → `true`（`[2,4]` 和为 6）',
                 f'本视频：`{NUMS}, k = {K}` → `true`（`[2,6,4]` 和为 12）'],
        quote='求前缀和的同时将其对k取模得到余数m，并使用dict将保存这些余数首次出现的位置。当某个余数已经在dict中出现过时，检测当前的位置与上次出现的位置之间的==间隔是否大于等于2==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`S = nums[l..r] = prefix_sum[r] − prefix_sum[l − 1] = n × k`',
              '若 `prefix_sum[l − 1] = x·k + m`，`prefix_sum[r] = y·k + m`，差就是 k 的倍数',
              '所以只要找两个==余数相同==、位置间隔 ≥ 2 的前缀'],
        result='返回 `True`：`[2, 6, 4]` 的和 12 是 6 的倍数',
        summary=['时间 `O(n)`，空间 `O(min(n, k))`',
                 '`{0: -1}` 不能漏：否则从下标 0 开始的子数组找不到',
                 '余数==只记第一次==出现的位置，间隔才最大；本例 `[6]` 长度 1 不算',
                 '`k == 0` 的特判来自旧题面（数非负时需要两个连续的 0）；现题面 `k ≥ 1`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动'],
    ),
)
