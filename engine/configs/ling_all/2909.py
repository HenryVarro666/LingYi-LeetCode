NUMS = [5, 4, 8, 3, 9, 7]
L_FORJ, L_RET = 11, 15


def _p1(S):
    """第一遍（倒着算后缀最小值）时的下标 i"""
    return S['i'] if 'ans' not in S and 'i' in S else None


def _pj(S):
    if 'ans' in S and 'j' in S and S['_line'] != L_RET:
        return S['j']
    return None


def _pj1(S):
    j = _pj(S)
    return j + 1 if j is not None else None


def _nums_color(S, k, v):
    i = _p1(S)
    if 'ans' not in S:
        if i is None:
            return None
        return 'pink' if k == i else ('orange' if k > i else None)
    j = _pj(S)
    if j is None:
        return None
    if k == j:
        return 'blue'
    if k < j:
        return 'green' if v == S['pre'] and S['nums'].index(v) == k and k < j else 'cyan'
    if k == j + 1 + list(S['nums'][j + 1:]).index(S['suf'][j + 1]):
        return 'orange'
    return None


def _formula(S):
    j = _pj(S)
    if 'ans' not in S:
        return '先从右往左算后缀最小值 `suf[i] = min(nums[i..n-1])`' if S.get('suf') is not None else ''
    if j is None:
        return '枚举完毕，`ans` 是所有山形三元组里元素和最小的'
    nums, pre, suf = S['nums'], S['pre'], S['suf']
    a, b, c = pre, nums[j], suf[j + 1]
    if S['_line'] == 14:
        return f'`j = {j}`：这一轮用完了，把 `nums[{j}] = {b}` 并进前缀，`pre = {pre}`'
    if S['_line'] == 11 or S['_line'] == 12:
        mark = '山形' if a < b > c else '不是山形'
        return f'`j = {j}`：左边最小 `{a}` < `{b}` > 右边最小 `{c}`？ → =={mark}=='
    return f'`j = {j}`：`pre + nums[j] + suf[j+1] = {a} + {b} + {c} = {a + b + c}`，`ans` = =={S["ans"]}=='


