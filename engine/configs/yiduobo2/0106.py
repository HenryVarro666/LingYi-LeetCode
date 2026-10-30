import views as V


def _calls_lite(cv, spec, st, box, vi, ctx):
    """和 calls 视图一样，但不显示 inorder/postorder/pos_dict 这些很长的参数（否则一行放不下）"""
    hide = spec.get('hide', ())
    frames = [dict(f, args=[a for a in f['args'] if a not in hide]) for f in st.get('_frames', [])]
    V.v_calls(cv, spec, dict(st, _frames=frames), box, vi, ctx)


V.VIEWS.setdefault('calls_lite', (_calls_lite, V.h_calls))

INO = [1, 9, 3, 15, 20, 7]
POST = [1, 9, 15, 7, 20, 3]
POS = {x: i for i, x in enumerate(INO)}
# 只在 inorder_pos 属于当前这一层时才显示（刚进入下一层、还没算出新的 inorder_pos 时，变量里是上一层的旧值）
IP = 'inorder_pos if pos_dict[postorder[root_pos]] == inorder_pos else None'


def _cur(S):
    """当前 build 的 (left, right, root_pos, k)；区间为空时返回 None"""
    l, r, rp = S.get('left'), S.get('right'), S.get('root_pos')
    if not isinstance(l, int) or not isinstance(r, int) or not isinstance(rp, int) or l >= r:
        return None
    return l, r, rp, POS[POST[rp]]


