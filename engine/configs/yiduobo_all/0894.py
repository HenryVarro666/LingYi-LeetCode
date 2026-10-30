def _cnt(v):
    return f'{len(v)} 棵'


def _cap_if(S, B, r):
    N, f = S['N'], S['f']
    if N in f:
        return f'`f[{N}]` 已经算过（{len(f[N])} 棵）→ ==直接复用==，不再重新搜索'
    return f'`{N}` 还不在 `f` 里 → 没算过，要现算'


def _cap_loop(S, B, r):
    i, b = S['_inner'], B['_inner']
    if 'cnt' in b and b['cnt'] == i['cnt']:
        return f'`cnt` 已经枚举完所有奇数（`range(1, {i["N"]}, 2)` 取尽）→ 结束循环'
    return f'枚举左子树节点数 `cnt`（只取奇数）：这一轮 `cnt = {i["cnt"]}`，右子树就有 `{i["N"]} - 1 - {i["cnt"]} = {i["N"] - 1 - i["cnt"]}` 个'


def _cap_l(S, B, r):
    b = B['_inner']
    return f'左子树取 `cnt = {b["cnt"]}` 个节点：递归求 `dfs({b["cnt"]})` 的所有真二叉树'


def _cap_r(S, B, r):
    b = B['_inner']
    return (f'右子树有 `{b["N"]} - 1 - {b["cnt"]} = {b["N"] - 1 - b["cnt"]}` 个节点：递归求 `dfs({b["N"] - 1 - b["cnt"]})`；'
            f'左有 `{len(b["left_list"])}` 种')


CONFIG = dict(
    num=894, title='所有可能的真二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='记忆化搜索 + 枚举左子树节点数',
    tags=[],
    code='''
class Solution(object):
    def allPossibleFBT(self, N):

        if N % 2 == 0:
            return []

        f = {}
        return self.dfs(N, f)
    
    def dfs(self, N, f):
        if N not in f:
            if N == 1:
                f[N] = [TreeNode(0)]
            else:
                f[N] = []
                for cnt in range(1, N, 2):
                    left_list = self.dfs(cnt, f)
                    right_list = self.dfs(N - 1 - cnt, f)
                    for left in left_list:
                        for right in right_list:
                            f[N].append(TreeNode(0))
                            f[N][-1].left = left
                            f[N][-1].right = right
        
        return f[N]
''',
    call='Solution().allPossibleFBT(5)',
    result_fn=lambda r: [tree_list(t) for t in r],
    expect=[[0, 0, 0, None, None, 0, 0], [0, 0, 0, 0, 0]],
    views=[
        dict(type='map', var='f', h=200, label='f：节点数 → 该节点数的所有真二叉树（显示棵数）', fmt=lambda k, v: f'{k} 个节点 → {len(v)} 棵' if isinstance(k, int) else str(v)),
        dict(type='calls', h=300),
    ],
    watch=['N', 'cnt', ('左子树棵数', lambda S: len(S['_inner'].get('left_list', []))),
           ('右子树棵数', lambda S: len(S['_inner'].get('right_list', [])))],
    captions={
        'if N % 2 == 0': lambda S, B, r: (f'`N = {S.N}` 是偶数：真二叉树节点数一定是奇数 → 返回 `[]`' if S.N % 2 == 0 else f'`N = {S.N}` 是奇数，可能有解 → 往下做'),
        'f = {}': '`f` 是记忆化表：`f[N]` 保存 `N` 个节点的所有真二叉树',
        'return self.dfs(N, f)': '开始记忆化搜索：求 `N = {N}` 个节点的所有真二叉树',
        'if N not in f': _cap_if,
        'if N == 1': lambda S, B, r: ('`N == 1` → ==只有一个节点，一棵树== 就是边界' if S['_inner'].get('N') == 1 else '`N > 1` → 根占 1 个，其余分给左右子树'),
        'f[N] = [TreeNode(0)]': '`f[1]` = 单个节点 `[TreeNode(0)]`，==递归边界==',
        'f[N] = []': '`f[{N}]` 先置空，往里追加组合出的树',
        'for cnt in range': _cap_loop,
        'left_list = self.dfs': _cap_l,
        'right_list = self.dfs': _cap_r,
        'for left in left_list': '取下一个左子树；取完就回到外层 `cnt` 循环',
        'for right in right_list': '取下一个右子树；取完就回到上一层循环',
        'f[N].append(TreeNode(0))': '新建根节点 `TreeNode(0)`，加入 `f[{N}]`，现在有 `{len(f[N])}` 棵',
        '.left = left': '把当前根的左子树接上 `left`',
        '.right = right': '右子树接上 `right`：这是一种新的组合',
        'return f[N]': '`f[{N}]` 共 `{len(f[N])}` 棵，返回给上一层',
    },
    cards=dict(
        one_liner='根占 1 个，其余在左右子树里分，两两组合',
        complexity='时间、空间与卡特兰数同阶，约 `O(4^n / n^1.5)`',
        problem=['返回所有含 `N` 个节点的真二叉树（原文称满二叉树）：每个节点恰有 `0` 或 `2` 个子节点，值都是 `0`',
                 '示例：`N = 7` → 5 棵；`N = 3` → `[[0,0,0]]`',
                 '本视频：`N = 5` → 2 棵'],
        quote='对于一颗有n个节点的满二叉树而言，设其根节点为root，那么root的左子树和右子树要么为空，要么也是满二叉树。',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数个节点一定无解，直接返回空列表',
              '枚举左子树节点数 `cnt = 1, 3, 5 ...`，右子树就是 `N-1-cnt` 个',
              '左右列表用记忆化搜索求出，再两两组合接到新根上'],
        summary=['`N` 为偶数返回 `[]`；`cnt` 取奇数，用 `range(1, N, 2)`',
                 '`f` 记忆化：相同节点数的子问题只算一次，不同的树共享子树节点',
                 '对比灵神：灵神按叶子数递推并预处理 `f`；yiduobo 按节点数自顶向下记忆化搜索',
                 '原文为 Python 2 风格，代码无需修改；题目叫真二叉树，原文称满二叉树'],
    ),
)
