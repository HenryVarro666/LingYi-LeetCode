def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    lo, hi = min(s), max(s)
    N = hi - lo + 1
    n = len(s)
    cell = min(90, (x1 - x0 - 40) / N)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * N) / 2
    ys, ch = y0 + 100, 90
    cv.text((x0 + 18, y0 + 4), '数轴（蓝 = 石子，空格 = 空位；粉框 = 长为 n 的窗口）', 22, T['muted'], bold=True)
    pos = set(s)
    for p in range(lo, hi + 1):
        X = sx + (p - lo) * cell
        if p in pos:
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), fill=T['blue'], r=8)
            cv.text((X + cell / 2, ys + ch / 2), p, 28, T['bg'], anchor='mm', bold=True)
        else:
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), outline=T['border'], r=8)
            cv.text((X + cell / 2, ys + ch + 8), p, 18, T['dim'], anchor='mt', mono=True)
    if 'sr' in S and 'left' in S and 'max_cnt' in S:
        a, b = S['sr'] - n + 1, S['sr']
        a2 = max(a, lo)
        cv.rect((sx + (a2 - lo) * cell - 3, ys - 8, sx + (b - lo + 1) * cell + 3, ys + ch + 8), outline=T['pink'], width=5, r=10)
        cv.text((sx + (a2 - lo) * cell, ys - 14), f'窗口 [{a}, {b}]（长 {n}）', 22, T['pink'], anchor='lb', bold=True)
        cnt = S['right'] - S['left'] + 1
        cv.text((x0 + 20, ys + ch + 70), f'窗口内石子 {cnt} 个 → 其余 {n - cnt} 个要搬进来', 26, T['text'], bold=True)
    elif 'e1' in S:
        cv.text((x0 + 20, ys + ch + 70), f"空位：e1 = {S['e1']}（不动最右），e2 = {S['e2']}（不动最左）", 26, T['text'], bold=True)


def _txt(S, B):
    if 'max_cnt' in S and 'right' in S:
        return f"窗口内最多石子 `max_cnt = {S['max_cnt']}` → 最小移动 `n - max_cnt = {S['n'] - S['max_cnt']}`"
    if 'max_move' in S:
        return f"最大移动次数 `max_move = {S['max_move']}`（最多空位数）"
    return '先算最大，再用滑动窗口算最小'


CONFIG = dict(
    num=1040, title='移动石子直到连续 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分类讨论 · 定长窗口找最多石子',
    tags=['贪心与思维', '难度分 2456'],
    code='''
class Solution:
    def numMovesStonesII(self, s: List[int]) -> List[int]:
        s.sort()
        n = len(s)
        e1 = s[-2] - s[0] - n + 2
        e2 = s[-1] - s[1] - n + 2  # 计算空位
        max_move = max(e1, e2)
        if e1 == 0 or e2 == 0:  # 特殊情况：没有空位
            return [min(2, max_move), max_move]
        max_cnt = left = 0
        for right, sr in enumerate(s):  # 滑动窗口：枚举右端点所在石子
            while sr - s[left] + 1 > n:  # 窗口长度大于 n
                left += 1  # 缩小窗口长度
            max_cnt = max(max_cnt, right - left + 1)  # 维护窗口内的最大石子数
        return [n - max_cnt, max_move]
''',
    call='Solution().numMovesStonesII([7,4,9,1,2])',
    expect=[2, 4],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='s', label='s（排序后）', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), cell=84, h=190),
        dict(type='text', h=70, size=28, fn=_txt),
    ],
    watch=[('n', 'n', 'cyan'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('max_cnt', 'max_cnt', 'green'), ('max_move', 'max_move', 'orange')],
    captions={
        's.sort()': '先排序，石子从左到右排好',
        'e1 = ': '不动最右石子时的空位：`s[-2] - s[0] - n + 2` = {e1}',
        'e2 = ': '不动最左石子时的空位：`s[-1] - s[1] - n + 2` = {e2}',
        'max_move = max': '最大移动次数：把端点石子移到次远处，一格一格浪费最少 → `max(e1, e2) = {max_move}`',
        'if e1 == 0 or e2 == 0': '`e1 = {e1}`，`e2 = {e2}`：{"有一个为 0，是特殊情况（只剩一个端点石子孤立）" if (e1 == 0 or e2 == 0) else "都不为 0，不是特殊情况，用滑动窗口"}',
        'max_cnt = left = 0': '`max_cnt` 记窗口里最多有几颗石子',
        'for right, sr': lambda S, B, r: ('右端点枚举完毕' if ('right' in B and B.right == S.right) else f'枚举右端点所在石子 `sr = {S.sr}`，窗口最长 `n = {S.n}`'),
        'while sr - s[left] + 1 > n': '窗口 `[s[left], sr] = [{s[left]}, {sr}]` 长 `{sr - s[left] + 1}`：{"比 n 大，缩小" if sr - s[left] + 1 > n else "不超过 n，OK"}',
        'left += 1': '`left` 右移到 {left}',
        'max_cnt = max': '窗口内 `{right - left + 1}` 颗石子：`max_cnt = max({B.max_cnt}, {right - left + 1}) = {max_cnt}`',
        'return [n - max_cnt': '窗口外的 `n - max_cnt` 颗石子各搬一步 → 最小 `{n - max_cnt}`，最大 `{max_move}`',
    },
    cards=dict(
        one_liner='最大看空位，最小找长为 n 的窗口里最多的石子',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴上有 `n` 颗石子，每次把一颗端点石子移到空位，且移完不再是端点',
                 '直到石子连续为止，返回 `[最小次数, 最大次数]`',
                 '示例：`[7,4,9]` → `[1,2]`；本视频：`[7,4,9,1,2]` → `[2,4]`'],
        quote='如果不是特殊情况，窗口内至少有 2 个空位，所以在窗口滑动时，是无论如何都不会出现==特殊情况==的。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['最大：第一步总要浪费一段空位，枚举「不动哪个端点」取空位多的 `max(e1, e2)`',
              '最小：终点一定是长为 `n` 的连续段，让它盖住最多石子，其余石子各搬一次',
              '特殊情况（只有一个端点孤立且隔着空位）要单独判，最少要 2 步'],
        summary=['时间 `O(n log n)`，排序是瓶颈；空间 `O(1)`',
                 '特殊情况在滑窗之前判断：`e1 == 0 or e2 == 0`',
                 '特殊情况下答案是 `[min(2, max_move), max_move]`',
                 '右端点较小时窗口左边是空的，不影响取 max，无需判断'],
    ),
)
