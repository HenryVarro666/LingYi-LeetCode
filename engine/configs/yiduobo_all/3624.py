def _fen_pic(cv, T, box, tree, old, vals, cur, title, vlabel='值'):
    """树状数组：上排 = 位置 1..m 的值，下面每根条 = tree[i] 管的关键区间 [i-lowbit+1, i]（按 lowbit 分层）；
    黄色 = 当前正在访问的 tree[i]，蓝色 = 它覆盖的位置，黄边 = 这一步刚改过"""
    x0, y0, x1, y1 = box
    m = len(tree) - 1
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    if m < 1:
        return
    cell = min(120, (x1 - x0 - 60) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    ty = y0 + 34
    nlev = max(i & -i for i in range(1, m + 1)).bit_length()
    rowh = min(60, (y1 - (ty + 76)) / nlev)
    lo = hi = None
    if cur is not None and 1 <= cur <= m:
        hi = cur
        lo = cur - (cur & -cur) + 1
    for i in range(1, m + 1):
        X = sx + (i - 1) * cell
        covered = lo is not None and lo <= i <= hi
        cv.rect((X + 2, ty, X + cell - 2, ty + 42), fill=T['blue'] if covered else T['panel2'], r=6, alpha=200 if covered else 255)
        v = vals[i - 1] if i - 1 < len(vals) else ''
        cv.text((X + cell / 2, ty + 21), v, 24, T['bg'] if covered else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 48), i, 18, T['dim'], anchor='mt', mono=True)
    by = ty + 72
    for i in range(1, m + 1):
        lb = i & -i
        lv = lb.bit_length() - 1
        xa, xb = sx + (i - lb) * cell + 3, sx + i * cell - 3
        ya = by + lv * rowh
        changed = old is not None and len(old) == len(tree) and old[i] != tree[i]
        if i == cur:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((xa, ya, xb, ya + rowh - 5), fill=fill, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1, r=6)
        lab = f't{i}={tree[i]}' if cell * lb > 150 else f'{tree[i]}'
        if lb > 1:
            lab = f't{i}={tree[i]}  [{i - lb + 1},{i}]' if cell * lb > 260 else f't{i}={tree[i]}'
        cv.text(((xa + xb) / 2, ya + (rowh - 5) / 2), lab, 20, tc, anchor='mm', bold=True)


def _lb_text(i):
    return f'`{i}` = `{i:b}`（二进制），lowbit = `{i & -i}`'
def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rows = S.get('f')
    nums = S.get('nums')
    if rows is None or nums is None:
        cv.text((x0 + 18, y0), '（还没建树）', 24, T['dim'])
        return
    old = B.get('f')
    n = len(nums)
    cell = min(110, (x1 - x0 - 230) / n)
    sx = x0 + 190
    cv.text((x0 + 18, y0), 'f[k] = 深度 k 的树状数组（黄 = 当前下标，蓝 = 刚改过）', 22, T['muted'], bold=True)
    ty = y0 + 40
    cv.text((x0 + 10, ty + 25), 'nums', 22, T['muted'], anchor='lm', bold=True)
    cv.text((x0 + 10, ty + 62), '(深度会原地替换)', 16, T['dim'], anchor='lm')
    for j, v in enumerate(nums):
        X = sx + j * cell
        cv.rect((X + 3, ty, X + cell - 3, ty + 50), fill=T['panel2'], r=6)
        cv.text((X + cell / 2, ty + 25), v, 26, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 70), j + 1, 18, T['dim'], anchor='mm', mono=True)
    ry = ty + 92
    rh = min(58, (y1 - ry) / len(rows))
    ck, cx = S.get('k'), S.get('x')
    for k, t in enumerate(rows):
        Y = ry + k * rh
        mine = ck == k and cx is not None
        cv.text((x0 + 10, Y + (rh - 6) / 2), f'f[{k}]', 24, T['yellow'] if mine else T['muted'], anchor='lm', bold=True, mono=True)
        for p in range(1, len(t)):
            X = sx + (p - 1) * cell
            changed = old is not None and k < len(old) and len(old[k]) == len(t) and old[k][p] != t[p]
            hot = mine and cx == p
            cv.rect((X + 3, Y, X + cell - 3, Y + rh - 6), fill=T['yellow'] if hot else T['panel2'],
                    outline=T['blue'] if changed else T['border'], width=3 if changed else 1, r=5)
            cv.text((X + cell / 2, Y + (rh - 6) / 2), t[p], 22, T['bg'] if hot else (T['text'] if t[p] else T['dim']), anchor='mm', bold=True)


def _info(S):
    q = S.get('q')
    if q is None:
        return ''
    if q[0] == 1:
        return f"查询 `[1,{q[1]},{q[2]},{q[3]}]`：下标 {q[1]}~{q[2]} 里深度 = {q[3]} 的有几个？"
    return f"查询 `[2,{q[1]},{q[2]}]`：把 `nums[{q[1]}]` 改成 {q[2]}"


