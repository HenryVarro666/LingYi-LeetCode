def _cur(S):
    q = S.get('q')
    if q is None or 'head' not in S:
        return set()
    return {id(n) for n in q[S['head']:S['tail']]}


def _info(S):
    if 'level' not in S:
        return '层序遍历：一层一层算层和，找最小的那层'
    s = S.get('s')
    txt = f"第 `{S['level']}` 层" + (f"，层和累加到 `s = {s}`" if s is not None else '')
    return txt + f"；目前最小 `mi = {S['mi']}`（第 `{S['res']}` 层）"


CONFIG = dict(
    num=3157, title='找到具有最小和的树的层数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 逐层求和',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def minimumLevel(self, root):

        head, tail = 0, 1
        q = [root]
        mi = root.val
        res = 1
        level = 1
        while head < tail:
            s = 0
            for now in q[head : tail]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            if s < mi:
                mi = s
                res = level

            head, tail = tail, len(q)
            level += 1
        
        return res
''',
    call='Solution().minimumLevel(Tr([1, 7, 0, 7, -8, None, None]))',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = 当前层，黄 = 正在累加的节点）', pointers={'now': 'yellow'}, path=False, h=330,
             color=lambda S, n: 'blue' if id(n) in _cur(S) else None),
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else [], label='队列 q（存节点值）',
             pointers={'head': 'blue', 'tail': 'pink'}, cell=72, h=170),
    ],
    watch=[('level', 'level', 'blue'), ('s', 's', 'yellow'), ('mi', 'mi', 'green'), ('res', 'res', 'pink')],
    captions={
        'head, tail = 0, 1': '`q[head:tail]` 就是当前这一层：开始时只有根，`head = 0, tail = 1`',
        'mi = root.val': '最小层和先取第 1 层（只有根）：`mi = {mi}`',
        'while head < tail': lambda S, B, r: (f'这一层还有节点（`head = {S.head} < tail = {S.tail}`）→ 处理它' if S.head < S.tail
                                              else f'`head = {S.head} = tail`：没有下一层了 → 结束'),
        's = 0': '每层从 `s = 0` 重新累加',
        'for now in q[head : tail]': lambda S, B, r: ('这一层的节点都处理完了 → 比较层和' if getattr(B.get('now'), '_uid', 0) == getattr(S.get('now'), '_uid', 1)
                                                      else f'依次取当前层的节点：`now = {S.now.val}`'),
        's += now.val': '把 `{now.val}` 加进层和：`s = {s}`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 放进 q 末尾，留给下一层' if S.now.left
                                        else f'`{S.now.val}` 没有左孩子 → 跳过'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 放进 q 末尾，留给下一层' if S.now.right
                                         else f'`{S.now.val}` 没有右孩子 → 跳过'),
        'q.append(now.left)': '左孩子入队：`q` 尾部变成 `{[n.val for n in q][-1]}`',
        'q.append(now.right)': '右孩子入队：`q` 尾部变成 `{[n.val for n in q][-1]}`',
        'if s < mi': lambda S, B, r: (f'本层和 `s = {S.s} < mi = {S.mi}` → ==更小，要更新==' if S.s < S.mi
                                      else f'本层和 `s = {S.s} >= mi = {S.mi}` → 不比之前小，保持原答案（相等时保留更浅的层）'),
        'mi = s': '更新最小层和：`mi = {mi}`',
        'res = level': '记下层数：`res = {res}`（更新用严格 `<`，所以相等时留下较浅层）',
        'head, tail = tail, len(q)': '这一层处理完：新的 `[head, tail) = [{head}, {tail})` 正好是刚入队的下一层',
        'level += 1': '层数加一：`level = {level}`',
        'return res': '最小层和 `{mi}` 出现在第 `{res}` 层',
    },
    skip=['res = 1', 'level = 1'],
    cards=dict(
        one_liner='层序遍历，边走边算每层的和，记录和最小的那层',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵节点带权重的二叉树 `root`，根在第 1 层',
                 '求==层和最小==的那一层的层号；层和相同取==层号最小==的（最浅的）',
                 '本视频：`root = [1,7,0,7,-8,null,null]`',
                 '三层的和分别为 `1`、`7`、`-1` → 答案 `3`'],
        quote='由于需要计算层和，那么在这里就可以从root开始向下进行层序遍历。每一轮只需一边计算当前层的层和并更新答案，一边将下一层节点加入到层序遍历的队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列 `q` 一直不删元素，用 `head, tail` 圈出当前这一层',
              '遍历这一层：累加 `s`，同时把孩子追加到 `q` 末尾',
              '一层完后 `head, tail = tail, len(q)`，刚追加的就是下一层'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '更新答案用严格 `s < mi`，相同层和时保留更浅的层',
                 '`for` 遍历的是 `q[head:tail]` 的切片副本，循环中追加 `q` 不会影响本层',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
