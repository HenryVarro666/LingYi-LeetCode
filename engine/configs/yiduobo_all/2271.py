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
    tiles = S['sorted_tiles']
    if 'end_pos' not in S:
        return tiles, None, None, {}, ''
    h = S.get('head_index', 0)
    lo, hi = tiles[h][0], S['end_pos']
    marks = {h: ('pink', 'head')}
    p = S.get('p', 0)
    marks[p] = ('blue', 'p') if p != h else ('blue', 'head=p')
    note = f"now（p 之前整段长度和）= {S['now']}" if 'now' in S else ''
    return tiles, lo, hi, marks, note


CONFIG = dict(
    num=2271, title='毯子覆盖的最多白色砖块数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='毯子左端贴段首 + 单调双指针',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2022'],
    code='''
class Solution(object):
    def maximumWhiteTiles(self, tiles, carpetLen):

        sorted_tiles = sorted(tiles, key=lambda d:d[0])
        n = len(sorted_tiles)
        end_pos = sorted_tiles[0][0] + carpetLen - 1

        p = 0
        now = sorted_tiles[0][1] - sorted_tiles[0][0] + 1
        while p + 1 < n and sorted_tiles[p + 1][0] <= end_pos:
            p += 1
            now += sorted_tiles[p][1] - sorted_tiles[p][0] + 1
        
        if end_pos >= sorted_tiles[p][1]:
            res = now
        else:
            res = now - (sorted_tiles[p][1] - sorted_tiles[p][0] + 1) + (end_pos - sorted_tiles[p][0] + 1)
        
        for head_index in range(1, n):
            end_pos = sorted_tiles[head_index][0] + carpetLen - 1
            now -= sorted_tiles[head_index - 1][1] - sorted_tiles[head_index - 1][0] + 1
            while p + 1 < n and sorted_tiles[p + 1][0] <= end_pos:
                p += 1
                now += sorted_tiles[p][1] - sorted_tiles[p][0] + 1
            
            if end_pos >= sorted_tiles[p][1]:
                res = max(res, now)
            else:
                res = max(res, now - (sorted_tiles[p][1] - sorted_tiles[p][0] + 1) + (end_pos - sorted_tiles[p][0] + 1))
        
        return res
''',
    call='Solution().maximumWhiteTiles([[1,5],[10,11],[12,18],[20,25],[30,32]], 10)',
    expect=9,
    views=[dict(type='custom', draw=_draw_factory(_get), h=420),
           dict(type='text', h=70, size=28, fn=lambda S: (f"毯子 `[{S['sorted_tiles'][S.get('head_index', 0)][0]}, {S['end_pos']}]`，当前最右相交的段是第 `{S['p']}` 段" if 'end_pos' in S and 'p' in S else '毯子从某一段白砖的起点开始铺'))],
    watch=[('head', 'head_index', 'pink'), ('p', 'p', 'blue'), 'end_pos', 'now', ('res', 'res', 'green')],
    skip=['now -= ', 'p += 1'],
    captions={
        'sorted_tiles = sorted': '先按起点排序',
        'end_pos = sorted_tiles[0][0]': '先让毯子从第 0 段起点开始：右端 `end_pos = {end_pos}`',
        'now = ': '`now`：从毯子起点段到 `p` 段，整段长度之和（先放第 0 段）= {now}',
        'while p + 1 < n': lambda S, B, r: ((f'第 `{S.p + 1}` 段起点 `{S.sorted_tiles[S.p + 1][0]} <= end_pos = {S.end_pos}` → 毯子碰到它，纳入' if S.p + 1 < len(S.sorted_tiles) and S.sorted_tiles[S.p + 1][0] <= S.end_pos else '后面的段起点已超过毯子右端（或没有了），不再向右扩')),
        'if end_pos >= sorted_tiles[p][1]': lambda S, B, r: (f'`end_pos = {S.end_pos} >= {S.sorted_tiles[S.p][1]}`：最后一段被整段盖住 → 直接用 `now`' if S.end_pos >= S.sorted_tiles[S.p][1]
                                                              else f'`end_pos = {S.end_pos} < {S.sorted_tiles[S.p][1]}`：最后一段只盖了一部分 → 要修正'),
        'now += sorted_tiles[p]': '纳入第 `{p}` 段：`now` → {now}',
        'res = now - ': '最后一段只盖前 `{end_pos - sorted_tiles[p][0] + 1}` 块：整段长度换成这一截 → `res` = =={res}==',
        'res = now': '整段都盖住：`res = now` = =={res}==',
        'for head_index': '换毯子起点到第 `{head_index}` 段起点 `{sorted_tiles[head_index][0]}`，右端 `{sorted_tiles[head_index][0] + carpetLen - 1}`',
        'end_pos = sorted_tiles[head_index]': '毯子右端 `end_pos = {end_pos}`',
        'res = max(res, now)': '整段盖住 → `res = max({B.res}, {now}) = {res}`',
        'res = max(res, now -': '最后一段只盖一截：`now` 修正后与 `res` 比较 → `res = {res}`',
        'return res': '最多盖住 =={res}== 块',
    },
    cards=dict(
        one_liner='毯子必有一种最优铺法是从某段白砖的起点开始',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`tiles` 是互不重叠的白砖段，毯子长 `carpetLen`', '问毯子最多盖住多少白砖',
                 '本视频：`[[1,5],[10,11],[12,18],[20,25],[30,32]]`，`carpetLen=10` → `9`'],
        quote='必然有某种最优方案是用毯子从某一段白色砖块的起点开始覆盖。……利用单调性，使用双指针来进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['p 落在空地：右移到下一段起点，白砖只增不减；p 落在段中：往左挪到段首，白砖只增不减',
              '于是枚举每一段的起点 `head_index` 当毯子起点',
              '毯子起点右移，`p`（最后相交的段）也只右移 → 双指针'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：最后一段可能只盖一截，用 `end_pos - 起点 + 1` 代替整段长度',
                 '起点右移要先减掉上一段的长度 `now -=`',
                 '对比灵神：灵神把毯子右端贴段尾、减左边多算的一截；这里是左端贴段首、改右边多算的一截'],
    ),
)
