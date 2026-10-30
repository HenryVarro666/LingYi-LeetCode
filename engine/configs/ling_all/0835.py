A0 = [[1, 1], [0, 1]]
B0 = [[0, 1], [1, 1]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    A, Bm = S['img1'], S['img2']
    n = len(A)
    dx, dy = S.get('dx'), S.get('dy')
    line = S['_line']
    cv.text((x0 + 18, y0 + 4), '蓝格 = img2 的 1，橙框 = 平移后的 img1 的 1，绿 = 两边都是 1', 22, T['muted'], bold=True)
    if dx is None:
        dx = dy = 0
    W = 3 * n - 2
    cell = min(130, (x1 - x0 - 40) / W, (y1 - y0 - 130) / W)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * W) / 2
    sy = y0 + 60
    ox = n - 1
    cv.rect((sx + ox * cell - 3, sy + ox * cell - 3, sx + (ox + n) * cell + 3, sy + (ox + n) * cell + 3),
            outline=T['dim'], width=3, r=4)
    for i in range(n):
        for j in range(n):
            X, Y = sx + (ox + j) * cell, sy + (ox + i) * cell
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=T['blue'] if Bm[i][j] else T['panel2'], alpha=255 if Bm[i][j] else 120, r=6)
    started = 'cnt1' in S and line >= 11
    for i in range(n):
        for j in range(n):
            if not A[i][j]:
                continue
            X, Y = sx + (ox + j + dy) * cell, sy + (ox + i + dx) * cell
            inb = 0 <= i + dx < n and 0 <= j + dy < n
            hit = inb and Bm[i + dx][j + dy]
            ii, jj = S.get('i'), S.get('j')
            counted = hit and started and (line >= 12 or (ii is not None and (i < ii or (i == ii and j <= jj))))
            if line < 11:
                counted = False
            if counted:
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=T['green'], r=6)
            cv.rect((X + 5, Y + 5, X + cell - 5, Y + cell - 5), outline=T['orange'] if inb else T['dim'], width=5, r=8)
    ii, jj = S.get('i'), S.get('j')
    if line == 11 and ii is not None and 0 <= ii < n and 0 <= jj < n:
        X, Y = sx + (ox + jj + dy) * cell, sy + (ox + ii + dx) * cell
        cv.rect((X - 2, Y - 2, X + cell + 2, Y + cell + 2), outline=T['pink'], width=5, r=10)
    yb = sy + W * cell + 22
    cv.text((x0 + 20, yb), f"img1 向下 dx = {dx}，向右 dy = {dy}", 30, T['text'], bold=True)
    cv.text((x0 + 20, yb + 44), f"本次平移的重叠 cnt1 = {S.get('cnt1', 0)}     目前最大 ans = {S.get('ans', 0)}", 30, T['green'], bold=True)


CONFIG = dict(
    num=835, title='图像重叠', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='暴力枚举平移',
    tags=['卷积', '难度分 1700'],
    code='''
class Solution:
    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        n = len(img1)
        ans = 0
        for dx in range(1 - n, n):
            for dy in range(1 - n, n):
                cnt1 = 0
                for i in range(max(-dx, 0), min(n - dx, n)):
                    for j in range(max(-dy, 0), min(n - dy, n)):
                        # 两个数都是 1，才能让 cnt1 增加 1
                        cnt1 += img1[i][j] * img2[i + dx][j + dy]
                ans = max(ans, cnt1)
        return ans
''',
    call=f'Solution().largestOverlap({A0}, {B0})',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('dx', 'dx', 'blue'), ('dy', 'dy', 'pink'), ('cnt1', 'cnt1', 'yellow'), ('ans', 'ans', 'green')],
    skip=['n = len', 'ans = 0', 'for dx in', 'for i in range', 'for j in range', 'cnt1 = 0'],
    max_steps=60,
    captions={
        'for dy in': lambda S, B, r: (f"`dy = {S.dy}` 已枚举完 → 换下一个 `dx`" if 'dy' in B and B.dy == S.dy and S.dy == S.n - 1 else
                                      f"平移 `dx = {S.dx}`（正 = 下移）、`dy = {S.dy}`（正 = 右移）：`img1[i][j]` 落在 `img2[i{S.dx:+}][j{S.dy:+}]` 上"),
        'cnt1 += img1': lambda S, B, r: (f"`img1[{S.i}][{S.j}] × img2[{S.i + S.dx}][{S.j + S.dy}]` = `{S.img1[S.i][S.j]} × {S.img2[S.i + S.dx][S.j + S.dy]}`"
                                       f" → 两个都是 1 才 +1，`cnt1` = =={S.cnt1}=="),
        'ans = max': '这个平移的重叠是 `{cnt1}`，`ans = max({B.ans}, {cnt1}) = {ans}`',
        'return ans': '所有 `(2n-1)^2 = {(2*n-1)**2}` 种平移都试过 → 最大重叠 =={ans}==',
    },
    cards=dict(
        one_liner='枚举所有平移 (dx, dy)，数两张图重叠的 1',
        complexity='时间 `O(n^4)`，空间 `O(1)`',
        problem=['两个 `n×n` 的 0/1 矩阵，可把其中一个上下左右平移（不旋转）',
                 '重叠 = 两图在同一位置都是 1 的个数，出界的 1 丢掉，求最大重叠',
                 '官方示例 3×3 → `3`；本视频用 2×2：`[[1,1],[0,1]]` 与 `[[0,1],[1,1]]`'],
        quote='把 $A$ 向下移动 $x$ 个单位，向右移动 $y$ 个单位，那么 $A_{i,j}$ 对应着 $B_{i+x,\\,j+y}$。超出下标范围的元素视作 $0$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`img1[i][j]` 平移后落在 `img2[i+dx][j+dy]` 上',
              '`dx`、`dy` 各有 `2n-1` 种取值，逐个数重叠',
              '只遍历不出界的 `i`、`j`：`max(-dx,0) ≤ i < min(n-dx,n)`'],
        summary=['时间 `O(n^4)`，`n ≤ 30` 够用；空间 `O(1)`',
                 '平移范围是 `1-n` 到 `n-1`，别漏掉负方向',
                 '`i`、`j` 的范围要保证 `i+dx`、`j+dy` 不越界',
                 '方法二：把 img2 翻转后与 img1 做二维卷积，最大值即答案，`O(n^2 log n)`（NumPy/SciPy 写法略）'],
    ),
)
