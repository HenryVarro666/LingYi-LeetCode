def _range(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    hi = max(S['ribbons'])
    n = hi + 1
    cv.text((x0 + 18, y0 + 4), '答案候选长度 0..max（蓝 left，粉 right，黄 mid）', 22, T['muted'], bold=True)
    cell = min(90, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 80
    live = 'left' in S and 'right' in S
    mid = S.get('mid') if live else None
    for v in range(n):
        X = sx + v * cell
        inside = live and S['left'] <= v <= S['right']
        fill = T['panel2'] if not inside else (52, 60, 72)
        if live and v == S['left'] and S['left'] == S['right']:
            fill = T['green']
        cv.rect((X + 3, ys, X + cell - 3, ys + cell * 0.8), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + cell * 0.4), v, 26, T['text'] if inside else T['dim'], anchor='mm', bold=True)
    if not live:
        return
    if mid is not None and 0 <= mid < n and S.get('_line', 0) >= 8:
        X = sx + mid * cell
        cv.rect((X + 1, ys - 4, X + cell - 1, ys + cell * 0.8 + 4), outline=T['yellow'], width=5, r=10)
        cv.text((X + cell / 2, ys - 10), 'mid', 22, T['yellow'], anchor='mb', bold=True)
    for name, idx, c, dy in (('left', S['left'], T['blue'], 0), ('right', S['right'], T['pink'], 26)):
        if 0 <= idx < n:
            X = sx + idx * cell + cell / 2
            yy = ys + cell * 0.8 + 14
            cv.tri_up(X, yy, 10, c)
            cv.text((X, yy + 16 + dy * (1 if S['left'] == S['right'] else 0)), name, 22, c, anchor='mt', bold=True)


def _cnt_text(S):
    if 'mid' not in S or 'cnt' not in S:
        return ''
    parts = '+'.join(str(r // S['mid']) for r in S['ribbons'])
    return f"每根剪成长 `{S['mid']}` 的段：`{parts}` = =={sum(r // S['mid'] for r in S['ribbons'])}== 段（已累计 `{S['cnt']}`），要求 `≥ {S['k']}`"


CONFIG = dict(
    num=1891, title='割绳子', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 · 最大长度',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def maxLength(self, ribbons, k):

        left = 0
        right = max(ribbons)
        while left < right:
            mid = (left + right + 1) // 2
            cnt = 0
            for r in ribbons:
                cnt += r // mid
            
            if cnt >= k:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maxLength([9,7,5], 3)',
    expect=5,
    views=[
        dict(type='text', fn=_cnt_text, size=26),
        dict(type='custom', draw=_range, h=230),
        dict(type='array', var='ribbons', label='ribbons（绳子长度）', cell=110, h=200,
             color=lambda S, i, v: ('green' if 'mid' in S and v // S['mid'] > 0 else None) if 'mid' in S else None,
             dim=lambda S, i, v: 'mid' in S and v // S['mid'] == 0),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'cnt', ('k', 'k', 'orange')],
    captions={
        'left = 0': '答案至少是 `0`（切不出）：`left = 0`',
        'right = max': '答案不会超过最长的绳子：`right = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，答案还在区间里 → 继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：区间收缩到一个数 → 结束'),
        'mid = (left': '取 mid：`({left} + {right} + 1) // 2 = {mid}`。==要 +1 向上取整==，否则 `left = mid` 会死循环',
        'cnt = 0': '开始数：每根绳子能剪出几段长 `{mid}` 的',
        'cnt += r': '`{r}` 能剪 `{r} // {mid} = {r // mid}` 段 → `cnt = {cnt}`',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}`：长度 `{S.mid}` 够分 → 成立' if S.cnt >= S.k
                                        else f'`cnt = {S.cnt} < k = {S.k}`：长度 `{S.mid}` 太长，不够分'),
        'left = mid': '`{mid}` 可行，可能还能更长：`left = {left}`（保留 mid 本身）',
        'right = mid - 1': '`{B.mid}` 不可行，更长的更不行：`right = {right}`（mid 已排除）',
        'return left': '区间收缩为 `{left}`：能剪出 `k` 段的最大长度',
    },
    cards=dict(
        one_liner='二分「每段的长度」：长度越长，能剪的段数越少',
        complexity='时间 `O(n log M)`，空间 `O(1)`，M 为最长绳子',
        problem=['给若干条绳子 `ribbons[i]` 和整数 `k`，把绳子剪成长度相同的整数长度的段',
                 '要求至少剪出 `k` 段，求这个==相同长度的最大值==；剪不出返回 `0`',
                 '示例：`ribbons = [9,7,5], k = 3` → `5`'],
        quote='又是这个经典的题型，与之前2226题完全相同，直接套用之前2226题相同的处理方法就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举段长 `mid`，每根绳子能剪 `r // mid` 段，加起来和 `k` 比',
              '段长越大段数越少：==单调==，所以能二分',
              '求最大可行长度：可行就 `left = mid`，不可行就 `right = mid - 1`'],
        summary=['时间 `O(n log M)`，空间 `O(1)`',
                 '`mid = (left + right + 1) // 2`：向上取整，配合 `left = mid` 避免死循环',
                 '`left` 从 `0` 开始：剪不出就返回 `0`，也不会出现除以 0（mid 至少为 1）',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`（共 2 处）',
                 '同类题：2226 每个小孩最多能分到多少糖果'],
    ),
)
