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



def _nodes(root):
    d = {}
    ids = {}
    def walk(nd, k):
        d[k] = nd
        ids[id(nd)] = k
        if nd.left is not None:
            walk(nd.left, 2 * k)
            walk(nd.right, 2 * k + 1)
    walk(root, 1)
    return d, ids


def _root(S):
    t = S.get('tree') or S.get('self')
    r = getattr(t, 'root', None)
    return r if r is not None and hasattr(r, 'maxs') else None


def _draw(cv, S, B, box, T):
    root = _root(S)
    sub = False
    if root is None:
        root = S.get('now') if S.get('now') is not None and hasattr(S.get('now'), 'maxs') else None
        sub = True
    if root is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    d, ids = _nodes(root)
    rb = _root(B) if not sub else None
    chg = set()
    if rb is not None:
        d0, _ = _nodes(rb)
        chg = {k for k in d if k in d0 and (d0[k].maxs, d0[k].ls, d0[k].rs, d0[k].lc, d0[k].rc) != (d[k].maxs, d[k].ls, d[k].rs, d[k].lc, d[k].rc)}
    cur = S['_inner'].get('now')
    n = root.r - root.l + 1
    leaves = {nd.l: nd.lc for nd in d.values() if nd.l == nd.r}
    nums = None if sub else [leaves.get(i, '') for i in range(root.l, root.r + 1)]
    _seg(cv, T, box, n, lambda k: f'{d[k].maxs} · {d[k].ls} · {d[k].rs}' if k in d else None, lambda k: (2 * k, 2 * k + 1),
         cur=(ids[id(cur)],) if cur is not None and id(cur) in ids else (), chg=chg, nums=nums,
         title=('正在建 [%d,%d] 的子树：' % (root.l, root.r) if sub else '') + '线段树：节点 = (maxs 最长段 · ls 最长前缀 · rs 最长后缀)')


def _info(S):
    inn = S['_inner']
    now = inn.get('now')
    if now is not None and hasattr(now, 'left') and now.left is not None and now.right is not None and now.l < now.r:
        return (f"区间 `[{now.l},{now.r}]`：左半末尾 `{now.left.rc}`，右半开头 `{now.right.lc}` → "
                + ('==相同，可拼接==' if now.left.rc == now.right.lc else '==不同，不拼接=='))
    return ''


