def _tbits(S):
    return bin(S['target'])[2:] if 'target' in S else ''


def _bcolor(S, k, v):
    if 'target' not in S or 'i' not in S:
        return 'yellow' if k == 0 else None
    kc = len(bin(S['target'])[2:]) - 1 - S['i']
    if k == 0:
        return 'yellow'
    if k < kc:
        return 'green'
    if k == kc:
        return 'blue'
    return None


def _top(S):
    if 'target' not in S:
        return '先看 `FindElements` 保存根节点；下面三次 `find(3)`、`find(5)`、`find(6)`'
    t = S['target']
    b = bin(t)[2:]
    if 'i' not in S:
        return f"`target + 1 = {t}` = 二进制 `{b}`：去掉最高位的 1，其余每一位就是从根往下的路线（0 左、1 右）"
    return f"`{b}`：最高位 1 = 根；之后 0 = ==往左==，1 = ==往右=="


CONFIG = dict(
    num=1261, title='在受污染的二叉树中查找元素', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='二进制即路径',
    tags=['灵神题单·位运算', '灵神题单·链表树与回溯', '难度分 1440'],
    setup='''
root = Tr([-1, -1, -1, -1, -1, None, -1])
# 树本来的值满足 左 = 2x+1、右 = 2x+2；被污染成 -1 后，find 并不用这些值。
# 这里把还原后的值画在节点上，方便观察（find 的代码只看 left / right，不读 val）
def _restore(nd, v):
    if nd is None:
        return
    nd.val = v
    _restore(nd.left, 2 * v + 1)
    _restore(nd.right, 2 * v + 2)
_restore(root, 0)
''',
    code='''
class FindElements:
    def __init__(self, root: Optional[TreeNode]):
        self.root = root

    def find(self, target: int) -> bool:
        target += 1
        cur = self.root  # 从根节点出发
        for i in range(target.bit_length() - 2, -1, -1):  # 从次高位开始枚举
            bit = (target >> i) & 1  # target 第 i 位的比特值
            cur = cur.right if bit else cur.left
            if cur is None:  # 走到空节点，说明 target 不在二叉树中
                return False
        return True  # 没有走到空节点，说明 target 在二叉树中
''',
    call='''f = FindElements(root)
[f.find(3), f.find(5), f.find(6)]''',
    expect=[True, False, True],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='tree', label='二叉树（节点上是还原后的值；蓝 = cur）', pointers={'cur': 'blue'}, path=False, h=300,
             color=lambda S, node: 'blue' if node is S.get('cur') else None),
        dict(type='string', var=_tbits, label='target + 1 的二进制（黄 = 最高位，绿 = 已走过，蓝 = 当前位）', cell=70, h=140,
             color=_bcolor),
    ],
    watch=['target', 'bit', ('cur', "cur.val if cur else None", 'blue')],
    captions={
        'self.root = root': '初始化 O(1)：只把根节点存下来，什么也不用还原',
        'target += 1': lambda S, B, ret: f'`target + 1 = {S.target}` = 二进制 `{bin(S.target)[2:]}`：节点值 +1 之后，二进制就是根到该节点的路线',
        'cur = self.root': '从根出发（最高位的 1 就对应根）',
        'for i in range': lambda S, B, ret: (f'`i = {S.i}`：看 target 的第 {S.i} 位' if 'i' in S and S.get('i') != B.get('i') or 'i' not in B
                                              else '所有位都走完了，没有碰到空节点'),
        'bit = ': '第 `{i}` 位是 `{bit}`：==0 往左，1 往右==',
        'cur = cur.right': lambda S, B, ret: (f"`bit = {S.bit}` → 走{'右' if S.bit else '左'}儿子：`cur` 到" +
                                              (f' 值为 `{S.cur.val}` 的节点' if S.cur else ' ==空==')),
        'if cur is None': lambda S, B, ret: ('`cur` 是空节点：这条路径不存在 → target 不在树里' if S.cur is None
                                             else '`cur` 不为空，继续往下走'),
        'return False': 'target 不在二叉树中，返回 `False`',
        'return True': '一路都没碰到空节点 → target 在树里，返回 `True`',
    },
    cards=dict(
        one_liner='节点值 + 1 的二进制，就是从根走下来的路线',
        complexity='初始化 `O(1)`，`find` 为 `O(min(h, log target))`，空间 `O(1)`',
        problem=['二叉树根值为 0，左儿子值 `2x+1`，右儿子值 `2x+2`；现在所有值都被污染成 -1',
                 '实现 `FindElements`：构造时还原树，`find(target)` 判断 target 是否存在',
                 '本视频：树 `[-1,-1,-1,-1,-1,null,-1]`，依次 `find(3)`、`find(5)`、`find(6)`'],
        quote='没有走到空节点，说明 target 在二叉树中；走到空节点，说明 target 不在二叉树中。',
        quote_src='—— 灵茶山艾府题解代码注释（方法二：二进制即路径）',
        idea=['值 `x` 加 1 后：左儿子是 `2(x+1)`，右儿子是 `2(x+1)+1`，等于在二进制末尾补 0 / 1',
              '所以 `target + 1` 的二进制，去掉最高位后：==0 走左，1 走右==',
              '不用真的还原整棵树，也不用哈希表；路上碰到空节点就说明不存在'],
        summary=['初始化 `O(1)`，`find` 最多走树高，空间 `O(1)`',
                 '一定要先 `target += 1`，否则根（值 0）没法用二进制表示',
                 '循环从次高位开始：`bit_length() - 2`，最高位对应根本身',
                 '视频里节点上画的是还原后的值，代码本身只用 left / right，不读 val',
                 '另一种写法：方法一 DFS 还原并把值存进哈希表，`find` 查表 `O(1)`，空间 `O(n)`'],
    ),
)
