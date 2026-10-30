CODE = '''
class Solution(object):
    def getDirections(self, root, startValue, destValue):

        self.start_path = []
        self.dest_path = []

        def dfs(now, path):
            if now.val == startValue:
                self.start_path = path[:]
            if now.val == destValue:
                self.dest_path = path[:]

            if now.left:
                path.append(now.left)
                dfs(now.left, path)
                path.pop()
            
            if now.right:
                path.append(now.right)
                dfs(now.right, path)
                path.pop()
        
        dfs(root, [root])
        p = min(len(self.start_path), len(self.dest_path)) - 1
        while self.start_path[p] != self.dest_path[p]:
            p -= 1

        res = ['U'] * (len(self.start_path) - 1 - p)
        for index in range(p, len(self.dest_path) - 1):
            if self.dest_path[index].left == self.dest_path[index + 1]:
                res.append('L')
            else:
                res.append('R')
        
        return ''.join(res)
'''


def _nodes(x):
    return '→'.join(str(n.val) for n in x) if x else '（还没找到）'


def _info(S):
    if 'self.start_path' not in S:
        return ''
    return f"根到起点 `start_path` = =={_nodes(S['self.start_path'])}==　　根到终点 `dest_path` = =={_nodes(S['self.dest_path'])}=="


def _vv(n):
    return str(n.val)


