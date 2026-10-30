def _expand(a):
    out = []
    for v, c in a:
        out += [v] * c
    return out


def _fmt(x):
    return f'{x[0]}×{x[1]}'


def _txt(S):
    if 'p1' not in S:
        return ''
    e1, e2 = S['encoded1'], S['encoded2']
    p1, p2 = S['p1'], S['p2']
    a = f"`{e1[p1][0]}×{e1[p1][1]}`" if p1 < len(e1) else '（已耗尽）'
    b = f"`{e2[p2][0]}×{e2[p2][1]}`" if p2 < len(e2) else '（已耗尽）'
    return f"两路当前段：{a} 与 {b}；各自还剩 =={S['cnt1']}== / =={S['cnt2']}== 个没用"


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    e1, e2 = S['encoded1'], S['encoded2']
    n = len(_expand(e1))
    cell = min(80, (x1 - x0 - 140) / n)
    sx = x0 + 120
    live = 'res' in S
    res = S.get('res') or []
    prod = []
    for v, c in res:
        prod += [v] * c
    p1, p2 = S.get('p1', -1), S.get('p2', -1)
    c1, c2 = S.get('cnt1', 0), S.get('cnt2', 0)
    y = y0 + 20
    for name, enc, col, p, cnt in (('encoded1', e1, 'blue', p1, c1), ('encoded2', e2, 'pink', p2, c2)):
        cv.text((x0 + 10, y + 26), name, 22, T['muted'], anchor='lm', bold=True)
        pos = 0
        for k, (v, c) in enumerate(enc):
            X0, X1 = sx + pos * cell, sx + (pos + c) * cell
            cur = live and k == p
            done = live and k < p
            cv.rect((X0 + 2, y, X1 - 2, y + 56), fill=T[col], r=8, alpha=60 if done else 200)
            if cur:
                cv.rect((X0 + 2, y, X1 - 2, y + 56), outline=T['yellow'], width=4, r=8)
            cv.text(((X0 + X1) / 2, y + 28), f'{v} × {c}', 24, T['bg'] if not done else T['muted'], anchor='mm', bold=True)
            pos += c
        y += 66
        if live and 0 <= p < len(enc):
            off = sum(c for _, c in enc[:p]) + enc[p][1] - cnt
            cv.text((sx + (off + cnt / 2) * cell, y + 4), f'剩 {cnt}', 20, T[col], anchor='mt', bold=True)
        y += 34
    cv.text((x0 + 10, y + 26), '已得积', 22, T['muted'], anchor='lm', bold=True)
    for i in range(n):
        X = sx + i * cell
        filled = i < len(prod)
        cv.rect((X + 2, y, X + cell - 2, y + 52), fill=T['green'] if filled else (50, 55, 64), r=6, alpha=200 if filled else 255)
        if filled:
            cv.text((X + cell / 2, y + 26), prod[i], 26, T['bg'], anchor='mm', bold=True)
    y += 80
    cv.text((x0 + 10, y), 'res（合并后的结果段）：' + ('  '.join(f'[{v}, {c}]' for v, c in res) if res else '空'), 24, T['green'], bold=True)


