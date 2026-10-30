TREE = [1, 2, 3, None, 4]


def _qvals(S):
    q = S.get('q')
    if q is None:
        return None
    return [x if isinstance(x, str) else ('N' if x is None else x.val) for x in q]


def _rq(S):
    return S.get('r') if 'data' not in S else None


def _in_ser(S):
    return 'data' not in S


def _cap_if_now(S, B, ret):
    now = B.now
    if now:
        return f'`{now.val}` 不是空节点 → 它的左右孩子（可能是空）都要入队'
    return '空节点：只占一个 `N` 的位置，没有孩子'


def _cap_child(side, word):
    def f(S, B, ret):
        d, r = B.data, B.r
        if d[r] != 'N':
            return f'`data[{r}] = {d[r]}`：`{B.now.val}` 有{word}孩子 → 新建节点 `{d[r]}` 挂上去并入队'
        return f'`data[{r}] = N`：`{B.now.val}` 没有{word}孩子'
    return f


CONFIG = dict(
    num=297, title='二叉树序列化与反序列化', difficulty='Hard', category='二叉树',
    author='yiduobo', technique='层序遍历 + 双指针还原',
    tags=['热题173'],
    code='''
class Codec:

    def serialize(self, root):
        if not root:
            return None

        q = [root]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now:
                q.append(now.left)
                q.append(now.right)
                r += 2

        q = [str(x.val) if x else 'N' for x in q]
        return ' '.join(q)

    def deserialize(self, data):
        if not data:
            return None

        data = data.split(' ')
        root = TreeNode(int(data[0]))
        q = [root]
        l = 0
        r = 1
        while l < len(q):
            now = q[l]
            l += 1
            if data[r] != 'N':
                now.left = TreeNode(int(data[r]))
                q.append(now.left)
            r += 1

            if data[r] != 'N':
                now.right = TreeNode(int(data[r]))
                q.append(now.right)
            r += 1

        return root
''',
    call=f'''root = Tr({TREE})
codec = Codec()
data = codec.serialize(root)
codec.deserialize(data)''',
    result_fn=tree_list,
    expect=TREE,
    skip=[8, 9, 12, 14, 15, 28, 29, 32, 35, 40],
    max_steps=80,
    views=[
        dict(type='text', fn=lambda S: ('① 序列化：层序遍历，空节点记成 `N`' if _in_ser(S)
                                        else '② 反序列化：`q[l]` 是当前节点，`data[r]`、`data[r+1]` 是它的左右孩子'), size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now）', h=300, pointers={'now': 'blue'}, path=False),
        dict(type='array', var=_qvals, label='q（序列化时含空节点 N；l 之前的已处理）', cell=70, pointers={'l': 'blue', _rq: 'pink'},
             pointer_labels={_rq: 'r'},
             dim=lambda S, i, v: 'l' in S and i < S['l']),
        dict(type='array', var=lambda S: S['data'] if isinstance(S.get('data'), list) else None,
             label='data（字符串按空格切开；r 指向下一个孩子）', cell=70, pointers={'r': 'pink'},
             color=lambda S, i, v: ('pink' if i == S.get('r') else None)),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', 'now', 'blue'),
           ('data', 'data if isinstance(data, str) else None', 'green')],
    captions={
        4: '`root` 非空，开始层序遍历',
        7: 'BFS 队列 `q = [root]`，`l` 指向当前节点、`r` 是队尾（左闭右开）',
        10: lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列里还有节点' if B.l < B.r else f'`l == r = {B.r}`：遍历结束，q 里按层序存了所有节点（含空）'),
        11: lambda S, B, r: f"取出 `q[{B.l}]` = `{S.now.val if S.now else 'None'}`",
        13: _cap_if_now,
        16: '`{now.val}` 的左孩子 `{now.left.val if now.left else "N"}`、右孩子 `{now.right.val if now.right else "N"}` 入队，`r += 2` → {r}',
        18: '空节点用特殊字符 `N` 表示，其余转成字符串：`{q}`',
        19: '用空格拼起来：序列化结果 `"{ret}"`',
        22: '`data = "{data}"` 非空，开始还原',
        25: '按空格切开：`data = {data}`',
        26: '`data[0] = {data[0]}` 是根：新建根节点',
        27: '队列 `q` 只放==非空节点==；`l = 0` 指向当前节点，`r = 1` 指向它的孩子值',
        30: lambda S, B, r: (f'`l = {B.l} < len(q) = {len(B.q)}`：还有节点等着接孩子' if B.l < len(B.q) else '所有节点都处理完 → 树还原好了'),
        31: '当前节点 `q[{B.l}] = {now.val}`',
        33: _cap_child('left', '左'),
        34: '`{now.val}.left = {now.left.val}`，并加入队列',
        36: '`r` → {r}',
        38: _cap_child('right', '右'),
        39: '`{now.val}.right = {now.right.val}`，并加入队列',
        41: '`r` → {r}：处理完一个节点，l 走 1 步、r 走了 2 步',
        43: '返回还原出的根 `{ret.val}`',
    },
    cards=dict(
        one_liner='层序遍历存成字符串（空节点写 N），再用 l、r 两个指针一层层还原',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['设计算法把二叉树==序列化==成字符串，并能==反序列化==还原成原来的树',
                 '格式不限，只要两者配套；例如 LeetCode 的层序格式',
                 '示例：`root = [1,2,3,null,null,4,5]` → 还原后仍是 `[1,2,3,null,null,4,5]`',
                 f'本视频：`root = [1,2,3,null,4]`'],
        quote='复原时，同样是bfs的思路，依次将非空节点加入到队列q中，并使用两个指针l和r，==q[l]指向当前处理的节点，data[r]则表示是当前节点的孩子节点的值==。',
        quote_src='—— yiduobo 题解原文',
        idea=['构造：对树做一趟==层次遍历==，所有节点存起来，空节点用特殊字符 `N`',
              '复原：`data[r]` 不是 `N` 就新建节点，作为 `q[l]` 的左孩子并入队；`data[r+1]` 同理是右孩子',
              '处理完一组，`l` 后移一位，`r` 后移两位'],
        summary=['时间 `O(n)`：构造与复原都是一趟 BFS',
                 '序列化的 q 里有空节点，所以 `r += 2`；反序列化的 q 只放非空节点',
                 '易错：空树 `serialize` 返回 None，`deserialize` 要先判空',
                 '原文为 Python 2 风格，只删去了文档字符串和 LeetCode 模板注释，代码未改'],
    ),
)
