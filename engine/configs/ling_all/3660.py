def _text(S):
    if 'suf_min' not in S:
        return '倒着算：分界线左边最大 ≤ 右边最小 → 左边跳不过去，答案就是左边最大'
    if 'i' not in S:
        return '`suf_min`：`nums[i+1:]` 的最小值，初始为无穷大'
    i, pm, sm = S['i'], S['pre_max'][S['i']], S['suf_min']
    ln = S.get('_line')
    if ln == 11:
        return '从右到左全部填完'
    if ln == 10 or ln == 9:
        smv = 'inf' if ln == 9 and sm == float('inf') else sm
        if ln == 10:
            return f'`suf_min` = nums[{i}:] 的最小值 = =={sm}=='
    else:
        smv = sm
    if ln == 8:
        return f'处理分界线 `[0..{i}] | [{i + 1}..]`：看左边最大和右边最小'
    if pm <= sm:
        return f'`pre_max[{i}] = {pm} ≤ suf_min = {smv}` → ans[{i}] = ==pre_max[{i}] = {pm}=='
    return f'`pre_max[{i}] = {pm} > suf_min = {sm}` → ans[{i}] = ==ans[{i + 1}] = {S["ans"][i]}=='


def _acol(S, i, v):
    if 'suf_min' not in S or 'i' not in S:
        return None
    done = i > S['i'] or (i == S['i'] and S.get('_line', 0) >= 10)
    return 'green' if done else None


def _pcol(S, i, v):
    if 'i' in S and i == S['i']:
        return 'yellow'
    return None


CONFIG = dict(
    num=3660, title='跳跃游戏 IX', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='前缀最大 + 后缀最小 · 倒推',
    tags=['灵神题单', '难度分 2187'],
    code='''
class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
        pre_max = list(accumulate(nums, max))  # nums 的前缀最大值

        ans = [0] * n
        suf_min = inf
        for i in range(n - 1, -1, -1):
            ans[i] = pre_max[i] if pre_max[i] <= suf_min else ans[i + 1]
            suf_min = min(suf_min, nums[i])
        return ans
''',
    call='Solution().maxValue([3,1,2,30,10,20])',
    expect=[3, 3, 3, 30, 30, 30],
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='nums', pointers={'i': 'blue'}, label='nums', h=190),
        dict(type='array', var='pre_max', label='pre_max：前缀最大值', color=_pcol, h=170),
        dict(type='array', var='ans', label='ans', color=_acol, h=170),
    ],
    watch=[('i', 'i', 'blue'), ('suf_min', 'suf_min', 'pink'), ('pre_max[i]', 'pre_max[i]', 'yellow')],
    captions={
        'pre_max = list': '`pre_max[i]` = `nums[0..i]` 的最大值：左半边能到的最大值',
        'ans = [0] * n': '`ans` 先占位，从右往左填',
        'suf_min = inf': '`suf_min` = 右边 `nums[i+1:]` 的最小值，最右边没有数，记为无穷大',
        'for i in range': lambda S, B, r: ('循环结束，`i` 已经走到 0' if (B.get('i') == 0 and S.i == 0) else f'倒着枚举 `i = {S.i}`'),
        'ans[i] = ': lambda S, B, r: ((f'`pre_max[{S.i}] = {S.pre_max[S.i]} ≤ suf_min = {B.suf_min}`：分界线右边的数都不比左边最大值小 → 跳不过去，`ans[{S.i}] = {S.ans[S.i]}`')
                                       if S.pre_max[S.i] <= B.suf_min else
                                       f'`pre_max[{S.i}] = {S.pre_max[S.i]} > suf_min = {B.suf_min}`：先跳到最大值，再跳到右边最小值，最后进入右半 → 和 `i+1` 互通，`ans[{S.i}] = ans[{S.i + 1}] = {S.ans[S.i]}`'),
        'suf_min = min': '把 `nums[{i}] = {nums[i]}` 并入后缀最小值：`suf_min` → {suf_min}',
        'return ans': '全部填完 → `{ret}`',
    },
    cards=dict(
        one_liner='倒着想：分界线左边最大值 ≤ 右边最小值，就跳不过去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`i → j`：向右只能跳到更小的数，向左只能跳到更大的数',
                 '对每个下标求：跳任意多次后==能到的最大值==',
                 '示例：`[2,1,3]` → `[2,2,3]`；本视频：`[3,1,2,30,10,20]`'],
        quote='所以倒着思考更简单。如果分界线左边的最大值比分界线右边的最小值还小（或者相等），那么无法从分界线左边跳到分界线右边，所以分界线左边的数无法跳到 nums 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ans[n-1]` 一定是整个数组的最大值，所以从右往左推',
              '若 `pre_max[i] ≤ suf_min[i+1]`：左右两半互相到不了 → `ans[i] = pre_max[i]`',
              '否则 `i` 能跳到左边最大，再到右边最小，再到 `i+1` → `ans[i] = ans[i+1]`'],
        after=[dict(heading='另外两种写法', lines=[
            '普通写法：用循环自己算 `pre_max`，逻辑相同',
            '省空间写法：直接把答案写回 `pre_max`，空间 `O(1)`',
            '本视频用的是 `accumulate(nums, max)` 版本'])],
        summary=['时间 `O(n)`，空间 `O(n)`（返回值不计则 `O(1)` 写法见上）',
                 '`suf_min` 初始为 `inf`，所以 `i = n-1` 总是取 `pre_max`',
                 '先用旧的 `suf_min` 判断，再把 `nums[i]` 并入 `suf_min`',
                 '条件取 `≤`：相等时也跳不过去'],
    ),
)
