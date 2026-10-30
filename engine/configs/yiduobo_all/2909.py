NUMS = [6, 9, 3, 8, 5, 7]
LOOP_LINES = (5, 6, 9, 10, 14, 15, 16, 17)
MAIN_LINES = (14, 15, 16, 17)


def _idx(S):
    if 'index' not in S or S['_line'] not in LOOP_LINES:
        return None
    return S['index']


def _pp(S):
    return S['index'] - 1 if S['_line'] in MAIN_LINES and 'res' in S and 'index' in S else None


def _ps(S):
    return S['index'] + 1 if S['_line'] in MAIN_LINES and 'res' in S and 'index' in S else None


def _pi_prefix(S):
    """第一遍时 prefix 里最新的那一格"""
    return S['index'] if S['_line'] in (5, 6) and 'index' in S else None


def _formula(S):
    ln = S['_line']
    if 'res' not in S:
        if 'suffix' not in S:
            return '先求前缀最小值 `prefix`，再求后缀最小值 `suffix`' if 'prefix' in S else ''
        return '后缀最小值：从右往左存，最后 `reverse` 才和 `nums` 对齐' if 'index' in S and ln != 11 or ln == 8 else \
            '`reverse` 之后：`suffix[i]` = `nums[i..n-1]` 的最小值'
    if ln not in MAIN_LINES or 'index' not in S:
        return '枚举山顶 `index`：左边最小 `prefix[index-1]`，右边最小 `suffix[index+1]`'
    j = S['index']
    nums, pre, suf = S['nums'], S['prefix'][j - 1], S['suffix'][j + 1]
    ok = pre < nums[j] and suf < nums[j]
    cand = pre + nums[j] + suf
    if ln in (14, 15):
        return f'`index = {j}`：`{pre} < {nums[j]}` 且 `{suf} < {nums[j]}`？ → =={"山形" if ok else "不是山形"}=='
    if ln == 16:
        return f'候选和 `{pre} + {nums[j]} + {suf} = {cand}`，当前最小 `res = {S["res"]}`'
    return f'更新：`res = {pre} + {nums[j]} + {suf} = {S["res"]}`'


