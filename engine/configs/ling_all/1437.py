CONFIG = dict(
    num=1437, title='是否所有 1 都至少相隔 k 个元素', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='记录上一个 1 的位置', tags=[],
    code='''
class Solution:
    def kLengthApart(self, nums: List[int], k: int) -> bool:
        last1 = -inf
        for i, x in enumerate(nums):
            if x != 1:
                continue
            if i - last1 <= k:
                return False
            last1 = i
        return True
''',
    call='Solution().kLengthApart([1,0,0,1,0,0,0,1,0,1], 2)',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: (f"当前 1 在 `{S['i']}`，上一个 1 在 `{S['last1']}`：间距 `{S['i']} − {S['last1']}` = =={S['i']-S['last1']}==，要求 `> {S['k']}`" if 'i' in S and S.get('x') == 1 and S['last1'] != float('-inf') else (f"首个 1 没有前驱，`last1 = −inf`" if 'i' in S and S.get('x') == 1 else '')), size=30),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260,
             color=lambda S, i, v: ('pink' if i == S.get('last1') else 'blue' if i == S.get('i') else None) if 'i' in S else None),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('last1', 'last1', 'pink'), 'k'],
    captions={
        'last1 = -inf': '`last1` 记录上一个 1 的下标；==初始 −inf==，这样第一个 1 一定通过检查',
        'if x != 1': lambda S, B, r: (f'`nums[{S.i}] = 0`，不是 1，跳过' if S.x != 1 else f'`nums[{S.i}] = 1`，是 1，要检查它和上一个 1 的距离'),
        'continue': '0 不影响答案，看下一个',
        'if i - last1 <= k': lambda S, B, r: (f'`{S.i} − {S.last1} = {S.i - S.last1} ≤ {S.k}`：中间不足 `k` 个元素 → ==不满足==' if S.i - S.last1 <= S.k else ('`last1 = −inf`：第一个 1 前面没有 1，一定满足' if S.last1 == float('-inf') else f'`{S.i} − {S.last1} = {S.i - S.last1} > {S.k}`：间隔够了')),
        'return False': '只要有一对相邻的 1 太近，就直接返回 `False`',
        'last1 = i': '更新 `last1 = {i}`，之后的 1 只需和它比较',
        'return True': '所有相邻的 1 都够远 → `True`',
    },
    cards=dict(
        one_liner='只需检查相邻的 1：它们够远，所有 1 就都够远',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给 0/1 数组 `nums` 和整数 `k`，问任意两个 1 之间是否至少隔 `k` 个元素',
                 '本视频：`[1,0,0,1,0,0,0,1,0,1]`，`k = 2`',
                 '最后两个 1 之间只隔了 1 个 0 → `False`'],
        quote='如果所有相邻的 1 都至少相隔 k 个元素，那么所有 1 都至少相隔 k 个元素。所以只需检查相邻的 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['维护上一个 1 的位置 `last1`',
              '中间元素个数是 `i − last1 − 1`，小于 `k` 即 `i − last1 <= k`',
              '初始化 `last1 = -inf`，兼容第一个 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '间隔元素数 = `i − last1 − 1`，别忘了减 1',
                 '`k = 0` 时任意 1 的位置都合法（`i − last1 >= 1`）',
                 '灵神用 `-inf` 做哨兵，省去对第一个 1 的特判'],
    ),
)
