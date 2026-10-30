def _pos(S):
    n = S.get('now')
    if n is None or 'row' not in S or 'num_dict' not in S:
        return ''
    return f"节点 `{n.val}` 在第 `{S['row']}` 行、第 `{S['col']}` 列；左孩子 `(row+1, col−1)`，右孩子 `(row+1, col+1)`"


def _res(S):
    if 'res' not in S:
        return ''
    return f"`res = {S['res']}`"


CONFIG = dict(
    num=987, title='二叉树的垂序遍历', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 记录行列 + 二级字典 + 三次排序',
    tags=['灵神题单', '链表树与回溯', '难度分 1676'],
    code='''
class Solution(object):
    def verticalTraversal(self, root):

        num_dict = {}
        self.dfs(root, 0, 0, num_dict)
    
        res = []
        for col in sorted(num_dict.keys()):
            res.append([])
            for row in sorted(num_dict[col].keys()):
                res[-1].extend(sorted(num_dict[col][row]))
        
        return res

    def dfs(self, now, row, col, num_dict):
        if col not in num_dict:
            num_dict[col] = {}
        
        if row not in num_dict[col]:
            num_dict[col][row] = []
        
        num_dict[col][row].append(now.val)
    
        if now.left:
            self.dfs(now.left, row + 1, col - 1, num_dict)
        
        if now.right:
            self.dfs(now.right, row + 1, col + 1, num_dict)
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,6,7])
s.verticalTraversal(s.tree)''',
    expect=[[4], [2], [1, 5, 6], [3], [7]],
    max_steps=90,
    skip=['num_dict = {}', 'num_dict[col] = {}', 'num_dict[col][row] = []'],
    views=[
        dict(type='text', fn=_pos, size=24, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=260),
        dict(type='map', var='num_dict', label='num_dict：col → {row: [值, ...]}',
             fmt=lambda k, v: f'列 {k}: {v}', h=190),
        dict(type='text', fn=_res, size=24, h=50),
        dict(type='calls', h=140, hide=('num_dict', 'root')),
    ],
    watch=[('now', lambda S: getattr(S.get('now'), 'val', None), 'blue'),
           ('row', lambda S: S['_inner'].get('row'), 'yellow'), ('col', lambda S: S['_inner'].get('col'), 'pink')],
    captions={
        'self.dfs(root, 0, 0': '根在 `(row=0, col=0)`，先 DFS 一趟，把每个节点按「列 → 行」存进二级字典',
        'if col not in num_dict': lambda S, B, r: (f'第 `{S.col}` 列还没出现过 → 新建这一列的字典' if S.col not in B.num_dict
                                                  else f'第 `{S.col}` 列已经有了'),
        'if row not in num_dict[col]': lambda S, B, r: (f'第 `{S.col}` 列的第 `{S.row}` 行还是空的 → 新建列表' if S.row not in B.num_dict[S.col]
                                                       else f'第 `{S.col}` 列第 `{S.row}` 行已有节点（同行同列）→ 值会放进同一个列表'),
        'num_dict[col][row].append': '节点 `{now.val}` 放进 `num_dict[{col}][{row}]` → `{num_dict[col][row]}`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 去 `(row+1, col−1) = ({S.row + 1}, {S.col - 1})`' if S.now.left
                                        else f'`{S.now.val}` 没有左孩子，跳过'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 去 `(row+1, col+1) = ({S.row + 1}, {S.col + 1})`' if S.now.right
                                         else f'`{S.now.val}` 没有右孩子，跳过'),
        'self.dfs(now.left': '进入左孩子：行 +1，列 −1',
        'self.dfs(now.right': '进入右孩子：行 +1，列 +1',
        'res = []': 'DFS 结束：`num_dict` 里已按列、行存好。现在先按列排序，再按行排序，最后按值排序',
        'for col in sorted': lambda S, B, r: (f'从左到右处理第 `{S.col}` 列' if len(S.res) < len(S.num_dict) else '所有列处理完了'),
        'res.append([])': '这一列的结果先放一个空列表',
        'for row in sorted': lambda S, B, r: (f'这一列里，从上到下处理第 `{S.row}` 行' if 'row' in S and S.row in S.num_dict[S.col] and len(S.res[-1]) < sum(len(v) for v in S.num_dict[S.col].values()) else '这一列的行都处理完了'),
        'res[-1].extend': '同一行同一列的值按大小排序后接上：`num_dict[{col}][{row}]` 排序得 `{sorted(num_dict[col][row])}` → `res[-1] = {res[-1]}`',
        'return res': '垂序遍历结果：`{res}`',
    },
    cards=dict(
        one_liner='DFS 时带着行列，用「列 → 行 → 值」的二级字典记下来，再三层排序输出',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['根在 `(0, 0)`，左孩子 `(row+1, col−1)`，右孩子 `(row+1, col+1)`',
                 '按列从左到右输出；列内按行从上到下；同行同列按值从小到大',
                 '本视频：`root = [1,2,3,4,5,6,7]` → `[[4],[2],[1,5,6],[3],[7]]`'],
        quote='由于最终是按列输出，因此dict的一级key为列，二级key为行。dfs完成后，先按列排序，然后按行排序，最后按当前列、行中节点的大小排序然后输出到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['DFS 时带着 `row`、`col`：往左 `col − 1`，往右 `col + 1`，每往下一层 `row + 1`',
              '`num_dict[col][row]` 是一个列表，装着同一个位置上的所有节点值',
              '输出时三层排序：`sorted(列)` → `sorted(行)` → `sorted(值)`，同位置的 5 和 6 在最后一层按值排好'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '对比灵神：灵神用 `(row, val)` 元组一次排序；yiduobo 用二级字典，把行也当 key 逐层排序',
                 '易错：同行同列的节点要按值排序，不是按 DFS 访问顺序',
                 '原文代码未改动，只删除了 LeetCode 模板的文档字符串'],
    ),
)
