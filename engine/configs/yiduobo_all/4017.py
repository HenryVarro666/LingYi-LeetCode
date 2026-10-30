def _fit(cv, s, size, maxw, bold=True):
    while size > 13 and cv.tlen(s, size, bold) > maxw:
        size -= 1
    return size


def _seg(cv, T, box, n, lab, kids, cur=(), chg=(), nums=None, num_hl=(), title='', root=1, bound=None):
    """线段树示意图：上排 = 数组（可选），下面每个节点 = 一段区间；黄色 = 当前节点，黄边 = 这一步刚改过，虚框 = 还没算出"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 60) / max(n, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 36
    if nums is not None:
        for i in range(n):
            X = sx + i * cell
            hl = i in num_hl
            cv.rect((X + 2, top, X + cell - 2, top + 40), fill=T['yellow'] if hl else T['panel2'], r=6)
            cv.text((X + cell / 2, top + 20), nums[i] if i < len(nums) else '', 24, T['bg'] if hl else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + 44), i, 16, T['dim'], anchor='mt', mono=True)
        top += 72
    nodes = {}
    def walk(nd, l, r, d):
        nodes[nd] = (l, r, d)
        if l < r:
            m = (l + r) // 2
            a, b = kids(nd)
            walk(a, l, m, d + 1)
            walk(b, m + 1, r, d + 1)
    walk(root, 0, n - 1, 0)
    depth = max(d for _, _, d in nodes.values()) + 1
    rowh = min(112, (y1 - top - 6) / depth)
    bh = min(54, rowh - 30)
    pos = {}
    for nd, (l, r, d) in nodes.items():
        cx = sx + (l + r + 1) / 2 * cell
        pos[nd] = (cx, top + d * rowh)
    for nd, (l, r, d) in nodes.items():
        if l < r:
            for c in kids(nd):
                cv.line([(pos[nd][0], pos[nd][1] + bh + 20), (pos[c][0], pos[c][1])], T['border'], 2)
    for nd, (l, r, d) in nodes.items():
        cx, cy = pos[nd]
        w = min(max(cell * (r - l + 1) - 8, 40), 190 if r > l else 130)
        s = lab(nd)
        is_cur = nd in cur
        changed = nd in chg
        if s is None:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['dim'], width=1, r=8)
            s = ''
        else:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), fill=T['yellow'] if is_cur else T['panel2'],
                    outline=T['yellow'] if changed else T['border'], width=4 if changed else 1, r=8)
        if is_cur and s == '':
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['yellow'], width=4, r=8)
        sz = _fit(cv, s, 24, w - 10)
        cv.text((cx, cy + bh / 2), s, sz, T['bg'] if is_cur and s else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + bh + 3), f'#{nd} [{l},{r}]', 15, T['dim'], anchor='mt', mono=True)



def _draw(cv, S, B, box, T):
    f, first, last = S.get('f'), S.get('first'), S.get('last')
    n = S.get('n')
    if f is None or first is None or n is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    fb, ib, lb = B.get('f'), B.get('first'), B.get('last')
    chg = set()
    if fb is not None and ib is not None and lb is not None and len(fb) == len(f):
        chg = {i for i in range(len(f)) if (fb[i], ib[i], lb[i]) != (f[i], first[i], last[i])}
    cur = S['_inner'].get('p')
    nums = S.get('nums')
    peak = S.get('peak')
    nums = nums if nums and len(nums) == n else None
    hl = {i for i in range(n) if peak and peak[i]} if peak else ()
    dash = lambda v: '–' if v is None else str(v)
    _seg(cv, T, box, n, lambda nd: f'{f[nd]} | {dash(first[nd])},{dash(last[nd])}' if nd < len(f) else None,
         lambda nd: (nd * 2 + 1, nd * 2 + 2), cur=(cur,) if cur is not None and 'left' in S['_inner'] else (), chg=chg,
         nums=nums, num_hl=hl, root=0,
         title='线段树：节点 = f｜first,last（首/末峰顶下标，– = 无）')


def _info(S):
    f, first, last = S.get('f'), S.get('first'), S.get('last')
    if f is None or first is None or 'nums' not in S:
        return ''
    pk = [i for i, v in enumerate(S['peak']) if v] if 'peak' in S else []
    return f"当前峰顶下标：`{pk}`，根 `f[0] = {f[0]}`，`first = {first[0]}`，`last = {last[0]}`"


CONFIG = dict(
    num=4017, title='数组中的峰值 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（峰顶下标之和公式）',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def countOfPeaks(self, nums, queries):
        
        n = len(nums)
        peak = [False] * n

        for index in range(1, n - 1):
            peak[index] = (nums[index] > nums[index - 1] and nums[index] > nums[index + 1])

        f = [0] * (n * 4)
        first = [None] * (n * 4)
        last = [None] * (n * 4)

        def build(p, left, right):
            if left == right:
                if peak[left]:
                    first[p] = left
                    last[p] = left
                return

            mid = (left + right) // 2
            build(p * 2 + 1, left, mid)
            build(p * 2 + 2, mid + 1, right)
            
            f[p] = f[p * 2 + 1] + f[p * 2 + 2]
            if last[p * 2 + 1] is not None and first[p * 2 + 2] is not None:
                f[p] += last[p * 2 + 1] * (first[p * 2 + 2] - last[p * 2 + 1])
            
            if first[p * 2 + 1] is None:
                first[p] = first[p * 2 + 2]
            else:
                first[p] = first[p * 2 + 1]
            
            if last[p * 2 + 2] is None:
                last[p] = last[p * 2 + 1]
            else:
                last[p] = last[p * 2 + 2]
        
        def query(p, left, right, start, end):
            if start == left and right == end:
                return f[p], first[p], last[p]
            
            mid = (left + right) // 2
            if end <= mid:
                return query(p * 2 + 1, left, mid, start, end)
            elif start > mid:
                return query(p * 2 + 2, mid + 1, right, start, end)
            else:
                left_v, left_first, left_last = query(p * 2 + 1, left, mid, start, mid)
                right_v, right_first, right_last = query(p * 2 + 2, mid + 1, right, mid + 1, end)

                tot = left_v + right_v
                if left_last is not None and right_first is not None:
                    tot += left_last * (right_first - left_last)

                if left_first is None:
                    interval_first = right_first
                else:
                    interval_first = left_first

                if right_last is None:
                    interval_last = left_last
                else:
                    interval_last = right_last

                return tot, interval_first, interval_last
        
        def update(p, left, right, index):
            if left == right:
                if peak[index]:
                    first[p] = index
                    last[p] = index
                else:
                    first[p] = None
                    last[p] = None
                return    
            
            mid = (left + right) // 2
            if index <= mid:
                update(p * 2 + 1, left, mid, index)
            else:
                update(p * 2 + 2, mid + 1, right, index)
            
            f[p] = f[p * 2 + 1] + f[p * 2 + 2]
            if last[p * 2 + 1] is not None and first[p * 2 + 2] is not None:
                f[p] += last[p * 2 + 1] * (first[p * 2 + 2] - last[p * 2 + 1])
            
            if first[p * 2 + 1] is None:
                first[p] = first[p * 2 + 2]
            else:
                first[p] = first[p * 2 + 1]
            
            if last[p * 2 + 2] is None:
                last[p] = last[p * 2 + 1]
            else:
                last[p] = last[p * 2 + 2]
        
        build(0, 0, n - 1)

        res = []
        for q in queries:
            if q[0] == 1:
                tot, interval_first, interval_last = query(0, 0, n - 1, q[1], q[2])
                if interval_first is None:
                    res.append(0)
                elif interval_first == interval_last:
                    res.append((interval_first - q[1]) * (q[2] - interval_first))
                else:
                    res.append(tot + interval_last * (q[2] - interval_last) - q[1] * (q[2] - interval_first))
            
            else:
                pending = []
                nums[q[1]] = q[2]
                for index in range(q[1] - 1, q[1] + 2):
                    if index <= 0 or index >= n - 1:
                        continue
                    
                    ori = peak[index]
                    peak[index] = (nums[index] > nums[index - 1] and nums[index] > nums[index + 1])
                    if ori and not peak[index]:
                        update(0, 0, n - 1, index)
                    elif not ori and peak[index]:
                        pending.append(index)
                
                for index in pending:
                    update(0, 0, n - 1, index)
                
                nums[q[1]] = q[2]

        return res
''',
    call='Solution().countOfPeaks([1, 3, 2, 4, 1], [[1, 0, 4], [2, 2, 5], [1, 1, 3]])',
    expect=[5, 1],
    max_steps=75,
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=['n', ('res', 'res', 'green')],
    skip=[4, 5, 7, 10, 11, 12, 98, 15, 16, 18, 19, 21, 22, 23, 26, 29, 30, 31, 32, 33, 34, 35, 36, 37, 40, 43, 44, 45, 46, 47, 49, 50, 53,
          56, 57, 58, 59, 61, 62, 63, 64, 66, 69, 72, 73, 75, 76, 78, 79, 80, 82, 85, 88, 89, 90, 91, 93, 94, 95, 96, 100, 102, 104, 106,
          112, 114, 115, 116, 118, 120, 122, 125, 128, 70],
    captions={
        8: lambda S, B, r: f"下标 `{S.index}`：`{S.nums[S.index - 1]} < {S.nums[S.index]} > {S.nums[S.index + 1]}` → " + ('==是峰顶==' if S.peak[S.index] else '不是峰顶'),
        17: '叶子 `[{left}]` 是峰顶：`first = last = {left}`（`f` 还是 0，因为只有一个峰顶）',
        25: '合并节点 `{p}`：`f[{p}] = 左.f + 右.f` = `{f[p*2+1]} + {f[p*2+2]}` = {f[p]}',
        84: '更新后重新合并节点 `{p}`：`f[{p}] = 左.f + 右.f` = `{f[p*2+1]} + {f[p*2+2]}` = {f[p]}',
        27: '左右都有峰顶：加上跨中点的一项 `左.last × (右.first − 左.last)` = `{last[p*2+1]} × ({first[p*2+2]} − {last[p*2+1]})` → `f[{p}]` = =={f[p]}==',
        86: '左右都有峰顶：加上跨中点的一项 `左.last × (右.first − 左.last)` = `{last[p*2+1]} × ({first[p*2+2]} − {last[p*2+1]})` → `f[{p}]` = =={f[p]}==',
        71: '位置 `{index}` 现在是峰顶：`first = last = {index}`',
        74: '位置 `{index}` 不再是峰顶：`first = last = None`',
        41: '要查的区间正好是节点 `[{left},{right}]`：直接取 `(f, first, last)` = `({f[p]}, {first[p]}, {last[p]})`',
        52: '区间被拆成左右两段：`tot = 左.f + 右.f` = `{left_v} + {right_v}` = {tot}',
        54: '两段都有峰顶：加上跨中点一项 `{left_last} × ({right_first} − {left_last})` → `tot` = =={tot}==',
        101: lambda S, B, r: ('所有操作处理完了' if B.get('q') == S.q else (f"查询 `[{S.q[1]}, {S.q[2]}]`：数 `nums[{S.q[1]}..{S.q[2]}]` 里的峰值子数组" if S.q[0] == 1 else f"修改 `nums[{S.q[1]}] = {S.q[2]}`：影响 `index-1, index, index+1` 三个位置的峰顶")),
        103: '线段树返回 `(tot, first, last)`：区间内 `f` 累计到 `last` 之前，`first` / `last` 是首尾峰顶（相对 `[left, right]`）',
        105: '区间里没有峰顶 → 答案 `0`',
        107: '只有一个峰顶 `p = {interval_first}`：左端点有 `p − left` 种，右端点有 `right − p` 种 → `({interval_first} − {q[1]}) × ({q[2]} − {interval_first})` = =={res[-1]}==',
        109: '多个峰顶：答案 = `tot + last×(right−last) − left×(right−first)` = `{tot} + {interval_last}×({q[2]}−{interval_last}) − {q[1]}×({q[2]}−{interval_first})` = =={res[-1]}==',
        113: '先把 `nums[{q[1]}]` 改成 `{q[2]}`',
        119: '位置 `{index}`：旧是峰顶 `{ori}` → 新是峰顶 `{peak[index]}`',
        121: '峰顶消失了：马上更新线段树里这个叶子',
        123: '新出现的峰顶：先记进 `pending`，等消失的都处理完再更新',
        126: '处理 `pending` 里新出现的峰顶：更新线段树',
        130: '所有类型 1 查询的答案：`{res}`',
    },
    cards=dict(
        one_liner='把「以每个峰顶为最右峰顶」的子数组数加起来，拆成可合并的 f',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['数组 `nums`，长度 ≥ 3 且内部有严格大于两邻居的元素的子数组叫峰值子数组',
                 '操作 `[1, l, r]`：数 `nums[l..r]` 内的峰值子数组；`[2, i, v]`：单点修改',
                 '示例：`nums=[3,6,2,7,1], queries=[[1,1,3],[2,3,0],[1,0,4]]` → `[0,3]`',
                 '本视频：`[1,3,2,4,1]`，查询 `[0,4]` → `5`；`nums[2]` 改成 `5` 后查 `[1,3]` → `1`'],
        quote='可以利用线段树维护 p0*(p1-p0) + ... + p[k-1]*(pk-p[k-1]) 这一段的结果，以及区间中最左侧以及最右侧的峰值下标 p0 和 pk',
        quote_src='—— yiduobo 题解',
        idea=['峰顶 `p0 < p1 < … < pk`：以 `pi` 为最右峰顶的子数组有 `(pi − left) × (p(i+1) − pi)` 个（最后一个用 `right`）',
              '把 `-left` 提出来，总数 = `Σ p_i(p_{i+1}−p_i)` 的和 `+ pk(right−pk) − left(right−p0)`',
              '线段树每个节点存 `f`（相邻峰顶项之和）、`first`、`last`；合并时多出一项 `左.last × (右.first − 左.last)`',
              '修改后重算 `index-1, index, index+1` 的峰顶：先处理消失的，再处理新出现的'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`；查询分「无峰顶 / 一个峰顶 / 多个」三种情况',
                 '易错：区间端点上的元素不算该区间内的峰顶，但合并时它可能是相邻区间的峰顶，不能漏',
                 '和灵神的区别：灵神存 `cnt / pre / suf` 直接合并个数；yiduobo 用峰顶下标做公式',
                 '原文可直接在 Python 3 运行，未做修改'],
    ),
)
