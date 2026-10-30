_CODE = '''
class Solution(object):
    def handleQuery(self, nums1, nums2, queries):

        n = len(nums1)
        v = [0] * (n * 4)
        rev = [False] * (n * 4)
        s = sum(nums2)

        def reverse(now, left, right, i, j):
            if left == right:
                v[now] = 1 - v[now]
                return
            
            if left == i and right == j:
                rev[now] = not rev[now]
                v[now] = right - left + 1 - v[now]
                return
            
            mid = (left + right) >> 1
            if rev[now]:
                reverse(now + now + 1, left, mid, left, mid)
                reverse(now + now + 2, mid + 1, right, mid + 1, right)
                rev[now] = False
            
            if j <= mid:
                reverse(now + now + 1, left, mid, i, j)
            elif i > mid:
                reverse(now + now + 2, mid + 1, right, i, j)
            else:
                reverse(now + now + 1, left, mid, i, mid)
                reverse(now + now + 2, mid + 1, right, mid + 1, j)
            
            v[now] = v[now + now + 1] + v[now + now + 2]

        for index in range(n):
            if nums1[index] == 1:
                reverse(0, 0, n - 1, index, index)

        res = []
        for q in queries:
            if q[0] == 1:
                reverse(0, 0, n - 1, q[1], q[2])
            elif q[0] == 2:
                s += v[0] * q[1]
            else:
                res.append(s)
        
        return res
'''


_NUMS1 = [0, 0, 1, 0]
_NUMS2 = [1, 2, 3, 4]
_QUERIES = [[1, 0, 1], [2, 1, 0], [3, 0, 0], [1, 1, 1], [2, 5, 0], [3, 0, 0]]
_N3 = sum(1 for q in _QUERIES if q[0] == 3)


def _expect():
    a, s, out = list(_NUMS1), sum(_NUMS2), []
    for op, l, r in _QUERIES:
        if op == 1:
            for i in range(l, r + 1):
                a[i] ^= 1
        elif op == 2:
            s += l * sum(a)
        else:
            out.append(s)
    return out


def _skeleton(n):
    out = []

    def go(p, l, r, d):
        out.append((p, l, r, d))
        if l < r:
            m = (l + r) >> 1
            go(p * 2 + 1, l, m, d + 1)
            go(p * 2 + 2, m + 1, r, d + 1)
    go(0, 0, n - 1, 0)
    return out


