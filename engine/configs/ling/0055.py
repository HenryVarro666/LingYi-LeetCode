def _draw_intervals(cv, S, B, box, T):
    """把 nums[k] 画成闭区间 [k, k+nums[k]]，绿色竖线是 mx"""
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        return
    n = len(nums)
    hi = max(k + v for k, v in enumerate(nums))
    cv.text((x0 + 18, y0 + 4), '另一种理解：区间 [i, i+nums[i]] 能否合并成一整段', 24, T['muted'], bold=True)
    L, R = x0 + 110, x1 - 40
    axis_y = y1 - 34

    def X(v):
        return L + v * (R - L) / hi

    cv.line([(L, axis_y), (R, axis_y)], T['border'], 2)
    for v in range(hi + 1):
        cv.text((X(v), axis_y + 4), v, 16, T['dim'], anchor='mt', mono=True)
    cv.dashed((X(n - 1), y0 + 40), (X(n - 1), axis_y), T['purple'], 2)
    cv.text((X(n - 1) + 8, y0 + 42), '终点 n-1', 18, T['purple'], anchor='lt')
    upto = S.get('i', -1)
    mx = S.get('mx')
    rowh = (axis_y - (y0 + 46)) / n
    for k, v in enumerate(nums):
        y = y0 + 46 + k * rowh + rowh / 2
        a, b = k, k + v
        if k > upto:
            c = T['panel2']
        elif mx is not None and k > (B.get('mx', 0) if k == upto else mx):
            c = T['red']
        elif k == upto:
            c = T['yellow']
        else:
            c = T['blue']
        cv.text((x0 + 22, y), f'i={k}', 18, T['muted'] if k <= upto else T['dim'], anchor='lm', mono=True)
        cv.rect((X(a) - 7, y - 8, max(X(b), X(a)) + 7, y + 8), fill=c, r=8)
    if mx is not None:
        cv.line([(X(mx), y0 + 44), (X(mx), axis_y)], T['green'], 3)
        cv.text((X(mx) + 6, axis_y - 6), f'mx={mx}', 18, T['green'], anchor='lb', bold=True)


CONFIG = dict(
    num=55, title='跳跃游戏', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='维护最右可达位置 mx',
    code='''
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        mx = 0
        for i, jump in enumerate(nums):
            if i > mx:  # 无法到达 i
                return False
            mx = max(mx, i + jump)  # 从 i 最右可以跳到 i+jump
        return True
''',
    call='Solution().canJump([3, 2, 1, 0, 4])',
    expect=False,
    views=[
        dict(type='array', var='nums', cell=110, h=200, pointers={'i': 'yellow'},
             window=('0', 'min(mx, len(nums) - 1)'),
             color=lambda S, k, v: 'red' if ('i' in S and k == S['i'] and S['i'] > S['mx']) else None),
        dict(type='text', h=50, size=26, text='青框 = 能到达的位置 `[0, mx]`'),
        dict(type='custom', h=360, draw=_draw_intervals),
    ],
    watch=[('i', 'i', 'yellow'), 'jump', ('mx', 'mx', 'green')],
    captions={
        'mx = 0': '`mx` 是目前==最右能到达的位置==，一开始站在 0',
        'for i, jump in enumerate': '来到 `i = {i}`，从这里最多能跳 `jump = {jump}` 步',
        'if i > mx': lambda S, B, ret: (f'`i = {S["i"]} > mx = {S["mx"]}`：前面所有位置最远只到 {S["mx"]}，==跳不到 {S["i"]}==' if S['i'] > S['mx']
                                        else f'`i = {S["i"]} ≤ mx = {S["mx"]}`：位置 {S["i"]} 能到达'),
        'mx = max(mx, i + jump)': lambda S, B, ret: (f'从 {S["i"]} 最右可以跳到 `{S["i"]} + {S["jump"]} = {S["i"] + S["jump"]}`，`mx = max({B["mx"]}, {S["i"] + S["jump"]}) = {S["mx"]}`'
                                                     + ('　==更远了==' if S['mx'] > B['mx'] else '　没有更远')),
        'return False': '返回 `False`：==区间在 3 和 4 之间断开了==，合并不成一整段',
        'return True': '一路都没断，返回 `True`',
    },
    max_steps=60,
    cards=dict(
        one_liner='边走边维护最右能到的位置 mx，走到 mx 外面就失败',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['站在下标 0，`nums[i]` 是从 `i` 出发==最多==能跳的步数',
                 '从 `i` 可以跳到闭区间 `[i, i + nums[i]]` 中的任意位置，问能否到达 `n-1`',
                 '示例：`[2,3,1,1,4]` → `true`；`[3,2,1,0,4]` → `false`'],
        quote='从左到右遍历 nums，同时维护能跳到的最远位置 mx。如果 i > mx，说明无法跳到 i，返回 false。否则，用 i+nums[i] 更新 mx 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`[3,2,1,0,4]`：从 0 能到 1、2、3，但 1、2、3 都跳不过 3',
              '遍历到 `i = 4` 时 `i > mx = 3` → 4 无法到达',
              '另一种理解：区间 `[i, i+nums[i]]` 能否==合并成一个大区间==（56. 合并区间）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判断 `i > mx`，再更新 `mx`：到不了的位置不能拿来“起跳”',
                 '优化：`mx >= n - 1` 时可以提前返回 `True`',
                 '45. 跳跃游戏 II 是它的升级版：问最少跳几次'],
    ),
)
