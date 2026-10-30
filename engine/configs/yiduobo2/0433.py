START, END = 'AACCGGTT', 'AAACGGTA'
BANK = ['AACCGGTA', 'AACCGCTA', 'AAACGGTA']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    now = S.get('now')
    if not isinstance(now, str) or not isinstance(S.get('index'), int) or S.get('_line') not in (15, 20, 22, 23, 24):
        cv.text((x0 + 18, y0 + 4), '把每个基因看成点：只差一个字符的两个基因之间连一条边', 24, T['muted'], bold=True)
        return
    idx, ch = S['index'], S['char']
    bank = S.get('gen_bank') or set()
    cv.text((x0 + 18, y0 + 4), f'当前出队 now，把第 {idx} 位换成另外 3 个字母：', 24, T['muted'], bold=True)
    cell = 62
    sx = x0 + 40
    y = y0 + 46
    cv.text((sx, y + cell / 2), 'now', 24, T['blue'], anchor='lm', bold=True)
    gx = sx + 110
    for i, c in enumerate(now):
        X = gx + i * cell
        hot = i == idx
        cv.rect((X + 3, y, X + cell - 3, y + cell), fill=T['orange'] if hot else T['panel2'], r=8,
                outline=T['orange'] if hot else T['border'])
        cv.text((X + cell / 2, y + cell / 2), c, 30, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
    yy = y + cell + 22
    for r, rc in enumerate([c for c in 'ACGT' if c != ch]):
        tmp = now[:idx] + rc + now[idx + 1:]
        Y = yy + r * (cell - 6)
        is_end = tmp == S['end']
        in_bank = tmp in bank
        col = T['green'] if is_end else (T['yellow'] if in_bank else T['dim'])
        for i, c in enumerate(tmp):
            X = gx + i * cell
            if i == idx:
                cv.rect((X + 3, Y + 2, X + cell - 3, Y + cell - 10), fill=col if (is_end or in_bank) else T['panel2'], r=8)
            cv.text((X + cell / 2, Y + (cell - 8) / 2), c, 26, T['bg'] if (i == idx and (is_end or in_bank)) else
                    (T['text'] if (is_end or in_bank) else T['dim']), anchor='mm', bold=i == idx, mono=True)
        tag = '就是 end → 返回' if is_end else ('在 bank 中 → 入队' if in_bank else '不在 bank')
        cv.text((gx + len(now) * cell + 16, Y + (cell - 8) / 2), tag, 22, col, anchor='lm', bold=is_end or in_bank)


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'q（数组当队列：框住的 [l, r) 是当前这一层，蓝 = 正在扩展的 now）', 24, T['muted'], bold=True)
    q = S.get('q')
    if not isinstance(q, list):
        return
    l, r = S.get('l'), S.get('r')
    w, gap = 190, 16
    sx = x0 + 30
    y = y0 + 50
    cur = S.get('now') if S.get('_line') in (14, 15, 20, 22, 23, 24) else None
    for i, g in enumerate(q):
        X = sx + i * (w + gap)
        inl = isinstance(l, int) and isinstance(r, int) and l <= i < r
        fill = T['blue'] if g == cur else T['panel2']
        cv.rect((X, y, X + w, y + 64), fill=fill, r=10, outline=T['cyan'] if inl else T['border'], width=4 if inl else 1)
        cv.text((X + w / 2, y + 32), g, 26, T['bg'] if g == cur else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + w / 2, y + 74), i, 18, T['dim'], anchor='mt', mono=True)
    for name, v, c, dy in (('l', l, T['blue'], 0), ('r', r, T['pink'], 0)):
        if isinstance(v, int):
            X = sx + v * (w + gap) - gap / 2
            cv.tri_up(X, y + 102, 9, c)
            cv.text((X + (14 if name == 'r' else -14), y + 118), name, 22, c, anchor='mt', bold=True)


def _cap_for_idx(S, B, ret):
    if S.get('index') == B.get('index') and 'index' in B and S.get('now') == B.get('now'):
        return f'`{S.now}` 的 8 个位置都试完了'
    now, i = S.now, S.index
    cands = [now[:i] + c + now[i + 1:] for c in 'ACGT' if c != now[i]]
    if S.end in cands:
        return f'第 `{i}` 位 `{now[i]}` 换成别的字母，其中一个==正好是 end==！'
    hits = [t for t in cands if t in S.gen_bank]
    if hits:
        return f'第 `{i}` 位 `{now[i]}` 换成别的字母：`{hits[0]}` ==在 bank 中=='
    return f'第 `{i}` 位 `{now[i]}` → 另外 3 个字母都不在 bank 中'


