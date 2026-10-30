NUMS = [0, 1, 1, 1, 1, 1, 0, 0, 0]


def _prefix(nums):
    out, s = [0], 0
    for x in nums:
        s += 1 if x else -1
        out.append(s)
    return out  # out[k + 1] = 下标 k 处的前缀和；out[0] 对应下标 -1


def _done(S, B):
    """当前已经算出前缀和的最后一个下标（-1 表示只有初始的 0）"""
    if 'i' not in S:
        return None
    if S.get('_line') == 6 and B.get('i') != S['i']:
        return S['i'] - 1
    return S['i']


def _p(v):
    return f'({v})' if v < 0 else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    pre = _prefix(nums)
    pos = S.get('pos') or {}
    done = _done(S, B)
    if done is None:
        done = -1 if 'pos' in S else -2
    ncol = n + 1
    cw = min(92, (x1 - x0 - 120) / ncol)
    sx = x0 + 90 + ((x1 - x0 - 120) - cw * ncol) / 2

    def X(k):  # 列中心，k = -1..n-1
        return sx + (k + 1) * cw + cw / 2

    cv.text((x0 + 18, y0 + 4), 'nums（0 看成 −1）与前缀和 s 的折线（紫点 = 该值首次出现，记在 pos 里）', 22, T['muted'], bold=True)
    ct, ch = y0 + 66, min(cw * 0.86, 60)
    win = None
    s = S.get('s')
    if done >= 0 and s in pos and pos[s] < done and done == S.get('i'):
        win = (pos[s] + 1, done)
    if win:
        cv.rect((X(win[0]) - cw / 2 - 2, ct - 6, X(win[1]) + cw / 2 + 2, ct + ch + 6), fill=T['cyan'], alpha=40, r=10)
        cv.rect((X(win[0]) - cw / 2 - 2, ct - 6, X(win[1]) + cw / 2 + 2, ct + ch + 6), outline=T['cyan'], width=3, r=10)
    for k in range(-1, n):
        xc = X(k)
        if k == -1:
            cv.text((xc, ct + ch / 2), '起点', 20, T['dim'], anchor='mm', bold=True)
        else:
            v = nums[k]
            fill = T['panel2'] if k > done else ((50, 70, 100) if v else (90, 55, 70))
            cv.rect((xc - cw / 2 + 3, ct, xc + cw / 2 - 3, ct + ch), fill=fill, outline=T['border'], r=8)
            cv.text((xc, ct + ch / 2 - 8), v, 28, T['text'] if k <= done else T['muted'], anchor='mm', bold=True)
            cv.text((xc, ct + ch - 12), '+1' if v else '−1', 16, T['blue'] if v else T['pink'], anchor='mm', bold=True)
        cv.text((xc, ct + ch + 8), k, 18, T['dim'], anchor='mt', mono=True)
    i = S.get('i')
    if isinstance(i, int):
        cv.tri_down(X(i), ct - 8, 10, T['yellow'])
        cv.text((X(i) + 12, ct - 14), 'i', 22, T['yellow'], anchor='lm', bold=True)
    # 折线
    gt, gb = ct + ch + 44, y1 - 34
    lo, hi = min(pre), max(pre)
    if hi == lo:
        hi = lo + 1

    def Y(v):
        return gb - (v - lo) / (hi - lo) * (gb - gt)

    for v in range(lo, hi + 1):
        cv.dashed((sx, Y(v)), (sx + ncol * cw, Y(v)), T['border'], 1, dash=6, gap=8)
        cv.text((sx - 10, Y(v)), f's={v}', 18, T['muted'], anchor='rm', mono=True)
    pts = [(X(k), Y(pre[k + 1])) for k in range(-1, done + 1)]
    if len(pts) > 1:
        cv.line(pts, T['muted'], 3)
    if win:
        l = win[0] - 1
        yv = Y(pre[done + 1])
        cv.line([(X(l), yv), (X(done), yv)], T['green'], 5)
        lab = f'长度 {done} − ({l}) = {done - l}' if l < 0 else f'长度 {done} − {l} = {done - l}'
        lw = cv.tlen(lab, 22, bold=True)
        mx = (X(l) + X(done)) / 2
        cv.rect((mx - lw / 2 - 6, yv - 40, mx + lw / 2 + 6, yv - 8), fill=T['panel'], r=6, alpha=230)
        cv.text((mx, yv - 10), lab, 22, T['green'], anchor='mb', bold=True)
    for k in range(-1, done + 1):
        v = pre[k + 1]
        first = pos.get(v) == k
        cur = k == done
        r = 11 if cur else 8
        c = T['yellow'] if cur else (T['purple'] if first else (110, 118, 130))
        cv.rect((X(k) - r, Y(v) - r, X(k) + r, Y(v) + r), fill=c, r=r)
        if cur or first:
            cv.text((X(k), Y(v) + 14), v, 18, c, anchor='mt', bold=True)


