_POS = {1: (0.08, 0.1), 2: (0.4, 0.1), 3: (0.08, 0.9), 4: (0.4, 0.9)}
_E = [(1, 2), (3, 4)]


def _gdraw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '填充 = 黑白染色（蓝 0 / 粉 1）　黄圈 = 本轮已访问　橙环 = 当前层　绿环 = 刚入队', 21, T['muted'], bold=True)
    W, Hh = x1 - x0 - 300, y1 - y0 - 150
    pt = {k: (x0 + 90 + p[0] * W, y0 + 80 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    color = inn.get('color') or {}
    q = inn.get('q') or []
    head, tail = inn.get('head'), inn.get('tail')
    for u, v in _E:
        cv.line([pt[u], pt[v]], T['dim'], 4)
    for k, (px, py) in pt.items():
        fill, tc = T['panel2'], T['text']
        if color.get(k) == 0:
            fill, tc = T['blue'], T['bg']
        elif color.get(k) == 1:
            fill, tc = T['pink'], T['bg']
        ol, w = T['border'], 3
        if k in color:
            ol, w = T['yellow'], 5
        if head is not None and tail is not None and k in q[head:tail]:
            ol, w = T['orange'], 7
        elif tail is not None and k in q[tail:]:
            ol, w = T['green'], 7
        cv.d.ellipse((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=ol, width=w)
        cv.text((px, py), k, 32, tc, anchor='mm', bold=True)


def _info(S):
    inn = S.get('_inner', {})
    if 'part_len' in inn and 'start' in inn:
        return f"从起点 `{inn['start']}` 做 BFS，已走 ==`{inn['part_len']}`== 轮；各连通分量当前最长 `{S.get('len_dict', {})}`"
    return '每个连通分量取最长的 BFS 轮数，再相加'


CONFIG = dict(
    num=2493, title='将节点分成尽可能多的组', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='黑白染色 + 每点 BFS 拉伸分量',
    tags=['灵神题单·图论算法', '难度分 2415'],
    code='''
class Solution(object):
    def magnificentSets(self, n, edges):

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        part = 0
        len_dict = {}
        belong_part = {}
        for start in range(1, n + 1):
            part_len = 0
            if start not in belong_part:
                belong_part[start] = part
                part += 1
            color = {start : 0}
            q = [start]
            head, tail = 0, 1
            while head < tail:
                part_len += 1
                for now in q[head : tail]:
                    for next in g.get(now, set()):
                        if next not in color:
                            color[next] = 1 - color[now]
                            q.append(next)
                        elif color[next] == color[now]:
                            return -1
                        if next not in belong_part:
                            belong_part[next] = belong_part[start]
                
                head, tail = tail, len(q)

            len_dict[belong_part[start]] = max(len_dict.get(belong_part[start], 0), part_len)
        
        return sum(len_dict.values())
''',
    call='Solution().magnificentSets(4, [[1, 2], [3, 4]])',
    expect=4,
    views=[
        dict(type='custom', draw=_gdraw, h=330),
        dict(type='text', fn=_info, size=22, h=60),
        dict(type='map', var='belong_part', label='belong_part（点 → 连通分量编号）', h=100, font=24),
        dict(type='map', var='len_dict', label='len_dict（分量 → 最多能分几组）', h=100, font=24),
    ],
    watch=[('start', 'start', 'blue'), ('part_len', 'part_len', 'orange'), ('head', 'head', 'yellow'), ('tail', 'tail', 'yellow')],
    skip=['for x, y in edges', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add', 'g[y].add',
          'for now in q[head', 'for next in g.get', 'part_len = 0', 'len_dict = {}', 'belong_part = {}'],
    captions={
        'g = {}': '`g` 是邻接表：点 → 邻居集合（边已建好）',
        'part = 0': '`part` 给连通分量编号，`len_dict` 记每个分量最多能分几组',
        'start not in belong_part': lambda S, B, r: (f'起点 `{S.start}` 还不属于任何分量 → 新分量' if S.start not in S.belong_part
                                                     else f'起点 `{S.start}` 已属于分量 `{S.belong_part[S.start]}`，仍要以它为起点 BFS 一遍（起点不同，层数不同）'),
        'belong_part[start] = part': '`{start}` 属于新分量 `{part}`',
        'part += 1': '下个新分量编号加一：`part = {part}`',
        'color = {start : 0}': '本轮 BFS 的染色表，起点染 `0`；==每个起点都重新来一遍==',
        'q = [start]': '队列从起点开始：`q = {q}`',
        'head, tail = 0, 1': '`q[head:tail]` = 当前这一层：`{q[head:tail]}`',
        'while head < tail': lambda S, B, r: (f'当前层 `{S.q[S.head:S.tail]}` 非空 → 处理这一层' if S.head < S.tail
                                              else f'没有新层了，BFS 结束：共 `{S.part_len}` 轮 = 这个起点能拉出的组数'),
        'part_len += 1': '又算一层：`part_len` = =={part_len}==',
        'next not in color': lambda S, B, r: (
            f'邻居 `{S.next}` 还没染色 → 放进下一层' if S.next not in S.color else f'邻居 `{S.next}` 本轮已染色，检查颜色是否冲突'),
        'color[next] = 1 - color[now]': '`{next}` 染成和 `{now}` 相反的色：`color[{next}] = {color[next]}`',
        'q.append(next)': '`{next}` 入队：`q = {q}`',
        'color[next] == color[now]': lambda S, B, r: (
            f'相邻两点同色（都是 `{S.color[S.now]}`）→ ==奇环==，不是二分图，返回 -1' if S.color[S.next] == S.color[S.now]
            else f'`{S.now}` 与 `{S.next}` 颜色不同，没问题'),
        'next not in belong_part': lambda S, B, r: (
            f'`{S.next}` 还没记分量 → 记成和起点同一分量' if S.next not in S.belong_part else f'`{S.next}` 已有分量编号，不用记'),
        'belong_part[next] = belong_part[start]': '`{next}` 归入分量 `{belong_part[next]}`',
        'head, tail = tail, len(q)': '这一层处理完：新层是 `q[{head}:{tail}]` = `{q[head:tail]}`',
        'len_dict[belong_part[start]] = max': '分量 `{belong_part[start]}` 取各起点轮数的最大值 → `len_dict` = `{len_dict}`',
        'return sum': '各分量最大层数相加 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='先黑白染色判二分图，再把每个分量尽量拉长',
        complexity='时间 `O(n(n+m))`，空间 `O(n+m)`',
        problem=['`n` 个点（编号 1..n）的无向图，可能不连通；分到编号 1..m 的组里',
                 '每条边两端所在组编号必须恰好差 `1`；求最大 `m`，不可能返回 `-1`',
                 '示例（改小）：`n=4`，边 `[[1,2],[3,4]]` → `4`'],
        quote='题目中的图必须是一个二分图，其中不能存在长度为奇数的简单环。……对于图中的每个连通分量，将这个连通分量拉得尽可能长，然后将每个连通分量拉伸的长度相加作为最终答案。',
        quote_src='—— yiduobo 题解',
        idea=['相邻点要放进相邻的组：有奇数长度的环就不可能 → 黑白染色检测，冲突返回 `-1`',
              '不同连通分量==串联==而不是并联，才能让总组数最多',
              '拉伸 = 从分量里每个点出发 BFS，一层一组，取最大轮数；染色和拉伸合在同一趟 BFS 里'],
        result='两个分量各 2 组，共 4 组',
        summary=['时间 `O(n(n+m))`，空间 `O(n+m)`',
                 '每个点都要当一次起点，`color` 每轮重建；`belong_part` 只记第一次的分量',
                 '`head, tail` 圈出当前层：`q[head:tail]`，处理完一层再更新',
                 '同色相邻 = 奇环，立刻 `return -1`',
                 '原文已可在 Python 3 运行（`next` 只是变量名），未作修改'],
    ),
)
