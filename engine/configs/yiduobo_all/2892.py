def _grp(S):
    """按贪心模拟：到当前处理位置为止，每个元素属于第几组"""
    nums, k = S['nums'], S['k']
    if 'v' not in S:
        upto = 0
    else:
        upto = nums.index(S['v'])
    g, now, out = 0, nums[0], [0]
    for j in range(1, upto + 1):
        if now * nums[j] <= k:
            now *= nums[j]
        else:
            now = nums[j]
            g += 1
        out.append(g)
    return out


def _col(S, i, v):
    if min(S['nums']) == 0 or 'now' not in S:
        return None
    g = _grp(S)
    if i < len(g):
        return ['blue', 'green', 'purple', 'orange', 'cyan'][g[i] % 5]
    return None


CONFIG = dict(
    num=2892, title='将相邻元素相乘后得到最小化数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 乘积不超过 k 的最少分组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minArrayLength(self, nums, k):

        res = 1
        if min(nums) == 0:
            return res
        
        now = nums[0]
        for v in nums[1:]:
            if now * v <= k:
                now *= v
            else:
                now = v
                res += 1
        
        return res
''',
    call='Solution().minArrayLength([2,3,4,1,5,8], 20)',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'nums.index(v)': 'pink'}, color=_col, h=300, label='nums（同色 = 同一组）'),
        dict(type='text', fn=lambda S: (f"当前组的乘积 `now` = =={S['now']}==，上限 `k` = {S['k']}" if 'now' in S else ''), h=90),
    ],
    watch=[('now', 'now', 'cyan'), ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 1': '数组至少是 1 组，`res` 从 1 开始',
        'if min(nums) == 0': lambda S, B, r: ('有 0：整个数组乘积就是 0 ≤ k，不用分' if min(S.nums) == 0
                                               else '没有 0，用贪心分组'),
        'return res': lambda S, B, r: ('有 0，整个数组只要 1 组' if min(S.nums) == 0 else f'`res` = =={S.res}== 组'),
        'now = nums[0]': '`now` 记当前组的乘积，从 `nums[0] = {now}` 开始',
        'for v in nums': '取下一个数 `v = {v}`',
        'if now * v': lambda S, B, r: (f'`now × v = {S.now} × {S.v} = {S.now * S.v}` ≤ `{S.k}` → ==并入当前组=='
                                        if S.now * S.v <= S.k else f'`now × v = {S.now} × {S.v} = {S.now * S.v}` > `{S.k}` → 放不下，要新开一组'),
        'now *= v': '尽量并进前面的组，后面剩得越短越好：`now` → =={now}==',
        'now = v': '`v = {v}` 另起一组，`now` 重置为 {now}',
        'res += 1': '分出一组，`res` = =={res}==',
    },
    cards=dict(
        one_liner='把数组切成最少的段，每段乘积不超过 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['相邻两数可以替换成它们的乘积（乘积不超过 `k`），求数组最短能变多长',
                 '等价于：划分成最少的子数组，每个子数组乘积 ≤ `k`',
                 '示例：`[2,3,4,1,5,8]`，`k = 20` → `3`（`[2,3]`、`[4,1,5]`、`[8]`）'],
        quote='对于nums[index]，应该尽量将其纳入前面的子数组，以使得后续剩余的子数组尽量短。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组里有 0：整体乘积是 0，答案就是 1',
              '否则从左到右，用 `now` 记当前组乘积',
              '能乘就乘进去，乘不下就把当前数当作新组的开头'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先特判 0：有 0 时任何一段包含 0 乘积都为 0',
                 '`now = v` 的同时 `res += 1`，别忘了新组也算一组',
                 '本题库内没有题面，题意按 yiduobo 文章和题目原意整理'],
    ),
)
