def _sim(nums):
    """按灵神的算法离线算出每座桥 (左端点=实际起跳位置, 右端点)，只用于画图"""
    out, cur, nxt, src = [], 0, 0, 0
    for k in range(len(nums) - 1):
        if k + nums[k] > nxt:
            nxt, src = k + nums[k], k
        if k == cur:
            out.append((src, nxt))
            cur = nxt
    return out


def _src(S):
    """目前收集到的、能跳最远的位置"""
    i, nums = S['i'], S['nums']
    best = max(range(i + 1), key=lambda k: (k + nums[k], -k))
    return best


def _draw_bridges(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        return
    n = len(nums)
    cell = min(104, (x1 - x0 - 60) / n)
    sx = x0 + (x1 - x0 - cell * n) / 2
    top = y1 - 150
    cv.text((x0 + 18, y0 + 4), 'nums（弧线 = 已造好的桥，黄色虚弧 = 正在收集的下一座桥）', 24, T['muted'], bold=True)

    def cx(k):
        return sx + k * cell + cell / 2

    cur = S.get('cur_end', 0)
    built = [b for b in _sim(nums) if cur > 0 and b[1] <= cur]
    for idx, (a, b) in enumerate(built):
        mid = cv.arc_arrow((cx(a), top - 4), (cx(b), top - 4), 60 + (b - a) * 50, T['green'], 4, 14)
        cv.text((mid[0], mid[1] - 8), f'桥 {idx + 1}', 20, T['green'], anchor='mb', bold=True)
    if 'i' in S and S.get('next_end', 0) > cur:
        a, b = _src(S), S['next_end']
        pts = []
        lift = 60 + (b - a) * 50
        mx_, my_ = (cx(a) + cx(b)) / 2, top - 4 - lift
        for t in range(41):
            u = t / 40
            pts.append(((1 - u) ** 2 * cx(a) + 2 * (1 - u) * u * mx_ + u * u * cx(b),
                        (1 - u) ** 2 * (top - 4) + 2 * (1 - u) * u * my_ + u * u * (top - 4)))
        for t in range(0, 40, 2):
            cv.line([pts[t], pts[t + 1]], T['yellow'], 3)
    for k, v in enumerate(nums):
        X = sx + k * cell
        reach = cur > 0 and k <= cur
        cv.rect((X + 4, top, X + cell - 4, top + cell - 8), fill=T['panel2'], r=10,
                outline=T['cyan'] if reach else T['border'], width=3 if reach else 1)
        cv.text((X + cell / 2, top + (cell - 8) / 2), v, 34, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + cell - 2), k, 18, T['dim'], anchor='mt', mono=True)
    if 'i' in S:
        X = cx(S['i'])
        cv.tri_up(X, top + cell + 22, 10, T['yellow'])
        cv.text((X, top + cell + 38), 'i', 22, T['yellow'], anchor='mt', bold=True)
    cv.text((cx(n - 1), top + cell + 18), '终点', 20, T['purple'], anchor='mt', bold=True)


CONFIG = dict(
    num=45, title='跳跃游戏 II', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='区间贪心 · 走到桥尽头才造桥',
    code='''
class Solution:
    def jump(self, nums: List[int]) -> int:
        ans = 0
        cur_end = 0  # 已建造的桥的右端点
        next_end = 0  # 下一座桥的右端点的最大值
        for i in range(len(nums) - 1):
            # 遍历的过程中，记录下一座桥的最远点
            next_end = max(next_end, i + nums[i])
            if i == cur_end:  # 无路可走，必须建桥
                cur_end = next_end  # 建桥后，最远可以到达 next_end
                ans += 1
        return ans
''',
    call='Solution().jump([2, 3, 1, 4, 1, 1, 1, 1])',
    expect=3,
    views=[
        dict(type='text', h=56, size=27,
             fn=lambda S: (f'已造的桥最远到 `cur_end = {S["cur_end"]}`　　下一座桥最远可到 `next_end = {S["next_end"]}`'
                           if 'next_end' in S else '`nums[i]`：从 `i` 最多能往右跳几格')),
        dict(type='custom', h=520, draw=_draw_bridges),
    ],
    watch=[('i', 'i', 'yellow'), ('cur_end', 'cur_end', 'cyan'), ('next_end', 'next_end', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans`：造了几座桥，也就是跳了几次',
        'cur_end = 0': '`cur_end`：==已建造的桥的右端点==，一开始只能待在 0',
        'next_end = 0': '`next_end`：==下一座桥的右端点的最大值==，边走边收集',
        'for i in range(len(nums) - 1)': lambda S, B, ret: (
            '遍历结束' if B.get('i') == S['i']
            else (f'走到 `i = {S["i"]}`（只遍历到 `n-2`：`n-1` 是终点，不需要再造桥）' if S['i'] == 0 else f'走到 `i = {S["i"]}`')),
        'next_end = max(next_end, i + nums[i])': lambda S, B, ret: (
            f'默默收集信息：从 {S["i"]} 最远到 `{S["i"]} + {S["nums"][S["i"]]} = {S["i"] + S["nums"][S["i"]]}`，`next_end = {S["next_end"]}`'
            + ('　==更远了==' if S['next_end'] > B['next_end'] else '')),
        'if i == cur_end': lambda S, B, ret: (
            f'`i == cur_end == {S["i"]}`：==走到桥的尽头，无路可走==，必须造新桥' if S['i'] == S['cur_end']
            else f'`i = {S["i"]} < cur_end = {S["cur_end"]}`：还在桥上，继续收集'),
        'cur_end = next_end': lambda S, B, ret: (
            f'==回到能跳最远的位置 {_src(S)} 造桥==（不是在 {S["i"]} 造）：新桥右端点 `cur_end = {S["cur_end"]}`'
            if _src(S) != S['i'] else f'在能跳最远的位置 {_src(S)} 造桥：`cur_end = {S["cur_end"]}`'),
        'ans += 1': '桥的数量 `ans = {ans}`',
        'return ans': '最少跳 `{ret}` 次',
    },
    max_steps=60,
    cards=dict(
        one_liner='在无路可走之前只收集信息；走到桥尽头，再从最远点造下一座桥',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从下标 0 出发，`nums[i]` 是从 `i` ==最多==能往右跳的长度',
                 '求到达 `n-1` 的==最少跳跃次数==（保证能到）',
                 '例：`[2,3,1,4,1,1,1,1]` → `3`（0 → 1 → 3 → 7）'],
        quote='不是在无路可走的那个位置造桥，而是当发现无路可走的时候，回到能跳到最远点的那个位置造桥。在无路可走之前，我们只是在默默地收集信息。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cur_end`：已造好的桥能到的最远点；`next_end`：途中看到的最远点',
              '走到 `i == cur_end` → 无路可走 → 造桥，`ans += 1`',
              '本质是递推：由“跳 k 次最远到哪”算出“跳 k+1 次最远到哪”'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只遍历到 `n-2`：`nums[n-1]` 没有意义，到终点不用再造桥',
                 '桥的左端点（实际起跳点）可能在当前这座桥的中间，比如本例的 1 和 3',
                 '若不保证能到终点：见 1326. 灌溉花园的最少水龙头数目'],
    ),
)
