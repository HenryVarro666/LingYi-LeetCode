CONFIG = dict(
    num=563, title='二叉树的坡度', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='后序递归返回 (和, 坡度)',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findTilt(self, root):
        return self.dfs(root)[1]

    def dfs(self, now):
        if not now:
            return 0, 0

        left_sum, left_tilt = self.dfs(now.left)
        right_sum, right_tilt = self.dfs(now.right)
        return left_sum + right_sum + now.val, left_tilt + right_tilt + abs(left_sum - right_sum)
''',
    call='Solution().findTilt(Tr([4,2,9,3,5,None,7]))',
    expect=15,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, h=320),
        dict(type='text', fn=lambda S: (f"左和 `{S['_inner']['left_sum']}`，右和 `{S['_inner']['right_sum']}` → 本节点坡度 ==|{S['_inner']['left_sum']} - {S['_inner']['right_sum']}| = "
                                         f"{abs(S['_inner']['left_sum'] - S['_inner']['right_sum'])}=="
                                         if 'right_sum' in S['_inner'] else ''), size=26, h=60),
        dict(type='calls', h=210, hide=('root',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('left_sum', lambda S: S['_inner'].get('left_sum'), 'yellow'),
           ('right_sum', lambda S: S['_inner'].get('right_sum'), 'yellow')],
    captions={
        'return self.dfs(root)[1]': '从根出发递归，==返回二元组的第 1 项（总坡度）==',
        'if not now': lambda S, B, r: ('空节点 → 和为 0、坡度为 0，这是==递归边界==' if S.now is None
                                      else f'节点 `{S.now.val}` 非空 → 先递归求左右子树，再算自己'),
        'return 0, 0': '空树 `(和, 坡度) = (0, 0)`',
        'left_sum, left_tilt =': '左子树返回：节点和 `{left_sum}`，坡度合计 `{left_tilt}`',
        'right_sum, right_tilt =': '右子树返回：节点和 `{right_sum}`，坡度合计 `{right_tilt}`',
        'return left_sum': lambda S, B, r: (f'节点 `{S.now.val}`：和 = `{S.left_sum} + {S.right_sum} + {S.now.val} = {r[0]}`；'
                                            f'坡度 = `{S.left_tilt} + {S.right_tilt} + |{S.left_sum} - {S.right_sum}| = {r[1]}`'),
    },
    cards=dict(
        one_liner='先求左右子树，再用两边的节点和差算自己的坡度',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['节点的坡度 = ==左子树节点和与右子树节点和之差的绝对值==',
                 '整棵树的坡度 = 所有节点坡度之和',
                 '示例：`root = [4,2,9,3,5,null,7]` → `15`'],
        quote='可以优先递归求解以p.left和p.right为根节点的子树的坡度以及节点之和，最后求解以p为根节点的子树的坡度以及节点之和。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)` 返回 `(子树节点和, 子树坡度合计)`',
              '节点和 = 左和 + 右和 + 自己',
              '坡度合计 = 左坡度 + 右坡度 + `|左和 - 右和|`'],
        summary=['时间 `O(n)`，每个节点只算一次；空间 `O(h)`',
                 '易错：坡度用的是==节点值之和==的差，不是节点个数之差',
                 '空节点必须返回 `(0, 0)`，否则叶子节点没法算',
                 '最后答案取返回二元组的第 1 项'],
    ),
)