CONFIG = dict(
    num=3624, title='位计数深度为 K 的整数数目 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='6 个树状数组 + 先替换成深度',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2086'],
    code='''
class Solution(object):
    def popcountDepth(self, nums, queries):
        
        n = len(nums)
        f = [[0] * (n + 1) for _ in range(6)]
        
        def add(k, x, delta):
            while x <= n:
                f[k][x] += delta
                x += x & -x

        def get(k, x):
            cnt = 0
            while x > 0:
                cnt += f[k][x]
                x -= x & -x
            return cnt

        for index, v in enumerate(nums):
            step = 0
            while v > 1:
                step += 1
                cnt = 0
                while v:
                    if v % 2 == 1:
                        cnt += 1
                    v //= 2
                v = cnt
            nums[index] = step
            add(step, index + 1, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                res.append(get(q[3], q[2] + 1) - get(q[3], q[1]))
            else:
                add(nums[q[1]], q[1] + 1, -1)
                step = 0
                v = q[2]
                while v > 1:
                    step += 1
                    cnt = 0
                    while v:
                        if v % 2 == 1:
                            cnt += 1
                        v //= 2
                    v = cnt
                add(step, q[1] + 1, 1)
                nums[q[1]] = step
        
        return res
''',
    call='Solution().popcountDepth([2, 4], [[1, 0, 1, 1], [2, 1, 1], [1, 0, 1, 0]])',
    expect=[2, 1],
    max_steps=66,
    skip=['f = [[0]', 'n = len(nums)', 'step = 0', 'cnt = 0', 'step += 1', 'while v:', 'if v % 2 == 1', 'cnt += 1', 'v //= 2', 'res = []', 'while x <= n', 'while x > 0'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='res', label='res', cell=64, h=110),
    ],
    watch=[('v', 'v', 'pink'), ('step', 'step', 'yellow'), ('cnt', 'cnt', 'green'), ('k', 'k', 'blue'), ('x', 'x', 'blue')],
    captions={
        'for index, v in enumerate(nums)': lambda S, B, r: ('每个数都换成深度、记进树里了' if ('index' in B and B['index'] == S.index) else
                                                           f'处理 `nums[{S.index}]` = `{S.v}`：先算它的位计数深度（只关心深度）'),
        'while v > 1': lambda S, B, r: (f'`v = {S.v}` > 1：还没到 1，继续取二进制里 1 的个数' if S.v > 1 else f'`v = {S.v}`：到 1 了，深度 `step = {S.step}`'),
        'v = cnt': '`v` 的二进制里有 `{cnt}` 个 1 → `v = {cnt}`，深度 +1（`step = {step}`）',
        'nums[index] = step': '`nums[{index}]` 原地换成它的深度 `{step}`，以后只关心深度',
        'add(step, index + 1, 1)': '深度是 `{step}` → 在树 `f[{step}]` 的位置 `{index + 1}` 加 1（下标 +1）',
        'f[k][x] += delta': '`f[{k}][{x}]` 管 [{x - (x & -x) + 1}, {x}]，加 `{delta}` → =={f[k][x]}==',
        'x += x & -x': '`x += lowbit` → `{x}`：下一个包含该位置的区间',
        'cnt += f[k][x]': '`f[{k}][{x}]` 管 [{x - (x & -x) + 1}, {x}]，整段加进 `cnt` → =={cnt}==',
        'x -= x & -x': '去掉最低位的 1：`{B.x}` → `{x}`',
        'return cnt': '前缀 [1, ·] 里深度 {k} 的个数 = `{ret}`',
        'for q in queries': lambda S, B, r: ('所有查询处理完了' if ('q' in B and B['q'] == S.q and B['q'] is not None and S.q == B['q'] and S.q[0] == 1 and len(S.res) == 2) else f'处理查询 `q = {S.q}`'),
        'res.append(get(q[3], q[2] + 1)': '深度 `{q[3]}`：前缀 [1, {q[2] + 1}] − 前缀 [1, {q[1]}]（下标 +1，所以右端 +1、左端不加）',
        'add(nums[q[1]], q[1] + 1, -1)': '修改下标 `{q[1]}`：先从旧深度 `{nums[q[1]]}` 的树里==移除==这个位置（−1）',
        'v = q[2]': '新值 `{q[2]}`，重新算深度',
        'add(step, q[1] + 1, 1)': '新深度 `{step}`：在树 `f[{step}]` 的位置 `{q[1] + 1}` 加 1',
        'nums[q[1]] = step': '`nums[{q[1]}]` 也换成新深度 `{step}`',
        'return res': '所有「计算」查询的答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='先把每个数换成深度，再按深度 0~5 各开一个树状数组',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['位计数深度：反复取二进制 1 的个数直到 1 的步数，如 `7(111) → 3 → 2 → 1` 是 3',
                 '`[1,l,r,k]` 数区间里深度恰为 `k` 的个数；`[2,idx,val]` 改一个数',
                 '示例：`nums=[2,4]`，`[[1,0,1,1],[2,1,1],[1,0,1,0]]` → `[2,1]`'],
        quote='可以对k从0到5这6种情况，每种情况都使用单独的数据结构来进行处理。又由于题目中还存在修改操作，那么结合起前缀运算，在这里使用6个树状数组来进行处理是比较合适的。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间 `[l, r]` 的个数 = 前缀 `[0, r]` − 前缀 `[0, l-1]`',
              '`k ≤ 5`：深度 0~5 各一个树状数组，位置上记 0/1',
              '先遍历一遍：把 `nums` 里的数换成深度，并在对应的树里加 1',
              '修改：先从旧深度的树里移除，再算新深度，加到新树里'],
        summary=['时间 `O((n + q) log n)`，空间 `O(n)`；深度计算每次最多几轮',
                 '易错：树状数组下标从 1 开始，查询用 `get(r + 1) − get(l)`',
                 '修改要==先移除旧的再加新的==，旧深度从 `nums` 里读，所以 `nums` 要同步改成新深度',
                 '对比灵神：灵神预处理 `≤ 50` 的深度表并用 `bit_count`；这里手写循环数 1 的个数'],
    ),
)
