def _range_txt(S):
    if 'low' in S and 'rem' in S:
        return f"猜 `low = {S['low']}`：每个游戏得分都 ≥ low，最多用 `m = {S['m']}` 步，剩余 `rem = {S['rem']}`"
    if 'mid' in S:
        return f"二分（开区间）：`left = {S['left']}` 可行，`right = {S['right']}` 不可行，试 `mid = {S['mid']}`"
    if 'left' in S:
        return f"二分（开区间）：`left = {S['left']}` 可行，`right = {S['right']}` 不可行"
    return '二分答案：最小得分 ≥ low 所需步数随 low 单调增加'


def _need_txt(S):
    if 'low' not in S or 'p' not in S:
        return ''
    k = S.get('k')
    if k is None:
        return ''
    return (f"第 `{S['i']}` 个数 `p = {S['p']}`：要踩 `ceil({S['low']}/{S['p']}) = {(S['low'] - 1) // S['p'] + 1}` 次，"
            f"左边已顺带 `pre = {S['pre']}` 次 → 还要 `k = {k}` 次，左右横跳 `2k-1 = {2 * k - 1}` 步")


CONFIG = dict(
    num=3449, title='最大化游戏分数的最小值', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 左右横跳贪心',
    tags=['二分算法', '贪心与思维', '难度分 2748'],
    code='''
class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        def check(low: int) -> bool:
            n = len(points)
            rem = m
            pre = 0
            for i, p in enumerate(points):
                k = (low - 1) // p + 1 - pre  # 还需要操作的次数
                if i == n - 1 and k <= 0:  # 最后一个数已经满足要求
                    break
                if k < 1:
                    k = 1  # 至少要走 1 步
                rem -= k * 2 - 1  # 左右横跳
                if rem < 0:
                    return False
                pre = k - 1  # 右边那个数顺带操作了 k-1 次
            return True

        left = 0
        right = (m + 1) // 2 * min(points) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().maxScore([1,2,3], 5)',
    expect=2,
    max_steps=70,
    views=[
        dict(type='text', fn=_range_txt, size=24, h=60),
        dict(type='array', var='points', label='points（蓝框 = 正在处理的游戏）', h=220, pointers={'i': 'blue'},
             color=lambda S, i, v: ('yellow' if S.get('i') == i and 'rem' in S else None),
             dim=lambda S, i, v: 'i' in S and 'rem' in S and i < S['i']),
        dict(type='text', fn=_need_txt, size=24, h=100),
    ],
    watch=['low', 'i', 'p', 'pre', 'k', 'rem', 'm', 'left', 'right', 'mid'],
    captions={
        'n = len(points)': '`n = {n}`',
        'rem = m': '剩余步数 `rem = m = {rem}`',
        'pre = 0': '`pre`：左边那次横跳顺带给当前数加了几次分，开始是 0',
        'k = (low - 1)': '要得分 ≥ `{low}` 需踩 `ceil({low}/{p})` 次，扣掉顺带的 `{pre}` 次 → 还需 `k = {k}` 次',
        'if i == n - 1 and k <= 0': lambda S, B, r: ('最后一个数已经够了，不用再走 → break' if (S.i == S.n - 1 and S.k <= 0) else f'`k = {S.k}`，不是「最后一个且已满足」，继续'),
        'if k < 1': lambda S, B, r: ('`k < 1`：已经够了，但还得走过去' if S.k < 1 else f'`k = {S.k} ≥ 1`'),
        'k = 1': '至少走 1 步到下一格，`k = 1`',
        'rem -= k * 2 - 1': lambda S, B, r: (f'最后一个数：再踩 `{S.k}` 次，花 `2×{S.k}-1 = {S.k * 2 - 1}` 步，`rem = {S.rem}`' if S.i == S.n - 1 else f'在 `{S.i}` 和 `{S.i + 1}` 间左右横跳：花 `2×{S.k}-1 = {S.k * 2 - 1}` 步，`rem = {S.rem}`'),
        'if rem < 0': lambda S, B, r: (f'`rem = {S.rem} < 0`：步数不够 → ==low 不可行==' if S.rem < 0 else f'`rem = {S.rem} ≥ 0`，还够'),
        'return False': '这个 `low` 做不到 → False',
        'pre = k - 1': '右边那个数顺带踩了 `k-1 = {pre}` 次，留给下一个数用',
        'return True': '走完所有数，步数没超 → `low` 可行',
        'left = 0': '`left = 0`：什么都不做，最小得分也是 0 ≥ 0，必可行',
        'right = (m + 1)': '`right = ceil(m/2) × min(points) + 1 = {right}`：连最小值都横跳不到的上界，必不可行',
        'while left + 1 < right': lambda S, B, r: (f'`({S.left}, {S.right})` 里还有候选' if S.left + 1 < S.right else f'`left + 1 = right`，答案 `{S.left}`'),
        'mid = (left': '猜 `mid = {mid}`',
        'if check(mid)': '调用 `check({mid})`：每个得分都 ≥ {mid} 吗？',
        'left = mid': '`{mid}` 可行 → `left = {left}`',
        'right = mid': '`{mid}` 不可行 → `right = {right}`',
        'return left': '最大可行的最小得分 = `{left}`',
    },
    cards=dict(
        one_liner='二分猜最小分，把来回移动拆成一对一对的左右横跳',
        complexity='时间 `O(n log(m·min))`，空间 `O(1)`',
        problem=['从下标 -1 出发，每步 ±1，把落脚处的 `points[i]` 加到得分上',
                 '至多 `m` 步，让 `gameScore` 的==最小值最大==',
                 '本视频：`points=[1,2,3], m=5` → `2`'],
        quote='我们可以把任何一种或长或短的、来来回回的移动方式，转换成若干组「左右横跳」，也就是先在 0 和 1 之间左右横跳，然后在 1 和 2 之间左右横跳……',
        quote_src='—— 灵茶山艾府题解',
        idea=['得分下界 `low` 越大，需要的步数越多 → ==二分答案==',
              '第 i 个数要踩 `k` 次：在 i 和 i+1 之间横跳，花 `2k-1` 步',
              '横跳时 i+1 顺带被踩 `k-1` 次，下一个数少踩这么多'],
        summary=['时间 `O(n log(m·min))`，空间 `O(1)`',
                 '上取整用 `(low - 1) // p + 1`',
                 '易错：最后一个数若已满足就 break；其余即使满足也至少走 1 步 (`k = 1`)',
                 '库函数写法用 `bisect_left`，check 取反，思路一样',
                 '同类：最大化最小值 + 贪心判定'],
    ),
)
