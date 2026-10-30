DESC = [[20, 15, 1], [20, 17, 0], [50, 20, 1], [50, 80, 0], [80, 19, 1]]


def _lr(n):
    return f"L={n.left.val if n.left else '-'} R={n.right.val if n.right else '-'}"


def _size(n):
    return 1 + (_size(n.left) if n.left else 0) + (_size(n.right) if n.right else 0)


def _big(S):
    nd = S.get('node_dict') or {}
    ks = list(nd.values())
    kids = {id(c) for n in ks for c in (n.left, n.right) if c}
    roots = [n for n in ks if id(n) not in kids]
    return max(roots, key=_size) if roots else None


def _edges(S):
    I = S['_inner']
    out = []
    for d in DESC:
        t = f'[{d[0]},{d[1]},{d[2]}]'
        out.append(f'=={t}==' if I.get('parent') == d[0] and I.get('child') == d[1] else f'`{t}`')
    return 'descriptions：' + ' '.join(out)


CONFIG = dict(
    num=2196, title='根据描述创建二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='哈希表建树 + 集合找根',
    tags=['链表树与回溯', '二叉树', '难度分 1644'],
    code='''
class Solution(object):
    def createBinaryTree(self, descriptions):
        f_set = set()
        node_dict = {}
        for parent, child, isLeft in descriptions:
            if parent not in node_dict:
                node_dict[parent] = TreeNode(parent)
            node_parent = node_dict[parent]

            if child not in node_dict:
                node_dict[child] = TreeNode(child)
            node_child = node_dict[child]

            if isLeft:
                node_parent.left = node_child
            else:
                node_parent.right = node_child

            f_set.add(child)

        for parent, _, _ in descriptions:
            if parent not in f_set:
                return node_dict[parent]
''',
    call='''s = Solution()
s.descs = ''' + repr(DESC) + '''
tree_list(s.createBinaryTree(s.descs))''',
    expect=[50, 20, 80, 15, 17, 19],
    views=[
        dict(type='text', fn=_edges, size=26, h=70),
        dict(type='map', var='node_dict', label='node_dict：值 → 节点（黄 = 刚创建 / 刚改动）', fmt=lambda k, v: f'{k} → {_lr(v)}', h=150),
        dict(type='set', var='f_set', label='f_set：当过孩子的值', fmt=lambda x: str(x), h=90),
        dict(type='tree', var=_big, label='已连好的最大子树', h=230),
    ],
    watch=[('parent', lambda S: S['_inner'].get('parent'), 'blue'), ('child', lambda S: S['_inner'].get('child'), 'pink'), ('isLeft', lambda S: S['_inner'].get('isLeft'))],
    captions={
        'f_set = set()': '`f_set` 记录==当过孩子的值==：没在里面的，就是根',
        'node_dict = {}': '`node_dict` 以节点值为 key、节点本身为 value：题目只给整数，要==自己创建节点，还要能按值找回==',
        'for parent, child, isLeft': '{"取一条边：`parent = " + str(parent) + "`，`child = " + str(child) + "`，`isLeft = " + str(isLeft) + "`" if not (B.get("child") == child and B.get("parent") == parent) else "所有边处理完，树已经建好，下面找根"}',
        'if parent not in node_dict': '父节点 `{parent}` {"还没有 → 新建" if parent not in node_dict else "已经建过 → 直接取用"}',
        'node_dict[parent] = TreeNode(parent)': '新建节点 `{parent}` 放进 `node_dict`',
        'node_parent = node_dict[parent]': '取出父节点 `{parent}`（不管是刚建的还是之前建的）',
        'if child not in node_dict': '孩子 `{child}` {"还没有 → 新建" if child not in node_dict else "已经建过 → 直接取用"}',
        'node_dict[child] = TreeNode(child)': '新建节点 `{child}` 放进 `node_dict`',
        'node_child = node_dict[child]': '取出孩子节点 `{child}`',
        'if isLeft:': '`isLeft = {isLeft}` → 接到父节点的{"左" if isLeft else "右"}边',
        'node_parent.left = node_child': '`{parent}` 的左儿子 = `{child}`',
        'node_parent.right = node_child': '`{parent}` 的右儿子 = `{child}`',
        'f_set.add(child)': '`{child}` 有父亲了 → 记入 `f_set = {sorted(f_set)}`，它不可能是根',
        'for parent, _, _ in descriptions': lambda S, B, r: f'再扫一遍所有父节点，找没当过孩子的：`parent = {S.parent}`',
        'if parent not in f_set': '`{parent}` {"不在 f_set 里 → 没有父亲 → 它就是根" if parent not in f_set else "在 f_set 里 → 有父亲，不是根"}',
        'return node_dict[parent]': lambda S, B, r: f'返回根节点 `node_dict[{S.parent}]`：整棵树已经连好',
    },
    cards=dict(
        one_liner='节点值当 key 建哈希表，从没当过孩子的值就是根',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`descriptions[i] = [parent, child, isLeft]`：`isLeft = 1` 表示 `child` 是 `parent` 的左儿子',
                 '节点值各不相同，构造二叉树，返回==根节点==',
                 '本视频：`[[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]` → `[50,20,80,15,17,19]`'],
        quote='由于题目中各节点的值各不相同，因此可以利用节点的值作为key，节点本身作为对应的value，通过哈希表来完成树的构建。……遍历所有节点，找出从未当过child的节点作为根节点返回即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['第一遍：遍历 `descriptions`，从 `node_dict` 按值取出父、孩子；没有就新建',
              '按 `isLeft` 把孩子接到父节点的左/右边，同时把孩子记入 `f_set`',
              '第二遍：扫父节点，第一个不在 `f_set` 里的就是根'],
        summary=['时间 `O(n)`，空间 `O(n)`（`n` 是 `descriptions` 的长度）',
                 '要两遍：第一遍建树 + 记孩子，第二遍找根；`f_set` 里存的是孩子，不是父亲',
                 '第二遍直接扫 `descriptions` 里的 `parent`，一定能找到根（题目保证树有效）',
                 '原文为 Python 2 风格：删去了函数开头的空白行，代码本身未改'],
    ),
)
