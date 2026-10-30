def _box(cv, X, Y, w, h, fill, txt, T, size=30, tc=None, outline=None):
    if fill is not None:
        cv.rect((X, Y, X + w, Y + h), fill=fill, r=8, alpha=210)
    if outline is not None:
        cv.rect((X, Y, X + w, Y + h), outline=outline, width=4, r=8)
    cv.text((X + w / 2, Y + h / 2), txt, size, tc or T['text'], anchor='mm', bold=True)


def _show(S, name):
    if name == 'j':
        return 'j' in S
    g = S.get('f')
    d = S.get('delta')
    return g is not None and len(g) > 0 and d is not None and d < g[-1] and S.get('_line', 0) >= 16


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    W = x1 - x0 - 40
    cand = S.get('envelopes') or S.get('a') or S.get('candidate')
    g = S.get('g') if S.get('g') is not None else S.get('f')
    cur = None
    if cand is not None and S.get('_') is not None:
        d = S.get('h') if S.get('h') is not None else S.get('delta')
        if (S['_'], d) in cand:
            cur = cand.index((S['_'], d))
    # row 1: nums
    cv.text((x0 + 18, y0 + 4), 'nums：值 x 必须 ≤ 下标 i 才可能成为固定点（绿 = 候选，灰 = 不可能）', 22, T['muted'], bold=True)
    cell = min(100, W / n)
    sx = x0 + 20 + (W - cell * n) / 2
    for i, x in enumerate(nums):
        ok = x <= i
        X = sx + i * cell
        _box(cv, X + 3, y0 + 40, cell - 6, 56, T['green'] if ok else (70, 76, 86), x, T, 30, T['bg'] if ok else T['muted'])
        cv.text((X + cell / 2, y0 + 100), f'i={i}', 18, T['dim'], anchor='mt', mono=True)
        if ok:
            cv.text((X + cell / 2, y0 + 124), f'i-x={i - x}', 19, T['cyan'], anchor='mt', bold=True)
    # row 2: candidate pairs
    y2 = y0 + 205
    if cand is not None:
        sorted_now = cand != [(x, i - x) for i, x in enumerate(nums) if x <= i]
        cv.text((x0 + 18, y2 - 34), ('二元组 (x, i-x)：已按 x 升序、i-x 降序排好' if sorted_now else '二元组 (x, i-x)：收集候选'), 22, T['muted'], bold=True)
        m = len(cand)
        c2 = min(120, W / max(m, 1))
        s2 = x0 + 20 + (W - c2 * m) / 2
        for k, (x, d) in enumerate(cand):
            col = None
            fill = (60, 66, 78)
            if cur is not None:
                if k == cur:
                    fill = T['yellow']
                elif k < cur:
                    fill = (90, 98, 112)
            _box(cv, s2 + k * c2 + 3, y2, c2 - 6, 56, fill, f'({x},{d})', T, 24, T['bg'] if cur == k else T['text'])
    # row 3: g
    y3 = y2 + 140
    if g is not None:
        cv.text((x0 + 18, y3 - 34), '末尾表：i-x 的最长非降子序列（第 k 格 = 长度 k+1 的最小结尾）', 22, T['muted'], bold=True)
        gc = 110
        gs = x0 + 20
        for k, v in enumerate(g):
            _box(cv, gs + k * gc + 3, y3, gc - 6, 56, T['green'], v, T, 30, T['bg'])
            cv.text((gs + k * gc + gc / 2, y3 + 60), k, 18, T['dim'], anchor='mt', mono=True)
        for name, c in (('j', T['pink']), ('left', T['blue']), ('right', T['pink']), ('mid', T['yellow'])):
            p = S.get(name)
            if isinstance(p, int) and cur is not None and 0 <= p <= len(g) and _show(S, name):
                X = gs + p * gc + gc / 2
                cv.tri_up(X, y3 + 88, 9, c)
                cv.text((X, y3 + 100), name, 20, c, anchor='mt', bold=True)


