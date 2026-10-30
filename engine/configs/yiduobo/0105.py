import views as V

PRE = [3, 9, 20, 15, 7]


def _calls_lite(cv, spec, st, box, vi, ctx):
    """和 calls 视图一样，但不显示 preorder/inorder/pos_dict 这些很长的参数（否则一行放不下）"""
    hide = spec.get('hide', ())
    frames = [dict(f, args=[a for a in f['args'] if a not in hide]) for f in st.get('_frames', [])]
    V.v_calls(cv, spec, dict(st, _frames=frames), box, vi, ctx)


V.VIEWS.setdefault('calls_lite', (_calls_lite, V.h_calls))
INO = [9, 3, 15, 20, 7]
POS = {x: i for i, x in enumerate(INO)}
# 只在 inorder_pos 属于当前这一层时才显示（进入下一层、还没算出新的 inorder_pos 时，变量里是上一层的旧值）
IP = 'inorder_pos if pos_dict[preorder[root_pos]] == inorder_pos else None'


def _cur(S):
    """当前 build 的 (left, right, root_pos)；区间为空时返回 None"""
    l, r, rp = S.get('left'), S.get('right'), S.get('root_pos')
    if not isinstance(l, int) or not isinstance(r, int) or l >= r:
        return None
    return l, r, rp