CONFIG = dict(
    num=2909, title='元素和最小的山形三元组 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间 · 前缀最小值数组 + 后缀最小值数组',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1479'],
    code='''
class Solution(object):
    def minimumSum(self, nums):
        n = len(nums)
        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(min(prefix[-1], nums[index]))

        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        suffix.reverse()

        res = -1
        for index in range(1, n - 1):
            if prefix[index - 1] < nums[index] and suffix[index + 1] < nums[index]:
                if res == -1 or res > prefix[index - 1] + nums[index] + suffix[index + 1]:
                    res = prefix[index - 1] + nums[index] + suffix[index + 1]

        return res
''',
    call=f'Solution().minimumSum({NUMS})',
    expect=16,
    skip=['n = len(nums)', 'for index in range(1, n):', 'for index in range(n - 2, -1, -1)'],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 山顶 index）', cell=80, min_slots=len(NUMS),
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'index'}, h=205),
        dict(type='array', var='prefix', label='prefix[i] = nums[0..i] 的最小值', cell=80, min_slots=len(NUMS),
             pointers={_pi_prefix: 'blue', _pp: 'cyan'}, pointer_labels={_pi_prefix: 'index', _pp: 'index-1'}, h=205),
        dict(type='array', var='suffix', label='suffix（先从右往左存；reverse 后 suffix[i] = nums[i..n-1] 的最小值）', cell=80,
             min_slots=len(NUMS), pointers={_ps: 'orange'}, pointer_labels={_ps: 'index+1'}, h=205),
    ],
    watch=[('index', _idx, 'blue'), ('res', 'res', 'green')],
    captions={
        'prefix = [nums[0]]': '`prefix[i]` 记录 `nums[0..i]` 的最小值（前缀最小值），先放进 `nums[0] = {nums[0]}`',
        'prefix.append(min(': '`prefix[{index}] = min(prefix[{index - 1}], nums[{index}]) = min({prefix[-2]}, {nums[index]})` = =={prefix[-1]}==',
        'suffix = [nums[-1]]': '后缀同理，但要==从右往左==求：先放 `nums[-1] = {nums[-1]}`',
        'suffix.append(min(': '后缀 `[{index}..n-1]` 的最小值 = `min({suffix[-2]}, nums[{index}])` = =={suffix[-1]}==，追加到末尾',
        'suffix.reverse()': '因为是倒着存的，`reverse` 之后 `suffix[i]` 才是 `nums[i..n-1]` 的最小值：`{suffix}`',
        'res = -1': '`res = -1` 表示还没找到山形三元组',
        'for index in range(1, n - 1)': lambda S, B, ret: ('山顶都枚举完了' if 'index' in B and S.index == B.index
                                                         else f'枚举山顶 `index = {S.index}`：`i < j < k`，所以 `index` 从 1 到 n-2'),
        'if prefix[index - 1] < nums[index] and': lambda S, B, ret: (
            f'左边最小 `prefix[{S.index - 1}] = {S.prefix[S.index - 1]}`，山顶 `{S.nums[S.index]}`，右边最小 `suffix[{S.index + 1}] = {S.suffix[S.index + 1]}`：'
            + ('两边都比山顶小 → ==山形==' if S.prefix[S.index - 1] < S.nums[S.index] and S.suffix[S.index + 1] < S.nums[S.index]
               else ('左边最小的都不比山顶小 → 找不出合法的 `i`' if not S.prefix[S.index - 1] < S.nums[S.index]
                     else '右边最小的都不比山顶小 → 找不出合法的 `k`'))),
        'if res == -1 or res >': lambda S, B, ret: (
            (f'`res == -1`：这是第一个山形，直接记下' if S.res == -1
             else (f'候选 `{S.prefix[S.index - 1] + S.nums[S.index] + S.suffix[S.index + 1]}` 比当前最小 `res = {S.res}` ==更小== → 更新'
                   if S.res > S.prefix[S.index - 1] + S.nums[S.index] + S.suffix[S.index + 1]
                   else f'候选 `{S.prefix[S.index - 1] + S.nums[S.index] + S.suffix[S.index + 1]}` 不比 `res = {S.res}` 小 → 不更新'))),
        'res = prefix[index - 1] + nums[index] + suffix[index + 1]': '`res = {prefix[index - 1]} + {nums[index]} + {suffix[index + 1]}` = =={res}=='
        ,
        'return res': lambda S, B, ret: (f'返回 `res = {S.res}`' if S.res != -1 else '一个山形都没找到，`res` 还是 -1'),
    },
    max_steps=70,
    cards=dict(
        one_liner='枚举山顶，左右各取最小值，总和一定最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找下标 `i < j < k`，满足 `nums[i] < nums[j]` 且 `nums[k] < nums[j]`（山形三元组）',
                 '返回元素和最小的山形三元组的和；没有则返回 `-1`',
                 '2908 和 2909 题设相同，2909 数据规模大（`n ≤ 10^5`），不能暴力',
                 '本视频：`[6,9,3,8,5,7]` → `16`'],
        quote='若nums[0]到nums[j - 1]之间最小值小于nums[j]，那么就应该选择这个数作为nums[i]才能使得最终答案最小；反之若最小值大于等于nums[j]，那么说明在0到j - 1找不出可用的i。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个山顶 `j`，要使总和最小，`i` 取左边的最小值，`k` 取右边的最小值',
              '左边最小值是前缀最小值数组 `prefix`，右边最小值是后缀最小值数组 `suffix`',
              '`prefix`、`suffix` 各遍历一遍求出，再枚举 `j`：`prefix[j-1] + nums[j] + suffix[j+1]`',
              '`prefix[j-1]` 或 `suffix[j+1]` 不小于 `nums[j]` 时，这个 `j` 不能作山顶'],
        summary=['时间 `O(n)`，空间 `O(n)`：两个数组 `prefix`、`suffix`',
                 '易错：`suffix` 是倒着 `append` 的，==必须 `reverse`== 才和下标对齐',
                 '`res` 用 `-1` 做哨兵：`res == -1 or res > 候选` 才更新',
                 '原文为 Python 2 风格写法（`class Solution(object)`），代码未改，只删去了空行里的缩进空格',
                 '对比灵神：灵神 `pre` 只用一个变量边枚举边更新，只需要一个 `suf` 数组；yiduobo 前后缀都存成数组'],
    ),
)
