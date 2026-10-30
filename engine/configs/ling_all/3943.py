def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    blocks = S.get('blocks')
    if not blocks:
        cv.text((x0 + 18, y0 + 4), 'nums2 还没分块', 24, T['muted'], bold=True)
        return
    nums2 = S['nums2']
    n = len(nums2)
    cv.text((x0 + 18, y0 + 4), '每块：哈希表 cnt（存旧值）+ 懒标记 add；格子里显示真实值 = 存储值 + add', 22, T['muted'], bold=True)
    K = len(blocks)
    gap = 24
    bw = (x1 - x0 - 40 - gap * (K - 1)) / K
    ql, qr = S.get('l'), S.get('r')
    inq = S.get('_inner', S).get('q', [0])[0] == 1 if isinstance(S.get('q'), list) else False
    cur = S.get('i') if isinstance(S.get('i'), int) and 'bl' in S else None
    for k, (bl, br, cnt, add) in enumerate(blocks):
        X0 = x0 + 20 + k * (bw + gap)
        cv.rect((X0, y0 + 50, X0 + bw, y1 - 10), fill=T['panel2'], outline=T['yellow'] if cur == k else T['border'], width=3 if cur == k else 1, r=14)
        cv.text((X0 + 14, y0 + 62), f'块 {k}  [{bl}, {br})', 24, T['text'], bold=True)
        cv.text((X0 + bw - 14, y0 + 62), f'add = {add}', 26, T['orange'] if add else T['dim'], anchor='ra', bold=True)
        w = br - bl
        cell = min(78, (bw - 28) / w)
        sx = X0 + (bw - cell * w) / 2
        ys = y0 + 130
        for j in range(bl, br):
            X = sx + (j - bl) * cell
            hit = inq and ql is not None and ql <= j < qr
            cv.rect((X + 3, ys, X + cell - 3, ys + cell * 0.85), fill=T['blue'] if hit else (60, 68, 80), r=8)
            cv.text((X + cell / 2, ys + cell * 0.42), nums2[j] + add, 28, T['bg'] if hit else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, ys + cell * 0.85 + 6), j, 17, T['dim'], anchor='mt', mono=True)
        cv.text((X0 + 14, ys + cell + 50), 'cnt（存储值: 次数）', 20, T['muted'], bold=True)
        items = sorted(cnt.items())
        yy = ys + cell + 84
        for t, (v, c) in enumerate(items):
            if c == 0:
                continue
            cv.text((X0 + 18, yy), f'{v}: {c}', 24, T['cyan'], mono=True, bold=True)
            yy += 32


def _qtxt(S):
    if 'ans' not in S:
        return ''
    q = S.get('q')
    if not q:
        return f'已回答 {S["ans"]}'
    if q[0] == 1:
        return f'当前询问 `{q}`：nums2[{q[1]}..{q[2]}] 全部 ==+{q[3]}=='
    return f'当前询问 `{q}`：统计 nums1[j] + nums2[k] == ==tot=={q[1]} 的数对；已答 `{S["ans"]}`'


