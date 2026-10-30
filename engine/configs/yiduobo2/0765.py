ROW = [0, 3, 2, 5, 4, 1, 6, 7]
_CC = ['blue', 'pink', 'green', 'purple']


def _rcolor(S, i, v):
    return _CC[v // 2 % 4]


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    row = S.get('row') or ROW
    n = len(row) // 2
    g = S.get('g') or {}
    used = S.get('used')
    now = S.get('now')
    cv.text((x0 + 18, y0 + 4), '座位图（节点 = 座位 index，边 = 一对情侣分坐两处；绿 = 已访问，黄 = now）', 22, T['muted'], bold=True)
    w = min(220, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - w * n) / 2
    cy = y1 - 70
    pts = []
    for i in range(n):
        cx = sx + i * w + w / 2
        pts.append(cx)
    drawn = set()
    for a, nb in g.items():
        for b in nb:
            if a == b:
                cv.text((pts[a], cy - 62), '自环：已配对', 20, T['dim'], anchor='mb', bold=True)
                continue
            key = (min(a, b), max(a, b))
            if key in drawn:
                continue
            drawn.add(key)
            d = abs(a - b)
            lift = 40 + 70 * (d - 1)
            off = w * 0.18 if d == 1 else -w * 0.18
            col = T['green'] if used and used[a] and used[b] else T['muted']
            cv.arc_arrow((pts[key[0]] + off, cy - 46), (pts[key[1]] - off, cy - 46), lift, col, width=4, frac=0.975)
    for i in range(n):
        cx = pts[i]
        fill = T['panel2']
        out = T['border']
        if used and used[i]:
            fill = (30, 70, 40)
            out = T['green']
        if now == i and 'now' in S:
            out = T['yellow']
        cv.rect((cx - w * 0.38, cy - 46, cx + w * 0.38, cy + 40), fill=fill, outline=out, width=4, r=12)
        a, b = row[2 * i], row[2 * i + 1]
        cv.text((cx - 22, cy - 4), a, 30, T[_CC[a // 2 % 4]], anchor='mm', bold=True)
        cv.text((cx + 22, cy - 4), b, 30, T[_CC[b // 2 % 4]], anchor='mm', bold=True)
        cv.text((cx, cy + 46), f'座位 {i}', 20, T['muted'], anchor='mt', bold=True)


def _for_idx(S, B, ret):
    i = S.get('index')
    if i is None or (i == B.get('index') and 'index' in B):
        return '遍历结束'
    return f'看座位 `{i}`：坐着 `{S.row[2 * i]}` 和 `{S.row[2 * i + 1]}`'


def _while_next(S, B, ret):
    if S.get('move_flag'):
        return f'`{S.now}` 还没访问过 → 沿边走过去，交换次数 `res` → =={S.res}=='
    return f'座位 `{S.now}` 的邻居都访问过 → 环走完了'


CONFIG = dict(
    num=765, title='情侣牵手', difficulty='Hard', category='图论',
    author='yiduobo', technique='座位建图 · 长度为 k 的环交换 k−1 次',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def minSwapsCouples(self, row):
        n = len(row) // 2
        pos_dict = {}
        for index in range(n):
            p1 = row[index * 2] // 2
            p2 = row[index * 2 + 1] // 2
            if p1 not in pos_dict:
                pos_dict[p1] = []
            pos_dict[p1].append(index)
            if p2 not in pos_dict:
                pos_dict[p2] = []
            pos_dict[p2].append(index)

        g = {}
        for x, y in pos_dict.values():
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        used = [False] * n
        res = 0
        for index in range(n):
            if not used[index]:
                now = index
                move_flag = True
                while move_flag:
                    used[now] = True
                    move_flag = False
                    for next in g[now]:
                        if not used[next]:
                            res += 1
                            now = next
                            move_flag = True
                            break

        return res
''',
    call=f'Solution().minSwapsCouples({ROW})',
    expect=2,
    skip=['if p1 not in pos_dict', 'if p2 not in pos_dict', 'pos_dict[p1] = []', 'pos_dict[p2] = []',
          'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add(y)',
          'move_flag = False', 'move_flag = True', 'now = index'],
    views=[
        dict(type='array', var='row', label='row（同色 = 同一对情侣；相邻两格 = 一个座位）', cell=90, h=150,
             color=_rcolor),
        dict(type='map', var='pos_dict', label='pos_dict（情侣编号 → 两人所在座位）',
             fmt=lambda k, v: f'{k} → {v}', h=100),
        dict(type='custom', draw=_graph, h=300),
        dict(type='array', var='used', label='used（座位是否访问过）', cell=70, h=130,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('index', 'index'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len(row) // 2': '`n = {n}` 个座位：固定是 (0,1)、(2,3)…，==不是任意相邻==',
        'pos_dict = {}': '`pos_dict`：每对情侣（编号 = 人 // 2）坐在哪两个座位',
        5: _for_idx,
        'p1 = row[index * 2] // 2': '左边的人 `{row[index * 2]}` 属于情侣 `{p1}`',
        'p2 = row[index * 2 + 1] // 2': '右边的人 `{row[index * 2 + 1]}` 属于情侣 `{p2}`',
        'pos_dict[p1].append(index)': '情侣 `{p1}` 有人坐在座位 `{index}` → `{pos_dict[p1]}`',
        'pos_dict[p2].append(index)': '情侣 `{p2}` 有人坐在座位 `{index}` → `{pos_dict[p2]}`',
        'g = {}': '建图：一对情侣分坐座位 x、y → x、y 之间连边（==一次交换的方向==）',
        'for x, y in pos_dict.values()': lambda S, B, ret: (f'情侣坐在座位 `{S.x}` 和 `{S.y}`' + (' → 同座 = 自环，已配对' if S.x == S.y else ' → 连边')
                                                            if 'x' in S and (S.get('x'), S.get('y')) != (B.get('x'), B.get('y')) or 'x' not in B and 'x' in S
                                                            else '图建好了：每个点度数为 2，图由若干==环==组成'),
        'g[y].add(x)': '连边 `{x} — {y}`',
        'used = [False] * n': '`used` 记录座位是否访问过',
        'res = 0': '`res`：交换次数',
        26: lambda S, B, ret: (f'从座位 `{S.index}` 出发' if S.get('index') != B.get('index') or 'used' not in B
                               else '所有环都走完了'),
        'if not used[index]': lambda S, B, ret: (f'座位 `{S.index}` 没访问过 → 从它出发走一圈环' if not S.used[S.index]
                                                 else f'座位 `{S.index}` 已在之前的环里 → 跳过'),
        'while move_flag': lambda S, B, ret: ('继续沿着环走' if S.move_flag else '这个环走完了'),
        'used[now] = True': '标记座位 `{now}` 已访问',
        'for next in g[now]': lambda S, B, ret: (f'座位 `{S.now}` 的邻居都看完了，没有可走的' if 'next' in B and B.next == S.next
                                                 else f'看座位 `{S.now}` 的邻居 `{S.next}`'),
        'if not used[next]': lambda S, B, ret: (f'邻居 `{S.next}` 没访问过 → 走过去' if not S.used[S.next]
                                                else f'邻居 `{S.next}` 已访问'),
        'res += 1': '每走到环上一个新座位，==相当于和上一个座位交换一次== → `res = {res}`',
        'now = next': '`now` → `{now}`',
        'break': '只走一条边，继续从 `{now}` 往下走',
        'return res': '长度 3 的环交换 2 次，自环 0 次 → 返回 `{ret}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='把座位看成点、情侣看成边：长度为 k 的环要交换 k−1 次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`2n` 个人坐成一排，`row[i]` 是第 i 个位置上的人，`(2k, 2k+1)` 是一对情侣',
                 '每次可交换任意两人，求让每对情侣==并肩坐==（座位 (0,1)、(2,3)…）的最少交换次数',
                 '示例：`[0,2,1,3]` → `1`；本视频：`[0,3,2,5,4,1,6,7]` → `2`'],
        quote='如果将每个座位看做图中的一个点，那么两种交换方式就可以在图中连出两条边，那么最终就可以得到一个图，其中存在一些环。对于一个长度为k的环，最优的情况就是经过k - 1次交换使得这k对情侣配对成功。',
        quote_src='—— yiduobo 题解',
        idea=['座位固定是 (0,1)、(2,3)…，不成对的座位只有==两种==交换方式',
              '一对情侣分坐座位 x、y → 连边 x—y；每个点度数 2，图是若干个环',
              '从未访问的点出发沿环走，每到一个新点 `res += 1`，即环长 − 1'],
        result='座位 0、1、2 成一个环（交换 2 次），座位 3 已配对 → 返回 `2`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`len(row) / 2`、`row[...] / 2` 的整除已改为 `//`',
                 '已配对的座位会得到自环 `{i}`，走不出去，贡献 0',
                 '易错：情侣座位是固定的 (2k, 2k+1)，不是“任意相邻两人”',
                 '同类：把数字 i 放到第 i 位的最少交换次数，也是“环长 − 1”'],
    ),
)