CONFIG = dict(
    num=1868, title='两个行程编码数组的积', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='二路归并 + 剩余计数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findRLEArray(self, encoded1, encoded2):

        p1 = p2 = 0
        cnt1, cnt2 = encoded1[0][1], encoded2[0][1]

        res = []
        while p1 < len(encoded1) and p2 < len(encoded2):
            v = encoded1[p1][0] * encoded2[p2][0]
            cnt = min(cnt1, cnt2)

            cnt1 -= cnt
            cnt2 -= cnt

            if cnt1 == 0:
                p1 += 1
                if p1 < len(encoded1):
                    cnt1 = encoded1[p1][1]
            
            if cnt2 == 0:
                p2 += 1
                if p2 < len(encoded2):
                    cnt2 = encoded2[p2][1]
            
            if res and res[-1][0] == v:
                res[-1][1] += cnt
            else:
                res.append([v, cnt])
        
        return res
''',
    call='Solution().findRLEArray([[1,3],[2,1],[3,2]], [[6,3],[3,3]])',
    expect=[[6, 4], [9, 2]],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('cnt1', 'cnt1', 'blue'), ('cnt2', 'cnt2', 'pink'), ('res', 'res', 'green')],
    captions={
        'p1 = p2 = 0': '两路各用一个下标：`p1 = p2 = 0`',
        'cnt1, cnt2 =': '`cnt1 = {cnt1}`、`cnt2 = {cnt2}`：各自当前这一段还==剩几个数没用==',
        'res = []': '`res` 存合并后的结果段',
        'while p1 <': lambda S, B, r: ('两路都还有段 → 继续' if S.p1 < len(S.encoded1) and S.p2 < len(S.encoded2) else '有一路用完了（题目保证两路总长相同，会同时用完）→ 结束'),
        'v = encoded1': '当前段的值相乘：`{encoded1[p1][0]} × {encoded2[p2][0]}` = =={v}==',
        'cnt = min': '两段剩余个数取小：`min({cnt1}, {cnt2})` = =={cnt}==，这么多个数的积都是 `{v}`',
        'cnt1 -= cnt': '`cnt1` 扣掉用掉的 → {cnt1}',
        'cnt2 -= cnt': '`cnt2` 扣掉用掉的 → {cnt2}',
        'if cnt1 == 0': lambda S, B, r: (f'`cnt1 = 0`：e1 这一段用完了 → 要换下一段' if S.cnt1 == 0 else f'`cnt1 = {S.cnt1}`：这一段还没用完，下标不动'),
        'p1 += 1': '`p1` → {p1}',
        'cnt1 = encoded1': '`cnt1` 重置为新一段的个数 {cnt1}',
        'if cnt2 == 0': lambda S, B, r: (f'`cnt2 = 0`：e2 这一段用完了 → 要换下一段' if S.cnt2 == 0 else f'`cnt2 = {S.cnt2}`：这一段还没用完，下标不动'),
        'p2 += 1': '`p2` → {p2}',
        'cnt2 = encoded2': '`cnt2` 重置为新一段的个数 {cnt2}',
        'if res and': lambda S, B, r: ('`res` 为空 → 直接新增一段' if not S.res else (f'`res` 末段的值 `{S.res[-1][0]}` == `{S.v}` → ==合并==，只累加个数' if S.res[-1][0] == S.v else f'末段的值 `{S.res[-1][0]}` ≠ `{S.v}` → 新增一段')),
        'res[-1][1] += cnt': '末段个数累加 `{cnt}` → `res = {res}`',
        'res.append': '新增一段 `[{v}, {cnt}]` → `res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='二路归并：每次取两段剩余个数的较小值，一口气乘掉',
        complexity='时间 `O(m+n)`，空间 `O(1)`（不计结果）',
        problem=['行程编码 `[值, 个数]` 表示连续重复的数，如 `[[1,3],[2,1]]` = `1,1,1,2`',
                 '把两个编码展开后==逐位相乘==，再重新压缩成行程编码返回',
                 '示例：`[[1,3],[2,1],[3,2]]` 与 `[[6,3],[3,3]]` → `[[6,4],[9,2]]`'],
        quote='直接套用二路归并的思路，不过在执行过程中除了需要记录两路的下标p1以及p2之外，还需要额外维护当前p1和p2对应的数值中还剩余几个数没有被使用过。',
        quote_src='—— yiduobo 题解原文',
        idea=['不展开数组（可能很长），只记每路==当前段还剩几个==：`cnt1`、`cnt2`',
              '取较小值 `cnt`，这 `cnt` 个位置的积都是同一个 `v`',
              '剩余为 0 的那一路换下一段；新 `v` 与末段相同就==合并==，否则新增'],
        summary=['时间 `O(m+n)`，空间 `O(1)`',
                 '易错：相邻结果段值相同必须合并（本例 `1×6` 与 `2×3` 都是 6）',
                 '换段时要先判断 `p < len`，否则下标越界',
                 '原文为 Python 2 风格，本题无需改动，直接可在 Python 3 运行'],
    ),
)
