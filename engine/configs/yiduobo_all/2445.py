def _heap(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    rev = S['reverse']
    cv.text((x0 + 18, y0 + 4), '完全二叉树：节点 i 的孩子是 2i、2i+1（绿 = 被翻转为 1，黄圈 = 当前节点）', 22, T['muted'], bold=True)
    D = n.bit_length()
    dy = min(110, (y1 - y0 - 100) / max(1, D))
    R = 26
    W = x1 - x0 - 80

    def P(i):
        d = i.bit_length() - 1
        j = i - (1 << d)
        return x0 + 40 + (j + 0.5) / (1 << d) * W, y0 + 80 + d * dy

    cur = S.get('index')
    if cur is None:
        cur = S.get('v')
    for i in range(2, n + 1):
        cv.line([P(i // 2), P(i)], T['border'], 3)
    for i in range(1, n + 1):
        X, Y = P(i)
        on = bool(rev[i])
        outline = T['yellow'] if i == cur else T['border']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if on else T['panel2'], outline=outline,
                     width=5 if i == cur else 2)
        cv.text((X, Y), i, 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + R + 4), '1' if on else '0', 18, T['green'] if on else T['dim'], anchor='mt', mono=True)


def _flip_cap(S, B, ret):
    return f'节点 `{S.v}` 翻转一次：`reverse[{S.v}]` = {S.reverse[S.v]}（出现偶数次会翻回来）'


def _if_rev(S, B, ret):
    if S.reverse[S.index]:
        return f'`reverse[{S.index}]` 为真：节点 {S.index} 当前是 ==1== → 计数，并把翻转往下传'
    return f'`reverse[{S.index}]` 为假：节点 {S.index} 是 0，什么也不传'


def _l(S, B, ret):
    return f'左孩子 `{S.left}`' + ('' if S.left <= S.n else f'，超过 n={S.n}，不存在')


def _r(S, B, ret):
    return f'右孩子 `{S.right}`' + ('' if S.right <= S.n else f'，超过 n={S.n}，不存在')


def _fl(S, B, ret):
    return f'子树翻转标记传给 `{S.left}`：`reverse[{S.left}]` = {S.reverse[S.left]}'


def _fr(S, B, ret):
    return f'子树翻转标记传给 `{S.right}`：`reverse[{S.right}]` = {S.reverse[S.right]}'


CONFIG = dict(
    num=2445, title='值为1的节点数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='离线标记 + 自顶向下传递翻转',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def numberOfNodes(self, n, queries):

        reverse = [False] * (n + 1)
        for v in queries:
            reverse[v] = not reverse[v]

        res = 0
        for index in range(1, n + 1):
            if reverse[index]:
                res += 1
                left = index * 2
                right = index * 2 + 1
                if left <= n:
                    reverse[left] = not reverse[left]
                if right <= n:
                    reverse[right] = not reverse[right]

        return res
''',
    call='Solution().numberOfNodes(7, [1, 2, 3, 3, 2, 2, 4])',
    expect=5,
    views=[
        dict(type='array', var='queries', label='queries（要翻转的节点）', cell=70, h=120),
        dict(type='custom', draw=_heap, h=330),
        dict(type='array', var='reverse', label='reverse[i]：节点 i 是否被翻转（下标 0 不用）', cell=70, h=150,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: i == 0),
    ],
    watch=[('v', 'v', 'pink'), ('index', 'index', 'blue'), ('left', 'left', 'cyan'), ('right', 'right', 'orange'),
           ('res', 'res', 'green')],
    captions={
        'reverse = [False]': '先假设所有节点都是 0：`reverse` 记录每个节点==被翻转的次数的奇偶==，下标 1 ~ n',
        'for v in queries': lambda S, B, r: ('翻转是==离线==的：先把所有 queries 过一遍，不用急着往下传' if 'v' not in B else '下一个查询'),
        'reverse[v] = not': _flip_cap,
        'res = 0': '`res` 统计最终值为 1 的节点数',
        'for index in range(1, n + 1)': lambda S, B, r: ('从根（节点 1）开始，==按编号从小到大==扫：父亲编号一定比孩子小，轮到孩子时父亲的标记已传完' if 'index' not in B else f'轮到节点 `{S.index}`'),
        'if reverse[index]': _if_rev,
        'res += 1': '`{index}` 最终是 1 → `res` = ==`{res}`==',
        'left = index * 2': _l,
        'right = index * 2 + 1': _r,
        'if left <= n': lambda S, B, r: ('`left <= n` 成立 → 左孩子存在' if S.left <= S.n else '`left > n`：左孩子不存在，不传'),
        'if right <= n': lambda S, B, r: ('`right <= n` 成立 → 右孩子存在' if S.right <= S.n else '`right > n`：右孩子不存在，不传'),
        'reverse[left] = not': _fl,
        'reverse[right] = not': _fr,
        'return res': '全部扫完，值为 1 的节点共 `{res}` 个',
    },
    cards=dict(
        one_liner='先离线打标记，再从根往下把翻转一层层传下去',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['有 `n` 个节点的完全二叉树，节点 `i` 的左右孩子是 `2i`、`2i+1`，初始值都是 0',
                 '每次查询 `queries[i]` 把该节点==整棵子树==的值 0/1 互换',
                 '返回全部查询后值为 1 的节点数',
                 '本视频：`n=7, queries=[1,2,3,3,2,2,4]` → `5`'],
        quote='由于题目的翻转操作是离线的，那么可以先一趟遍历，将queries中的节点都进行翻转，然后再计算树中有哪些节点被翻转过。',
        quote_src='—— yiduobo 题解原文',
        idea=['`reverse[v]` 只记「==这个节点自己==被翻转的奇偶」，同一节点出现两次就抵消',
              '自顶向下扫：若 `reverse[now]` 为真，节点值为 1，并把翻转==传给两个孩子==',
              '孩子的编号总比父亲大，所以一个 for 循环就等于一次 dfs'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '易错点：queries 里可能有重复节点，要用「取反」而不是「置 True」',
                 '孩子 `2i`、`2i+1` 可能超过 n，传递前要判断',
                 '原文用 dfs 描述，代码用按编号扫描实现，效果相同：父亲先于孩子被处理'],
    ),
)