CONFIG = dict(
    num=3943, title='递增后的数对数量', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分块 + 懒标记',
    tags=['灵神题单·常用数据结构', '难度分 2410'],
    code='''
class Solution:
    def numberOfPairs(self, nums1: list[int], nums2: list[int], queries: list[list[int]]) -> list[int]:
        m, n = len(nums1), len(nums2)
        B = isqrt(m * n)

        # blocks[i] = [l, r, cnt, add]
        # l, r: 这一段对应 nums2 的子数组 [l, r)，注意是左闭右开区间
        # cnt: 这一段每个元素的出现次数
        # add: 这一段整体要增加 add
        blocks = []
        for i in range(0, n, B):
            r = min(i + B, n)
            blocks.append([i, r, Counter(nums2[i: r]), 0])

        ans = []
        for q in queries:
            if q[0] == 1:
                l, r, val = q[1], q[2] + 1, q[3]
                for i, (bl, br, cnt, _) in enumerate(blocks):
                    if br <= l:
                        continue
                    if bl >= r:
                        break
                    # blocks[i] 在 [l, r) 中
                    if l <= bl and br <= r:
                        blocks[i][3] += val
                        continue
                    # blocks[i] 的一部分在 [l, r) 中
                    # 暴力更新 nums2 的子数组的元素值及其出现次数
                    for j in range(max(bl, l), min(br, r)):
                        cnt[nums2[j]] -= 1  # 撤销旧的
                        nums2[j] += val
                        cnt[nums2[j]] += 1  # 添加新的
            else:
                res = 0
                for _, _, cnt, add in blocks:
                    target = q[1] - add
                    for x in nums1:
                        res += cnt.get(target - x, 0)  # 避免把不在 cnt 中的 key 插入哈希表
                ans.append(res)
        return ans
''',
    call='Solution().numberOfPairs([1, 2], [3, 4, 3, 5, 4, 3], [[2, 6], [1, 0, 3, 1], [2, 6]])',
    expect=[3, 4],
    views=[
        dict(type='text', fn=_qtxt),
        dict(type='array', var='nums1', label='nums1（m ≤ 5，很短）', h=120, cell=70),
        dict(type='custom', draw=_draw, h=430),
    ],
    watch=['B', ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'res', ('ans', 'ans', 'green')],
    captions={
        'B = isqrt': lambda S, B, r: f'块大小 `B = isqrt(m·n) = isqrt({S.m}·{S.n}) = =={S.B}==`：更新 `O(B + n/B)`，查询 `O(m·n/B)`，取平衡点',
        'blocks.append': '第 {len(blocks)} 块 `[{i}, {r})`：用 Counter 记下块内每个值出现几次，`add = 0`',
        'l, r, val = q': '类型 1：区间 `[{l}, {r})` 里每个数加 `{val}`',
        'if br <= l': lambda S, B, r: (f'块 `[{S.bl}, {S.br})` 整个在 `l = {S.l}` 左边，和更新无关 → 跳过' if S.br <= S.l
                                       else f'块 `[{S.bl}, {S.br})` 和 `[{S.l}, {S.r})` 有交集 → 继续看'),
        'if bl >= r': lambda S, B, r: (f'块 `[{S.bl}, {S.br})` 已在 `r = {S.r}` 右边 → 后面都不用看，`break`' if S.bl >= S.r
                                       else f'块左端 `{S.bl} < r = {S.r}`，这一块要处理'),
        'if l <= bl and br <= r': lambda S, B, r: (f'`l={S.l} ≤ bl={S.bl}` 且 `br={S.br} ≤ r={S.r}`：==整块被覆盖==' if S.l <= S.bl and S.br <= S.r
                                                   else f'块 `[{S.bl}, {S.br})` 只被盖住一部分，不能直接打标记'),
        'blocks[i][3] += val': '整块覆盖 → 不动元素，只把懒标记 `add` 加 `{val}`，变成 =={blocks[i][3]}==，`O(1)`',
        'for j in range': '暴力改下标 `{max(bl, l)}..{min(br, r) - 1}`（块内被盖住的部分）',
        'cnt[nums2[j]] -= 1': '撤销旧值 `{nums2[j]}` 的计数',
        'nums2[j] += val': '`nums2[{j}]` 加 `{val}` → {nums2[j]}',
        'cnt[nums2[j]] += 1': '登记新值 `{nums2[j]}` 的计数 → `{cnt[nums2[j]]}`',
        'res = 0': '类型 2：目标和 `tot = {q[1]}`，累计数对数 `res = 0`',
        'target = q[1] - add': '这一块整体加了 `{add}`，存储值要凑 `tot - add = {target}`',
        'res += cnt.get': '需要存储值 `{target} - {x} = {target - x}`，查表得 `{cnt.get(target - x, 0)}` 个 → `res = {res}`',
        'ans.append(res)': '本次询问答案 `{res}` 入 `ans`',
        'return ans': '全部处理完，返回 `{ans}`',
    },
    skip=['m, n = len', 'r = min(i + B, n)', 'ans = []', 'blocks = []', 'continue'],
    max_steps=90,
    cards=dict(
        one_liner='把 nums2 分块：整块打懒标记，零碎块暴力改',
        complexity='时间 `O(n + q·√(mn))`，空间 `O(n)`',
        problem=['`nums2` 区间加 `val`；查询有多少对 `nums1[j] + nums2[k] == tot`',
                 '`nums1` 很短（m ≤ 5），`nums2` 与询问数都到 5×10^4',
                 '示例：`nums1=[1,2]`，`nums2=[3,4,3,5,4,3]`，三条询问，答案 `[3, 4]`'],
        quote='把 nums2 分成若干段，每段 B 个元素。对于每一段，用一个哈希表维护每个元素的出现次数，用一个变量 add 记录这一段整体增加了 add（借鉴 Lazy 线段树的懒标记思想）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力哈希表：查询 `O(m)`，但区间加要 `O(n)`，太慢',
              '分块：整块只改 `add`；残缺块逐个改，并同步更新 `cnt`',
              '查询时每块要凑的值是 `tot - nums1[j] - add`，在块的哈希表里 `O(1)` 查'],
        summary=['更新 `O(B + n/B)`，查询 `O(m·n/B)`；取 `B = √(mn)` 最优，总计 `O(n + q√(mn))`',
                 '易错：残缺块要先 `cnt[旧值] -= 1` 再加新值；查询用 `cnt.get`，别往哈希表里塞新 key',
                 '区间 `[l, r)` 是左闭右开，题目的 `y` 要 `+1`',
                 '同类：分块 + 懒标记，是线段树 lazy 的根号版'],
    ),
)
