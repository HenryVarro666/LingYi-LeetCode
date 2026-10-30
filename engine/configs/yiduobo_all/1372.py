CONFIG = dict(
    num=1372, title='二叉树中的最长交错路径', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='树形 dfs · 返回三元组',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def longestZigZag(self, root):

        return self.dfs(root)[0] - 1
    
    def dfs(self, now):
        if not now.left:
            l_res = 0
            l_left = 0
            l_right = 0
        else:
            l_res, l_left, l_right = self.dfs(now.left)
        
        if not now.right:
            r_res = 0
            r_left = 0
            r_right = 0
        else:
            r_res, r_left, r_right = self.dfs(now.right)
        
        res = max(l_res, r_res, l_right + 1, r_left + 1)

        return res, l_right + 1, r_left + 1
''',
    call='Solution().longestZigZag(Tr([1,2,3,None,4,None,None,5]))',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=320),
        dict(type='text', fn=lambda S: (lambda I: f"左孩子返回 `(l_res, l_left, l_right) = ({I.get('l_res','?')}, {I.get('l_left','?')}, {I.get('l_right','?')})`  右孩子返回 `(r_res, r_left, r_right) = ({I.get('r_res','?')}, {I.get('r_left','?')}, {I.get('r_right','?')})`")(S['_inner']) if 'now' in S else '', size=22, h=60),
        dict(type='calls', h=240, hide=()),
    ],
    watch=[('now', lambda S: S['now'].val if 'now' in S and S['now'] else None, 'blue'),
           ('l_right', lambda S: S['_inner'].get('l_right'), 'cyan'),
           ('r_left', lambda S: S['_inner'].get('r_left'), 'pink'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'return self.dfs(root)[0] - 1': '从根开始 dfs：返回的第一个数是==节点数==，最后要 `- 1` 才是路径长度',
        'if not now.left': lambda S, B, r: (f'`{S.now.val}` 没有左孩子 → 左侧的三个值都是 `0`' if not S.now.left else f'`{S.now.val}` 有左孩子 → 递归求左子树'),
        'l_res = 0': '左侧不存在：`l_res = 0`',
        'l_left = 0': '`l_left = 0`',
        'l_right = 0': '`l_right = 0`',
        'l_res, l_left, l_right = self.dfs': lambda S, B, r: ('进入左孩子，先求它的三元组' if 'l_res' not in S['_inner'] else f'左孩子返回：子树最长 `l_res = {S.l_res}`，以它为起点第一步向左 `l_left = {S.l_left}`、向右 `l_right = {S.l_right}`'),
        'if not now.right': lambda S, B, r: (f'`{S.now.val}` 没有右孩子 → 右侧的三个值都是 `0`' if not S.now.right else f'`{S.now.val}` 有右孩子 → 递归求右子树'),
        'r_res = 0': '右侧不存在：`r_res = 0`',
        'r_left = 0': '`r_left = 0`',
        'r_right = 0': '`r_right = 0`',
        'r_res, r_left, r_right = self.dfs': lambda S, B, r: ('进入右孩子，先求它的三元组' if 'r_res' not in S['_inner'] else f'右孩子返回：子树最长 `r_res = {S.r_res}`，以它为起点第一步向左 `r_left = {S.r_left}`、向右 `r_right = {S.r_right}`'),
        'res = max': '`res = max(l_res, r_res, l_right + 1, r_left + 1)` = `max({l_res}, {r_res}, {l_right + 1}, {r_left + 1})` = =={res}==：要么在子树里，要么经过 now（先左 `{l_right + 1}` / 先右 `{r_left + 1}`）',
        'return res, l_right': '返回 `({res}, {l_right + 1}, {r_left + 1})`：向上一层时，第一步向左 = 左孩子「先向右」的长度 + 1，向右同理',
    },
    skip=[],
    cards=dict(
        one_liner='每个节点返回三个数：子树最长、先向左、先向右',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['交错路径：选一个起点和方向，向左右孩子走，==每一步都要换方向==',
                 '路径长度 = 节点数 − 1，求最长交错路径',
                 '本视频：`root = [1,2,3,null,4,null,null,5]` → `3`（1→2→4→5）'],
        quote='因此方便起见我们也可以将题目转化成求最终交错路径上节点的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先向左的路径：下一个点是 `now.left`，从它开始必须向右，所以 `left = l_right + 1`',
              '先向右同理：`right = r_left + 1`',
              '`res = max(l_res, r_res, left, right)`：最长路径要么在子树里，要么经过 now'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错点：==dfs 算的是节点数==，最后要 `- 1` 才是路径长度',
                 '没有孩子时三个值都是 `0`，所以叶子返回 `(1, 1, 1)`',
                 '原文本来就是 Python 3 可跑的写法，未做修改'],
    ),
)
