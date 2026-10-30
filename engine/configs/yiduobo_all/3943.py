def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cnt = S.get('cnt')
    if not cnt:
        cv.text((x0 + 18, y0 + 4), 'nums2 还没分块', 24, T['muted'], bold=True)
        return
    nums2, b = S['nums2'], S['b']
    delta = S['delta']
    K = len(cnt)
    cv.text((x0 + 18, y0 + 4), '每块：cnt[p]（块内旧值计数）+ delta[p]（整块未下放的增量）；格子 = 存储值 + delta', 21, T['muted'], bold=True)
    gap = 24
    bw = (x1 - x0 - 40 - gap * (K - 1)) / K
    n = len(nums2)
    lo, hi = S.get('x'), S.get('y')
    isup = isinstance(S.get('q'), list) and S['q'][0] == 1 and lo is not None
    for p in range(K):
        X0 = x0 + 20 + p * (bw + gap)
        cv.rect((X0, y0 + 50, X0 + bw, y1 - 10), fill=T['panel2'], outline=T['border'], r=14)
        cv.text((X0 + 14, y0 + 62), f'块 {p}  [{p * b}, {min(n, (p + 1) * b) - 1}]', 24, T['text'], bold=True)
        cv.text((X0 + bw - 14, y0 + 62), f'delta = {delta[p]}', 26, T['orange'] if delta[p] else T['dim'], anchor='ra', bold=True)
        w = min(n, (p + 1) * b) - p * b
        cell = min(78, (bw - 28) / w)
        sx = X0 + (bw - cell * w) / 2
        ys = y0 + 130
        for j in range(p * b, p * b + w):
            X = sx + (j - p * b) * cell
            hit = isup and lo <= j <= hi
            cv.rect((X + 3, ys, X + cell - 3, ys + cell * 0.85), fill=T['blue'] if hit else (60, 68, 80), r=8)
            cv.text((X + cell / 2, ys + cell * 0.42), nums2[j] + delta[p], 28, T['bg'] if hit else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, ys + cell * 0.85 + 6), j, 17, T['dim'], anchor='mt', mono=True)
        cv.text((X0 + 14, ys + cell + 50), 'cnt[p]（存储值: 次数）', 20, T['muted'], bold=True)
        yy = ys + cell + 84
        for v, c in sorted(cnt[p].items()):
            if c == 0:
                continue
            cv.text((X0 + 18, yy), f'{v}: {c}', 24, T['cyan'], mono=True, bold=True)
            yy += 32


def _qtxt(S):
    if 'res' not in S:
        return ''
    q = S.get('q')
    if not q:
        return ''
    if q[0] == 1:
        return f'修改 `{q}`：下标 {q[1]}..{q[2]} 全部 ==+{q[3]}==，每块 {S["b"]} 个'
    return f'查询 `{q}`：数 nums1[p] + nums2[q] == =={q[1]}== 的对数；答案 `{S["res"]}`'


