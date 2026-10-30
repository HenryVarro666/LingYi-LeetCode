def _cap_first(S, B, ret):
    lv, n = B['level'], len(B['res'])
    if n == lv:
        return f'`len(res) = {n}` 等于 `level = {lv}` → ==第 {lv} 层第一次被访问==：先右后左，所以它就是这层最右的'
    return f'`len(res) = {n}` > `level = {lv}`：第 {lv} 层已经有更靠右的 `{B["res"][lv]}` 了，被挡住，不记录'


def _cap_has(side, word, first):
    def f(S, B, ret):
        nd = B['now']
        if getattr(nd, side) is not None:
            return f'`{nd.val}` 有{word}儿子 → {first}递归{word}子树'
        return f'`{nd.val}` 没有{word}儿子，跳过'
    return f


CONFIG = dict(
    num=199, title='二叉树的右视图', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='先右后左的 DFS + 答案数组长度判断',
    code='''
class Solution(object):
    def rightSideView(self, root):
        if not root:
            return []

        res = []
        self.dfs(root, 0, res)
        return res

    def dfs(self, now, level, res):
        if len(res) == level:
            res.append(now.val)

        if now.right:
            self.dfs(now.right, level + 1, res)
        if now.left:
            self.dfs(now.left, level + 1, res)
''',
    call='Solution().rightSideView(Tr([1,2,3,4,None,None,None,5]))',
    expect=[1, 3, 4, 5],
    views=[
        dict(type='text', fn=lambda S: f"当前深度 `level = {S['level']}`，已记录 `len(res) = {len(S['res'])}` 层" if 'level' in S else ''),
        dict(type='array', var='res', label='res（res[i] = 第 i 层最右边的节点）', cell=60, color=lambda S, i, v: 'orange'),
        dict(type='tree', pointers={'now': 'blue'}, h=360,
             color=lambda S, n: 'orange' if n.val in (S.get('res') or []) else None),
        dict(type='calls', h=170),
    ],
    watch=[('now', 'now', 'blue'), ('level', 'level', 'cyan'), ('res', 'res', 'orange')],
    captions={
        'if not root': '根不为空，开始 DFS',
        'res = []': '`res[i]` 用来存第 `i` 层最右边的节点值',
        'self.dfs(root, 0, res)': '从根出发，深度 `level = 0`',
        'if len(res) == level': _cap_first,
        'res.append(now.val)': '`res` 加入 `{now.val}`：它是第 {level} 层的最右节点',
        'if now.right:': _cap_has('right', '右', '==先=='),
        'self.dfs(now.right': '进入右儿子 `{now.val}`，深度 `level = {level}`',
        'if now.left:': _cap_has('left', '左', '再'),
        'self.dfs(now.left': '进入左儿子 `{now.val}`，深度 `level = {level}`',
        'return res': '每层第一个到达的节点连起来就是右视图：返回 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='从右往左遍历，每层第一个碰到的就是最右边的节点',
        complexity='时间 `O(n)`，空间 `O(h)`（h 为树高）',
        problem=['站在二叉树的==右侧==，从上到下返回你能看到的节点值',
                 '每一层只能看到==最右边==的那个节点',
                 '示例：`root = [1,2,3,4,null,null,null,5]` → `[1,3,4,5]`'],
        quote='实际上就是先求出二叉树的==层序遍历==，然后将每一层的最后一个节点组合起来…可以将遍历顺序改成==从右往左==，然后通过==答案数组的长度==来判断当前节点是否为本层最右侧节点。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先递归右儿子、再递归左儿子：同一层里==右边的节点总是先被访问==',
              '`res` 里已经有 `len(res)` 层的答案；`len(res) == level` 说明这层第一次来',
              '不用存整个层序遍历，只用答案数组的长度判断'],
        summary=['时间 `O(n)`；空间 `O(h)` 的递归栈',
                 '易错：一定要先 `right` 后 `left`，否则拿到的是左视图',
                 '易错：右视图不一定都是右儿子，左子树更深时（如本例的 `4`、`5`）也能被看到',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
