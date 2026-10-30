def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tgt, stp = S['target'], S['stamp']
    m, n = len(tgt), len(stp)
    f = S.get('f') or []
    used = S.get('used') or [False] * m
    now = S.get('now')
    cell = min(92, (x1 - x0 - 200) / m)
    sx = x0 + 150 + ((x1 - x0 - 200) - cell * m) / 2
    ty = y0 + 70
    ch = cell * 0.8
    cv.text((x0 + 18, y0 + 4), f'target（绿 = 已被戳印覆盖成通配符）　stamp = "{stp}"', 24, T['muted'], bold=True)
    for p, c in enumerate(tgt):
        X = sx + p * cell
        fill = T['green'] if used[p] else T['panel2']
        cv.rect((X + 4, ty, X + cell - 4, ty + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ty + ch / 2), '*' if used[p] else c, 38, T['bg'] if used[p] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ty + ch + 6), p, 18, T['dim'], anchor='mt', mono=True)
        if now == p and S['_line'] >= 29:
            cv.rect((X, ty - 5, X + cell, ty + ch + 5), outline=T['yellow'], width=5, r=12)
    yy = ty + ch + 56
    cv.text((x0 + 18, yy - 6), '每个候选戳印位置 i：红 = 还没对上的位置，灰 = 本来就对得上，绿 = 已被通配符补上', 20, T['muted'], bold=True)
    yy += 36
    rh = min(70, (y1 - yy - 10) / max(1, m - n + 1))
    for i in range(m - n + 1):
        Y = yy + i * rh
        have = i < len(f)
        ok = have and len(f[i][1]) == 0
        cv.text((sx - 14, Y + rh * 0.4), f'位置 {i}', 24, (T['green'] if ok else T['muted']) if have else T['dim'], anchor='rm', bold=True)
        for j in range(n):
            p = i + j
            X = sx + p * cell
            if not have:
                fill, txt, tc = T['panel2'], stp[j], T['dim']
            elif p in f[i][1]:
                fill, txt, tc = T['red'], stp[j], T['bg']
            elif p in f[i][0]:
                fill, txt, tc = (70, 76, 86), stp[j], T['text']
            else:
                fill, txt, tc = T['green'], '*', T['bg']
            cv.rect((X + 4, Y, X + cell - 4, Y + rh * 0.78), fill=fill, r=8)
            cv.text((X + cell / 2, Y + rh * 0.39), txt, 28, tc, anchor='mm', bold=True, mono=True)
        if ok:
            cv.text((sx + (i + n) * cell + 8, Y + rh * 0.4), '可以戳', 22, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=936, title='戳印序列', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='倒推 · 通配符 BFS',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def movesToStamp(self, stamp, target):

        m = len(target)
        n = len(stamp)

        f = []
        res = []
        used = [False] * m
        q = []
        for i in range(m - n + 1):
            f.append([set(), set()])
            for j in range(n):
                if target[i + j] == stamp[j]:
                    f[-1][0].add(i + j)
                else:
                    f[-1][1].add(i + j)

            if len(f[-1][1]) == 0:
                res.append(i)
                for j in range(i, i + n):
                    if not used[j]:
                        used[j] = True
                        q.append(j)

        head = 0
        tail = len(q)
        while head < tail:
            now = q[head]
            head += 1
            l = max(0, now - n + 1)
            r = min(m - n, now)
            for index in range(l, r + 1):
                if now in f[index][1]:
                    f[index][1].remove(now)
                    if len(f[index][1]) == 0:
                        res.append(index)
                        for pos in f[index][0]:
                            if not used[pos]:
                                used[pos] = True
                                q.append(pos)
                                tail += 1
        
        flag = True
        for index in range(m):
            if not used[index]:
                flag = False
                break

        if flag:
            return res[::-1]

        return []
''',
    call='Solution().movesToStamp("ab", "aabb")',
    expect=[2, 0, 1],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', h=60, size=26, fn=lambda S: f"res（倒着的戳印顺序）= `{S['res']}`" if 'res' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('now', 'now', 'yellow'), ('res', 'res', 'green'), ('q', 'q', 'cyan')],
    skip=['m = len(target)', 'n = len(stamp)', 'f = []', 'res = []', 'q = []', 'head = 0', 'tail = len(q)', 'f.append([set(), set()])', 'flag = True', 'not used[index]', 'head += 1', 'l = max(0, now - n + 1)', 'tail += 1', 'if not used[pos]',
          'for j in range(n)', 'for j in range(i, i + n)', 'for pos in f[index][0]', 'for index in range(m)', 'for index in range(l, r + 1)'],
    max_steps=120,
    captions={
        'used = [False]': '`used[p]` 记录 target 的第 p 个字符是否已被「通配符」覆盖。`f[i]` 记录候选位置 i 的 `[已对上, 没对上]` 两个集合',
        'for i in range(m - n + 1)': lambda S, B, r: (f'逐个检查候选戳印位置 `i = {S.i}`：stamp 盖在 `target[{S.i}:{S.i + S.n}]`' if S.get('i') != B.get('i') or 'i' not in B
                                                      else '候选位置都检查完了，开始用通配符 BFS'),
        'for j in range(n)': lambda S, B, r: (f'比较 `target[{S.i + S.j}] = {S.target[S.i + S.j]}` 与 `stamp[{S.j}] = {S.stamp[S.j]}`' if S.j != B.get('j') or S.i != B.get('i')
                                              else '这个候选位置的 stamp 比较完了'),
        'if target[i + j] == stamp[j]': lambda S, B, r: (f"`target[{S.i + S.j}] = {S.target[S.i + S.j]}` 与 `stamp[{S.j}] = {S.stamp[S.j]}` " + ('相同 → 对得上' if S.target[S.i + S.j] == S.stamp[S.j] else '不同 → 对不上')),
        'f[-1][0].add': '对得上：位置 {i + j} 记入「已对上」集合',
        'f[-1][1].add': '对不上：位置 {i + j} 记入「没对上」集合，需要被通配符补上',
        'if len(f[-1][1]) == 0': lambda S, B, r: (f'位置 {S.i} 没有「没对上」的了 → ==这里可以直接戳一个完整的 stamp==（可作为最后一次戳印）' if not S['f'][-1][1]
                                                  else f'位置 {S.i} 还有 {len(S["f"][-1][1])} 个对不上，暂时不能戳'),
        'res.append(i)': '记下 `{i}`：它是倒推的第一个（实际最后一个）戳印位置',
        'for j in range(i, i + n)': '这次戳印覆盖的每个字符都变成通配符，放入队列 `q`',
        'if not used[j]': lambda S, B, r: (f'`target[{S.j}]` 还不是通配符' if not S.used[S.j] else f'`target[{S.j}]` 已经是通配符，跳过'),
        'used[j] = True': '`target[{j}]` 变成通配符',
        'q.append(j)': '位置 `{j}` 入队，之后检查哪些候选位置会因它受益：`q = {q}`',
        'while head < tail': lambda S, B, r: (f'队列里还有 {S.tail - S.head} 个通配符位置要处理' if S.head < S.tail else '队列处理完了'),
        'now = q[head]': '取出通配符位置 `now = {now}`',
        'r = min(m - n, now)': '能覆盖位置 `now = {now}` 的候选起点范围：`{l}` 到 `{r}`',
        'q.append(pos)': '位置 `{pos}` 入队：`q = {q}`',
        'used[pos] = True': '位置 `{pos}` 在这次戳印下本来就对上，现在也变成通配符，入队后再去影响别的候选',
        'if now in f[index][1]': lambda S, B, r: (f'`now = {S.now}` 在候选 {S.index} 的「没对上」里 → 通配符能匹配任何字符，把它划掉' if S.now in S.f[S.index][1]
                                                  else f'候选 {S.index} 本来就对得上位置 {S.now}（或已划掉），无变化'),
        'f[index][1].remove': '划掉后候选 {index} 还剩没对上的：{f[index][1]}',
        'if len(f[index][1]) == 0': lambda S, B, r: (f'候选 {S.index} 没有对不上的了 → ==它现在也能戳==（先戳它，再戳后面的）' if not S.f[S.index][1] else f'候选 {S.index} 还有对不上的，先不能戳'),
        'res.append(index)': '记下 `{index}`：倒推时它排在 `{res[-2]}` 之后',
        'for pos in f[index][0]': '这次戳印里「本来对上」的字符也变成通配符',
        'for index in range(m)': lambda S, B, r: (f'检查 `target[{S.index}]` 是否被覆盖' if S.index != B.get('index') or 'index' not in B else '检查完毕'),
        'if flag': lambda S, B, r: ('每个字符都被覆盖 → 可以做到，返回倒过来的顺序' if S.flag else '有字符没被覆盖 → 做不到'),
        'return res[::-1]': '戳印顺序要倒过来：先戳 `{res[-1]}`，最后戳 `{res[0]}` → `{ret}`',
    },
    cards=dict(
        one_liner='倒着想：最后一次戳印一定完整，把它变成通配符',
        complexity='时间 `O(m·n)`，空间 `O(m·n)`（`m = len(target)`，`n = len(stamp)`）',
        problem=['空串（全 `?`）反复盖上 `stamp`，每次可盖在任意位置，后盖的覆盖先盖的',
                 '要变成 `target`，返回每次盖的起始下标；不可能返回 `[]`',
                 '示例：`stamp = "ab"`，`target = "aabb"` → `[2, 0, 1]`（答案不唯一）'],
        quote='对于这个序列的最后一次操作，其必然在最终的target上留下来一个完整的stamp，那么我们可以先找到这个stamp的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['倒推：最后一次戳印是完整的 `stamp`，先找出所有已完全匹配的位置',
              '这些字符变成通配符，通配符能让别的候选位置的「不匹配」消失',
              '从字母出发 BFS：每个字符只处理一次，复杂度 `O(m·n)`'],
        summary=['`f[i]` 存候选位置 `i` 的「匹配 / 不匹配」位置集合，不匹配集合空了就能戳',
                 '最后要检查每个字符都变成通配符（`used` 全真），否则返回 `[]`',
                 '答案要倒过来：`res[::-1]`',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '只靠首尾 KMP 处理不了「头尾都被盖住」的情形，所以按字符 BFS'],
    ),
)