def _true_leaves(n, v, rev):
    res = {}

    def go(p, l, r, par):
        if l == r:
            res[l] = (v[p] ^ par, par)
            return
        m = (l + r) >> 1
        p2 = par ^ (1 if rev[p] else 0)
        go(p * 2 + 1, l, m, p2)
        go(p * 2 + 2, m + 1, r, p2)
    go(0, 0, n - 1, 0)
    return res


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['nums1'])
    v, rev = S['v'], S['rev']
    bv, br = B.get('v', v), B.get('rev', rev)
    sk = _skeleton(n)
    maxd = max(d for *_, d in sk) + 1
    cv.text((x0 + 18, y0 + 4), '线段树：每个节点 = 区间里 1 的个数 v（橙色「rev」= 整段待翻转，还没下放）', 22, T['muted'], bold=True)
    slot = (x1 - x0 - 40) / n
    bw, bh = min(slot * 0.9, 130), 66
    dy = min(110, (y1 - y0 - 190 - bh) / max(1, maxd - 1))
    inner = S.get('_inner', {})
    cur = inner.get('now') if 'now' in inner else None
    qr = None
    q = S.get('q')
    if q is not None and q[0] == 1 and 'res' in S:
        qr = (q[1], q[2])
    pos = {}
    for p, l, r, d in sk:
        pos[p] = (x0 + 20 + (l + r + 1) / 2 * slot, y0 + 48 + d * dy + bh / 2)
    for p, l, r, d in sk:
        if l < r:
            for c in (p * 2 + 1, p * 2 + 2):
                cv.line([(pos[p][0], pos[p][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'], 3)
    for p, l, r, d in sk:
        X, Y = pos[p]
        outline, width = T['border'], 2
        if v[p] != bv[p] or rev[p] != br[p]:
            outline, width = T['yellow'], 4
        if p == cur:
            outline, width = T['blue'], 4
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=(80, 56, 30) if rev[p] else T['panel2'], outline=outline, width=width, r=10)
        cv.text((X - bw / 2 + 8, Y - bh / 2 + 4), f'[{l},{r}]' if l < r else f'[{l}]', 16, T['muted'], mono=True)
        cv.text((X, Y + 8), v[p], 28, T['green'], anchor='mm', bold=True)
        if rev[p]:
            cv.text((X + bw / 2 - 6, Y - bh / 2 + 4), 'rev', 17, T['orange'], anchor='ra', bold=True)
    leaves = _true_leaves(n, v, rev)
    ya = y1 - 64
    cv.text((x0 + 18, ya - 58), '真实的 nums1（叶子里的值 × 祖先上待下放的翻转）', 19, T['muted'], bold=True)
    cw = min(70, (x1 - x0 - 40) / n)
    for k in range(n):
        val, par = leaves[k]
        X = x0 + 20 + (x1 - x0 - 40 - cw * n) / 2 + k * cw
        inq = qr is not None and qr[0] <= k <= qr[1]
        cv.rect((X + 3, ya - 20, X + cw - 3, ya + 20), fill=T['panel2'], outline=T['yellow'] if inq else (T['orange'] if par else T['border']), width=3 if (inq or par) else 2, r=8)
        cv.text((X + cw / 2, ya), val, 26, T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, ya + 32), k, 15, T['dim'], anchor='mt', mono=True)
    if qr is not None:
        cv.text((x1 - 20, ya - 58), f'黄框 = 本次翻转区间 [{qr[0]}, {qr[1]}]', 19, T['yellow'], anchor='ra', bold=True)


_LINES = _CODE.strip('\n').split('\n')


def _ln(text):
    for i, l in enumerate(_LINES):
        if text in l:
            return i + 1
    return 10 ** 6


def _hint(S, B):
    if 's' not in S or 'v' not in S:
        return ''
    return f"`nums2` 总和 `s` = =={S['s']}==；`nums1` 里 1 的个数 `v[0]` = =={S['v'][0]}=="


CONFIG = dict(
    num=2569, title='更新数组后处理求和查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='懒更新线段树 · 区间翻转 + 区间和',
    tags=['灵神题单·常用数据结构', '难度分 2398'],
    code=_CODE,
    call=f'Solution().handleQuery({_NUMS1!r}, {_NUMS2!r}, {_QUERIES!r})',
    expect=_expect(),
    views=[
        dict(type='text', fn=_hint, h=50),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('now', 'now', 'blue'), ('left', 'left'), ('right', 'right'), ('s', 's', 'green'), ('res', 'res', 'green')],
    skip=['n = len(nums1)', 'if left == right', 'mid = (left + right) >> 1', 'rev = [False]', 'res = []',
          'if q[0] == 1', 'elif q[0] == 2', 'for index in range(n)'] + [i + 1 for i, l in enumerate(_LINES) if l.strip() == 'return'],
    max_steps=70,
    captions={
        'v = [0]': '`v[now]`：节点管的区间里 1 的个数；`rev[now]`：整段待翻转的懒标记（两个数组都开 4n）',
        's = sum(nums2)': '`s` = `nums2` 的总和 = =={s}==',
        'if nums1[index] == 1': '`nums1[{index}] = {nums1[index]}`：{"是 1 → 在树里把这一位单点翻转一次（0 变 1）" if nums1[index] == 1 else "是 0，树里本来就是 0，不用动"}',
        'reverse(0, 0, n - 1, index, index)': '单点翻转 `[{index}, {index}]`，从根 `[0, {n - 1}]` 往下找',
        'if left == i and right == j': '节点 `[{left}, {right}]` 对目标 `[{i}, {j}]`：=={"刚好对上" if left == i and right == j else "没对上，继续往下"}==',
        'rev[now] = not rev[now]': '整段刚好被盖住：只打懒标记 `rev[{now}]` = =={rev[now]}==，不往子孙走',
        'v[now] = right - left + 1 - v[now]': '翻转后 1 的个数 = 区间长 `{right - left + 1}` − 原个数 → =={v[now]}==',
        'v[now] = 1 - v[now]': '叶子 `[{left}]` 直接翻转：`v[{now}]` = =={v[now]}==',
        'if rev[now]': '节点 `{now}` 有待下放的标记吗？ → =={"有：先传给两个儿子再往下" if rev[now] else "没有，直接往下"}==',
        'reverse(now + now + 1, left, mid, left, mid)': '标记传给左儿子 `[{left}, {mid}]`：它整段翻转',
        'reverse(now + now + 2, mid + 1, right, mid + 1, right)': '标记传给右儿子 `[{mid + 1}, {right}]`：它整段翻转',
        'rev[now] = False': '标记传完了，节点 `{now}` 自己的清掉',
        'if j <= mid': '`j <= mid`（`{j} <= {mid}`）→ =={"目标整段在左半" if j <= mid else "不全在左半"}==',
        'elif i > mid': '`i > mid`（`{i} > {mid}`）→ =={"目标整段在右半" if i > mid else "目标跨过 mid"}==',
        'reverse(now + now + 1, left, mid, i, j)': '递归左儿子 `[{left}, {mid}]`',
        'reverse(now + now + 2, mid + 1, right, i, j)': '递归右儿子 `[{mid + 1}, {right}]`',
        'reverse(now + now + 1, left, mid, i, mid)': '目标跨过 mid：左边查 `[{i}, {mid}]`',
        'reverse(now + now + 2, mid + 1, right, mid + 1, j)': '目标跨过 mid：右边查 `[{mid + 1}, {j}]`',
        'v[now] = v[now + now + 1] + v[now + now + 2]': '回溯：节点 `{now}` = 左 `{v[now + now + 1]}` + 右 `{v[now + now + 2]}` = =={v[now]}==',
        'for q in queries': lambda S, B, r: ('操作都处理完了' if (B.get('q') is not None and B.q[0] == 3 and len(B.get('res') or []) == _N3) else
                                             f'取下一个操作 `{S.q}`：' + {1: f'翻转 `nums1[{S.q[1]}..{S.q[2]}]`', 2: f'`s` 加上 `{S.q[1]} × 1 的个数`', 3: '记录当前 `s`'}[S.q[0]]),
        'reverse(0, 0, n - 1, q[1], q[2])': '操作 1：翻转 `nums1[{q[1]}..{q[2]}]`，从根节点开始',
        's += v[0] * q[1]': '操作 2：`s += v[0] × p` = `{v[0]} × {q[1]}`，`s` = =={s}==',
        'res.append(s)': '操作 3：把当前总和 `s` = =={s}== 记进答案',
    },
    cards=dict(
        one_liner='把「要不要翻转」记在节点上，用到时才往下传',
        complexity='时间 `O(n log n + q log n)`，空间 `O(n)`',
        problem=['`nums1` 是 0/1 数组，`nums2` 是整数数组，三种操作：',
                 '1：翻转 `nums1[l..r]`；2：`nums2[i] += nums1[i] × p`；3：求 `nums2` 的和',
                 '本视频：`nums1=[0,0,1,0]`，`nums2=[1,2,3,4]`'],
        quote='如果使用一个变量s维护nums2的和的话，就可以在O(1)的时间内处理第三种操作了。而对于第二种操作而言，就相当于将s加上k个p，这里的k为nums1中1的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 维护 `nums2` 的和；操作 2 只要知道 `nums1` 里有 `k` 个 1，`s += k × p`',
              '所以只剩一个问题：区间翻转 + 全局 1 的个数 → 带 `rev` 标记的线段树',
              '懒更新：区间正好对上节点就打标记，下次要往下走时再把标记下放'],
        summary=['时间 `O(n log n + q log n)`（初始化用单点翻转，逐个插入），空间 `O(n)`',
                 '翻转后个数 = 区间长 − 原个数；叶子直接取反，不打标记',
                 '要往下走之前先下放 `rev`，回溯时再用左右儿子求和',
                 '原文本身可直接在 Python 3 运行（`>> 1` 即整除 2），代码未改动',
                 '对比灵神：灵神用递归 `build` 建树，yiduobo 把初始的 1 当作单点翻转插入'],
    ),
)