CONFIG = dict(
    num=3943, title='递增后的数对数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='分块 · 整块 delta',
    tags=['灵神题单·常用数据结构', '难度分 2410'],
    code='''
class Solution(object):
    def numberOfPairs(self, nums1, nums2, queries):
        
        m = len(nums2)

        b = int(m ** 0.5) + 1

        cnt = []
        delta = []
        for start in range(0, m, b):
            cnt.append({})
            delta.append(0)
            for v in nums2[start : start + b]:
                cnt[-1][v] = cnt[-1].get(v, 0) + 1

        res = []
        for q in queries:
            if q[0] == 1:
                x, y, val = q[1:]
                p = 0
                while (p + 1) * b - 1 < x:
                    p += 1
                
                for index in range(x, min(y + 1, (p + 1) * b)):
                    cnt[p][nums2[index]] -= 1
                    nums2[index] += val
                    cnt[p][nums2[index]] = cnt[p].get(nums2[index], 0) + 1
                
                if y <= (p + 1) * b - 1:
                    continue

                p += 1
                while (p + 1) * b - 1 < y:
                    delta[p] += val
                    p += 1
                
                for index in range(p * b, y + 1):
                    cnt[p][nums2[index]] -= 1
                    nums2[index] += val
                    cnt[p][nums2[index]] = cnt[p].get(nums2[index], 0) + 1
            
            else:
                res.append(0)
                for v in nums1:
                    target = q[1] - v
                    for p in range(len(cnt)):
                        res[-1] += cnt[p].get(target - delta[p], 0)

        return res
''',
    call='Solution().numberOfPairs([1, 2], [3, 4, 3, 5, 4, 3, 4, 5], [[2, 6], [1, 1, 7, 1], [2, 5]])',
    expect=[5, 3],
    views=[
        dict(type='text', fn=_qtxt),
        dict(type='array', var='nums1', label='nums1（n ≤ 5，很短）', h=120, cell=70),
        dict(type='custom', draw=_draw, h=430),
    ],
    watch=['b', ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'm = len(nums2)': '`nums2` 长度 `m = {m}`，长度固定不变 → 适合分块',
        'b = int': '块长 `b = ceil(√m)` 取 `int({m} ** 0.5) + 1 = =={b}==`，块数 `k ≤ b`',
        'cnt.append': '新开一块：`cnt[{len(cnt) - 1}]` 记块内计数，`delta` 记整块增量，初始 0',
        'x, y, val = q[1:]': '修改：下标 `{x}..{y}` 全部加 `{val}`',
        'while (p + 1) * b - 1 < x': lambda S, B, r: (f'块 `{S.p}` 的右端 `{(S.p + 1) * S.b - 1}` 还在 `x = {S.x}` 左边 → 往后找' if (S.p + 1) * S.b - 1 < S.x
                                                       else f'块 `{S.p}` 的右端 `{(S.p + 1) * S.b - 1} ≥ x = {S.x}`：==块 {S.p} 含 x=='),
        'p += 1': lambda S, B, r: f'`p` → {S.p}',
        'for index in range(x,': '头部残块：暴力改下标 `{x}..{min(y, (p + 1) * b - 1)}`，只在块 {p} 内',
        'cnt[p][nums2[index]] -= 1': '撤销旧值 `{nums2[index]}` 的计数',
        'nums2[index] += val': '`nums2[{index}]` 加 `{val}` → {nums2[index]}',
        'cnt[p][nums2[index]] = ': '登记新值 `{nums2[index]}`，块 {p} 里 `cnt = {cnt[p][nums2[index]]}`',
        'if y <= (p + 1) * b - 1': lambda S, B, r: (f'`y = {S.y}` 也在块 {S.p} 内 → 改完了，处理下一个询问' if S.y <= (S.p + 1) * S.b - 1
                                                     else f'`y = {S.y}` 超出块 {S.p} 的右端 `{(S.p + 1) * S.b - 1}` → 还要往后推进'),
        'while (p + 1) * b - 1 < y': lambda S, B, r: (f'块 {S.p} 右端 `{(S.p + 1) * S.b - 1} < y = {S.y}`：整块被覆盖' if (S.p + 1) * S.b - 1 < S.y
                                                       else f'块 {S.p} 右端 `{(S.p + 1) * S.b - 1} ≥ y = {S.y}`：y 在这块里，停'),
        'delta[p] += val': '整块不动元素，只记 `delta[{p}] += {val}` → =={delta[p]}==',
        'for index in range(p * b, y + 1)': '尾部残块：暴力改下标 `{p * b}..{y}`',
        'res.append(0)': '查询：`nums1[p] + nums2[q] == {q[1]}`，给本次答案占位 0',
        'target = q[1] - v': '`nums1` 里取 `v = {v}`，需要 `nums2` 里恰好有 `target = {q[1]} - {v} = {target}`',
        'res[-1] +=': '块 {p}：消去 delta → 查 `cnt[{p}][{target} - {delta[p]}]` = `{cnt[p].get(target - delta[p], 0)}` 个 → 本次答案 `{res[-1]}`',
        'return res': '全部询问处理完，返回 `{res}`',
    },
    skip=['m = len(nums2)', 'p = 0', 'for p in range(len(cnt))', 'continue', 'for v in nums2[start', 'cnt[-1][v] =', 'delta.append(0)', 'res = []', 'cnt = []', 'delta = []'],
    max_steps=80,
    cards=dict(
        one_liner='nums2 长度不变 → 分块；整块记 delta，零碎块暴力改',
        complexity='时间 `O(q·√m)`（`nums1` 很短，当常数），空间 `O(m)`',
        problem=['`nums2` 区间加 `val`；查询 `nums1[p] + nums2[q] == tot` 的对数',
                 '`nums1` 长度 ≤ 5，`nums2` 和询问数 ≤ 50000',
                 '示例：`nums1=[1,2]`，`nums2=[3,4,3,5,4,3,4,5]`，答案 `[5, 3]`'],
        quote='题目涉及到区间修改，还需要查询全局状态下，等于某个特定值的元素数量，使用树形结构并不是很好处理。不过好在本题中nums2的长度是不变的，因此在这里可以采用分块的思路进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt[p][v]`：第 p 块里值 v 出现几次；`delta[p]`：整块还没下放的增量',
              '修改：头块暴力 → 中间整块 `delta += val` → 尾块暴力',
              '查询：对每个 `v`，每块查 `cnt[p][tot - v - delta[p]]` 累加'],
        summary=['修改 `O(b + k)`，查询 `O(n·k)`，`k ≤ b ≈ √m`，总 `O(q·√m)`',
                 '易错：头块、尾块和整块要分开处理；`y` 就在头块里时要提前 `continue`',
                 '原文是 Python 2 风格，本题代码不需要改动，直接可在 Python 3 运行',
                 '对比灵神：灵神每块存 `[l, r, cnt, add]` 一次遍历；yiduobo 先定位含 x 的块再往后推'],
    ),
)
