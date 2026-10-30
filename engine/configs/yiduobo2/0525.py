NUMS = [0, 1, 1, 0, 1, 1, 1, 0]


def _prefix(nums):
    out, s = [0], 0
    for x in nums:
        s += -1 if x else 1
        out.append(s)
    return out  # out[k + 1] = 下标 k 处的前缀和；out[0] 对应下标 -1


def _done(S, B):
    """当前已经算出 diff 的最后一个下标（-1 表示只有初始的 0）"""
    if 'index' not in S:
        return None
    if S.get('_line') == 8 or (S.get('_line') == 7 and B.get('index') != S['index']):
        return S['index'] - 1
    return S['index']


def _p(v):
    return f'({v})' if v < 0 else str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    pre = _prefix(nums)
    pos = S.get('prefix_dict') or {}
    done = _done(S, B)
    if done is None:
        done = -1 if 'prefix_dict' in S else -2
    ncol = n + 1
    cw = min(92, (x1 - x0 - 120) / ncol)
    sx = x0 + 90 + ((x1 - x0 - 120) - cw * ncol) / 2

    def X(k):  # 列中心，k = -1..n-1
        return sx + (k + 1) * cw + cw / 2

    cv.text((x0 + 18, y0 + 4), 'nums 与 diff（0 的个数 − 1 的个数）折线（紫点 = 首次出现，记在 prefix_dict）', 22, T['muted'], bold=True)
    ct, ch = y0 + 66, min(cw * 0.86, 60)
    win = None
    s = S.get('now')
    if done >= 0 and s in pos and pos[s] < done and done == S.get('index'):
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
            fill = T['panel2'] if k > done else ((90, 55, 70) if v else (50, 70, 100))
            cv.rect((xc - cw / 2 + 3, ct, xc + cw / 2 - 3, ct + ch), fill=fill, outline=T['border'], r=8)
            cv.text((xc, ct + ch / 2 - 8), v, 28, T['text'] if k <= done else T['muted'], anchor='mm', bold=True)
            cv.text((xc, ct + ch - 12), '−1' if v else '+1', 16, T['pink'] if v else T['blue'], anchor='mm', bold=True)
        cv.text((xc, ct + ch + 8), k, 18, T['dim'], anchor='mt', mono=True)
    i = S.get('index')
    if isinstance(i, int):
        cv.tri_down(X(i), ct - 8, 10, T['yellow'])
        cv.text((X(i) + 12, ct - 14), 'index', 22, T['yellow'], anchor='lm', bold=True)
    # 折线
    gt, gb = ct + ch + 44, y1 - 34
    lo, hi = min(pre), max(pre)
    if hi == lo:
        hi = lo + 1

    def Y(v):
        return gb - (v - lo) / (hi - lo) * (gb - gt)

    for v in range(lo, hi + 1):
        cv.dashed((sx, Y(v)), (sx + ncol * cw, Y(v)), T['border'], 1, dash=6, gap=8)
        cv.text((sx - 10, Y(v)), f'{v}', 18, T['muted'], anchor='rm', mono=True)
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
    author='yiduobo', technique='区间转前缀和 · dict 记每种 diff 首次出现的位置',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def findMaxLength(self, nums):
        prefix_dict = {0: -1}
        now = 0
        res = 0

        for index, num in enumerate(nums):
            if num == 0:
                now += 1
            else:
                now -= 1
            if now in prefix_dict:
                res = max(res, index - prefix_dict[now])
            else:
                prefix_dict[now] = index

        return res
''',
    call=f'Solution().findMaxLength({NUMS})',
    expect=4,
    views=[
        dict(type='text', fn=lambda S, B: (
            f"`diff = {S['now']}` 第一次在下标 `{S['prefix_dict'][S['now']]}` → "
            f"`[{S['prefix_dict'][S['now']]} + 1, {S['index']}]` 这段 0、1 数量相等"
            if 'index' in S and _done(S, B) == S['index'] and S['now'] in S['prefix_dict']
            and S['prefix_dict'][S['now']] < S['index']
            else '`l..r` 中 0、1 个数相等 ⇔ `diff[l-1] == diff[r]`'), size=28),
        dict(type='custom', draw=_draw, h=470),
        dict(type='map', var='prefix_dict', label='prefix_dict（diff → 第一次出现的位置）', h=110,
             fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'yellow'), ('num', 'num'), ('now', 'now', 'purple'), ('res', 'res', 'green')],
    captions={
        'prefix_dict = {0: -1}': '`prefix_dict = {{0: -1}}`：什么都没扫时差值为 0，记在==位置 -1==',
        'now = 0': '`now` 就是当前的 `diff[index]`：==0 的个数减去 1 的个数==',
        'res = 0': '`res` 记最长区间长度',
        'for index, num in enumerate': lambda S, B, ret: (
            f'扫描到 `index = {S.index}`，`num = {S.num}`' if S.get('index') != B.get('index') or 'index' not in B
            else '一趟扫描结束'),
        'if num == 0': lambda S, B, ret: (f'`num = 0`：0 多了一个 → 差值 +1' if S.num == 0
                                          else f'`num = 1`：1 多了一个 → 差值 −1'),
        'now += 1': '`now = {now}`',
        'now -= 1': '`now = {now}`',
        'if now in prefix_dict': lambda S, B, ret: (
            f'差值 `{S.now}` ==出现过==（位置 {S.prefix_dict[S.now]}）→ '
            f'`{S.prefix_dict[S.now] + 1}` 到 `{S.index}` 这段 0、1 数量相等'
            if S.now in S.prefix_dict else f'差值 `{S.now}` 没出现过'),
        'res = max': lambda S, B, ret: (f'区间长度 `{S.index} − {_p(S.prefix_dict[S.now])} = '
                                        f'{S.index - S.prefix_dict[S.now]}`，`res = max({B.res}, '
                                        f'{S.index - S.prefix_dict[S.now]}) = {S.res}`'),
        'prefix_dict[now] = index': lambda S, B, ret: (
            f'加入 dict：`prefix_dict[{S.now}] = {S.index}`，==只存第一次出现的位置==，后面的区间才能最长'
            if len(S.prefix_dict) <= 3 else f'`prefix_dict[{S.now}] = {S.index}`'),
        'return res': '最长区间长度 =={res}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='0、1 个数相等的区间 ⇔ 两个前缀的「0 个数 − 1 个数」相等',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制数组 `nums`，找含有==相同数量的 0 和 1== 的最长连续子数组，返回其长度',
                 '示例：`[0,1,1,1,1,1,0,0,0]` → `6`',
                 f'本视频：`{NUMS}` → `4`（`[0,1,1,0]`）'],
        quote='要求l到r这一段中0和1的个数相等，可以看做==0到l - 1这一段中0和1个数的差值等于0到r这一段中0和1个数的差值==，于是就可以使用类似前缀和的做法求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`diff[index]` = `nums[0..index]` 中 ==0 的个数减去 1 的个数==',
              '用 dict 保存每种 diff ==第一次出现==的位置',
              '再次遇到同一个 diff：`dict[diff] + 1` 到 `index` 这一段 0、1 数量相等'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`{0: -1}` 是关键：让从下标 0 开始的区间也能被统计',
                 '已出现过的 diff ==不要覆盖==，否则区间变短',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神把 0 看成 −1 求「1 − 0」，这里求「0 − 1」，本质相同'],
    ),
)
