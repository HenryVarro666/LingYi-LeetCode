H = [2, 1, 1, 2, 1, 2, 2]


def _col(S, i, v):
    if 'choose' not in S:
        return None
    return 'green' if i == S['choose'] and S['choose'] != S['k'] else None


CONFIG = dict(
    num=755, title='倒水', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟：先往左找落差，再往右',
    tags=['单调栈'],
    code='''
class Solution(object):
    def pourWater(self, heights, volume, k):

        for _ in range(volume):
            p = k
            choose = k
            while p - 1 >= 0 and heights[p - 1] <= heights[p]:
                if heights[p - 1] < heights[p]:
                    choose = p - 1
                p -= 1

            if choose != k:
                heights[choose] += 1
                continue
            
            p = k
            choose = k
            while p + 1 < len(heights) and heights[p + 1] <= heights[p]:
                if heights[p + 1] < heights[p]:
                    choose = p + 1
                p += 1

            if choose != k:
                heights[choose] += 1
                continue
            
            heights[k] += 1
        
        return heights
''',
    call=f'Solution().pourWater({H}, 4, 3)',
    expect=[2, 2, 2, 3, 2, 2, 2],
    setup='',
    views=[
        dict(type='text', fn=lambda S: ('每滴水：先向左走到最后一个落差，没有再向右，都没有就停在 `k`' if 'p' not in S
             else f"落点 `k = {S['k']}`；当前探到 `p = {S['p']}`，已选落脚点 `choose = {S['choose']}`"), h=60),
        dict(type='bars', var='heights', label='heights（蓝 = 落点 k，粉 = 探索位置 p，绿 = 水最终停的位置）',
             pointers={'k': 'blue', 'p': 'pink'}, h=420, color=_col),
    ],
    watch=[('k', 'k', 'blue'), ('p', 'p', 'pink'), ('choose', 'choose', 'green'), ('_', '_')],
    captions={
        'for _ in range(volume)': '倒第 `{_ + 1}` 滴水，从 `k = {k}` 落下',
        'p = k': '从落点 `k` 出发探索，`p = {p}`',
        'choose = k': '`choose` 记录水最终停的位置，先假设就在 `k`',
        'while p - 1 >= 0 and': lambda S, B, r: (
            f'左边 `heights[{S.p - 1}] = {S.heights[S.p - 1]}` ≤ 当前 `{S.heights[S.p]}`：水还能继续往左流' if S.p - 1 >= 0 and S.heights[S.p - 1] <= S.heights[S.p]
            else '左边出界，或左边更高：水流不动了，结束向左探索'),
        'if heights[p - 1] < heights[p]': lambda S, B, r: (
            f'`{S.heights[S.p - 1]} < {S.heights[S.p]}`：出现==落差==，水可以落到 `{S.p - 1}`（记为 choose）' if S.heights[S.p - 1] < S.heights[S.p]
            else '相等：平台，不是落差，只往前走'),
        'choose = p - 1': '`choose = {choose}`：==只记最后一个落差==，水会流到最低处',
        'p -= 1': '继续往左：`p = {p}`',
        'if choose != k': lambda S, B, r: (f'`choose = {S.choose} ≠ k`：左边有落差 → 水停在左边' if S.choose != S.k
                                          else '`choose == k`：左边没有落差，接着试右边'),
        'heights[choose] += 1': '水落在 `{choose}`：`heights[{choose}]` 变成 `{heights[choose]}`，处理下一滴',
        'continue': '这一滴水已经落定',
        'while p + 1 < len(heights)': lambda S, B, r: (
            f'右边 `heights[{S.p + 1}] = {S.heights[S.p + 1]}` ≤ 当前 `{S.heights[S.p]}`：水还能继续往右流' if S.p + 1 < len(S.heights) and S.heights[S.p + 1] <= S.heights[S.p]
            else '右边出界，或右边更高：结束向右探索'),
        'if heights[p + 1] < heights[p]': lambda S, B, r: (
            f'`{S.heights[S.p + 1]} < {S.heights[S.p]}`：出现==落差==，水可以落到 `{S.p + 1}`' if S.heights[S.p + 1] < S.heights[S.p]
            else '相等：平台，不是落差，只往前走'),
        'choose = p + 1': '`choose = {choose}`：记下最后一个落差',
        'p += 1': '继续往右：`p = {p}`',
        'heights[k] += 1': '左右都没有落差：水停在 `k = {k}`，`heights[{k}]` = `{heights[k]}`',
        'return heights': '所有水倒完：`{heights}`',
    },
    cards=dict(
        one_liner='每滴水先往左找最后一个落差，找不到再往右',
        complexity='时间 `O(volume × n)`，空间 `O(1)`',
        problem=['`heights[i]` 是第 `i` 格地形高度，在位置 `k` 倒下 `volume` 滴水，每滴一格',
                 '水先尽量往左落到更低处，不行再往右，都不行就停在 `k`',
                 '示例：`[2,1,1,2,1,2,2]`，`volume = 4`，`k = 3` → `[2,2,2,3,2,2,2]`'],
        quote='首先从k开始向左遍历，到首个非单调不增的位置停止，在遍历过程中记录最后一次落差出现的位置。若存在这个落差出现的位置，那么水最终就会留在这个落差的下方。',
        quote_src='—— yiduobo 题解原文',
        idea=['`volume ≤ 2000`、长度 ≤ 100：直接暴力模拟每一滴水',
              '向左走：高度不增就继续，遇到更矮的格子就记下 `choose`（最后一个落差）',
              '左边没有落差再向右同样走一遍；都没有就加在 `k` 上'],
        summary=['时间 `O(volume × n)`，空间 `O(1)`，原地修改 `heights`',
                 '==只记最后一次落差==：同高平台上水停在离 `k` 最近的最低处',
                 '平台（相等）继续走，更高的格子就挡住了',
                 '原文题面缺失，题意按力扣 755 题与 yiduobo 文章说明演示',
                 '作者提到单调性 + 数据结构可以更快，但细节繁琐，暴力已足够'],
    ),
)
