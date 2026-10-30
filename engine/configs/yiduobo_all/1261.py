_LAST = {}


def _qvals(S):
    q = S.get('q')
    if q is not None:
        _LAST['q'] = [n.val for n in q]
        _LAST['l'] = S.get('l', 0)
    return _LAST.get('q', [])


def _wl(S):
    return S.get('l') if S.get('q') is not None and S['l'] < len(S['q']) else None


def _wr(S):
    return len(S['q']) - 1 if S.get('q') is not None and S['l'] < len(S['q']) else None


def _top(S):
    if 'target' in S:
        return f"`find({S['target']})`：直接在集合里查 → `{S['target']} in {sorted(S['self.num_set'])}`"
    if 'now' in S and 'q' in S:
        return f"层序遍历：处理节点 `{S['now'].val}`，它的孩子 = `2×{S['now'].val}+1`、`2×{S['now'].val}+2`"
    return '被污染的树：所有节点值都是 -1，层序遍历把值一层层还原'


def _color(S, node):
    if node is S.get('now'):
        return 'blue'
    return 'green' if node.val != -1 else None


CONFIG = dict(
    num=1261, title='在受污染的二叉树中查找元素', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层序遍历还原 + set 判重',
    tags=['灵神题单·位运算', '灵神题单·链表树与回溯', '难度分 1440'],
    setup='root = Tr([-1, -1, -1, -1, -1, None, -1])',
    code='''
class FindElements(object):

    def __init__(self, root):
        self.num_set = set([0])
        root.val = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now.left:
                now.left.val = now.val * 2 + 1
                self.num_set.add(now.left.val)
                q.append(now.left)
                r += 1
            if now.right:
                now.right.val = now.val * 2 + 2
                self.num_set.add(now.right.val)
                q.append(now.right)
                r += 1

    def find(self, target):
        return target in self.num_set
''',
    call='''f = FindElements(root)
[f.find(3), f.find(5), f.find(6)]''',
    expect=[True, False, True],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='tree', label='二叉树（-1 = 还没还原，绿 = 已还原，蓝 = now）', pointers={'now': 'blue'}, path=False, h=290,
             color=_color),
        dict(type='array', var=_qvals, label='q：层序队列里节点的值（框 = 还没处理的 l..r-1）', cell=70, h=140,
             window=(_wl, _wr)),
        dict(type='set', var='self.num_set', label='num_set：已出现的值', h=110),
    ],
    watch=['l', 'r', ('now', "now.val if now else None", 'blue'), 'target'],
    captions={
        'self.num_set = set([0])': '`num_set` 记录所有还原出来的值，先放入根的值 `0`',
        'root.val = 0': '根节点的值规定是 `0`：先还原根',
        'q = [root]': '`q` 是层序遍历的队列，先放进根',
        'l = 0': '`l` 指向队首：下一个要处理的节点',
        'r = 1': '`r` 指向队尾之后：队列里一共 `r` 个节点',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：队列里还有节点没处理' if S.l < S.r
                                          else f'`l = {S.l} == r = {S.r}`：队列处理完，整棵树还原完毕'),
        'now = q[l]': '取出队首节点，它的值已经还原：`now.val = {now.val}`',
        'l += 1': '`l` 右移一位，相当于出队：`l` → {l}',
        'if now.left': lambda S, B, ret: ('有左孩子 → 还原它的值' if S.now.left else '没有左孩子，跳过'),
        'now.left.val =': '左孩子 = `2 × {now.val} + 1` = =={now.left.val}==',
        'self.num_set.add(now.left.val)': '把 `{now.left.val}` 加入 `num_set`',
        'q.append(now.left)': '左孩子入队，之后再还原它的孩子',
        'if now.right': lambda S, B, ret: ('有右孩子 → 还原它的值' if S.now.right else '没有右孩子，跳过'),
        'now.right.val =': '右孩子 = `2 × {now.val} + 2` = =={now.right.val}==',
        'self.num_set.add(now.right.val)': '把 `{now.right.val}` 加入 `num_set`',
        'q.append(now.right)': '右孩子入队',
        'r += 1': '队列多了一个节点：`r` → {r}',
        'return target in': lambda S, B, ret: f'`{S.target} in num_set` → =={ret}==（集合查找 O(1)）',
    },
    cards=dict(
        one_liner='先层序遍历把整棵树还原，值都记进 set，查询只查 set',
        complexity='初始化 `O(n)`，`find` 为 `O(1)`，空间 `O(n)`',
        problem=['二叉树根值为 0，左儿子值 `2x+1`，右儿子值 `2x+2`；现在所有值都被污染成 -1',
                 '实现 `FindElements`：构造时还原树，`find(target)` 判断 target 是否存在',
                 '本视频：树 `[-1,-1,-1,-1,-1,null,-1]`，依次 `find(3)`、`find(5)`、`find(6)`'],
        quote='二叉树中每个节点的值都与其父节点有关，因此我们可以使用层序遍历先将整棵树还原出来，并使用一个set记录所有出现过的节点值。',
        quote_src='—— yiduobo 题解原文',
        idea=['孩子的值由父节点决定，所以必须==从上往下==一层层还原',
              '用列表 `q` 加两个下标 `l`、`r` 手写队列：`l` 出队，`r` 入队',
              '每还原一个值就放进 `num_set`；`find` 直接判断 `target in num_set`'],
        summary=['初始化 `O(n)`，`find` 为 `O(1)`，空间 `O(n)`',
                 '`q` 不真正删除队首，只移动 `l`，所以 `l < r` 就是队列非空',
                 '先给根赋值 `0` 并把 `0` 放进 set，再处理孩子',
                 '原文本身是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用 DFS 还原，或用「值 + 1 的二进制 = 路径」连还原都省掉'],
    ),
)