CONFIG = dict(
    num=2096, title='从二叉树一个节点到另一个节点每一步的方向', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='根到 s、t 的节点路径 · 找 LCA 再看左右孩子',
    tags=['难度分 1805'],
    code=CODE,
    call='''s = Solution()
s.tree = Tr([5,1,2,3,None,6])
s.getDirections(s.tree, 3, 6)''',
    expect='UURL',
    views=[
        dict(type='tree', label='二叉树（蓝 = now；起点 3，终点 6）', pointers={'now': 'blue'}, h=240),
        dict(type='stack', var='path', label='path（根到 now 的节点，绿 = 刚入栈）', fmt=_vv, h=100),
        dict(type='text', fn=_info, size=22, h=62),
        dict(type='calls', h=210, hide=('path',)),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') is not None else None, 'blue'),
           ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'self.start_path = []': '`start_path` 将保存==根到 s== 的节点序列（原文叫 dfs 序）',
        'self.dest_path = []': '`dest_path` 保存==根到 t== 的节点序列',
        'if now.val == startValue': lambda S, B, r: (f'`{B.now.val}` 就是 s → 复制当前路径' if B.now.val == B.startValue else f'`{B.now.val}` 不是 s'),
        'self.start_path = path[:]': lambda S, B, r: f'记下根到 s：=={_nodes(S["self.start_path"])}==（`path[:]` 复制一份，因为 `path` 还会变）',
        'if now.val == destValue': lambda S, B, r: (f'`{B.now.val}` 就是 t → 复制当前路径' if B.now.val == B.destValue else f'`{B.now.val}` 不是 t'),
        'self.dest_path = path[:]': lambda S, B, r: f'记下根到 t：=={_nodes(S["self.dest_path"])}==',
        'if now.left:': lambda S, B, r: (f'`{B.now.val}` 有左孩子 `{B.now.left.val}` → 走进去' if B.now.left else f'`{B.now.val}` 没有左孩子'),
        'if now.right:': lambda S, B, r: (f'`{B.now.val}` 有右孩子 `{B.now.right.val}` → 走进去' if B.now.right else f'`{B.now.val}` 没有右孩子'),
        'path.append(now.left)': '左孩子 `{now.left.val}` 入 `path`',
        'path.append(now.right)': '右孩子 `{now.right.val}` 入 `path`',
        'dfs(now.left, path)': lambda S, B, r: f'递归左孩子 `{B.now.left.val}`',
        'dfs(now.right, path)': lambda S, B, r: f'递归右孩子 `{B.now.right.val}`',
        'path.pop()': '==回溯==：这个孩子的子树搜完，`path` 弹出一个节点',
        'dfs(root, [root])': '从根出发，`path` 一开始只有根',
        'p = min(': lambda S, B, r: (f'两条路径长度 `{len(S["self.start_path"])}` 和 `{len(S["self.dest_path"])}`，取短的最后一位 `p = {S.p}` 开始往前找'),
        'while self.start_path[p] != self.dest_path[p]': lambda S, B, r: (
            f'`start_path[{S.p}] = {S["self.start_path"][S.p].val}`，`dest_path[{S.p}] = {S["self.dest_path"][S.p].val}`：'
            + ('相同 → 找到了最近公共祖先 ==' + str(S["self.start_path"][S.p].val) + '==' if S["self.start_path"][S.p] is S["self.dest_path"][S.p]
               or S["self.start_path"][S.p].val == S["self.dest_path"][S.p].val else '不同 → 还没到公共部分，继续往前')),
        'p -= 1': '这一位不同 → 往根的方向退一格：`p` → {p}',
        "res = ['U']": '从 s 到 lca：路径上 `{len(self.start_path) - 1 - p}` 步全是 ==向上 `U`==（`len(start_path) - 1 - p`）',
        'for index in range': lambda S, B, r: (
            '从 lca 到 t：逐对考察 `dest_path` 里相邻的节点' if 'index' not in B else
            (f'看下一对：`index = {S.index}`' if B.index + 1 < len(S['self.dest_path']) - 1 else '相邻的节点都看完了 → 方向收集完毕')),
        'if self.dest_path[index].left': lambda S, B, r: (
            f'`{S["self.dest_path"][S.index + 1].val}` 是 `{S["self.dest_path"][S.index].val}` 的左孩子' if S["self.dest_path"][S.index].left == S["self.dest_path"][S.index + 1]
            else f'`{S["self.dest_path"][S.index + 1].val}` 不是 `{S["self.dest_path"][S.index].val}` 的左孩子 → 是右孩子'),
        "res.append('L')": '后一个节点是左孩子 → 加 `L` → `{res}`',
        "res.append('R')": '后一个节点是右孩子 → 加 `R` → `{res}`',
        'return': '拼接得到答案 ==`{ret}`==',
    },
    max_steps=100,
    cards=dict(
        one_liner='先找根到 s、根到 t 的两条路，公共部分的末尾就是 lca',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树里给起点 `s` 和终点 `t`，求最短路径每一步的方向',
                 '`L` 去左孩子，`R` 去右孩子，`U` 回父亲',
                 '示例：`[5,1,2,3,null,6,4]`，`3 → 6` → `"UURL"`',
                 '本视频：`[5,1,2,3,null,6]`，起点 `3`，终点 `6`'],
        quote='最短路径就是从s向上走到s和t的最近公共祖先，再从这个最近公共祖先向下走到t。',
        quote_src='—— yiduobo 题解',
        idea=['做一次 DFS，`path` 里放==节点==（不是方向），遇到 s、t 各复制一份',
              '两条路径的前缀相同的部分都是公共祖先，==最后一个相同节点 = lca==',
              's 到 lca：向上走 `len(start_path) - 1 - p` 步，全是 `U`',
              'lca 到 t：看 `dest_path` 相邻两节点，后者是前者的左孩子就 `L`，否则 `R`'],
        result='运行结束，返回 `"UURL"`：`3 → 1 → 5` 上两步，`5 → 2` 是 `R`，`2 → 6` 是 `L`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`path[:]` 要复制，否则回溯后里面的内容会被改掉',
                 '`p` 从较短路径的末尾往前退，直到两条路径在同一位置节点相同',
                 '对比灵神：灵神 `path` 存 `L/R` 字符、求最长公共前缀；yiduobo 存节点、再判断左右孩子',
                 '原文为 Python 2 风格，仅删去了 `:type` 文档字符串；为满足 `self.xxx` 变量展示，驱动里先建了 `Solution` 对象'],
    ),
)
