CONFIG = dict(
    num=2641, title='二叉树的堂兄弟节点 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='两次层序遍历 · 预存层和与子节点和',
    tags=['灵神题单', '链表树与回溯', '难度分 1677'],
    code='''
class Solution(object):
    def replaceValueInTree(self, root):

        level_s = []
        q = [root]
        sons_s = []
        head, tail = 0, 1
        while head < tail:
            level_s.append(0)
            for index in range(head, tail):
                now = q[index]
                sons_s.append(0)
                level_s[-1] += now.val
                if now.left:
                    sons_s[index] += now.left.val
                    q.append(now.left)
                if now.right:
                    sons_s[index] += now.right.val
                    q.append(now.right)
            
            head, tail = tail, len(q)

        q = [root]
        head, tail = 0, 1
        level = 0
        while head < tail:
            level += 1
            for index in range(head, tail):
                now = q[index]
                if now.left:
                    now.left.val = level_s[level] - sons_s[index]
                    q.append(now.left)
                if now.right:
                    now.right.val = level_s[level] - sons_s[index]
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        root.val = 0
        return root
''',
    call='Solution().replaceValueInTree(Tr([5,4,9,1,10,None,7]))',
    expect=[0, 0, 0, 7, 7, None, 11],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, path=False, h=240),
        dict(type='array', var='level_s', label='level_s（每层总和）', cell=64, h=125),
        dict(type='array', var='sons_s', label='sons_s[index]（该节点的子节点值之和）', cell=64, h=125),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（head..tail-1 是当前层）',
             pointers={'head': 'blue'}, window=('head', 'tail - 1'), cell=52, h=190),
    ],
    watch=['head', 'tail', 'index', ('now', lambda S: S['now'].val if S.get('now') else None, 'blue'), ('level', lambda S: S.get('level'), 'yellow')],
    captions={
        'level_s = []': '第一轮要算好两样东西：`level_s`（每层总和）和 `sons_s`（每个节点的子节点值之和）',
        'q = [root]': lambda S, B, r: ('`q` 放根，开始第一轮层序遍历' if S.get('level') is None else '`q` 重新放根，开始第二轮：这次真正改值'),
        'head, tail = 0, 1': '当前层范围：`head = 0`，`tail = 1`',
        'while head < tail': lambda S, B, r: (f'当前层 `q[{S.head}:{S.tail}]` 非空 → 处理' if S.head < S.tail else '这一轮遍历结束'),
        'level_s.append(0)': '新的一层，给它开一个层和 0',
        'level += 1': '`level = {level}`：下面处理的是第 {level} 层的==儿子==（根不用改）',
        'for index in range': '遍历当前层的下标 `{head}` 到 `{tail-1}`',
        'now = q[index]': '取出节点 `{now.val}`（下标 `{index}`）',
        'sons_s.append(0)': '给下标 `{index}` 的节点留一个子节点和的位置，初值 0',
        'level_s[-1] += now.val': '`{now.val}` 累加进本层层和 → `level_s = {level_s}`',
        'sons_s[index] += now.left.val': '左儿子 `{now.left.val}` 计入 `{now.val}` 的子节点和 → `sons_s[{index}] = {sons_s[index]}`',
        'sons_s[index] += now.right.val': '右儿子 `{now.right.val}` 计入 `{now.val}` 的子节点和 → `sons_s[{index}] = {sons_s[index]}`',
        'now.left.val =': '左儿子 = ==层和 − 兄弟和== = `{level_s[level]} - {sons_s[index]}` = `{now.left.val}`',
        'now.right.val =': '右儿子 = ==层和 − 兄弟和== = `{level_s[level]} - {sons_s[index]}` = `{now.right.val}`',
        'q.append': '儿子入队，属于下一层',
        'head, tail = tail': '进入下一层：`head = {head}`，`tail = {tail}`',
        'root.val = 0': '根没有堂兄弟 → 最后把根置 `0`',
        'return root': '返回改好的树',
    },
    skip=['if now.left:', 'if now.right:'],
    cards=dict(
        one_liner='先层序遍历存好层和与子节点和，再遍历一次套公式改值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把每个节点的值换成它所有==堂兄弟==节点值的和',
                 '堂兄弟：深度相同、父节点不同',
                 '示例：`[5,4,9,1,10,null,7]` → `[0,0,0,7,7,null,11]`'],
        quote='堂兄弟节点值之和可以认为是该节点所在层中所有节点值之和，减去该节点父亲节点的所有子节点之和，于是可以进行一次层序遍历，同时将每一层节点值之和以及每个节点的子节点之和都计算好，接下来再进行一次层序遍历。',
        quote_src='—— yiduobo 题解',
        idea=['第一轮层序遍历：`level_s` 记每层总和，`sons_s[index]` 记第 index 个节点的子节点和',
              '第二轮层序遍历：它的儿子 = `level_s[level] - sons_s[index]`',
              '根没有堂兄弟，最后把 `root.val` 置 0'],
        result='运行结束，树变为 `[0,0,0,7,7,null,11]`',
        summary=['时间 `O(n)`，空间 `O(n)`（三个列表）',
                 '易错：`sons_s` 的下标和 `q` 的下标一一对应，所以用 `index` 而不是 `now`',
                 '易错：根不要提前改，否则第一轮之后根的值已变，所以最后才置 0',
                 '对比灵神：灵神一轮 BFS 里先后遍历两次当前层，不需要额外保存 `level_s`、`sons_s`'],
    ),
)