CONFIG = dict(
    num=2213, title='由单个字符重复的最长子字符串', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（lc/rc + ls/rs + maxs）',
    tags=['灵神题单·常用数据结构', '难度分 2629'],
    code='''
class Node(object):

    def __init__(self, l, r, lc, rc):
        self.l = l
        self.r = r
        self.lc = lc
        self.rc = rc
        self.left = self.right = None
        self.ls = self.rs = 1
        self.maxs = 1

class SegementTree(object):

    def __init__(self, arr):
        self.root = self.build(0, len(arr) - 1, arr)
    
    def build(self, l, r, arr):
        now = Node(l, r, arr[l], arr[r])
        if l < r:
            mid = (l + r) >> 1
            now.left = self.build(l, mid, arr)
            now.right = self.build(mid + 1, r, arr)
            
            now.ls = now.left.ls
            now.rs = now.right.rs
            now.maxs = max(now.left.maxs, now.right.maxs)

            if now.left.rc == now.right.lc:
                if now.ls == mid - l + 1:
                    now.ls += now.right.ls
                if now.rs == r - mid:
                    now.rs += now.left.rs
                now.maxs = max(now.maxs, now.left.rs + now.right.ls)

        return now

    def insert(self, now, p, v):
        if now.l == now.r:
            now.lc = now.rc = v
        else:
            mid = (now.l + now.r) >> 1
            if p <= mid:
                self.insert(now.left, p, v)
            else:
                self.insert(now.right, p, v)
            
            now.lc = now.left.lc
            now.ls = now.left.ls

            now.rc = now.right.rc
            now.rs = now.right.rs

            now.maxs = max(now.left.maxs, now.right.maxs)

            if now.left.rc == now.right.lc:
                if now.ls == mid - now.l + 1:
                    now.ls += now.right.ls
                if now.rs == now.r - mid:
                    now.rs += now.left.rs
                now.maxs = max(now.maxs, now.left.rs + now.right.ls)

    def query(self, p, v):
        self.insert(self.root, p, v)
        return self.root.maxs

class Solution(object):
    def longestRepeating(self, s, queryCharacters, queryIndices):

        tree = SegementTree(s)
        res = []
        for index in range(len(queryCharacters)):
            res.append(tree.query(queryIndices[index], queryCharacters[index]))
        
        return res
''',
    call='Solution().longestRepeating("aabbc", "aa", [2, 3])',
    expect=[3, 4],
    max_steps=70,
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=[('res', 'res', 'green')],
    skip=['self.l = l', 'self.r = r', 'self.lc = lc', 'self.rc = rc', 'self.left = self.right', 'self.ls = self.rs = 1', 'self.maxs = 1',
          'mid = (l + r)', 'mid = (now.l + now.r)', 'now.left = self.build', 'now.right = self.build', 'if l < r', 'return now', 'return self.root',
          'self.root = self.build', 'tree = SegementTree', 'self.insert(', 'if now.l == now.r', 'now.ls = now.left.ls', 'now.rs = now.right.rs',
          'now.maxs = max(now.left.maxs', 'now.lc = now.left.lc', 'now.rc = now.right.rc', 'res = []', 'return res'],
    captions={
        'now = Node(l, r': lambda S, B, r: f"新建节点 `[{S.l},{S.r}]`：`lc = {S.arr[S.l]}`，`rc = {S.arr[S.r]}`，`ls = rs = maxs = 1`" + ('，叶子到此为止' if S.l == S.r else '，先递归建左右子树，回来再合并'),
        'if now.left.rc == now.right.lc': lambda S, B, r: (f"先继承：`ls = 左.ls`，`rs = 右.rs`，`maxs = max(左.maxs, 右.maxs)`。左半末尾 `{S.now.left.rc}` 与右半开头 `{S.now.right.lc}` "
                                                         + ('==相同==，可能跨中点拼接' if S.now.left.rc == S.now.right.lc else f'==不同==：不拼接，保持 `ls={S.now.ls}`，`rs={S.now.rs}`，`maxs={S.now.maxs}`')),
        'if now.ls == mid - l + 1': lambda S, B, r: f"左半整段都是同一字符吗？`ls = {S.now.ls}` 对比左半长度 `{S.mid - S.now.l + 1}` → " + ('==是==，ls 能延伸到右半' if S.now.ls == S.mid - S.now.l + 1 else '否，ls 不变'),
        'if now.ls == mid - now.l + 1': lambda S, B, r: f"左半整段都是同一字符吗？`ls = {S.now.ls}` 对比左半长度 `{S.mid - S.now.l + 1}` → " + ('==是==，ls 能延伸到右半' if S.now.ls == S.mid - S.now.l + 1 else '否，ls 不变'),
        'now.ls += now.right.ls': '`ls += 右.ls` → ls = =={now.ls}==',
        'if now.rs == r - mid': lambda S, B, r: f"右半整段都是同一字符吗？`rs = {S.now.rs}` 对比右半长度 `{S.r - S.mid}` → " + ('==是==，rs 能延伸到左半' if S.now.rs == S.r - S.mid else '否，rs 不变'),
        'if now.rs == now.r - mid': lambda S, B, r: f"右半整段都是同一字符吗？`rs = {S.now.rs}` 对比右半长度 `{S.now.r - S.mid}` → " + ('==是==，rs 能延伸到左半' if S.now.rs == S.now.r - S.mid else '否，rs 不变'),
        'now.rs += now.left.rs': '`rs += 左.rs` → rs = =={now.rs}==',
        'now.maxs = max(now.maxs, now.left.rs': '跨中点的段 = 左.rs `{now.left.rs}` + 右.ls `{now.right.ls}` = `{now.left.rs + now.right.ls}`，`maxs` → =={now.maxs}==',
        'now.lc = now.rc = v': '到达叶子：字符改成 `{v}`',
        'if p <= mid': lambda S, B, r: f'`p = {S.p}` ' + ('≤' if S.p <= S.mid else '>') + f' `mid = {S.mid}`：位置在' + ('左' if S.p <= S.mid else '右') + '半，往那边走，回溯时重新合并',
        'for index in range': lambda S, B, r: (f"查询都处理完了，答案 `{S.res}`" if B.get('index') == S.index else (f"上一次答案 `{S.res[-1]}`；" if S.res else '') + f"第 `{S.index}` 次查询：把下标 `{S.queryIndices[S.index]}` 改成 `{S.queryCharacters[S.index]}`"),
        'res.append(tree.query': '`tree.query`：先沿路径把字符改掉并重新合并，最后返回根节点的 `maxs`，这就是整个字符串的答案',
    },
    cards=dict(
        one_liner='区间合并时只看中点两侧：lc/rc 判断能不能拼，ls/rs 记两头的连续长度',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['字符串 `s`，`k` 次单点修改：`s[queryIndices[i]] = queryCharacters[i]`',
                 '每次修改后，求只由单个字符重复的最长子串长度',
                 '示例：`s="babacc"`，改 3 次 → `[3,3,4]`',
                 '本视频：`s="aabbc"`，改 `s[2]`、`s[3]` 为 `a` → `[3,4]`'],
        quote='常规的线段树无法处理本题要求的单个字符重复的最长子串，需要进行特殊处理。',
        quote_src='—— yiduobo 题解',
        idea=['区间 `[l, r]` 的答案三种来源：左半、右半、==横跨中点==',
              '横跨中点 = 左半的 `rs` + 右半的 `ls`，前提：左半 `rc` == 右半 `lc`',
              '`ls` 要延伸：左半 `ls` 等于左半长度（整段同字符）且中点两侧字符相同；`rs` 对称',
              '每个节点存 `lc / rc / ls / rs / maxs`，修改后只重算一条路径'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`；每次查询 = 单点修改 + 读根节点 `maxs`',
                 '易错：`ls / rs` 的延伸条件是「整段同字符」，不是「两侧字符相同」就够',
                 '和灵神的区别：yiduobo 用节点对象存 `lc / rc`，灵神用 `_s[m] == _s[m+1]` 判断',
                 '原文可直接在 Python 3 运行，未做修改'],
    ),
)