def _in_color(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    l, r, rp, k = c
    if i == k:
        return 'orange'
    if l <= i < k:
        return 'blue'
    if k < i < r:
        return 'pink'
    return None


def _post_color(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    l, r, rp, k = c
    rs = r - 1 - k  # 右子树大小
    ls = k - l      # 左子树大小
    if i == rp:
        return 'orange'
    if rp - rs <= i < rp:
        return 'pink'
    if rp - rs - ls <= i < rp - rs:
        return 'blue'
    return None


def _post_dim(S, i, v):
    c = _cur(S)
    if c is None:
        return False
    l, r, rp, k = c
    return not (rp - (r - l) < i <= rp)


def _cap_if(S, B, ret):
    l, r = B['left'], B['right']
    if l == r:
        return f'`left == right = {l}`：中序区间为空 → 空树'
    return f'中序区间 `[{l}, {r})` 非空，当前子树的根在后序的 `root_pos = {B["root_pos"]}`'


def _cap_pos(S, B, ret):
    k, l, r = S['inorder_pos'], S['left'], S['right']
    return f'根 `{S["root_val"]}` 在中序的位置 `{k}`：左子树 `[{l}, {k})` 有 {k - l} 个，右子树 `[{k + 1}, {r})` 有 {r - 1 - k} 个'


def _entered(S, B):
    return S.get('root_pos') != B.get('root_pos')


def _enter_msg(S, side):
    return f'进入{side}子树：`build(left={S["left"]}, right={S["right"]}, root_pos={S["root_pos"]})`'


def _cap_if_r(S, B, ret):
    k, r = B['inorder_pos'], B['right']
    if k < r - 1:
        return f'`{k} < {r} - 1`：根右边还有数 → ==先建右子树=='
    return f'`{k} == {r} - 1`：根是区间最后一个 → 没有右子树'


def _cap_build_r(S, B, ret):
    if _entered(S, B):
        return _enter_msg(S, '右')
    k, r, rp = B['inorder_pos'], B['right'], B['root_pos']
    return (f'后序倒着看是==根-右-左==：根的前一个就是右子树的根 → '
            f'`root_pos - 1 = {rp - 1}`，中序 `[{k + 1}, {r})`')


def _cap_if_l(S, B, ret):
    k, l = B['inorder_pos'], B['left']
    if k > l:
        return f'`{k} > {l}`：根左边有 {k - l} 个数 → 再建左子树'
    return f'`{k} == {l}`：根左边没有数 → 没有左子树'


def _cap_build_l(S, B, ret):
    if _entered(S, B):
        return _enter_msg(S, '左')
    k, l, r, rp = B['inorder_pos'], B['left'], B['right'], B['root_pos']
    rs = r - 1 - k
    return (f'左子树的根要==跳过根和整棵右子树==（{rs} 个）：'
            f'`{rp} - {rs} - 1 = {rp - rs - 1}`，中序 `[{l}, {k})`')


CONFIG = dict(
    num=106, title='从中序与后序遍历序列构造二叉树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='后序定根 · root_pos 倒着走（先右后左）',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def buildTree(self, inorder, postorder):
        if not inorder:
            return None

        pos_dict = {}
        for index, val in enumerate(inorder):
            pos_dict[val] = index

        return self.build(0, len(inorder), inorder, postorder, len(inorder) - 1, pos_dict)

    def build(self, left, right, inorder, postorder, root_pos, pos_dict):
        if left == right:
            return None

        root_val = postorder[root_pos]
        inorder_pos = pos_dict[root_val]
        root = TreeNode(root_val)

        if inorder_pos < right - 1:
            root.right = self.build(inorder_pos + 1, right, inorder, postorder,
                                    root_pos - 1, pos_dict)
        if inorder_pos > left:
            root.left = self.build(left, inorder_pos, inorder, postorder,
                                   root_pos - (right - 1 - inorder_pos) - 1, pos_dict)
        return root
''',
    call=f'Solution().buildTree({INO}, {POST})',
    result_fn=tree_list,
    expect=[3, 9, 20, 1, None, 15, 7],
    views=[
        dict(type='array', var='inorder', label='inorder（窗口 = [left, right)，橙 = 根，蓝 = 左，粉 = 右）', cell=64,
             window=('left', 'right - 1'), color=_in_color, pointers={IP: 'orange'}, pointer_labels={IP: 'inorder_pos'}),
        dict(type='array', var='postorder', label='postorder（根在最后，往前依次是右子树、左子树）', cell=64,
             color=_post_color, dim=_post_dim, pointers={'root_pos': 'cyan'}),
        dict(type='tree', label='正在构造的树（先建根，返回后才接上右、左子树）', h=180),
        dict(type='calls_lite', h=110, hide=('inorder', 'postorder', 'pos_dict')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('root_pos', 'root_pos', 'cyan'),
           ('inorder_pos', IP, 'orange')],
    captions={
        'return self.build(0': '`pos_dict` 记下中序位置；整棵树：中序 `[0, {len(inorder)})`，根是后序==最后一个== `root_pos = {len(inorder) - 1}`',
        'if left == right': _cap_if,
        'root_val = postorder[root_pos]': '==后序遍历的最后一个节点就是根==：`postorder[{root_pos}] = {root_val}`，先把根建出来',
        'inorder_pos = pos_dict': _cap_pos,
        'if inorder_pos < right - 1': _cap_if_r,
        'root.right = self.build': _cap_build_r,
        'if inorder_pos > left': _cap_if_l,
        'root.left = self.build': _cap_build_l,
        'return root': '以 `{root.val}` 为根的子树建好了，返回',
    },
    skip=['root = TreeNode(root_val)', 'if not inorder', 'pos_dict = {}', 'for index, val', 'pos_dict[val] = index', 'return None',
          'if left == right', 'root_pos - 1, pos_dict)', 'root_pos - (right - 1 - inorder_pos) - 1, pos_dict)'],
    max_steps=60,
    cards=dict(
        one_liner='后序最后一个是根，中序分左右；root_pos 倒着走，先建右子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给出同一棵树的==中序遍历== `inorder` 和==后序遍历== `postorder`，构造这棵二叉树',
                 '示例：`inorder = [9,3,15,20,7]`，`postorder = [9,15,7,20,3]` → `[3,9,20,null,null,15,7]`',
                 '本视频：`inorder = [1,9,3,15,20,7]`，`postorder = [1,9,15,7,20,3]`',
                 '→ `[3,9,20,1,null,15,7]`'],
        quote='前序遍历的顺序为根-左-右，而后序遍历则是左-右-根，因此前序遍历的第一个节点为根节点，而==后续遍历的最后一个节点为根节点==。找到根节点后，通过中序遍历得到左右子树节点的数目，然后在前序/后序遍历中划分出左右子树。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`root_pos`：当前子树的根在后序中的位置，==不切分数组==（沿用 105 题的写法）',
              '后序倒过来是==根-右-左==：右子树的根就在 `root_pos - 1`',
              '左子树的根还要跳过整棵右子树：`root_pos - 右子树大小 - 1`'],
        summary=['时间 `O(n)`：`pos_dict` 让找根 `O(1)`；空间 `O(n)`',
                 '易错：右子树存在的条件是 `inorder_pos < right - 1`（区间左闭右开）',
                 '易错：左子树的根 = `root_pos - (right - 1 - inorder_pos) - 1`，别漏了跳过右子树',
                 '对比灵神：灵神 dfs 用 `post_l/post_r` 表示区间、先左后右；这里只记一个 `root_pos`',
                 '原文为 Python 2 风格：删去了文档字符串；两行过长的调用拆成两行，逻辑未改'],
    ),
)
