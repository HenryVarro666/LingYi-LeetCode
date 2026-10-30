T8 = 8


def _path_to(root, uid):
    if root is None:
        return None
    if root._uid == uid:
        return [root]
    for ch in (root.left, root.right):
        p = _path_to(ch, uid)
        if p:
            return [root] + p
    return None


def _cap_ans(S, B, ret):
    s, t = S['s'], S['targetSum']
    c = S['ans'] - B['ans']
    head = f'把 `{S["node"].val}` 当路径==终点==：起点个数 = `cnt[{s} - {t}] = cnt[{s - t}] = {c}`'
    if c:
        nodes = _path_to(S['root'], S['node']._uid) or []
        pre, found = 0, []
        for i, nd in enumerate(nodes):
            if pre == s - t:
                found.append('→'.join(str(x.val) for x in nodes[i:]))
            pre += nd.val
        return head + f' → ==找到 {c} 条==：`{"`、`".join(found)}`'
    return head + ' → 这里没有'


def _cap_call(word):
    def f(S, B, ret):
        kid = S.get('node')
        par = B['node'].val
        if kid is None:
            return f'`{par}` 的{word}儿子为空 → 直接返回'
        return f'递归{word}子树 `{kid.val}`，把 `s = {S["s"]}` 传下去（参数是==复制==的，不用恢复）'
    return f


def _text(S):
    if S.get('node') is None or 's' not in S or 'cnt' not in S:
        return ''
    nodes = _path_to(S.get('root'), S['node']._uid) or []
    if S['s'] != sum(n.val for n in nodes):  # 刚进入这一层，s 还没加上 node.val
        return ''
    s, t = S['s'], S['targetSum']
    return f"`s = {s}`：要找的起点前缀和 = `s − targetSum = {s - t}`，`cnt` 里有 =={S['cnt'].get(s - t, 0)}== 个"


CONFIG = dict(
    num=437, title='路径总和 III', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='前缀和 + 哈希表 + 恢复现场',
    code='''
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # key：从根到 node 的节点值之和
        # value：节点值之和的出现次数
        # 注意在递归过程中，哈希表只保存根到 node 的路径的前缀的节点值之和
        cnt = defaultdict(int)
        cnt[0] = 1
        ans = 0

        # s 表示从根到 node 的父节点的节点值之和（node 的节点值尚未计入）
        def dfs(node: Optional[TreeNode], s: int) -> None:
            if node is None:
                return

            nonlocal ans
            s += node.val
            # 把 node 当作路径的终点，统计有多少个起点
            ans += cnt[s - targetSum]

            cnt[s] += 1
            dfs(node.left, s)
            dfs(node.right, s)
            cnt[s] -= 1  # 恢复现场（撤销 cnt[s] += 1）

        dfs(root, 0)
        return ans
''',
    call='Solution().pathSum(Tr([10,5,-3,3,None,None,11]), 8)',
    expect=2,
    views=[
        dict(type='text', fn=_text),
        dict(type='map', var=lambda S: {k: v for k, v in S['cnt'].items() if v} if 'cnt' in S else None,
             label='cnt（前缀和 → 出现次数；只画次数 > 0 的键）',
             fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='tree', pointers={'node': 'blue'}, h=330),
        dict(type='calls', h=170),
    ],
    watch=[('s', 's', 'cyan'), ('targetSum', 'targetSum'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '哈希表 `cnt`：根到当前节点的路径上，每个==前缀和==出现了几次',
        'cnt[0] = 1': '`cnt[0] = 1`：相当于前缀和数组的 `s[0] = 0`，这样==从根出发的路径==也能写成两个前缀和之差',
        'ans = 0': '`ans` 统计答案',
        's += node.val': '`s` = 根到 `{node.val}` 的路径和 = `{B.s} + {node.val}` = =={s}==',
        'ans += cnt[': _cap_ans,
        'cnt[s] -= 1': '==恢复现场==：`{node.val}` 的子树走完了，撤销前缀和 `{s}`，别的分支用不到它',
        'cnt[s] += 1': '把前缀和 `{s}` 记进 `cnt`：给 `{node.val}` 下面的节点当==起点==用',
        'dfs(node.left, s)': _cap_call('左'),
        'dfs(node.right, s)': _cap_call('右'),
        'dfs(root, 0)': '从根出发，`s = 0`（根的值还没计入）',
        'return ans': '每个节点都当过一次终点：返回 =={ret}==',
    },
    skip=['if node is None', '                return'],
    max_steps=60,
    cards=dict(
        one_liner='把树上的路径当成 560 题的子数组：枚举终点，用前缀和数起点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求二叉树里节点值之和等于 `targetSum` 的==路径==数目',
                 '路径不必从根开始、不必在叶子结束，但方向必须==向下==（父 → 子）',
                 '示例：`root = [10,5,-3,3,null,null,11]`，`targetSum = 8`',
                 '→ `2` 条：`5→3` 和 `-3→11`'],
        quote='DFS 遍历这棵树，遍历到节点 node 时，假设 node 是路径的==终点==，那么有多少个==起点==，满足起点到终点 node 的路径总和恰好等于 targetSum？',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 560 题一样：一边遍历，一边用 `cnt` 统计根到当前节点的==前缀和==',
              '设根到 `node` 的路径和为 `s`，起点个数就是 `cnt[s - targetSum]`',
              '递归完 `node` 的子树要==恢复现场== `cnt[s] -= 1`，否则会被其他分支误用'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希表 + 递归栈）',
                 '易错：`cnt[0] = 1` 不能少，否则从根开始的路径统计不到',
                 '易错：先更新 `ans` 再 `cnt[s] += 1`，否则 `targetSum = 0` 时会把空路径算进去',
                 '`s` 是参数，按值传递，不用恢复；`cnt` 是共享的，必须恢复',
                 '注：`defaultdict` 查询不存在的键会插入 0，动画里只画次数大于 0 的键'],
    ),
)
