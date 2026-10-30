def _draw_factory(get):
    def _draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        tiles, lo, hi, marks, note = get(S)
        cv.text((x0 + 18, y0 + 4), '数轴：白砖段（灰=不在毯子内，绿=被毯子盖住的部分）', 22, T['muted'], bold=True)
        mx = max(t[1] for t in tiles) + 2
        unit = (x1 - x0 - 60) / mx
        sx = x0 + 30
        ty = y0 + 200
        th = 70
        # carpet band
        if lo is not None:
            cv.rect((sx + lo * unit, ty - 80, sx + (hi + 1) * unit, ty + th + 24), fill=T['green'], alpha=40, r=8,
                    outline=T['green'], width=3)
            cv.text(((sx + lo * unit + sx + (hi + 1) * unit) / 2, ty - 100), f'毯子 [{lo}, {hi}]', 24, T['green'], anchor='mb', bold=True)
        for i, (a, b) in enumerate(tiles):
            X0, X1 = sx + a * unit, sx + (b + 1) * unit
            cv.rect((X0, ty, X1, ty + th), fill=(110, 118, 130), r=6)
            if lo is not None:
                ca, cb = max(a, lo), min(b, hi)
                if ca <= cb:
                    cv.rect((sx + ca * unit, ty, sx + (cb + 1) * unit, ty + th), fill=T['green'], r=6)
            cv.text(((X0 + X1) / 2, ty + th / 2), f'{b - a + 1}', 24, T['bg'], anchor='mm', bold=True)
            cv.text((X0, ty + th + 30), a, 18, T['dim'], anchor='mt', mono=True)
            if b > a:
                cv.text((X1 - unit, ty + th + 30), b, 18, T['dim'], anchor='mt', mono=True)
        for i, (c, label) in marks.items():
            a, b = tiles[i]
            X0, X1 = sx + a * unit, sx + (b + 1) * unit
            cv.rect((X0 - 3, ty - 3, X1 + 3, ty + th + 3), outline=T[c], width=5, r=8)
            cv.tri_up((X0 + X1) / 2, ty + th + 82, 10, T[c])
            cv.text(((X0 + X1) / 2, ty + th + 100), label, 22, T[c], anchor='mt', bold=True)
        if note:
            cv.text((x0 + 18, y0 + 40), note, 24, T['yellow'])
    return _draw


def _get(S):
    tiles = S['tiles']
    if 'carpet_left' not in S or 'tr' not in S:
        return tiles, None, None, {}, ''
    cl, tr = S['carpet_left'], S['tr']
    marks = {}
    cur = [i for i, t in enumerate(tiles) if t[1] == tr]
    lf = S['left']
    if lf < len(tiles):
        marks[lf] = ('blue', 'left')
    if cur:
        marks[cur[0]] = ('pink', 'tl,tr') if cur[0] != lf else ('pink', 'left=当前')
    note = f"cover（完整段长度和）= {S['cover']}" + (f"；多算的 uncover = {S['uncover']}" if 'uncover' in S else '')
    return tiles, max(cl, 0), tr, marks, note


CONFIG = dict(
    num=2271, title='毯子覆盖的最多白色砖块数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='毯子右端点贴段尾 + 双指针',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2022'],
    code='''
class Solution:
    def maximumWhiteTiles(self, tiles: List[List[int]], carpetLen: int) -> int:
        tiles.sort(key=lambda x: x[0])
        ans = cover = left = 0
        for tl, tr in tiles:
            cover += tr - tl + 1  # 统计完整区间长度和

            carpet_left = tr - carpetLen + 1  # 毯子左端点
            while tiles[left][1] < carpet_left:  # tiles[left] 完全不在窗口中
                cover -= tiles[left][1] - tiles[left][0] + 1
                left += 1

            # tiles[left] 中的小于 carpet_left 的这部分不在窗口中
            uncover = max(carpet_left - tiles[left][0], 0)
            ans = max(ans, cover - uncover)  # 注意这里没有修改 cover，cover 始终是完整区间长度和
        return ans
''',
    call='Solution().maximumWhiteTiles([[1,5],[10,11],[12,18],[20,25],[30,32]], 10)',
    expect=9,
    views=[dict(type='custom', draw=_draw_factory(_get), h=420),
           dict(type='text', h=70, size=28, fn=lambda S: (f"毯子左端 = `{S['tr']} − {S['carpetLen']} + 1` = =={S['carpet_left']}==" if 'carpet_left' in S and 'tr' in S else '毯子长度 `carpetLen` = 10，右端点贴着某段白砖的右端'))],
    watch=[('tl', 'tl', 'blue'), ('tr', 'tr', 'pink'), 'carpet_left', 'left', 'cover', 'uncover', ('ans', 'ans', 'green')],
    skip=['cover -= tiles[left]'],
    captions={
        'tiles.sort': '先按左端点排序，白砖段从左到右排好',
        'ans = cover = left = 0': '`cover` 记录窗口内各段的==完整长度和==，`left` 是窗口最左的一段',
        'for tl, tr in tiles': '枚举毯子右端点：放在这一段的右端 `tr = {tr}`（放在段中间不如挪到段尾，只会多盖不会少盖）',
        'cover += ': '把这一段 `[{tl}, {tr}]` 整段算进来：`cover` = =={cover}==',
        'carpet_left =': '毯子左端 = `{tr} − {carpetLen} + 1` = =={carpet_left}==',
        'while tiles[left][1] <': lambda S, B, r: (f'`tiles[{S.left}]` 右端 `{S.tiles[S.left][1]} < {S.carpet_left}`：这段整个在毯子左边 → 要扔掉' if S.tiles[S.left][1] < S.carpet_left
                                                   else f'`tiles[{S.left}]` 右端 `{S.tiles[S.left][1]} >= {S.carpet_left}`：这段至少有一部分被盖住，停止收缩'),
        'left += 1': '`left` 右移到 {left}，`cover` 扣掉被扔掉的整段 → {cover}',
        'uncover =': '`tiles[left]` 左端是 `{tiles[left][0]}`，毯子从 `{carpet_left}` 开始 → 左边多算了 `uncover` = =={uncover}==',
        'ans = max': '实际盖住 `cover − uncover` = `{cover} − {uncover}` = {cover - uncover} → `ans = {ans}`（注意 cover 本身不改）',
        'return ans': '最多盖住 =={ans}== 块',
    },
    cards=dict(
        one_liner='毯子右端贴段尾，左边多算的那截再减掉',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['`tiles[i] = [l, r]` 表示 `l..r` 都是白砖，段互不重叠', '用一块长 `carpetLen` 的毯子，最多盖住多少块白砖',
                 '示例：`[[1,5],[10,11],[12,18],[20,25],[30,32]]`，`carpetLen=10` → `9`'],
        quote='毯子右端点放在一段瓷砖中间，是不如直接放在这段瓷砖右端点的（因为从中间向右移动，能覆盖的瓷砖数不会减少），所以可以枚举每段瓷砖的右端点来摆放毯子的右端点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后枚举每段的右端 `tr`，毯子左端就是 `tr − carpetLen + 1`',
              '`left` 只会右移：整段落在毯子左边的段不再需要',
              '`left` 那段若被毯子截断，减去 `carpet_left − tiles[left][0]`'],
        summary=['时间 `O(n log n)`，瓶颈是排序；双指针部分 `O(n)`',
                 '易错：`left` 那段可能只盖一部分，要减 `uncover`（为负则不减）',
                 '`cover` 始终是完整段长度和，`uncover` 只用来算答案，不写回 `cover`',
                 '进阶：带权版本见 3413 题'],
    ),
)
