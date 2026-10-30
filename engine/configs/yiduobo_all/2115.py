import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


POS = {'yeast': (0.0, 0.2), 'flour': (0.0, 0.8),
       'bread': (0.5, 0.5), 'sandwich': (1.0, 0.5)}


def _name(S, num):
    for k, v in S['mapping_dict'].items():
        if v == num:
            return k
    return None


def _draw(cv, S, B, box, T):
    md = S.get('mapping_dict', {})
    rec = S.get('recipes', [])
    g = S.get('g', {})
    edges, st, sub = [], {}, {}
    for num, outs in g.items():
        a = _name(S, num)
        for i in outs:
            edges.append((a, rec[i]))
    q, used, ind = S.get('q'), S.get('used'), S.get('ind')
    for k in POS:
        if k not in md:
            continue
        num = md[k]
        if q is not None and num in q:
            st[k] = 'cyan'
        if used is not None and num in used and k in rec:
            st[k] = 'green'
        if k in rec and ind is not None and num < len(ind):
            sub[k] = '' if st.get(k) == 'green' else f'还缺 {ind[num]}'
    hot = None
    if 'now' in S and 'next' in S and 42 <= S.get('_line', 0) <= 46 and q is not None:
        hot = (_name(S, S['now']), rec[S['next']])
    _gdraw(cv, box, T, POS, edges, st, sub, hot, '节点 = 材料 / 菜；青 = 在队列里；绿 = 能做出的菜')


def _k(S):
    """当前这次出队里，已经处理过几个依赖它的菜；以及依赖它的菜列表"""
    ING = [2, 1]
    dec = sum(ING) - sum(S['ind'])
    before = sum(len(S['g'].get(p, ())) for p in S['q'][:S['l'] - 1])
    return dec - before, list(S['g'].get(S['now'], ()))


def _nm(S):
    inv = {v: k for k, v in S['mapping_dict'].items()}
    return lambda i: inv.get(i, str(i))


