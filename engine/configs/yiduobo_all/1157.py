_CODE = '''
class Node(object):

    def __init__(self, left=None, right=None, v=0):
        self.left = left
        self.right = right
        self.v = v

class MajorityChecker(object):

    def __init__(self, arr):
        self.root_list = [Node()]
    
        self.n = max(arr)
        for num in arr:
            new_root = Node(self.root_list[-1].left, self.root_list[-1].right, self.root_list[-1].v)
            new_root.v += 1
            self.insert(1, self.n, self.root_list[-1], new_root, num)
            self.root_list.append(new_root)

    def insert(self, l, r, pre, now, num):
        if l == r:
            return
        mid = (l + r) >> 1
        if num <= mid:
            if pre and pre.left:
                new_left = Node(pre.left.left, pre.left.right, pre.left.v)
            else:
                new_left = Node()

            new_left.v += 1
            now.left = new_left

            if pre:
                self.insert(l, mid, pre.left, new_left, num)
            else:
                self.insert(l, mid, None, new_left, num)
        
        else:
            if pre and pre.right:
                new_right = Node(pre.right.left, pre.right.right, pre.right.v)
            else:
                new_right = Node()

            new_right.v += 1
            now.right = new_right

            if pre:
                self.insert(mid + 1, r, pre.right, new_right, num)
            else:
                self.insert(mid + 1, r, None, new_right, num)

    def find(self, l, r, pre, now, threshold):
        if l == r:
            return l
        
        mid = (l + r) >> 1

        pre_l = pre_r = 0
        if pre and pre.left:
            pre_l = pre.left.v
        if pre and pre.right:
            pre_r = pre.right.v
        
        if now and now.left and now.left.v - pre_l >= threshold:
            if pre is None:
                return self.find(l, mid, None, now.left, threshold)
            else:
                return self.find(l, mid, pre.left, now.left, threshold)
        
        if now and now.right and now.right.v - pre_r >= threshold:
            if pre is None:
                return self.find(mid + 1, r, None, now.right, threshold)
            else:
                return self.find(mid + 1, r, pre.right, now.right, threshold)
        
        return -1
        
        

    def query(self, left, right, threshold):

        return self.find(1, self.n, self.root_list[left], self.root_list[right + 1], threshold)
'''


_LINES = _CODE.strip('\n').split('\n')

ARR = [1, 3, 3, 3]
QS = [(0, 3, 3), (0, 1, 2), (1, 2, 2)]


def _ln(text, nth=1):
    k = 0
    for i, l in enumerate(_LINES):
        if text in l:
            k += 1
            if k == nth:
                return i + 1
    return 10 ** 6


def _expect():
    out = []
    for l, r, t in QS:
        seg = ARR[l:r + 1]
        ans = -1
        for x in set(seg):
            if seg.count(x) >= t:
                ans = x
        out.append(ans)
    return out


def _count(nd):
    return nd.v if nd is not None else 0


def _pair(S):
    """返回要画的两棵树 (标题, 根)；查询阶段是 root_list[left] 与 root_list[right+1]；建树阶段是旧版本与正在建的新版本"""
    roots = S.get('self.root_list') or []
    if 'right' in S and 'threshold' in S and 'self.n' in S:
        L, R = S['left'], S['right'] + 1
        return [(f'pre = root_list[{L}]（前 {L} 个数）', roots[L]), (f'now = root_list[{R}]（前 {R} 个数）', roots[R])]
    new = S.get('new_root')
    if new is None:
        return [(f'root_list[{len(roots) - 1}]', roots[-1])] if roots else []
    old = roots[-2] if len(roots) > 1 and roots[-1] is new else (roots[-1] if roots else None)
    k = len(roots) - (2 if roots and roots[-1] is new else 1)
    return [(f'旧版本 root_list[{k}]', old), ('新版本（正在建）', new)]


def _walk(root, lo, hi):
    """(l, r) -> node，按值域区间切分，和代码里的 mid 一致"""
    out = {}

    def go(nd, l, r):
        out[(l, r)] = nd
        if l == r:
            return
        mid = (l + r) >> 1
        go(nd.left if nd is not None else None, l, mid)
        go(nd.right if nd is not None else None, mid + 1, r)
    go(root, lo, hi)
    return out