CONFIG = dict(
    num=525, title='连续数组', difficulty='Medium', category='子串',
    author='灵茶山艾府', technique='式子变形 + 枚举右维护左',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        # 前缀和数组的首项 0 相当于在 -1 下标
        pos = {0: -1}
        ans = s = 0
        for i, x in enumerate(nums):
            s += 1 if x else -1
            if s in pos:
                ans = max(ans, i - pos[s])
            else:
                pos[s] = i
        return ans
''',
    call=f'Solution().findMaxLength({NUMS})',
    expect=6,
    views=[
        dict(type='text', fn=lambda S, B: (
            f"`s = {S['s']}` 在下标 `{S['pos'][S['s']]}` 首次出现 → 子数组 `[{S['pos'][S['s']] + 1}, {S['i']}]` 中 0、1 一样多"
            if 'i' in S and _done(S, B) == S['i'] and S['s'] in S['pos'] and S['pos'][S['s']] < S['i']
            else '目标：前缀和数组 `sum` 中==一对相等元素的最远距离=='), size=28),
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='pos', label='pos（前缀和 → 首次出现的下标）', h=110, fmt=lambda k, v: f's={k}: {v}'),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x'), ('s', 's', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'pos = {0: -1}': '`pos = {{0: -1}}`：空前缀的和是 0，==相当于在下标 -1==，这样从开头开始的子数组也能算到',
        'ans = s = 0': '`s` 是前缀和（1 记 +1，0 记 −1），`ans` 记最长长度',
        'for i, x in enumerate': lambda S, B, ret: (f'枚举右端点 `i = {S.i}`，`x = {S.x}`' if S.get('i') != B.get('i') or 'i' not in B
                                                    else '遍历结束'),
        's += 1 if x else -1': lambda S, B, ret: (f'`x = {S.x}` → `s` {"+1" if S.x else "−1"}，前缀和 `s = {S.s}`'),
        'if s in pos': lambda S, B, ret: (
            f'`s = {S.s}` ==以前出现过==（下标 {S.pos[S.s]}）：`sum[{S.i + 1}] = sum[{S.pos[S.s] + 1}]`，中间这段和为 0'
            if S.s in S.pos else f'`s = {S.s}` 第一次出现 → 记下它的下标'),
        'ans = max': lambda S, B, ret: (f'长度 `i − pos[s] = {S.i} − {_p(S.pos[S.s])} = {S.i - S.pos[S.s]}`，'
                                        f'`ans = max({B.ans}, {S.i - S.pos[S.s]}) = {S.ans}`'),
        'pos[s] = i': lambda S, B, ret: (f'维护左：`pos[{S.s}] = {S.i}`，==只记首次出现==，以后再遇到 `{S.s}` 时距离最远'
                                         if len(S.pos) <= 3 else f'`pos[{S.s}] = {S.i}`'),
        'return ans': '最长的 0、1 个数相等的子数组长度：=={ans}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='把 0 看成 −1，计算和为 0 的最长子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制数组 `nums`，找含有==相同数量的 0 和 1== 的最长连续子数组，返回其长度',
                 '示例：`[0,1,0]` → `2`',
                 f'本视频：`{NUMS}` → `6`（`[1,1,1,0,0,0]`）'],
        quote='子数组 `[l,r)` 中 1 和 0 的出现次数相等，即 `S1[r] − S1[l] = S0[r] − S0[l]`，移项得 `S1[r] − S0[r] = S1[l] − S0[l]`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `sum[i] = S1[i] − S0[i]`：问题变成==一对相等元素的最远距离==',
              '枚举右，维护左：哈希表记每个前缀和==首次出现==的下标',
              '`sum` 的首项 0 放在下标 `-1`，合并两个循环后只需一个变量 `s`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`pos = {0: -1}` 不能漏：否则从下标 0 开始的子数组算不到',
                 '只在==第一次==出现时记录下标，重复出现不覆盖（要最远距离）',
                 '子数组 `[l,r)` 长度是 `r − l`，无需加一',
                 '优化前写法：先算 `accumulate` 前缀和数组，再枚举；同类题：560 和为 K 的子数组'],
    ),
)
