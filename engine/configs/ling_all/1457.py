def nv(x):
    return '空' if x is None else str(x.val)


def _bits(m):
    return ''.join('1' if m >> k & 1 else '0' for k in range(9, 0, -1))


def _mask_txt(S):
    m = S['_inner'].get('mask')
    if m is None:
        return ''
    odd = [k for k in range(1, 10) if m >> k & 1]
    return f'`mask` 第 1~9 位（高→低 9…1）= `{"".join("1" if m >> k & 1 else "0" for k in range(9, 0, -1))}`，出现奇数次的数字：=={odd if odd else "无"}=='


def _leaf(S, B, ret):
    r = S.root
    if r is None:
        return '空节点 → 没有路径，返回 `0`'
    if r.left is None and r.right is None:
        return f'`{r.val}` 是==叶子==：路径到此结束，检查 `mask` 是否至多一个 1'
    return f'`{r.val}` 不是叶子 → 继续往下走，把 `mask` 传给左右儿子'


def _xor(S, B, ret):
    return f'`{S.root.val}` 加入路径：翻转第 {S.root.val} 位 → `mask = {_bits(S.mask)}`'


def _chk(S, B, ret):
    m = S.mask
    if m & (m - 1) == 0:
        return f'`mask & (mask-1) = 0` → 至多一个奇数次数字 → ==伪回文路径，计 1=='
    return f'`mask & (mask-1) = {m & (m - 1)} ≠ 0` → 有 ≥ 2 个奇数次数字 → 不是伪回文，计 0'


CONFIG = dict(
    num=1457, title='二叉树中的伪回文路径', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS + 位运算维护奇偶性',
    tags=['灵神题单', '链表树与回溯', '难度分 1405'],
    code='''
class Solution:
    def pseudoPalindromicPaths(self, root: Optional[TreeNode], mask=0) -> int:
        if root is None:
            return 0
        mask ^= 1 << root.val  # 修改 root.val 出现次数的奇偶性
        if root.left is None and root.right is None:  # root 是叶子节点
            return 1 if mask & (mask - 1) == 0 else 0
        return self.pseudoPalindromicPaths(root.left, mask) + \\
               self.pseudoPalindromicPaths(root.right, mask)
''',
    call='Solution().pseudoPalindromicPaths(Tr([2,3,1,3,1,None,1]))',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前节点，黄圈 = 递归路径）', pointers={'root': 'blue'}, h=300),
        dict(type='text', fn=_mask_txt, size=24, h=60),
        dict(type='calls', h=210),
    ],
    watch=[('root', lambda S: S['_inner'].get('root').val if S['_inner'].get('root') is not None else None, 'blue'),
           ('mask', lambda S: bin(S['_inner']['mask'])[2:] if 'mask' in S['_inner'] else None, 'yellow')],
    captions={
        'if root is None': lambda S, B, r: ('`root` 是空节点 → 没有路径' if S.root is None else f'节点 `{S.root.val}` 非空 → 继续'),
        'return 0': '空节点：没有路径 → 返回 `0`',
        'mask ^= 1 <<': _xor,
        'if root.left is None and root.right is None': _leaf,
        'return 1 if': _chk,
        'return self.pseudo': lambda S, B, r: (f'先递归左儿子 `{nv(S.root.left)}`，把当前 `mask` 传下去' if r is None else
                                               f'左右子树的伪回文路径数相加 → 返回 `{r}`；`mask` 是参数，回上一层自动恢复，==不用手动回溯=='),
        'self.pseudoPalindromicPaths(root.right': lambda S, B, r: f'再递归右儿子 `{nv(S.root.right)}`，同样传入当前 `mask`',
    },
    cards=dict(
        one_liner='路径能重排成回文 ⇔ 至多一个数字出现奇数次，用一个 mask 记奇偶',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树节点值为 `1~9`，从根到叶的路径若能把节点值重排成回文，就叫伪回文',
                 '返回根到叶子的伪回文路径条数',
                 '示例：`[2,3,1,3,1,null,1]` → `2`（`[2,3,3]` 和 `[2,1,1]`）'],
        quote='所以**恰好有一个数字的出现次数为奇数，其余数字的出现次数均为偶数**。对于长为奇数的路径，只要路径上数字的出现次数满足该要求，就一定可以重新排列成回文序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶回文：每个数出现偶数次；奇回文：拿掉中间那个数，剩下也都是偶数次',
              '只关心奇偶 → 用 ==9 个比特== 压成 `mask`，进节点就异或 `1 << val`',
              '`mask & (mask-1) == 0` 表示至多一个 1（去掉最低位后为空）'],
        summary=['时间 `O(n)`，空间 `O(n)`（链状树时递归栈最深）',
                 '`mask` 按值传参，回溯时不用手动恢复；写法一的数组 `p` 是共享的，必须 `p[x] ^= 1` 恢复',
                 '易错：只在==叶子==判断；`mask == 0`（全偶）也是合法的',
                 '写法一用数组 `p` 维护奇偶、再 `sum(p) <= 1` 判断，本视频演示更简洁的位运算写法',
                 '思考题：2791 把路径放到边权上，用同样的 mask + 哈希表'],
    ),
)