def _skel(lo, hi):
    out = []

    def go(l, r, d):
        out.append((l, r, d))
        if l < r:
            mid = (l + r) >> 1
            go(l, mid, d + 1)
            go(mid + 1, r, d + 1)
    go(lo, hi, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('self.n')
    trees = _pair(S)
    if n is None:
        n = max(ARR)
    sk = _skel(1, n)
    maxd = max(d for *_, d in sk) + 1
    cv.text((x0 + 18, y0 + 4), '值域线段树：节点 = 值域区间 + 区间内出现次数 v（两版本共享的节点画虚线）', 22, T['muted'], bold=True)
    inner = S.get('_inner', {})
    cur = (inner.get('l'), inner.get('r')) if 'l' in inner and 'r' in inner and 'pre' in inner else None
    w = (x1 - x0 - 40) / max(1, len(trees))
    other = None
    maps = [_walk(rt, 1, n) for _, rt in trees]
    bmaps = []
    for (title, rt) in _pair(B) if 'self.root_list' in B else []:
        bmaps.append(_walk(rt, 1, n))
    for ti, ((title, rt), mp) in enumerate(zip(trees, maps)):
        tx0 = x0 + 20 + ti * w
        cv.text((tx0 + w / 2, y0 + 58), title, 20, T['blue'] if ti == 0 else T['pink'], anchor='mm', bold=True)
        slot = w / n
        bw, bh = min(slot * 0.86, 96), 58
        dy = min(110, (y1 - y0 - 190 - bh) / max(1, maxd - 1))
        pos = {}
        for l, r, d in sk:
            pos[(l, r)] = (tx0 + (l - 1 + r) / 2 * slot, y0 + 94 + d * dy + bh / 2)
        for l, r, d in sk:
            if l < r:
                mid = (l + r) >> 1
                for c in ((l, mid), (mid + 1, r)):
                    ok = mp[c] is not None
                    cv.line([(pos[(l, r)][0], pos[(l, r)][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'] if ok else T['panel2'], 3)
        for l, r, d in sk:
            X, Y = pos[(l, r)]
            nd = mp[(l, r)]
            rect = (X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2)
            if nd is None:
                cv.rect(rect, outline=T['dim'], width=1, r=8)
                cv.text((X, Y - bh / 2 + 3), f'[{l},{r}]' if l < r else f'[{l}]', 15, T['dim'], anchor='mt', mono=True)
                continue
            shared = any(oi != ti and omp.get((l, r)) is nd for oi, omp in enumerate(maps))
            outline, width = T['border'], 2
            if (l, r) == cur:
                outline, width = T['yellow'], 4
            if shared:
                cv.rect(rect, fill=T['panel2'], r=8)
                cv.dashed((rect[0], rect[1]), (rect[2], rect[1]), T['muted'], 2, 8, 5)
                cv.dashed((rect[0], rect[3]), (rect[2], rect[3]), T['muted'], 2, 8, 5)
                if outline != T['border']:
                    cv.rect(rect, outline=outline, width=width, r=8)
            else:
                fill = (70, 60, 30) if (ti == 1 and len(trees) == 2 and 'threshold' not in S) else T['panel2']
                cv.rect(rect, fill=fill, outline=outline, width=width, r=8)
            cv.text((X, Y - bh / 2 + 3), f'[{l},{r}]' if l < r else f'[{l}]', 15, T['muted'], anchor='mt', mono=True)
            cv.text((X, Y + 10), nd.v, 26, T['green'] if nd.v else T['dim'], anchor='mm', bold=True)
    # 原数组
    ya = y1 - 70
    cv.text((x0 + 18, ya - 4), 'arr', 20, T['muted'], anchor='lm', bold=True)
    cw = 54
    for k, v in enumerate(ARR):
        X = x0 + 70 + k * cw
        inwin = 'right' in S and 'threshold' in S and S['left'] <= k <= S['right']
        cv.rect((X, ya - 20, X + cw - 6, ya + 20), fill=(70, 60, 30) if inwin else T['panel2'], outline=T['yellow'] if inwin else T['border'], width=2, r=6)
        cv.text((X + (cw - 6) / 2, ya), v, 24, T['text'], anchor='mm', bold=True)
    if 'right' in S and 'threshold' in S and 'self.n' in S:
        cv.text((x0 + 70 + len(ARR) * cw + 14, ya), f"查询 [{S['left']}, {S['right']}]，阈值 {S['threshold']}", 21, T['yellow'], anchor='lm', bold=True)


CONFIG = dict(
    num=1157, title='子数组中占绝大多数的元素', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='主席树（可持久化值域线段树）',
    tags=['灵神题单·常用数据结构', '灵神题单·数学算法'],
    code=_CODE,
    setup='ARR_ = %r' % (ARR,),
    call='obj = MajorityChecker(ARR_)\n[obj.query(l, r, t) for l, r, t in %r]' % (QS,),
    expect=_expect(),
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('threshold', 'threshold', 'yellow'), ('l', 'l'), ('r', 'r')],
    skip=['new_root = Node(', 'new_root.v += 1', 'if l == r', 'mid = (l + r) >> 1', 'if pre and pre.left', 'if pre and pre.right',
          'if pre:', 'if num <= mid', 'pre_l = pre_r = 0', 'if pre is None', 'return self.find(l, mid, None', 'return self.find(mid + 1, r, None',
          'self.insert(l, mid, None', 'self.insert(mid + 1, r, None', 'self.n = max(arr)', 'self.root_list = [Node()]',
          22, 'self.left = left', 'self.right = right', 'self.v = v', 'pre_l = pre.left.v', 'pre_r = pre.right.v'],
    max_steps=64,
    captions={
        'for num in arr': '{("加入第 `" + str(num) + "` 个值：生成一个新版本（新根）") if len(self.root_list) <= 4 else "全部加完：共 5 个版本（含最前面的空版本）"}',
        'self.insert(1, self.n, self.root_list[-1]': '`insert`：复制旧根（左右子树先共享），根的 `v` 加 1，再沿着 `{num}` 所在的值域往下，只新建这一条路径',
        'new_left = Node(pre.left.left': '`pre` 里已有左儿子：==复制==一份（它的子树继续共享）',
        'new_left = Node()': '`pre` 里没有这个子节点：新建一个空节点',
        'new_right = Node(pre.right.left': '`pre` 里已有右儿子：==复制==一份（它的子树继续共享）',
        'new_right = Node()': '`pre` 里没有这个子节点：新建一个空节点',
        'new_left.v += 1': '新节点的计数加 1：`v = {new_left.v}`',
        'new_right.v += 1': '新节点的计数加 1：`v = {new_right.v}`',
        'now.left = new_left': '挂到新版本上：新版本的左儿子换成新节点，其余节点仍与旧版本共享',
        'now.right = new_right': '挂到新版本上：新版本的右儿子换成新节点，其余节点仍与旧版本共享',
        'self.insert(l, mid, pre.left, new_left, num)': '往下一层：值域 `[{l}, {mid}]`',
        'self.insert(mid + 1, r, pre.right, new_right, num)': '往下一层：值域 `[{mid + 1}, {r}]`',
        'self.root_list.append(new_root)': '这个版本建好了，存进 `root_list`：它代表「前 {len(self.root_list) - 1} 个数」的计数树',
        'return self.find(1, self.n, self.root_list[left]': '查询 `[{left}, {right}]`，阈值 `{threshold}`：比较版本 `{left}`（前 {left} 个）和版本 `{right + 1}`（前 {right + 1} 个）',
        'now.left.v - pre_l >= threshold': '值域 `[{l}, {(l + r) >> 1}]` 里的个数：`{(now.left.v if now.left else 0)} − {pre_l} = {(now.left.v if now.left else 0) - pre_l}`，{">=" if (now.left.v if now.left else 0) - pre_l >= threshold else "<"} 阈值 `{threshold}` → =={"绝大多数只能在左半" if (now.left.v if now.left else 0) - pre_l >= threshold else "左半不够"}==',
        'now.right.v - pre_r >= threshold': '值域 `[{((l + r) >> 1) + 1}, {r}]` 里的个数：`{(now.right.v if now.right else 0)} − {pre_r} = {(now.right.v if now.right else 0) - pre_r}`，{">=" if (now.right.v if now.right else 0) - pre_r >= threshold else "<"} 阈值 `{threshold}` → =={"绝大多数在右半" if (now.right.v if now.right else 0) - pre_r >= threshold else "右半也不够"}==',
        'return self.find(l, mid, pre.left, now.left, threshold)': '往左半值域 `[{l}, {mid}]` 走，两个版本各下一层',
        'return self.find(mid + 1, r, pre.right, now.right, threshold)': '往右半值域 `[{mid + 1}, {r}]` 走，两个版本各下一层',
        'return l': '值域缩到单点，就是它：返回 `{l}`',
        'return -1': '左右两半都不到阈值 → 没有绝大多数元素，返回 `-1`',
    },
    cards=dict(
        one_liner='每加一个数就复制一条根到叶子的路径，历史版本全部保留',
        complexity='建树 `O(n log V)`，每次查询 `O(log V)`；空间 `O(n log V)`',
        problem=['`MajorityChecker(arr)`：数组 `arr`',
                 '`query(left, right, threshold)`：返回 `arr[left..right]` 中出现次数 `>= threshold` 的元素，没有就返回 `-1`',
                 '保证 `threshold` 超过区间长度的一半，所以至多一个这样的数'],
        quote='这里的线段树节点对应的数值，而非区间……每一轮最多新增O(logn)个节点……这里的n个根节点实际上就是由于[0, 0]，[0, 1]，[0, 2]，...，[0, n - 1]这n个前缀区间所做成的n棵线段树。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素做法：前缀里记每个数出现次数，两个前缀相减，但空间是平方级',
              '线段树建在==值域==上，节点 `v` = 区间内数的个数；每插一个数只新建一条路径，其余子树共享',
              '查询 `[l, r]`：同时走 `root_list[l]` 和 `root_list[r+1]`，两边相减就是区间内的个数，哪边 `>= threshold` 往哪边走'],
        summary=['建树 `O(n log V)`，每次查询 `O(log V)`，`V` 是值域大小',
                 '版本 `k` = 前 `k` 个数；区间 `[l, r]` 用版本 `r+1` 减版本 `l`',
                 '先判左半，再判右半：因为 `threshold` 过半，两边不会同时达标',
                 '两边都不到阈值就返回 `-1`；值域缩到单点 `l == r` 时返回 `l`',
                 '原文本身可直接在 Python 3 运行（`>> 1` 即整除 2），代码未改动'],
    ),
)
