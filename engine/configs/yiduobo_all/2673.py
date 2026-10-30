
def ROLES(S):
    if S.get('j') is None or 'res' not in S or S.get('_line') is None:
        return None, None
    j = S['j']
    return (j - 1, j), (j - 1) // 2

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
    author='yiduobo', technique='按层收缩 · 兄弟调齐后并入父节点',
    tags=['灵神题单', '链表树与回溯', '难度分 1917'],
    code='''
class Solution(object):
    def minIncrements(self, n, cost):

        tmp = n
        level = 0
        while tmp:
            level += 1
            tmp >>= 1
        
        pre_end = n - 1
        res = 0
        for i in range(level - 1, 0, -1):
            node_cnt = 1 << i
            for j in range(pre_end, pre_end - node_cnt, -2):
                if cost[j] < cost[j - 1]:
                    res += cost[j - 1] - cost[j]
                    cost[j] = cost[j - 1]
                else:
                    res += cost[j] - cost[j - 1]
                    cost[j - 1] = cost[j]
                
                cost[(j - 1) // 2] += cost[j]
            
            pre_end -= node_cnt

        return res
''',
    call=f'Solution().minIncrements(7, {COST})',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='cost', label='cost（下标 = 节点编号 - 1）', h=190,
             pointers={'j': 'pink', 'j - 1': 'blue', '(j - 1) // 2': 'yellow'},
             pointer_labels={'j': '右', 'j - 1': '左', '(j - 1) // 2': '父'}),
    ],
    watch=['level', 'i', 'j', ('res', 'res', 'green')],
    captions={
        'level += 1': '数一数 `n` 有几个二进制位：`level = {level}`（树有 {level} 层）',
        'pre_end = n - 1': '`pre_end`：当前最底层最后一个节点的下标 = `{pre_end}`',
        'for i in range(level - 1': lambda S, B, r: (f'处理从下往上的一层：这层有 `{1 << S.i}` 个节点' if B.get('i') != S.i else '每一层都收缩完，只剩根节点'),
        'node_cnt = 1 << i': '这一层有 `{node_cnt}` 个节点，从下标 `{pre_end}` 往前每 2 个一组',
        'for j in range': lambda S, B, r: (f'一组兄弟：下标 `{S.j-1}` 和 `{S.j}`' if B.get('j') != S.j else '这一层的兄弟都处理完了'),
        'if cost[j] < cost[j - 1]': lambda S, B, r: (f'右 `{S.cost[S.j]}` < 左 `{S.cost[S.j-1]}` → 右边要补' if S.cost[S.j] < S.cost[S.j-1] else f'右 `{S.cost[S.j]}` >= 左 `{S.cost[S.j-1]}` → 左边要补（相等不用补）'),
        'res += cost[j - 1] - cost[j]': '右边补 `{res - B.res}` 次 → `res = {res}`',
        'cost[j] = cost[j - 1]': '右边补成和左边一样：`{cost[j]}`',
        'res += cost[j] - cost[j - 1]': '左边补 `{res - B.res}` 次 → `res = {res}`',
        'cost[j - 1] = cost[j]': '左边补成和右边一样：`{cost[j]}`',
        'cost[(j - 1) // 2] +=': '两兄弟相等，收缩进父节点 `{(j-1)//2}`：把值 `{cost[j]}` 累加上去 → =={cost[(j-1)//2]}==',
        'pre_end -= node_cnt': '这一层处理完，下一层的最后一个节点下标是 `{pre_end}`',
        'return res': '一共 `{res}` 次',
    },
    cards=dict(
        one_liner='先把最底层的兄弟调成一样，再收缩进父节点，层层往上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['满二叉树，节点 `i` 的孩子是 `2i`、`2i+1`，`cost` 是节点值',
                 '每次可把任意节点值加 1，使所有根到叶子的路径和相等，求最少次数；示例：`n=7, cost=[1,5,2,2,3,3,1]` → `6`'],
        quote='可以将这两个孩子节点收缩到当前节点，同时将叶子节点的值累加到当前节点。这样一来，就相当于移除掉了整颗二叉树的最下层。',
        quote_src='—— yiduobo 题解原文',
        idea=['叶子兄弟到根的路径只差自己，值必须相同，先调成一致',
              '调完后两个孩子合并进父节点，树少一层，重复同样的过程'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先用 `while` 数出层数，再每层算出节点数和起止下标',
                 '`range(pre_end, pre_end - node_cnt, -2)` 以步长 2 取一组兄弟（`j-1`、`j`）',
                 '父节点下标是 `(j - 1) // 2`，注意下标从 0 开始',
                 '对比灵神：灵神一个循环倒着走，yiduobo 显式按层处理'],
    ),
)