CONFIG = dict(
    num=433, title='最小基因变化', difficulty='Medium', category='图论',
    author='yiduobo', technique='BFS 按层扩展 · 基因看成点',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def minMutation(self, start, end, bank):
        gen_bank = set(bank)
        if end not in gen_bank:
            return -1

        q = [start]
        l = 0
        r = 1
        res = 0
        while l < r:
            res += 1
            new_r = r
            for now in q[l:r]:
                for index, char in enumerate(now):
                    for replace_char in ['A', 'C', 'G', 'T']:
                        if replace_char != char:
                            tmp = now[:index] + replace_char + now[index + 1:]
                            if tmp == end:
                                return res
                            if tmp in gen_bank:
                                q.append(tmp)
                                new_r += 1
                                gen_bank.remove(tmp)
            l = r
            r = new_r

        return -1
''',
    call=f'Solution().minMutation({START!r}, {END!r}, {BANK!r})',
    expect=2,
    views=[
        dict(type='custom', draw=_draw_q, h=200),
        dict(type='set', var='gen_bank', label='gen_bank（还没访问过的基因）', h=100, font=24),
        dict(type='custom', draw=_draw, h=310),
    ],
    watch=[('res', 'res', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('new_r', 'new_r'), ('now', 'now', 'blue')],
    skip=['for replace_char in', 'if replace_char != char', 'tmp = now[:index]', 'if tmp == end', 'if tmp in gen_bank',
          'l = 0', 9, 'res = 0'],
    captions={
        'gen_bank = set(bank)': '`bank` 转成集合，方便 `O(1)` 判断、删除',
        'if end not in gen_bank': lambda S, B, ret: ('`end` 不在 bank 中 → 不可能变到' if S.end not in S.gen_bank
                                                     else '`end` 在 bank 中，开始 BFS'),
        'q = [start]': '队列里先放起点 `start`；`l = 0`、`r = 1` 圈出第一层，`res = 0`',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：这一层有 `{S.r - S.l}` 个基因要扩展' if S.l < S.r
                                          else '队列空了，到不了 end'),
        'res += 1': '进入第 `{res}` 轮：这一轮新生成的基因都需要 `{res}` 次变化',
        'new_r = r': '`new_r` 记录下一层的右端点',
        'for now in q[l:r]': lambda S, B, ret: ('这一层的基因都扩展完了' if 'now' in B and B.now == S.now
                                                else f'取出这一层的 `now = "{S.now}"`'),
        'for index, char in enumerate(now)': _cap_for_idx,
        'return res': '生成的 `tmp` 就是 end → 第 `{res}` 轮到达，返回 =={ret}==',
        'q.append(tmp)': '`{tmp}` 在 bank 中：入队（下一层）',
        'new_r += 1': '`new_r` → {new_r}',
        'gen_bank.remove(tmp)': '从 bank 删掉 `{B.tmp}`，==避免重复访问==',
        'l = r': '这一层扩展完：`l` → {l}',
        '            r = new_r': '`r` → {r}：`q[{l}:{r}]` 是下一层',
    },
    max_steps=60,
    cards=dict(
        one_liner='基因是点，改一个字符能到的基因连边，从 start 做 BFS，到 end 的轮数就是答案',
        complexity='时间 `O(n·L·4)`，空间 `O(n)`（`n` = bank 大小，`L = 8`）',
        problem=['基因是长为 8、由 `A C G T` 组成的字符串；一次变化 = 改一个字符',
                 '每次变化后的基因都必须在 `bank` 中；求 `start` 变到 `end` 的最少次数，不能则 `-1`',
                 f'示例：`start = "{START}"`，`end = "{END}"`',
                 f'`bank = {BANK}` → `2`'],
        quote='如果将bank中的所有基因看成点，那么对于基因x，若替换其中某个字符后能变成基因y，那么就认为在x到y之间存在一条边。我们==从start开始进行bfs，抵达end的轮次即为最终答案==。',
        quote_src='—— yiduobo 题解',
        idea=['用数组 `q` 当队列，`[l, r)` 是当前层，`new_r` 是下一层的右端点',
              '每个基因的 8 个位置各换成另外 3 个字母，在 bank 中的就入队',
              '入队后从 bank 删掉，防止走回头路；生成 end 时直接返回轮数'],
        result=f'`{START}` → `AACCGGTA` → `{END}`，共 2 次 ✓',
        summary=['时间：每个基因出队一次，枚举 `8 × 3` 个邻居',
                 '`end` 不在 bank 中可以直接返回 `-1`',
                 '入队时就从集合里删除，比出队时再判重更省',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改',
                 '同类：127 单词接龙（同样的 BFS 套路）'],
    ),
)
