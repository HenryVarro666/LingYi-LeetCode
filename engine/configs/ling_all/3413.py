def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tiles = S.get('tiles') or S['coins']
    lo = min(t[0] for t in tiles)
    hi = max(t[1] for t in tiles)
    n = hi - lo + 1
    cell = min(86, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys, ch = y0 + 110, 96
    flip = lo < 0
    cv.text((x0 + 18, y0 + 4), '数轴上的袋子（数字 = 每个袋子的硬币数，空格 = 0；粉框 = 毯子/选中的 k 个袋子）' if not flip
            else '反转后的数轴（区间改成 [-r, -l]，原来的左端点对齐变成右端点对齐）', 22, T['muted'], bold=True)
    colors = [T['blue'], T['green'], T['purple'], T['cyan'], T['orange']]
    for ti, (a, b, c) in enumerate(sorted(tiles, key=lambda t: t[0])):
        for p in range(a, b + 1):
            X = sx + (p - lo) * cell
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), fill=colors[ti % 5], alpha=200, r=8)
            cv.text((X + cell / 2, ys + ch / 2), c, 32, T['bg'], anchor='mm', bold=True)
    for p in range(lo, hi + 1):
        X = sx + (p - lo) * cell
        cv.rect((X + 2, ys, X + cell - 2, ys + ch), outline=T['border'], r=8)
        cv.text((X + cell / 2, ys + ch + 8), p, 18, T['dim'], anchor='mt', mono=True)
    if 'carpet_left' in S and 'tr' in S and 'left' in S and S.get('_line') is not None:
        cl, cr = S['carpet_left'], S['tr']
        a, b = max(cl, lo), min(cr, hi)
        cv.rect((sx + (a - lo) * cell - 3, ys - 8, sx + (b - lo + 1) * cell + 3, ys + ch + 8), outline=T['pink'], width=5, r=10)
        cv.text((sx + (a - lo) * cell, ys - 14), f'毯子 [{cl}, {cr}]', 22, T['pink'], anchor='lb', bold=True)
        L = tiles[S['left']]
        cv.line([(sx + (L[0] - lo) * cell + 4, ys + ch + 44), (sx + (L[1] - lo + 1) * cell - 4, ys + ch + 44)], T['yellow'], 6)
        cv.text(((sx + (L[0] - lo) * cell + sx + (L[1] - lo + 1) * cell) / 2, ys + ch + 52), 'left 区间', 20, T['yellow'], anchor='mt', bold=True)


def _txt(S, B):
    if 'carpet_left' not in S or 'cover' not in S:
        return '把毯子右端点对齐某个区间的右端点，再滑窗'
    u = S.get('uncover')
    base = f"窗口内整段硬币 `cover = {S['cover']}`"
    if u is not None and S.get('_line') is not None and 'ans' in S:
        return base + f'，最左区间多算的 `uncover = {u}`，净收益 ==`{S["cover"] - u}`=='
    return base


CONFIG = dict(
    num=3413, title='收集连续 K 个袋子可以获得的最多硬币数量', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 · 左右端点各跑一遍',
    tags=['不定长滑动窗口', '难度分 2374'],
    code='''
class Solution:
    # 2271. 毯子覆盖的最多白色砖块数
    def maximumWhiteTiles(self, tiles: List[List[int]], carpetLen: int) -> int:
        ans = cover = left = 0
        for tl, tr, c in tiles:
            cover += (tr - tl + 1) * c
            carpet_left = tr - carpetLen + 1
            while tiles[left][1] < carpet_left:
                cover -= (tiles[left][1] - tiles[left][0] + 1) * tiles[left][2]
                left += 1
            uncover = max((carpet_left - tiles[left][0]) * tiles[left][2], 0)
            ans = max(ans, cover - uncover)
        return ans

    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        coins.sort(key=lambda c: c[0])
        ans = self.maximumWhiteTiles(coins, k)

        coins.reverse()
        for t in coins:
            t[0], t[1] = -t[1], -t[0]
        return max(ans, self.maximumWhiteTiles(coins, k))
''',
    call='Solution().maximumCoins([[8,10,1],[1,3,2],[5,6,4]], 4)',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', h=70, size=28, fn=_txt),
    ],
    watch=[('left', 'left', 'blue'), ('cover', 'cover', 'cyan'), ('uncover', 'uncover', 'orange'), ('ans', 'ans', 'green')],
    skip=['ans = cover = left = 0', 'for t in coins', 't[0], t[1] = -t[1]'],
    captions={
        'cover += (': '右端点对齐：区间 `[{tl}, {tr}]` 整段进窗口，加 `{tr-tl+1} × {c}` → `cover = {cover}`',
        'carpet_left = ': '毯子右端点贴着 `tr = {tr}`，长 `{carpetLen}` → 左端点 `carpet_left = {carpet_left}`',
        'while tiles[left][1] <': '`left` 区间右端 `{tiles[left][1]}` 与 `carpet_left = {carpet_left}` 比：{"整段在毯子左边，要踢出" if tiles[left][1] < carpet_left else "已经碰到毯子，停止"}',
        'cover -= (': '把整个 `left` 区间踢出窗口，`cover` 减去它的硬币 → {cover}',
        'left += 1': '`left` 右移到 {left}',
        'uncover = max': '最左区间只被毯子盖住一部分：毯子左端 `{carpet_left}` 左边还有该区间的 `{max(carpet_left - tiles[left][0], 0)}` 格，要扣掉，`uncover = {uncover}`',
        'ans = max(ans, cover - uncover)': '`ans = max({B.ans}, {cover} - {uncover}) = {ans}`',
        'coins.sort': '先按左端点排序，区间互不重叠，所以右端点也有序',
        'ans = self.maximumWhiteTiles(coins, k)': '第一遍：毯子右端点对齐每个区间右端点',
        'coins.reverse()': '要试「左端点对齐」：把数轴镜像，区间顺序反转，每个 `[l, r]` 变成 `[-r, -l]`',
        'return max(ans': '镜像后再跑一遍，两遍取较大者',
        'return ans': '这一遍的最大收益是 `{ans}`',
    },
    cards=dict(
        one_liner='和右端点对齐滑一遍，再镜像翻转滑一遍',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴上若干不重叠区间 `[l, r, c]`，区间内每个袋子有 `c` 枚硬币',
                 '连续选 `k` 个袋子，求最多收集多少硬币',
                 '示例：`[[8,10,1],[1,3,2],[5,6,4]], k = 4` → `10`'],
        quote='如果出现两个相邻区间，左边区间 c 大，右边区间 c 小的情况，那么和右端点对齐就不是最优的，==和左端点对齐==反而是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先照搬 2271（毯子覆盖砖块）：毯子右端点对齐区间右端点，滑动窗口',
              '带权后，左边 c 大右边 c 小时应改为左端点对齐',
              '把区间改成 `[-r, -l]` 再跑一遍，复用同一段代码'],
        summary=['时间 `O(n log n)`，排序是瓶颈；空间 `O(1)`',
                 '`uncover` 要和 0 取 max：毯子左端若落在空隙里就不用扣',
                 '反转时先 `reverse()` 保证有序，再把坐标取负交换',
                 '变形题：区间可重叠时，用差分哈希表先拆成不重叠区间'],
    ),
)