CONFIG = dict(
    num=2115, title='从给定原材料中找到所有可以做出的菜', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='字符串映射成编号 · 数组模拟拓扑排序',
    tags=['灵神题单', '图论算法', '难度分 1679'],
    code='''
class Solution(object):
    def findAllRecipes(self, recipes, ingredients, supplies):

        mapping_dict = {}

        n = len(recipes)
        for index in range(n):
            mapping_dict[recipes[index]] = index
        
        g = {}
        cnt = n
        ind = []
        for index in range(n):
            ind.append(len(ingredients[index]))
            for info in ingredients[index]:
                if info not in mapping_dict:
                    mapping_dict[info] = cnt
                    cnt += 1
                
                num = mapping_dict[info]
                if num not in g:
                    g[num] = set()
                g[num].add(index)

        q = []
        used = set()
        for info in supplies:
            if info not in mapping_dict:
                mapping_dict[info] = cnt
                cnt += 1
            
            num = mapping_dict[info]
            q.append(num)
            used.add(num)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    used.add(next)
                    r += 1
        
        res = []
        for index in range(n):
            if index in used:
                res.append(recipes[index])
        
        return res
''',
    call="Solution().findAllRecipes(['bread','sandwich'], [['yeast','flour'],['bread']], ['yeast','flour'])",
    expect=['bread', 'sandwich'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='mapping_dict', label='mapping_dict（名字 → 编号，菜在前）', h=100),
        dict(type='array', var='q', label='q（编号；l 指向队首，r 是队尾后一位）', pointers={'l': 'blue', 'r': 'pink'}, h=170),
    ],
    watch=[('ind', 'ind', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('used', 'used', 'green'), ('res', 'res', 'cyan')],
    skip=['mapping_dict = {}', 'cnt = n', 'cnt += 1', 'ind = []', 'q = []', 'used = set()', 'res = []', 'n = len(recipes)', 'num = mapping_dict[info]', 'if num not in g', 'r += 1', 'used.add(num)'],
    max_steps=110,
    captions={
        'mapping_dict[recipes[index]] = index': '菜名 `{recipes[index]}` 编号 `{index}`（菜占 `0 ~ n-1`）',
        'ind.append': '`{recipes[index]}` 需要 `{len(ingredients[index])}` 种材料 → 入度 `{ind}`',
        'if info not in mapping_dict': lambda S, B, r: (f'`{S.info}` 还没有编号，先分配' if S.info not in S.mapping_dict
                                                         else f'`{S.info}` 已经有编号了，不重复分配'),
        'mapping_dict[info] = cnt': '新材料 `{info}` 的编号 = `{cnt}`',
        'num = mapping_dict[info]': '`{info}` 的编号是 `{num}`',
        'g[num] = set()': '给编号 `{num}` 建出边集合',
        'g[num].add(index)': '边：材料 `{num}` → 菜 `{index}`：`g` = {g}',
        'q.append(num)': '初始材料 `{info}`（编号 `{num}`）入队并记入 `used`：它==不缺任何东西==',
        'l = 0': '`l` 队首，`r` 队尾后一位：`[l, r)` 里是待处理的编号',
        'r = len(q)': '`r = len(q) = {r}`：初始材料全部在队里',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，队列非空' if S.l < S.r else f'`l = {S.l}` ≥ `r = {S.r}`：队列处理完 → 结束'),
        'now = q[l]': lambda S, B, r_: f'队首 `now = {S.now}`（{_nm(S)(S.now)}）',
        'for next in g.get': lambda S, B, r_: (lambda kk, lst: (
            f'`{_nm(S)(S.now)}` 没有被任何菜依赖，直接跳过' if not lst else
            '依赖它的菜都处理完了，回到 while' if kk >= len(lst) else
            (f'看谁依赖 `{_nm(S)(S.now)}`：`{_nm(S)(lst[kk])}`' if kk == 0 else f'下一道依赖它的菜：`{_nm(S)(lst[kk])}`')))(*_k(S)),
        'ind[next] -= 1': lambda S, B, r_: f'`{_nm(S)(S.now)}` 就绪：`{_nm(S)(S.next)}` 还缺 `{S.ind[S.next]}` 种',
        'if ind[next] == 0': lambda S, B, r_: (f'`ind[{S.next}] = 0`：材料齐了 → ==这道菜能做，入队==' if S.ind[S.next] == 0
                                               else f'`ind[{S.next}] = {S.ind[S.next]}` > 0：还不能做'),
        'used.add(next)': lambda S, B, r_: f'`{_nm(S)(S.next)}` 做得出来：`used` = {S.used}，队尾 `r` 后移',
        'if index in used': lambda S, B, r_: (f'`{S.recipes[S.index]}`（编号 `{S.index}`）在 `used` 里 → 能做' if S.index in S.used
                                              else f'`{S.recipes[S.index]}` 不在 `used` → 做不出'),
        'res.append': '答案加入 `{recipes[index]}`：`{res}`',
        'return res': '按菜单顺序还原菜名：`{res}`',
    },
    cards=dict(
        one_liner='材料连边到菜，拓扑排序走到的菜就是能做的菜',
        complexity='时间 `O(L)`，空间 `O(L)`（L 为材料总数）',
        problem=['`ingredients[i]` 是做 `recipes[i]` 的材料，菜也可以当材料；`supplies` 里的材料无限',
                 '返回所有做得出的菜（顺序任意）',
                 '本视频：`bread` = yeast + flour，`sandwich` = bread → `[bread, sandwich]`'],
        quote='拓扑排序的初始对列为所有的材料，而最终答案就是拓扑排序能够遍历到的菜谱。',
        quote_src='—— yiduobo 题解原文',
        idea=['材料 → 菜连有向边，`ind[菜]` = 需要的材料数',
              '为避免字符串比较，先把名字映射成编号：==菜在前，材料在后==',
              '用数组 + `l`、`r` 模拟队列：初始材料全入队，缺口归零的菜也入队'],
        summary=['时间 `O(L)`：每条「材料 → 菜」的边只处理一次',
                 '菜编号是 `0 ~ n-1`，所以最后直接 `index in used` 即可判断',
                 '用 `set` 存出边，防止同一材料重复计数',
                 '原文本身是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神直接用字符串当键，yiduobo 先映射成编号'],
    ),
)