CONFIG = dict(
    num=2909, title='元素和最小的山形三元组 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间 · 前缀最小值 + 后缀最小值数组',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1479'],
    code='''
class Solution:
    def minimumSum(self, nums: List[int]) -> int:
        n = len(nums)
        suf = [0] * n
        suf[-1] = nums[-1]  # 后缀最小值
        for i in range(n - 2, 1, -1):
            suf[i] = min(suf[i + 1], nums[i])

        ans = inf
        pre = nums[0]  # 前缀最小值
        for j in range(1, n - 1):
            if pre < nums[j] > suf[j + 1]:  # 山形
                ans = min(ans, pre + nums[j] + suf[j + 1])  # 更新答案
            pre = min(pre, nums[j])
        return ans if ans < inf else -1
''',
    call=f'Solution().minimumSum({NUMS})',
    expect=15,
    skip=['n = len(nums)'],
    views=[
        dict(type='text', fn=_formula, size=28, h=80),
        dict(type='array', var='nums', label='nums（蓝 = 山顶 j，青 = 左边，绿 = 左边最小 pre，橙 = 右边最小 suf[j+1]）', cell=96,
             pointers={_p1: 'pink', _pj: 'blue'}, pointer_labels={_p1: 'i', _pj: 'j'}, color=_nums_color, h=220),
        dict(type='array', var='suf', label='suf[i] = min(nums[i..n-1])（下标 0、1 用不到）', cell=96,
             pointers={_p1: 'pink', _pj1: 'orange'}, pointer_labels={_p1: 'i', _pj1: 'j+1'},
             dim=lambda S, k, v: k < 2, h=220),
    ],
    watch=[('pre', 'pre', 'cyan'), ('nums[j]', lambda S: S['nums'][S['j']] if _pj(S) is not None else None, 'blue'),
           ('suf[j+1]', lambda S: S['suf'][S['j'] + 1] if _pj(S) is not None else None, 'orange'),
           ('ans', lambda S: S['ans'] if S.get('ans') != float('inf') else '∞', 'green')],
    captions={
        'suf = [0] * n': '`suf[i]` 表示 `nums[i]` 到 `nums[n-1]` 的最小值；先全填 0，只有 `suf[2..n-1]` 会被用到',
        'suf[-1] = nums[-1]': '最后一个数的后缀最小值就是它自己：`suf[{n - 1}] = {nums[-1]}`',
        'for i in range(n - 2, 1, -1)': lambda S, B, ret: ('后缀最小值算完：`suf = ' + str(S.suf) + '`' if 'i' in B and S.i == B.i
                                                           else (f'从右往左，`i = {S.i}`：`j ≥ 1`，用到的 `suf[j+1]` 下标 ≥ 2，所以只倒着算到 2'
                                                                 if 'i' not in B else f'`i = {S.i}`：接着算 `suf[{S.i}]`')),
        'suf[i] = min(': '`suf[{i}] = min(suf[{i + 1}], nums[{i}]) = min({suf[i + 1]}, {nums[i]})` = =={suf[i]}==',
        'ans = inf': '`ans = inf`：还没找到山形三元组',
        'pre = nums[0]': '`pre` 是 `j` 左边所有数的最小值，一开始 `j = 1`，左边只有 `nums[0] = {pre}`',
        'for j in range(1, n - 1)': lambda S, B, ret: ('枚举完所有山顶' if 'j' in B and S.j == B.j
                                                       else (f'枚举山顶 `j = {S.j}`：`i < j < k`，所以 `j` 从 1 到 n-2，左右都至少有一个数'
                                                             if 'j' not in B else f'下一个山顶 `j = {S.j}`：看 `nums[{S.j}] = {S.nums[S.j]}` 左右两边的最小值')),
        'if pre < nums[j] > suf[j + 1]': lambda S, B, ret: (
            f'左边最小 `pre = {S.pre}`、`nums[{S.j}] = {S.nums[S.j]}`、右边最小 `suf[{S.j + 1}] = {S.suf[S.j + 1]}`：'
            + ('两边最小的都比山顶小 → ==山形==，选它俩总和最小' if S.pre < S.nums[S.j] > S.suf[S.j + 1]
               else ('左边最小的 `pre` 都不比山顶小 → 左边没有合法的 `i`' if not S.pre < S.nums[S.j]
                     else '右边最小的 `suf` 都不比山顶小 → 右边没有合法的 `k`'))),
        'ans = min(ans, pre + nums[j] + suf[j + 1])': ('`pre + nums[j] + suf[j+1] = {pre} + {nums[j]} + {suf[j + 1]} = {pre + nums[j] + suf[j + 1]}`，'
                                                       '`ans = min({B.ans}, ·)` = =={ans}=='),
        'pre = min(pre, nums[j])': '`j` 用完了，把 `nums[{j}] = {nums[j]}` 并进前缀：`pre = min({B.pre}, {nums[j]}) = {pre}`（==判断之后==才更新）',
        'return ans if ans < inf else -1': lambda S, B, ret: (f'`ans = {S.ans}`，找到了山形 → 返回 `{ret}`' if S.ans < float('inf')
                                                              else '`ans` 还是 inf，不存在山形 → 返回 `-1`'),
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举山顶 j：左边最小 + nums[j] + 右边最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找下标 `i < j < k`，满足 `nums[i] < nums[j]` 且 `nums[k] < nums[j]`（山形三元组）',
                 '返回所有山形三元组里==元素和最小==的那个；不存在返回 `-1`',
                 '示例：`[8,6,1,5,3]` → `9`（下标 `2,3,4`）',
                 '本视频：`[5,4,8,3,9,7]` → `15`'],
        quote='对于有三个（或者四个）变量的问题，枚举中间的变量往往更好算。枚举中间的 nums[j]，我们需要求出 j 左边所有元素的最小值和右边所有元素的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `j` 作山顶：`i`、`k` 被 `j` 隔开，互不影响',
              '总和要最小 → `i` 取左边的最小值 `pre`，`k` 取右边的最小值 `suf[j+1]`',
              '`suf[i] = min(suf[i+1], nums[i])` 倒着递推；`pre` 一边枚举 `j` 一边更新，只要一个变量'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suf` 数组）',
                 '`pre < nums[j] > suf[j+1]` 是链式比较：两边最小的都严格小于山顶才是山形',
                 '易错：`pre = min(pre, nums[j])` 要放在==判断之后==，否则 `j` 会成为自己的左边',
                 '`suf` 只需要算到下标 2：`j ≥ 1`，所以 `suf[j+1]` 的下标 `≥ 2`',
                 '同类题：2908（数据范围小的版本）、2874、2552'],
    ),
)
