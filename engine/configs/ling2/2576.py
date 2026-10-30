NUMS = [9, 5, 12, 3, 8, 4, 7, 6]
SORTED = sorted(NUMS)
N = len(NUMS)
START = (N + 1) // 2


def _j(S):
    """当前 x 在排序后数组中的下标（右半部分）"""
    x = S.get('x')
    if x is None or S.get('_line', 0) < 5:
        return None
    for k in range(START, N):
        if SORTED[k] == x:
            return k
    return None


def _pairs(S, B):
    """模拟到当前为止的匹配：[(左下标, 右下标)]"""
    j = _j(S)
    if j is None:
        return []
    out, i = [], 0
    just = S.get('_line') == 5 and S.get('x') != B.get('x')
    for k in range(START, j + 1):
        if k == j and just:  # 刚取出 x，还没判断
            break
        if SORTED[i] * 2 <= SORTED[k]:
            out.append((i, k))
            i += 1
    return out


def draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '排序后的 nums：左半找小数，右半找大数（绿线 = 已匹配）', 24, T['muted'], bold=True)
    nums = S.get('nums')
    if nums is None:
        return
    sorted_now = nums == SORTED
    cell = min(100, (x1 - x0 - 60) / N)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * N) / 2
    cy = y0 + 230
    ch = cell * 0.8
    pairs = _pairs(S, B) if sorted_now else []
    j = _j(S)
    i = S.get('i')
    done_l = {a for a, _ in pairs}
    done_r = {b for _, b in pairs}
    for a, b in pairs:
        X1, X2 = sx + a * cell + cell / 2, sx + b * cell + cell / 2
        cv.arc_arrow((X1, cy - 4), (X2, cy - 4), 40 + (b - a) * 12, T['green'], 4, 12, frac=0.98)
    if sorted_now and j is not None and i is not None and S.get('_line') in (6, 7) and (i, j) not in pairs:
        X1, X2 = sx + i * cell + cell / 2, sx + j * cell + cell / 2
        cv.arc_arrow((X1, cy - 4), (X2, cy - 4), 40 + (j - i) * 12, T['red'], 3, 12, frac=0.98)
    if sorted_now:
        Xm = sx + START * cell - 2
        cv.dashed((Xm, cy - 30), (Xm, cy + ch + 40), T['dim'], 2, 8, 6)
    for k, v in enumerate(nums):
        X = sx + k * cell
        fill = T['panel2']
        skipped = sorted_now and j is not None and START <= k < j and k not in done_r
        if k in done_l or k in done_r:
            fill = T['green']
        elif skipped:
            fill = (40, 45, 53)
        elif sorted_now and k == j:
            fill = T['orange']
        elif sorted_now and k == i and S.get('_line', 0) >= 5:
            fill = T['blue']
        cv.rect((X + 4, cy, X + cell - 4, cy + ch), fill=fill, r=8, outline=T['border'])
        tc = T['dim'] if skipped else (T['bg'] if fill != T['panel2'] else T['text'])
        cv.text((X + cell / 2, cy + ch / 2), str(v), 30, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, cy + ch + 6), str(k), 18, T['dim'], anchor='mt', mono=True)
    if sorted_now and i is not None:
        X = sx + i * cell + cell / 2
        cv.tri_up(X, cy + ch + 34, 10, T['blue'])
        cv.text((X, cy + ch + 50), 'i', 22, T['blue'], anchor='mt', bold=True)
    if sorted_now and j is not None:
        X = sx + j * cell + cell / 2
        cv.tri_up(X, cy + ch + 34, 10, T['orange'])
        cv.text((X, cy + ch + 50), 'x', 22, T['orange'], anchor='mt', bold=True)


CONFIG = dict(
    num=2576, title='求出最多标记下标', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 同向双指针（左半配右半）',
    tags=['字节30天'],
    code='''
class Solution:
    def maxNumOfMarkedIndices(self, nums: List[int]) -> int:
        nums.sort()
        i = 0
        for x in nums[(len(nums) + 1) // 2:]:
            if nums[i] * 2 <= x:  # 找到一个匹配
                i += 1
        return i * 2
''',
    call=f'Solution().maxNumOfMarkedIndices({NUMS})',
    expect=6,
    views=[
        dict(type='custom', draw=draw, h=420),
        dict(type='text', fn=lambda S: ('配对规则：`2 * nums[i] <= nums[j]`；暗 = 配不上被跳过的大数'
                                        if S.get('_line', 0) < 6 else
                                        f"判断 `nums[{S['i']}] * 2 = {S['nums'][S['i']] * 2}` ≤ `x = {S['x']}` ?"), size=26),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange')],
    captions={
        'nums.sort()': '先排序：`{nums}`，小数在左、大数在右',
        'i = 0': '`i`：左半部分中==下一个待匹配的小数==',
        'for x in nums': lambda S, B, ret: (f'枚举右半部分的 `x = {S.x}`（从下标 `(n + 1) // 2 = {START}` 开始）'
                                            if S.get('x') is not None and S.x != B.get('x') and B.get('x') is None else
                                            f'枚举右半部分的下一个 `x = {S.x}`' if S.get('x') is not None and S.x != B.get('x')
                                            else '右半部分枚举完了'),
        'if nums[i] * 2 <= x': lambda S, B, ret: (f'`{S.nums[S.i]} × 2 = {S.nums[S.i] * 2} ≤ {S.x}` → ==找到一个匹配=='
                                                  if S.nums[S.i] * 2 <= S.x else
                                                  f'`{S.nums[S.i]} × 2 = {S.nums[S.i] * 2} > {S.x}`：`{S.x}` 太小配不上 → 跳过它，`i` 不动'),
        'i += 1': lambda S, B, ret: (f'`nums[{B.i}] = {S.nums[B.i]}` 和 `{S.x}` 配对：`i` 右移到 `{S.i}`'
                                     + ('；下一个小数只能配==更右边==的数' if B.i == 0 else '')),
        'return i * 2': '匹配了 `{i}` 对，共标记 `{i} × 2 = {ret}` 个下标',
    },
    cards=dict(
        one_liner='排序后左半的小数依次去匹配右半的大数，能配就配',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈开销）',
        problem=['每次选两个==未标记==的下标 `i`、`j`，满足 `2 * nums[i] <= nums[j]`，标记它们',
                 '求最多可以标记多少个下标',
                 '示例：`[9,2,5,4]` → `4`；本视频 `[9,5,12,3,8,4,7,6]` → `6`'],
        quote='我们需要用 nums ==左半部分中的数，去匹配 nums 右半部分中的数==。在 nums 的右半部分中，找到第一个满足 `2·nums[0] ≤ nums[j]` 的 j，那么 nums[1] 只能匹配右半部分中的下标大于 j 的数。',
        quote_src='—— 灵茶山艾府题解（方法二：同向双指针）',
        idea=['若能配 k 对，一定可以让==最小的 k 个数==配==最大的 k 个数==',
              '所以小数只在左半找，大数只在右半找',
              '`i` 指向左半下一个小数，`x` 枚举右半：能配就 `i += 1`，配不上就扔掉 x'],
        result='运行结束：配成 3 对（3-7、4-8、5-12），返回 `6` ✓',
        summary=['时间 `O(n log n)`（排序），双指针部分 `O(n)`',
                 '右半从 `(n + 1) // 2` 开始：奇数长度时中间的数归左半',
                 '为什么小数配“第一个够大的”：更大的留给后面更大的小数',
                 '方法一：二分答案 k，检查 `nums[i] * 2 <= nums[n-k+i]` 是否对所有 `i < k` 成立'],
    ),
)
