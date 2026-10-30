TREE = [3, 1, 4, None, 2]


def _bound(S):
    d = S.get('data')
    if not isinstance(d, list) or 'now' not in S or 'min_num' not in S:
        return ''
    inner = S['_inner']
    if 'val' not in inner:
        return ''
    lo = inner['min_num'] if inner['min_num'] > -10**9 else '−∞'
    hi = inner['max_num'] if inner['max_num'] < 10**9 else '+∞'
    return f"合法范围 `({lo}, {hi})`，当前取到 `val = {inner['val']}`"


def _tag(S):
    if 'data' in S and isinstance(S['data'], list):
        return '② 反序列化：先序序列 + 上下界，还原出树'
    return '① 序列化：先序遍历，节点值用空格连起来'


def _cap_val(S, B, r):
    if S.now == len(S.data):
        return '先序序列用完了 → 没有节点，返回 `None`'
    return f'取先序序列第 `{S.now}` 个：`val = {S.data[S.now]}`'


def _cap_range(S, B, r):
    v, lo, hi = S.val, S.min_num, S.max_num
    lo_s = '−∞' if lo < -10**9 else lo
    hi_s = '+∞' if hi > 10**9 else hi
    if v < lo or v > hi:
        return f'`{v}` 不在 `[{lo_s}, {hi_s}]` 里 → ==它不属于这棵子树==，返回 `None`，留给别处'
    return f'`{v}` 在 `[{lo_s}, {hi_s}]` 里 → 可以当这棵子树的根'


CONFIG = dict(
    num=449, title='序列化和反序列化二叉搜索树', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='先序遍历 + 上下界还原 BST',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Codec:

    def dfs(self, now):
        if not now:
            return []
        return [now.val] + self.dfs(now.left) + self.dfs(now.right)

    def serialize(self, root):
        return ' '.join([str(x) for x in self.dfs(root)])

    def build(self, data, now, min_num, max_num):
        if now == len(data):
            return None, 0
        val = int(data[now])
        if val < min_num or val > max_num:
            return None, 0
        node = TreeNode(val)
        left, left_offset = self.build(data, now + 1, min_num, val)
        right, right_offset = self.build(data, now + left_offset + 1, val, max_num)
        node.left = left
        node.right = right
        return node, left_offset + right_offset + 1

    def deserialize(self, data):
        if not data:
            return None

        return self.build(data.split(' '), 0, -2147483648, 2147483647)[0]
''',
    call=f'''root = Tr({TREE})
codec = Codec()
data = codec.serialize(root)
codec.deserialize(data)''',
    result_fn=tree_list,
    expect=TREE,
    max_steps=90,
    skip=['if not now:', 'return []'],
    views=[
        dict(type='text', fn=_tag, size=26, h=56),
        dict(type='tree', label='二叉搜索树（蓝 = 当前 node）', pointers={'node': 'blue', 'now': None} if False else {'node': 'blue'}, h=230, path=False),
        dict(type='text', fn=_bound, size=24, h=50),
        dict(type='array', var=lambda S: S['data'] if isinstance(S.get('data'), list) else None,
             label='data（先序序列；蓝 = 当前位置 now）', cell=70, h=140,
             pointers={'now': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('now') else None),
        dict(type='text', fn=lambda S: f"序列化结果 `data = \"{S['data']}\"`" if isinstance(S.get('data'), str) else '', size=24, h=50),
        dict(type='calls', h=150, hide=('data', 'root')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') if isinstance(S['_inner'].get('now'), int) else None, 'blue'),
           ('val', lambda S: S['_inner'].get('val'), 'yellow'),
           ('min_num', lambda S: S['_inner'].get('min_num'), 'cyan'),
           ('max_num', lambda S: S['_inner'].get('max_num'), 'pink')],
    captions={
        'return [now.val] + self.dfs': lambda S, B, r: ('空节点 → 先序为空列表 `[]`' if S.now is None else
                                                      f'先序：先放自己 `{S.now.val}`，再接左子树、右子树的先序'),
        "' '.join": lambda S, B, r: ('`dfs(root)` 先序遍历：根、左、右，收集成列表' if r is None else
                                     f'用空格连起来：`"{r}"`。BST 的先序序列已经足够还原，不用记空节点'),
        'if now == len(data)': lambda S, B, r: ('序列用完了 → 没有节点可建，返回 `None, 0`' if S.now == len(S.data)
                                               else f'`now = {S.now}` 还没到序列末尾（共 `{len(S.data)}` 个）'),
        'val = int(data[now])': _cap_val,
        'if val < min_num': _cap_range,
        'return None, 0': lambda S, B, r: ('序列用完 → 返回 `None`，用掉 `0` 个数' if S.now == len(S.data)
                                          else '范围不对 → 返回 `None`，用掉 `0` 个数，这个数留给别处'),
        'node = TreeNode(val)': '新建节点 `{val}`',
        'left, left_offset': '左子树：从下一个数 `now + 1` 开始，范围缩成 `(min_num, {val})`——==左边不能比根大==',
        'right, right_offset': lambda S, B, r: f'右子树：跳过左子树用掉的 `{S.left_offset}` 个数，从 `now + {S.left_offset} + 1` 开始，范围 `({S.val}, max_num)`——==右边不能比根小==',
        'node.left = left': lambda S, B, r: f'`{S.node.val}.left` 挂上左子树 `{S.left.val if S.left else None}`',
        'node.right = right': lambda S, B, r: f'`{S.node.val}.right` 挂上右子树 `{S.right.val if S.right else None}`',
        'return node, left_offset': '返回节点 `{node.val}`，它的子树一共用掉 `{left_offset} + {right_offset} + 1 = {ret[1]}` 个数',
        'if not data': '`data` 非空，开始还原',
        'return self.build': '按空格切开，从第 `0` 个数开始，初始范围是整个 int，递归还原',
    },
    cards=dict(
        one_liner='BST 的先序遍历配上「上下界」，不需要空节点标记就能还原',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['设计算法把==二叉搜索树==序列化成字符串，再还原回来',
                 '格式不限，只要 `serialize` 和 `deserialize` 配套；字符串越短越好',
                 '本视频：`root = [3,1,4,null,2]`，先序 `3 1 2 4`'],
        quote='依然是按照先序遍历逐个确定节点，而对于每个节点，设置一个上界与一个下界，若当前先序遍历位置上的值val在上界与下界之间，才生成对应的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['BST 的中序一定递增，所以只要有==先序==就能唯一还原',
              '递归 `build(data, now, min_num, max_num)`：值在 `[min, max]` 内才当根',
              '左子树上界变成根值，右子树下界变成根值；`build` 还返回用掉了几个数，右子树据此找起点'],
        summary=['时间 `O(n)`，空间 `O(n)`；比层序加空节点的写法更短',
                 '`build` 返回 `(节点, 用掉的个数)`：右子树的起点 = `now + 左子树个数 + 1`',
                 '值越界就返回 `None, 0`，不消耗序列，留给上层的右子树或更上层',
                 '原文为 Python 2 写法，只删去了 `:type`/`:rtype` 文档字符串；`-maxint` 原文已写成常数 `-2147483648`'],
    ),
)
