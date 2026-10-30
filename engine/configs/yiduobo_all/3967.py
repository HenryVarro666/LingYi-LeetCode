# 示例：n=4, edges=[[0,1],[0,2],[2,3]], baseTime=[2,3,1,4]
BASE_ = [2, 3, 1, 4]
POS_ = {0: (0.5, 0.10), 1: (0.2, 0.50), 2: (0.78, 0.50), 3: (0.78, 0.90)}
EDGE_ = [(0, 1), (0, 2), (2, 3)]
LEFT_ = (1,)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 150, y1 - y0 - 130
    P = {k: (x0 + 75 + v[0] * W, y0 + 65 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('now'), inn.get('nxt')
    cv.text((x0 + 18, y0 + 4), 'b 基础时间 · f 以 0 为根 · h 换根修正 · res 以它为根；黄框 now，粉框 nxt', 22, T['muted'], bold=True)
    for a, b in EDGE_:
        hot = (cx, cy) in ((a, b), (b, a))
        cv.line([P[a], P[b]], T['yellow'] if hot else T['border'], 6 if hot else 3)
    f, h, res = S.get('f'), S.get('h'), S.get('res')
    for k, (px, py) in P.items():
        cv.rect((px - 24, py - 24, px + 24, py + 24), fill=T['panel2'], outline=T['blue'], width=3, r=24)
        if k == cx:
            cv.rect((px - 32, py - 32, px + 32, py + 32), outline=T['yellow'], width=5, r=32)
        if k == cy:
            cv.rect((px - 32, py - 32, px + 32, py + 32), outline=T['pink'], width=5, r=32)
        cv.text((px, py), k, 28, T['text'], anchor='mm', bold=True)
        lines = [(f'b={BASE_[k]}', T['muted'])]
        if f is not None and f[k] is not None:
            lines.append((f'f={f[k]}', T['cyan']))
        if h is not None and h[k] is not None:
            lines.append((f'h={h[k]}', T['pink']))
        if res is not None and res[k] is not None:
            lines.append((f'res={res[k]}', T['orange']))
        left = k in LEFT_
        for i, (s, c) in enumerate(lines):
            cv.text((px - 38 if left else px + 38, py - 30 + i * 25), s, 22, c, anchor='rm' if left else 'lm', bold=True, mono=True)


CAPS = {
    'dfs(0, -1)': '第一遍：以 0 为根，自底向上算每个任务的完成时间 `f`',
    'f[now] = baseTime[now]': '`{now}` 是叶子：完成时间就是 `baseTime[{now}]` = =={f[now]}==',
    'earliest = f[nxt]': '孩子 `{nxt}` 的 `f = {f[nxt]}`，是目前最小的 → `earliest = {earliest}`',
    'latest = f[nxt]': '孩子 `{nxt}` 的 `f = {f[nxt]}`，是目前最大的 → `latest = {latest}`',
    'f[now] = latest +': '`f[{now}] = latest + (latest − earliest) + base` = {latest} + ({latest} − {earliest}) + {baseTime[now]} = =={f[now]}==',
    'calc(0, -1)': '第二遍：换根。`res[i]` = 以 `i` 为根时的完成时间，`h[i]` = `i` 挂到某个孩子下面后的完成时间',
    'first_e, second_e = f[nxt]': '孩子 `{nxt}`（`f={f[nxt]}`）成为新的最小：`first_e = {first_e}`，旧最小退为次小 `{second_e}`',
    'second_e = f[nxt]': '孩子 `{nxt}`（`f={f[nxt]}`）不是最小，只更新次小：`second_e = {second_e}`',
    'first_l, second_l = f[nxt]': '孩子 `{nxt}`（`f={f[nxt]}`）成为新的最大：`first_l = {first_l}`，旧最大退为次大 `{second_l}`',
    'second_l = f[nxt]': '孩子 `{nxt}`（`f={f[nxt]}`）不是最大，只更新次大：`second_l = {second_l}`',
    'first_e, second_e = h[fa]': '父亲 `{fa}` 也成了 `{now}` 的孩子，它的修正值 `h[{fa}] = {h[fa]}` 要一起参与：最小 `first_e = {first_e}`',
    'second_e = h[fa]': '父亲的修正值 `h[{fa}] = {h[fa]}`：成为次小 `second_e = {second_e}`',
    'first_l, second_l = h[fa]': '父亲的修正值 `h[{fa}] = {h[fa]}`：成为新的最大 `first_l = {first_l}`，次大 `{second_l}`',
    'second_l = h[fa]': '父亲的修正值 `h[{fa}] = {h[fa]}`：成为次大 `second_l = {second_l}`',
    'res[now] = f[now]': '`{now}` 没有任何相邻任务 → `res[{now}] = f[{now}]`',
    'res[now] = first_l': '以 `{now}` 为根：`res[{now}] = {first_l} − {first_e} + {baseTime[now]} + {first_l}` = =={res[now]}==（所有相邻点都当孩子）',
    'e, l = first_e, first_l': '准备把 `{now}` 挂到孩子 `{nxt}` 下面：先取全部孩子的最小 `e = {e}`、最大 `l = {l}`',
    'e = second_e': '`f[{nxt}]` 恰好是最小值 → 去掉它后，最小改用次小 `e = {e}`',
    'l = second_l': '`f[{nxt}]` 恰好是最大值 → 去掉它后，最大改用次大 `l = {l}`',
    'h[now] = baseTime[now]': '`{now}` 去掉 `{nxt}` 后没有别的孩子 → 是叶子，`h[{now}] = baseTime[{now}]`',
    'h[now] = l - e': '`{now}` 挂到 `{nxt}` 下后的完成时间：`h[{now}] = {l} − {e} + {baseTime[now]} + {l}` = =={h[now]}==',
    'return min(res)': '取所有根里最小的完成时间 `min(res)` = ==7==',
}

CONFIG = dict(
    num=3967, title='任务完成时间II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换根 DP · 最大/次大 + 最小/次小',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def finishTime(self, n, edges, baseTime):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [None] * n
        h = [None] * n
        res = [None] * n

        def dfs(now, fa):
            earliest = None
            latest = None
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                if earliest is None or earliest > f[nxt]:
                    earliest = f[nxt]
                if latest is None or latest < f[nxt]:
                    latest = f[nxt]
            
            if earliest is None:
                f[now] = baseTime[now]
            else:
                f[now] = latest + (latest - earliest) + baseTime[now]
        
        def calc(now, fa):
            first_e, second_e = None, None
            first_l, second_l = None, None
            for nxt in g[now]:
                if nxt == fa:
                    continue

                if first_e is None or first_e > f[nxt]:
                    first_e, second_e = f[nxt], first_e
                elif second_e is None or second_e > f[nxt]:
                    second_e = f[nxt]
                
                if first_l is None or first_l < f[nxt]:
                    first_l, second_l = f[nxt], first_l
                elif second_l is None or second_l < f[nxt]:
                    second_l = f[nxt]

            if fa != -1:
                if first_e is None or first_e > h[fa]:
                    first_e, second_e = h[fa], first_e
                elif second_e is None or second_e > h[fa]:
                    second_e = h[fa]

                if first_l is None or first_l < h[fa]:
                    first_l, second_l = h[fa], first_l
                elif second_l is None or second_l < h[fa]:
                    second_l = h[fa]
            
            if first_e is None:
                res[now] = f[now]
            else:
                res[now] = first_l - first_e + baseTime[now] + first_l

            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                e, l = first_e, first_l
                if f[nxt] == e:
                    e = second_e
                if f[nxt] == l:
                    l = second_l
                
                if e is None:
                    h[now] = baseTime[now]
                else:
                    h[now] = l - e + baseTime[now] + l
                
                calc(nxt, now)

        dfs(0, -1)
        calc(0, -1)
        return min(res)
''',
    call='Solution().finishTime(4, [[0,1],[0,2],[2,3]], [2,3,1,4])',
    expect=7,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=150, hide=('f', 'h', 'res')),
    ],
    watch=['now', 'nxt', 'first_e', 'second_e', 'first_l', 'second_l'],
    skip=['g = [[]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'f = [None]', 'h = [None]', 'res = [None]',
          'earliest = None', 'latest = None', 'first_e, second_e = None', 'first_l, second_l = None',
          'if nxt == fa', 'continue', 'for nxt in g[now]',
          'if earliest is None:', 'if first_e is None:', 'if e is None:', 'if fa != -1:', 'if earliest is None or', 'if latest is None or', 'if first_e is None or', 'elif second_e is None or',
          'if first_l is None or', 'elif second_l is None or'],
    captions=CAPS,
    cards=dict(
        one_liner='大小值一网打尽：最大、次大、最小、次小，换根时绕开自己',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树上每个任务有 `baseTime`，选任一点当根，叶子完成时间 = 自己的 `baseTime`',
                 '非叶子：`latest + (latest − earliest) + baseTime`（`earliest/latest` 是孩子完成时间的最小/最大）',
                 '求所有根里「根的完成时间」的最小值；示例答案 `9`'],
        quote='鉴于题目中计算完成时间涉及到孩子节点完成时间的最小值以及最大值，而换根的过程中，下一个目标根节点可能恰好就是当前节点孩子完成时间中的最小值或者最大值，不能继续使用，因此在这里需要为每个节点维护所有孩子完成时间的最大、次大以及最小、次小值。',
        quote_src='—— yiduobo 题解',
        idea=['先以 0 为根 `dfs`，求每个点的完成时间 `f`',
              '再 `calc` 换根：当前点把所有孩子加上「父亲修正后的 `h[fa]`」，记最大/次大、最小/次小，得到 `res[now]`',
              '递归进孩子 `nxt` 之前：若 `f[nxt]` 恰是最大或最小，就用次大/次小顶替，算出 `now` 挂到 `nxt` 下面时的 `h[now]`'],
        summary=['时间 `O(n)`，空间 `O(n)`；答案取 `min(res)`',
                 '易错：`h[now]` 对每个孩子都要重新算，不是固定值',
                 '`f[nxt] == e` 用来判断「去掉的这个孩子是不是最小值」，最大值同理',
                 '前一题 3965 是只算一个根的简单版；本题加换根'],
    ),
)