CONFIG = dict(
    num=3920, title='删除元素后最大固定点数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='候选二元组 · 排序后 LNDS（手写二分）',
    tags=['灵神题单·动态规划', '难度分 2264'],
    code='''
class Solution(object):
    def maxFixedPoints(self, nums):
        
        candidate = []
        for index, v in enumerate(nums):
            if v <= index:
                candidate.append((v, index - v))

        candidate.sort(key=lambda d:(d[0], -d[1]))

        f = []
        for _, delta in candidate:
            if not f or delta >= f[-1]:
                f.append(delta)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) // 2
                    if f[mid] <= delta:
                        left = mid + 1
                    else:
                        right = mid

                f[left] = delta

        return len(f)
''',
    call='Solution().maxFixedPoints([1,0,1,2,2,1,4,3])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=[('delta', 'delta', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('f', 'f', 'green')],
    captions={
        'candidate = []': '`candidate` 存候选二元组 `(v, delta)`',
        'if v <= index': lambda S, B, r: (f'`v = {S.v}`，`index = {S.index}`：' + ('`v <= index` ==可能成为固定点==' if S.v <= S.index else '`v > index`，往左移也到不了 `v` → ==不可能==')),
        'candidate.append': '`delta = {index} − {v}` = `{index - v}`：要删掉它左边 `{index - v}` 个元素',
        'candidate.sort': '按 `v` 升序、`delta` ==降序==排：这样只要 `delta` 不减，`v` 就一定递增',
        'f = []': '`f`：`delta` 的最长不减子序列（`f[k]` = 长度 `k+1` 的最小结尾）',
        'for _, delta in candidate': lambda S, B, r: (f'取下一个候选，`delta = {S.delta}`' if (S.get('_'), S.get('delta')) != (B.get('_'), B.get('delta')) else '候选都处理完了'),
        'if not f or delta >= f[-1]': lambda S, B, r: ('`f` 为空：直接放入' if not S.f else
            (f'`{S.delta} >= f[-1] = {S.f[-1]}`：不比末尾小 → ==直接接在后面==' if S.delta >= S.f[-1]
             else f'`{S.delta} < f[-1] = {S.f[-1]}`：接不到末尾 → 二分找 `f` 里第一个 ==大于== `{S.delta}` 的位置')),
        'f.append(delta)': '`f` 变长：`{f}`',
        'left = 0': '二分区间 `[left, right]` = `[0, {len(f) - 1}]`',
        'right = len(f) - 1': '右端取 `len(f) - 1` = `{right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续缩小' if S.left < S.right else f'`left = right = {S.left}`：找到位置'),
        'mid = (left + right)': '`mid = ({left} + {right}) // 2` = `{mid}`',
        'if f[mid] <= delta': lambda S, B, r: (f'`f[{S.mid}] = {S.f[S.mid]} <= {S.delta}`：这个数还能让 delta 接在后面 → 答案在右边' if S.f[S.mid] <= S.delta
                                               else f'`f[{S.mid}] = {S.f[S.mid]} > {S.delta}`：这个数太大 → 答案在 `mid` 或左边'),
        'left = mid + 1': '`left` → `{left}`',
        'right = mid': '`right` → `{right}`',
        'f[left] = delta': '把 `f[{left}]` 换成更小的 `{delta}`：长度不变，结尾更小，`f = {f}`',
        'return len(f)': '`len(f) = {ret}`：最多 `{ret}` 个固定点',
    },
    skip=['right = len(f) - 1'],
    max_steps=110,
    cards=dict(
        one_liner='只有 v ≤ index 才可能成固定点：变成二维偏序里的最长链',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums[index] = index` 称为固定点；可任意删除元素，删后左移',
                 '求能得到的最大固定点数',
                 '本视频：`[1,0,1,2,2,1,4,3]` → `4`'],
        quote='靠前的元素如果移除掉了太多的前缀元素，那么后续的元素就已经被移动到目标位置左侧，移动不回来了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`delta = index − v` 是让 `v` 到位要删掉的前缀个数，选出的元素 `delta` 必须==不减==',
              '先按 `v` 升序、`delta` 降序排序，再对 `delta` 求最长不减子序列',
              '手写二分：`f[mid] <= delta` 则 `left = mid + 1`，找第一个大于 `delta` 的位置'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`delta` 相等也允许，所以比较用 `>=` 和 `<=`',
                 '同一个 `v` 按 `delta` 降序排，防止重复选同一个值',
                 '对比灵神：灵神用 `bisect_right` 并点明这是 354 题；yiduobo 直接手写二分'],
    ),
)
