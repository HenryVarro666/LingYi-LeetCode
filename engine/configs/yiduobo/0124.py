def _cap_l(S, B, ret):
    kid = S.get('now')
    return f'先递归求左儿子的 `f`（`{B["now"].val}` 的左边' + ('是空的）' if kid is None else f'是 `{kid.val}`）')


def _cap_r(S, B, ret):
    kid = S.get('now')
    return f'`f[左] = max_left = {B["max_left"]}`；再递归右儿子' + ('（空的）' if kid is None else f'（`{kid.val}`）')


def _cap_res(S, B, ret):
    l, r, v = S['max_left'], S['max_right'], S['now'].val
    cand = v + max(l, 0) + max(r, 0)
    old, new = B['self.res'], S['self.res']
    up = '==更新==' if new != old else '不变'
    return (f'以 `{v}` 为根配左右两段：`{v} + max({l}, 0) + max({r}, 0) = {cand}`，'
            f'`res = max({old}, {cand})` → {up} `{new}`')


def _cap_ret(S, B, ret):
    l, r, v = S['max_left'], S['max_right'], S['now'].val
    s = f'`f[{v}] = max({l}, {r}, 0) + {v} = {ret}`：以 `{v}` 为端点的最大路径值'
    if ret < 0:
        s += '（==是负数也照样返回==，父亲那里会和 0 比较）'
    return s


CONFIG = dict(
    num=124, title='二叉树中的最大路径和', difficulty='Hard', category='二叉树',
    author='yiduobo', technique='树形 DP：f[p] = 以 p 为端点的最大路径值',
    code='''
class Solution(object):
    def maxPathSum(self, root):
        self.res = root.val
        self.dfs(root)
        return self.res

    def dfs(self, now):
        if not now:
            return 0

        max_left = self.dfs(now.left)
        max_right = self.dfs(now.right)

        self.res = max(self.res, now.val + max(max_left, 0) + max(max_right, 0))
        return max(max_left, max_right, 0) + now.val
''',
    call='Solution().maxPathSum(Tr([-10,9,20,None,None,15,-7]))',
    expect=35,
    views=[
        dict(type='text', fn=lambda S: (f"`f[{S['now'].val}] = max({S['max_left']}, {S['max_right']}, 0) + {S['now'].val}` = =={max(S['max_left'], S['max_right'], 0) + S['now'].val}=="
                                        if S.get('now') is not None and 'max_right' in S and 'max_left' in S else
                                        '转移方程 `f[p] = max(f[p.left], f[p.right], 0) + p.val`')),
        dict(type='tree', pointers={'now': 'blue'}, h=400),
        dict(type='calls', h=180),
    ],
    watch=[('max_left', 'max_left', 'cyan'), ('max_right', 'max_right', 'purple'), ('res', 'self.res', 'green')],
    captions={
        'self.res = root.val': '`res` 先设为根的值：路径至少包含一个节点',
        'self.dfs(root)': '从根开始，递归求每个节点的 `f`',
        'return 0': '空节点：`f = 0`',
        'max_left = self.dfs': _cap_l,
        'max_right = self.dfs': _cap_r,
        'self.res = max(': _cap_res,
        'return max(max_left': _cap_ret,
        'return self.res': '返回 =={ret}==',
    },
    skip=['if not now'],
    max_steps=60,
    cards=dict(
        one_liner='f[p] 是以 p 为端点的最优路径；答案 = 某个 root 配上左右两段',
        complexity='时间 `O(n)`，空间 `O(h)`（h 为树高）',
        problem=['路径：沿着边走、每个节点最多一次、==至少一个节点==，不一定经过根',
                 '求所有路径中节点值之和的最大值',
                 '示例：`root = [-10,9,20,null,null,15,-7]` → `35`（`15→20`）'],
        quote='这条路径的形式一定是==某棵子树的root==，以及root连接起来的左子树中包含root.left的路径和右子树中包含root.right的路径。左右子树中的这两条路径==都是可以为空的==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['定义 `f[p]`：以 `p` 为根的子树中，==以 p 为端点==的最大路径值',
              '转移：`f[p] = max(f[左], f[右], 0) + p.val`，小于 0 的一侧不接',
              '答案：`p.val + max(f[左],0) + max(f[右],0)`；`f` 只用一次，递归传值即可'],
        summary=['时间 `O(n)`，空间 `O(h)` 的递归栈',
                 '`res` 初始化为 `root.val`，保证全是负数时也正确',
                 '和灵神写法的区别：这里 `f` 可以是负数，在==使用时==才和 0 取 max',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
