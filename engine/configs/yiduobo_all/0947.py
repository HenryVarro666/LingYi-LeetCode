OFF = 10001
STONES = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _nm(k):
    return f'行{k}' if k < OFF else f'列{k - OFF}'


def _root(fa, k):
    n = 0
    while fa.get(k, k) != k and n < 50:
        k = fa[k]
        n += 1
    return k


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    done = [p for p in S['stones'] if p[0] in fa]
    roots = {_root(fa, p[0]) for p in done}
    if 'res' in S:
        return f'`res` = n − 已数到的根 → ==`{S["res"]}`==（每个连通块的根只数一次）'
    return f'已连入 ==`{len(done)}`== 块石头，当前连通块 ==`{len(roots)}`== 个'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    stones = S['stones']
    fa = S.get('fa', {})
    touched = set(fa) | set(fa.values())
    R = max(p[0] for p in stones) + 1
    C = max(p[1] for p in stones) + 1
    cell = min(130, (x1 - x0 - 200) / max(C, 1), (y1 - y0 - 150) / max(R, 1))
    gx = x0 + (x1 - x0 - cell * (C - 1)) / 2
    gy = y0 + 112
    cv.text((x0 + 18, y0 + 4), '石头（同行 / 同列相连；同色 = 同一连通块，白圈 = 正在处理的石头）', 22, T['muted'], bold=True)
    roots = sorted({_root(fa, p[0]) for p in stones if p[0] in touched})
    col = {}
    for i, r in enumerate(roots):
        col[r] = T[PAL[i % len(PAL)]]
    pos = lambda p: (gx + p[1] * cell, gy + p[0] * cell)
    for r in range(R):
        cv.text((gx - 60, gy + r * cell), f'行{r}', 20, T['dim'], anchor='rm', bold=True)
    for c in range(C):
        cv.text((gx + c * cell, gy - 40), f'列{c}', 20, T['dim'], anchor='mb', bold=True)
    done = [p for p in stones if p[0] in touched]
    for i, a in enumerate(done):
        for b in done[i + 1:]:
            if a[0] == b[0] or a[1] == b[1]:
                cv.line([pos(a), pos(b)], col.get(_root(fa, a[0]), T['muted']), 5)
    cur = [S.get('row'), S.get('col')] if S.get('row') is not None and S.get('col') is not None else None
    for p in stones:
        X, Y = pos(p)
        ok = p[0] in touched
        c = col.get(_root(fa, p[0])) if ok else T['panel2']
        cv.d.ellipse((X - 26, Y - 26, X + 26, Y + 26), fill=c, outline=T['border'])
        cv.text((X, Y), f'{p[0]},{p[1]}', 20, T['bg'] if ok else T['muted'], anchor='mm', bold=True)
        if cur is not None and list(p) == cur:
            cv.d.ellipse((X - 33, Y - 33, X + 33, Y + 33), outline=T['text'], width=4)



CONFIG = dict(
    num=947, title='移除最多的同行或同列石头', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='行列当节点 · 并查集',
    tags=['七、并查集', '§7.3 中介并查集', '难度分 2035'],
    code='''
class Solution(object):
    def removeStones(self, stones):

        fa = {}

        for row, col in stones:
            self.union(row, col + 10001, fa)

        res = len(stones)
        for x in fa:
            if self.find(x, fa) == x:
                res -= 1

        return res

    def union(self, x, y, fa):
        if x not in fa:
            fa[x] = x
        if y not in fa:
            fa[y] = y
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
    
    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)
        
        return fa[x]
''',
    call=f'Solution().removeStones({STONES})',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='map', var='fa', label='fa：行 / 列节点 → 父亲（行 x，列 y + 10001）',
             fmt=lambda k, v: f'{_nm(k)} → {_nm(v)}', h=150, font=26),
        dict(type='text', fn=_info, size=30, h=70),
    ],
    watch=[('row', 'row', 'blue'), ('col', 'col', 'pink'), ('fa_x', 'fa_x', 'blue'), ('fa_y', 'fa_y', 'pink'), ('res', 'res', 'green')],
    skip=['fa = {}', 'if x != fa[x]', 'return fa[x]', 'if x not in fa', 'if y not in fa'],
    captions={
        'for row, col in stones': lambda S, B, r: (f'取石头 `({S.row}, {S.col})`：合并「行 {S.row}」与「列 {S.col}」这两个点'
                                                   if 'row' not in B or (B.row, B.col) != (S.row, S.col) else '所有石头处理完，开始数连通块'),
        'self.union(row': lambda S, B, r: f'调用 `union({B.row}, {B.col + 10001})`',
        'fa[x] = x': '行节点第一次出现，先让它自成一个连通块：`fa[x] = x`',
        'fa[y] = y': '列节点第一次出现，也自成一块：`fa[y] = y`',
        'fa_x = self.find': '找 `x` 的最原始父亲',
        'fa_y = self.find': '找 `y` 的最原始父亲',
        'if fa_x < fa_y': lambda S, B, r: (f'`{_nm(S.fa_x)}` 与 `{_nm(S.fa_y)}` 是同一个根，已经连通' if S.fa_x == S.fa_y
                                           else f'根不同（{_nm(S.fa_x)} 与 {_nm(S.fa_y)}）→ 要合并，约定让编号小的当根'),
        'fa[fa_y] = fa_x': '`fa_y` 挂到 `fa_x` 下：==两个连通块合并==',
        'fa[fa_x] = fa_y': lambda S, B, r: ('两根相同，赋值不改变结构' if S.fa_x == S.fa_y else '`fa_x` 挂到 `fa_y` 下：==两个连通块合并=='),
        'fa[x] = self.find': '路径压缩：递归找到根，让 `fa[x]` 直接指向根',
        'if self.find(x, fa) == x': '`find(x)` 等于 `x` 自己吗？等于就说明它是某个连通块的根',
        'res = len(stones)': '先假设每块石头都能移走：`res = {res}`，下面每找到一个连通块的根就减 1（这块石头必须留下）',
        'for x in fa': '遍历出现过的行 / 列节点 `x`',
        'res -= 1': lambda S, B, r: f'`{_nm(S.x)}` 是自己的根 → 代表一个连通块，留下 1 块石头：`res` → ==`{S.res}`==',
        'return res': '剩下的就是最多能移除的石头数：==`{res}`==',
    },
    max_steps=80,
    cards=dict(
        one_liner='石头当边、行列当点：每个连通块只能留下一块',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['石头在整数坐标上，==同行或同列有别的石头== 才能移除它',
                 '问最多能移除多少块',
                 '示例：`[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]` → `5`'],
        quote='对于石头(x, y)，我们可以看做这块石头在行x以及列y之间连上了一条边，而最后依然是每个连通块中将遗留下一个石头。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想石头当点、同行同列连边：连通块有 `k` 个点，至多删 `k − 1` 个，但建图是 `O(n²)`',
              '换思路：同行同列是多对多关系，==把行和列当节点==，石头是它们之间的一条边',
              '并查集合并 `x` 与 `y + 10001`；根节点个数 = 连通块数，`res = n −` 根数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：行号和列号会重合，列要加 `10001` 偏移',
                 '最后数的是「行 / 列节点」中的根，不是石头；每个连通块恰有一个根',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神把 `find` 写成不存在就返回自己，用集合收集代表元；yiduobo 在 `union` 里先登记再合并'],
    ),
)