def _in_color(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    l, r, rp = c
    k = POS[PRE[rp]]
    if i == k:
        return 'orange'
    if l <= i < k:
        return 'blue'
    if k < i < r:
        return 'pink'
    return None


def _pre_color(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    l, r, rp = c
    k = POS[PRE[rp]]
    if i == rp:
        return 'orange'
    if rp < i <= rp + (k - l):
        return 'blue'
    if rp + (k - l) < i < rp + (r - l):
        return 'pink'
    return None


def _cap_if(S, B, ret):
    l, r = B['left'], B['right']
    if l == r:
        return f'`left == right = {l}`：中序区间为空 → 空树，返回 `None`'
    return f'中序区间 `[{l}, {r})` 非空，当前子树的根在先序的 `root_pos = {B["root_pos"]}`'


def _cap_pos(S, B, ret):
    k, l, r = S['inorder_pos'], S['left'], S['right']
    return (f'根 `{S["root_val"]}` 在中序的位置 `{k}`：把中序切成==左子树== `[{l}, {k})` 和==右子树== `[{k + 1}, {r})`')


def _cap_if_l(S, B, ret):
    k, l = B['inorder_pos'], B['left']
    if k > l:
        return f'`{k} > {l}`：根左边有 {k - l} 个数 → 有左子树'
    return f'`{k} == {l}`：根左边没有数 → 没有左子树'


def _entered(S, B):
    return S.get('root_pos') != B.get('root_pos')


def _enter_msg(S, side):
    l, r = S['left'], S['right']
    s = f'进入{side}子树：`build(left={l}, right={r}, root_pos={S["root_pos"]})`'
    return s + ('，`left == right` → ==空区间==，返回 `None`' if l == r else '')


def _cap_build_l(S, B, ret):
    k, l, rp = B['inorder_pos'], B['left'], B['root_pos']
    if _entered(S, B):
        return _enter_msg(S, '左')
    return f'`{k} > {l}`：根左边有 {k - l} 个数 → 建左子树，中序 `[{l}, {k})`，它的根在先序的 `root_pos + 1 = {rp + 1}`'


def _cap_build_r(S, B, ret):
    k, l, rp = B['inorder_pos'], B['left'], B['root_pos']
    if _entered(S, B):
        return _enter_msg(S, '右')
    pre = '根左边没有数，不用建左子树；' if k == l else '左子树建好了；'
    return (f'{pre}右子树：中序 `[{k + 1}, {B["right"]})`，先序要==跳过根和左子树的 {k - l} 个== → '
            f'`{rp} + ({k} - {l}) + 1 = {rp + k - l + 1}`')


CONFIG = dict(
    num=105, title='从前序与中序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='递归：中序左右边界 + 先序根位置 root_pos',
    code='''
class Solution(object):
    def buildTree(self, preorder, inorder):
        if not preorder:
            return None

        pos_dict = {}
        for index, val in enumerate(inorder):
            pos_dict[val] = index

        return self.build(0, len(inorder), preorder, inorder, 0, pos_dict)

    def build(self, left, right, preorder, inorder, root_pos, pos_dict):
        if left == right:
            return None

        root_val = preorder[root_pos]
        inorder_pos = pos_dict[root_val]
        root = TreeNode(root_val)
        if inorder_pos > left:
            root.left = self.build(left, inorder_pos, preorder, inorder,
                                   root_pos + 1, pos_dict)
        if inorder_pos < right:
            root.right = self.build(inorder_pos + 1, right, preorder, inorder,
                                    root_pos + inorder_pos - left + 1, pos_dict)
        return root
''',
    call='Solution().buildTree([3,9,20,15,7], [9,3,15,20,7])',
    result_fn=tree_list,
    expect=[3, 9, 20, None, None, 15, 7],
    views=[
        dict(type='array', var='inorder', label='inorder（窗口 = [left, right)，橙 = 根，蓝 = 左，粉 = 右）', cell=64,
             window=('left', 'right - 1'), color=_in_color, pointers={IP: 'orange'}, pointer_labels={IP: 'inorder_pos'}),
        dict(type='array', var='preorder', label='preorder', cell=64, color=_pre_color, pointers={'root_pos': 'cyan'}),
        dict(type='tree', label='正在构造的树（先建根，再接左右子树）', h=260),
        dict(type='calls_lite', h=150, hide=('preorder', 'inorder', 'pos_dict')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('root_pos', 'root_pos', 'cyan'), ('inorder_pos', IP, 'orange')],
    captions={
        'if not preorder': '序列不为空',
        'pos_dict = {}': '`pos_dict` 用来查询根节点在中序遍历中的位置',
        'for index, val': lambda S, B, ret: (f'记录 `{S["val"]}` 在中序的位置 `{S["index"]}`' if S.get('val') is not None else '位置表建好了'),
        'pos_dict[val] = index': '`pos_dict[{val}] = {index}`',
        'return self.build(0': '整棵树：中序区间 `[left, right) = [0, 5)`，根在先序的第 `root_pos = 0` 位',
        'if left == right': _cap_if,
        'return None': '返回 `None`',
        'root_val = preorder[root_pos]': '==先序遍历的第一个节点就是根==：`preorder[{root_pos}] = {root_val}`',
        'inorder_pos = pos_dict': _cap_pos,
        'root = TreeNode(root_val)': '先把根 `{root_val}` 建出来（根-左-右，相当于前序遍历）',
        'if inorder_pos > left': _cap_if_l,
        'root.left = self.build': _cap_build_l,
        'if inorder_pos < right': lambda S, B, ret: f'右边区间 `[{B["inorder_pos"] + 1}, {B["right"]})`：递归右子树（为空会在下一层返回 `None`）',
        'root.right = self.build': _cap_build_r,
        'return root': '以 `{root.val}` 为根的子树建好了，返回',
    },
    skip=['if left == right', 'for index, val', 'pos_dict[val] = index', 'if not preorder', 'if inorder_pos > left', 'if inorder_pos < right',
          'return None', 'root_pos + 1, pos_dict)', 'root_pos + inorder_pos - left + 1, pos_dict)'],
    max_steps=60,
    cards=dict(
        one_liner='先序定根，中序分左右；用 root_pos 代替切分数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==先序遍历== `preorder` 和==中序遍历== `inorder`，构造这棵二叉树',
                 '先序：根-左-右；中序：左-根-右；节点值==互不相同==',
                 '示例：`preorder = [3,9,20,15,7]`，`inorder = [9,3,15,20,7]`',
                 '→ 构造出 `[3,9,20,null,null,15,7]`'],
        quote='首先，==前序遍历的第一个节点就是整棵树的根节点==。接下来，我们可以在中序遍历中找到根节点的位置，这个位置将中序遍历序列分成了两个部分。',
        quote_src='—— yiduobo 知乎题解',
        idea=['左子树中序的长度 = 左子树节点数；先序里根往后数这么多个就是左子树',
              '按「根-左-右」建树就是前序遍历：维护 `root_pos` = 当前子树的根在先序中的位置',
              '进左子树 `root_pos + 1`；进右子树再跳过左子树的长度，==不用切分数组=='],
        summary=['时间 `O(n)`：`pos_dict` 让找根 `O(1)`；空间 `O(n)`',
                 '易错：右子树的根要跳过左子树：`root_pos + inorder_pos - left + 1`',
                 '前提：树中没有相同元素，先序和中序才能一一对应',
                 '原文为 Python 2 风格：删去了文档字符串；两行过长的调用拆成两行，逻辑未改'],
    ),
)
