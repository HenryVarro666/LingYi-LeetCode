def _layout(node, depth, pos, out, ch=''):
    """返回节点 x（叶子按顺序编号，内部节点取孩子均值）"""
    kids = list(node[0].items())
    if not kids:
        x = pos[0]
        pos[0] += 1
    else:
        xs = [_layout(c, depth + 1, pos, out, k) for k, c in kids]
        x = sum(xs) / len(xs)
    out.append((node, depth, x, ch))
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'Trie（节点里的数 = 以该节点结尾的字符串编号；黄框 = 正在处理的节点）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    out, pos = [], [0]
    _layout(root, 0, pos, out)
    nl = max(1, pos[0])
    depth = max(d for _, d, _, _ in out)
    W = x1 - x0 - 120
    gx = min(190, W / max(1, nl))
    sx = x0 + 60 + (W - gx * (nl - 1)) / 2
    gy = min(120, (y1 - y0 - 150) / max(1, depth))
    sy = y0 + 90
    P = {id(n): (sx + x * gx, sy + d * gy) for n, d, x, _ in out}
    now = S.get('now')
    for n, d, x, ch in out:
        X, Y = P[id(n)]
        for k, c in n[0].items():
            cx, cy = P[id(c)]
            cv.line([(X, Y + 20), (cx, cy - 20)], T['border'], 3)
            cv.text(((X + cx) / 2 + 12, (Y + cy) / 2), k, 26, T['cyan'], anchor='lm', bold=True, mono=True)
    for n, d, x, ch in out:
        X, Y = P[id(n)]
        cur = n is now
        done = bool(n[1]) and bool(n[0])   # 已合并排序的内部节点
        cv.rect((X - 50, Y - 20, X + 50, Y + 20), fill=T['panel'] if 'panel' in T else None,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 2, r=10)
        lab = ','.join(str(v) for v in n[1]) if n[1] else ('root' if n is root else '')
        cv.text((X, Y), lab, 22 if len(lab) < 8 else 17, T['green'] if n[1] else T['dim'], anchor='mm', bold=True)


def _rev_fn(S):
    if 'rev' not in S or 'chars' not in S:
        return ''
    ch = S['chars']
    parts = []
    for a in range(len(ch)):
        for b in range(len(ch)):
            if a != b:
                parts.append(f"`{ch[a]}` 在 `{ch[b]}` 前：=={S['rev'][a][b]}==")
    return '把左边子树放在右边之前的逆序对数 rev：' + '；'.join(parts)


def _f_fn(S):
    if 'f' not in S or 'chars' not in S or not isinstance(S['f'], list):
        return ''
    ch = S['chars']
    items = []
    for st, v in enumerate(S['f']):
        if st == 0:
            continue
        names = ''.join(ch[i] for i in range(len(ch)) if st >> i & 1)
        items.append(f"f[{{{names}}}] = {'?' if v is None else v}")
    return '状压 DP：' + '，'.join(items)


