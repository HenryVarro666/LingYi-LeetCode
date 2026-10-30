CONFIG = dict(
    num=3355, title='零数组变换 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 区间减一次数',
    tags=['灵神题单·常用数据结构', '难度分 1591'],
    code='''
class Solution:
    def isZeroArray(self, nums: List[int], queries: List[List[int]]) -> bool:
        diff = [0] * (len(nums) + 1)
        for l, r in queries:
            diff[l] += 1
            diff[r + 1] -= 1

        for x, sum_d in zip(nums, accumulate(diff)):
            # 此时 sum_d 表示 x=nums[i] 要减掉多少
            if x > sum_d:  # x 无法变成 0
                return False
        return True
''',
    call='Solution().isZeroArray([2,1,2,1,2], [[0,2],[0,2],[2,4]])',
    expect=False,
    views=[
        dict(type='array', var='nums', h=160, label='nums'),
        dict(type='array', var='diff', h=160, label='diff（差分数组）'),
        dict(type='text', fn=lambda S: (f"查询 `[{S['l']}, {S['r']}]`：`diff[{S['l']}] += 1`，`diff[{S['r']+1}] −= 1`" if 'l' in S and 'sum_d' not in S else (f"`x = {S['x']}`，最多能减 `sum_d = {S['sum_d']}` 次" if 'sum_d' in S else ''))),
    ],
    watch=['l', 'r', ('x', 'x', 'blue'), ('sum_d', 'sum_d', 'orange')],
    captions={
        'diff = [0]': '差分数组，长度多开一位，这样 `r + 1` 不会越界',
        'diff[l] += 1': '区间 `[{l}, {r}]` 整体减一：从 `{l}` 开始多一次 → `diff[{l}] = {diff[l]}`',
        'diff[r + 1] -= 1': '到 `{r+1}` 结束这次减一 → `diff[{r+1}] = {diff[r+1]}`',
        'for x, sum_d': '`accumulate(diff)` 的前缀和，就是每个位置被减一的次数 `sum_d`',
        'if x > sum_d': lambda S, B, r: f'`x = {S.x}`，最多被减 `{S.sum_d}` 次：' + (f'`{S.x} > {S.sum_d}`，减完还大于 0，变不成 0' if S.x > S.sum_d else f'`{S.x} <= {S.sum_d}`，够减（多的可以不选）'),
        'return False': '这一位凑不够 → 直接 ==返回 False==',
        'return True': '每个位置都够减 → `True`',
    },
    cards=dict(
        one_liner='先问「最多能减几次」，多出来的次数可以不选',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['每个查询 `[l, r]` 可以在区间内任选一些下标各减 1',
                 '能否按顺序处理完所有查询后让 `nums` 全为 0',
                 '示例：`[2,1,2,1,2]`，查询 `[[0,2],[0,2],[2,4]]` → `False`'],
        quote='如果所有元素都 ≤ 0，那么我们可以撤销一部分元素的减一，使其调整为 0，从而满足原始题意的要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把「选子集」改成「区间全减一」，只要最终都 `≤ 0` 就行',
              '差分数组 `diff` 做区间加一，前缀和 `sum_d` = 该位置被覆盖的次数',
              '`x > sum_d` 说明覆盖次数不够，直接返回 `False`'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`diff` 要开 `n + 1`，因为有 `diff[r + 1]`',
                 '只比较「次数够不够」，不用管具体选哪些下标',
                 '同类题：差分数组 §2.1 一维差分'],
    ),
)
