
def ROLES(S):
    if 'i' not in S or S['i'] < 1:
        return None, None
    i = S['i']
    return (i * 2 - 1, i * 2), i - 1

def _roles(S):
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    c = S['cost']
    n = len(c)
    cv.text((x0 + 18, y0 + 4), '满二叉树（节点值 = 已累加的路径和，蓝/粉 = 正在比较的兄弟，黄 = 父节点）', 24, T['muted'], bold=True)
    kids, par = ROLES(S)
    depth = n.bit_length()
    W = x1 - x0 - 60
    top, gap = y0 + 90, min(120, (y1 - y0 - 150) / max(1, depth - 1))
    pos = {}
    for k in range(n):
        d = (k + 1).bit_length() - 1
        idx = k + 1 - (1 << d)
        cnt = 1 << d
        pos[k] = (x0 + 30 + W * (idx + 0.5) / cnt, top + d * gap)
    for k in range(1, n):
        p = (k - 1) // 2
        cv.line([pos[p], pos[k]], T['border'], 3)
    for k in range(n):
        X, Y = pos[k]
        fill = T['panel2']
        if kids and k == kids[0]:
            fill = T['blue']
        elif kids and k == kids[1]:
            fill = T['pink']
        elif par is not None and k == par:
            fill = T['yellow']
        hl = fill != T['panel2']
        cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=fill, outline=T['border'], width=2, r=34)
        cv.text((X, Y), c[k], 30, T['bg'] if hl else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 40), f'#{k + 1}', 18, T['dim'], anchor='mt', mono=True)


COST = [1, 5, 2, 2, 3, 3, 1]

CONFIG = dict(
    num=2673, title='使二叉树所有路径值相等的最小代价', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自底向上 · 兄弟补差 · 路径和上传',
    tags=['贪心与思维', '链表树与回溯', '难度分 1917'],
    code='''
class Solution:
    def minIncrements(self, n: int, cost: List[int]) -> int:
        ans = 0
        for i in range(n // 2, 0, -1):  # 从最后一个非叶节点开始算
            ans += abs(cost[i * 2 - 1] - cost[i * 2])  # 两个子节点变成一样的
            cost[i - 1] += max(cost[i * 2 - 1], cost[i * 2])  # 累加路径和
        return ans
''',
    call=f'Solution().minIncrements(7, {COST})',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='cost', label='cost（下标 = 节点编号 - 1）', h=190,
             pointers={'i and i * 2 - 1': 'blue', 'i and i * 2': 'pink', 'i and i - 1': 'yellow'},
             pointer_labels={'i and i * 2 - 1': '左', 'i and i * 2': '右', 'i and i - 1': '父'}),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计增加次数',
        'for i in range': lambda S, B, r: (f'节点 `{S.i}`（下标 `{S.i-1}`）：它的两个孩子是节点 `{S.i*2}`、`{S.i*2+1}`' if B.get('i') != S.i else '根节点也算完了，循环结束'),
        'ans += abs': '左右孩子值 `{cost[i*2-1]}` 和 `{cost[i*2]}`：较小的补到一样，花费 `|差|` = {abs(cost[i*2-1]-cost[i*2])} → `ans = {ans}`',
        'cost[i - 1] +=': '补齐后两边路径和相同，上传较大值：`cost[{i-1}]` 变成 =={cost[i-1]}==（含自己）',
        'return ans': '最少增加 `{ans}` 次',
    },
    cards=dict(
        one_liner='兄弟子树的路径和必须相等：把小的补到大的，再把路径和往上传',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['满二叉树，节点 `i` 的孩子是 `2i`、`2i+1`，`cost` 是节点值',
                 '每次可把任意节点值加 1，使所有根到叶子的路径和相等，求最少次数；示例：`n=7, cost=[1,5,2,2,3,3,1]` → `6`'],
        quote='这两条路径除了叶子节点不一样，其余节点都一样，所以为了让这两条路径的路径和相等，必须修改叶子节点的值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['兄弟节点之上的路径完全相同，所以只能改兄弟自己：把较小的增加 `|x-y|`',
              '把路径和从叶子往上传（取较大值累加到父节点），上一层又变成兄弟比较'],
        summary=['时间 `O(n)`，直接在 `cost` 上累加，空间 `O(1)`',
                 '节点编号转下标要减 1：孩子是 `2i-1`、`2i`，自己是 `i-1`',
                 '从 `n // 2` 倒着循环：最后一个非叶节点，保证孩子先算好',
                 '增加祖先节点可以同时抬高多条路径，所以只补兄弟之差就够'],
    ),
)