CONFIG = dict(
    num=4077, title='前缀树中的最小逆序对数目', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='Trie 递归 + 子树归并算逆序 + 状压 DP 排顺序', tags=[],
    code='''
class Solution(object):
    def minInversions(self, words, target):

        root = [{}, []]
        order = [0] * len(target)
        for index, t in enumerate(target):
            order[t] = index

        for index, (w, t) in enumerate(zip(words, target)):
            now = root
            for c in w:
                if c not in now[0]:
                    now[0][c] = [{}, []]
                now = now[0][c]
            
            now[1].append(order[index])

        global res
        res = 0

        def dfs(now):
            if not now[0]:
                return

            for c in now[0]:
                dfs(now[0][c])
            
            chars = list(now[0].keys())
            m = len(chars)
            rev = [[0] * m for _ in range(m)]
            final = now[1][:]

            global res

            for a in range(m):
                tmp = []
                p, q = 0, 0
                o1, o2 = final, now[0][chars[a]][1]
                while p < len(o1) and q < len(o2):
                    if o1[p] < o2[q]:
                        tmp.append(o1[p])
                        p += 1
                    else:
                        tmp.append(o2[q])
                        q += 1
                
                tmp.extend(o1[p:])
                tmp.extend(o2[q:])
                final = tmp[:]

                if now[1]:
                    o1 = now[1]
                    p, q = 0, 0
                    while p < len(o1) or q < len(o2):
                        if q == len(o2) or (p < len(o1) and o1[p] < o2[q]):
                            res += q
                            p += 1
                        else:
                            q += 1

                for b in range(a + 1, m):
                    p, q = 0, 0
                    o1 = now[0][chars[a]][1]
                    o2 = now[0][chars[b]][1]
                    while p < len(o1) or q < len(o2):
                        if p == len(o1) or (q < len(o2) and o2[q] < o1[p]):
                            rev[b][a] += p
                            q += 1
                        else:
                            rev[a][b] += q
                            p += 1
            
            now[1] = final[:]

            max_state = 1 << m
            f = [None] * max_state

            for index in range(m):
                f[1 << index] = 0
            
            for state in range(1, max_state):
                if f[state] is not None:
                    continue
                
                last_candidate = []
                for index in range(m):
                    if state & (1 << index) == (1 << index):
                        last_candidate.append(index)
                
                for last in last_candidate:
                    cost = 0
                    for other in last_candidate:
                        cost += rev[other][last]
                    if f[state] is None or f[state] > f[state ^ (1 << last)] + cost:
                        f[state] = f[state ^ (1 << last)] + cost

            res += f[-1]

        dfs(root)
        return res
''',
    call="Solution().minInversions(['ab', 'ac', 'b'], [1, 2, 0])",
    expect=1,
    max_steps=150,
    skip=['tmp.extend', 'final = tmp[:]', 'tmp = []', 'p, q = 0, 0', 'p += 1', 'q += 1', 'for index in range(m)',
          'order[t] = index', 'now[1].append', 'if c not in now[0]', 'now[0][c] = [{}, []]', 'now = now[0][c]',
          'now = root', 'for c in w', 'last_candidate.append', 'cost += rev', 'if state & (1 << index)', 'o1, o2 =',
          'o1 = ', 'o2 = ', 'while p <', 'if o1[p] < o2[q]', 'tmp.append', 'if q == len(o2)', 'if p == len(o1)',
          'rev[b][a] += p', 'rev[a][b] += q', 'res += q', 'for last in last_candidate', 'if f[state] is not None',
          'last_candidate = []', 'cost = 0', 'f[1 << index] = 0', 'if now[1]:', 'for other in last_candidate', 'continue', 'for b in range', 'for a in range', 'for index, t in enumerate(target)', 'for index, (w, t)', 'order = [0]', 'm = len(chars)'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', size=26, h=90, fn=_rev_fn),
        dict(type='text', size=26, h=80, fn=_f_fn),
        dict(type='calls', label='递归调用栈', h=110, hide=('words', 'target')),
    ],
    watch=[('chars', 'chars', 'cyan'), ('rev', 'rev', 'orange'), ('final', 'final', 'blue'), ('res', 'res', 'green')],
    captions={
        'root = [{}, []]': '建 Trie：节点是 `[孩子字典, 结尾编号列表]`；字符串编号 `order[i]` 记在它的结尾节点上（图中已建好）',
        'res = 0': '`res` 累计全部节点产生的逆序对',
        'if not now[0]': '`dfs`：当前节点{"是叶子，没有孩子要排，返回" if not now[0] else "有孩子，先递归处理每个孩子"}',
        'for c in now[0]': '遍历孩子（当前 `{c}`）：先递归，让它的编号数组先排好序；孩子都处理完就往下算本节点',
        'dfs(now[0][c])': '孩子的子树处理完，回到这一层',
        'chars = list': '当前节点的孩子字符：`{chars}`',
        'rev = [[0]': '`rev[x][y]`：子树 x 排在 y 前面时，两棵子树之间的逆序对数',
        'final = now[1][:]': '`final`：先放本节点自己结尾的编号，之后把各孩子的有序编号数组逐个归并进来；同时两两双指针数出 `rev`',
        'now[1] = final[:]': '本节点所有编号已有序：`{now[1]}`，留给父节点使用',
        'max_state = 1 << m': '`m = {m}` 个孩子，最多 10 个 → 用状态压缩枚举遍历顺序',
        'f = [None] * max_state': '`f[state]`：已遍历 state 里这些子树时的最少逆序对数',
        'for state in range': '状态 `{state}`（二进制 {bin(state)[2:]}）：枚举最后遍历哪棵子树',
        'if f[state] is None or f[state] > ': '`last` 排最后：`f[{state ^ (1 << last)}] + cost` = `{f[state ^ (1 << last)] + cost}`，取最小',
        'f[state] = f[state ^ (1 << last)] + cost': '更新 `f[{state}] = {f[state]}`',
        'res += f[-1]': '所有孩子都遍历完，最少逆序对 `f[-1] = {f[-1]}` → 加进全局 `res`',
        'return res': '全部节点处理完，最少逆序对 =={res}==',
    },
    cards=dict(
        one_liner='Trie 每层孩子的顺序互不影响：逐层状压 DP',
        complexity='时间 `O(10·n·L + 2^10·10·10)`，空间 `O(n·L)`',
        problem=['`words` 里 n 个互不相同的字符串（字母 a~j），`target` 是 0~n-1 的排列',
                 '`words[i]` 的编号是 `p`，满足 `target[p] = i`',
                 '用 words 建 Trie，先序遍历，每个节点可任选孩子顺序；首次遇到字符串结尾时记下编号',
                 '求得到的编号数组里最少有多少逆序对',
                 '本视频：`words = [ab, ac, b]`，`target = [1,2,0]` → `1`'],
        quote='由于题目中是通过先序遍历获取编号数组的，那么就意味着不同子树包含的字符串的编号必然是互相隔离开的。这样一来，就可以逐个节点递归计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['先序遍历里每棵子树的编号连成一段：各节点的孩子排序互不干扰',
              '一个节点最多 10 个孩子 → 状压 DP：`f[state]` 枚举最后遍历哪棵子树',
              '两棵子树之间的逆序对 `rev[x][y]`，像归并排序一样双指针算；归并后顺便得到有序编号数组'],
        summary=['时间约 `O(10·n·L)` 算 rev，加每个节点 `O(2^m·m^2)` 的状压 DP，空间 `O(n·L)`',
                 '易错：字符串恰好在当前节点结束时，它排在所有子树之前，要额外算它和子树的逆序对（代码里 `if now[1]` 那段）',
                 '易错：算完 rev 还要把编号归并成有序数组交给父节点',
                 '`f[x] > f[...] + cost` 取最小；只有一个孩子时 `f` 直接为 0',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
