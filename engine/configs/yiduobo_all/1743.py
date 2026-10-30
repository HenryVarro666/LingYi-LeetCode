CONFIG = dict(
    num=1743, title='从相邻元素对还原数组', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='邻接表 + 从端点顺序还原', tags=[],
    code='''
class Solution(object):
    def restoreArray(self, adjacentPairs):

        g = {}
        for x, y in adjacentPairs:
            if x not in g:
                g[x] = []
            g[x].append(y)
            if y not in g:
                g[y] = []
            g[y].append(x)
        
        for x in g:
            if len(g[x]) == 1:
                break
        
        res = [x]
        used = set([x])
        while len(res) < len(adjacentPairs) + 1:
            x = res[-1]
            if g[x][0] not in used:
                res.append(g[x][0])
                used.add(g[x][0])
            else:
                res.append(g[x][1])
                used.add(g[x][1])
        
        return res
''',
    call='Solution().restoreArray([[4,-2],[1,4],[-3,1]])',
    expect=[-2, 4, 1, -3],
    views=[
        dict(type='map', var='g', label='g（每个数的邻居）', h=250),
        dict(type='array', var='res', label='res（已还原）', cell=80, h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='set', var='used', label='used', h=130),
    ],
    watch=[('x', 'x', 'blue'), ('res', 'res', 'green')],
    captions={
        'g = {}': '`g` 邻接表：记录每个数相邻的数',
        'for x, y in adjacentPairs': '取一对相邻元素 `({x}, {y})`',
        'if x not in g': '`{x}` 第一次出现，先给它建空列表',
        'g[x].append(y)': '`{x}` 的邻居里加入 `{y}`：`g[{x}] = {g[x]}`',
        'if y not in g': '`{y}` 第一次出现，先给它建空列表',
        'g[y].append(x)': '相邻是双向的，`{y}` 的邻居里加入 `{x}`：`g[{y}] = {g[y]}`',
        'for x in g': '依次检查每个数',
        'if len(g[x]) == 1': lambda S, B, r: (f'`{S.x}` 只有 1 个邻居 → 它是数组的端点！' if len(S.g[S.x]) == 1 else f'`{S.x}` 有 {len(S.g[S.x])} 个邻居 → 在中间，继续找'),
        'break': '找到端点 `{x}`，任选一个端点当起点',
        'res = [x]': '起点 `{x}` 放在最左侧',
        'used = set': '`used` 记录已放入的数，避免走回头路',
        'while len(res)': lambda S, B, r: (f'`len(res) = {len(S.res)} < {len(S.adjacentPairs)+1}`，还没填满，继续' if len(S.res) < len(S.adjacentPairs) + 1 else f'`res` 已填满 {len(S.res)} 个 → 结束'),
        'x = res[-1]': '看最右侧的数 `{x}`，它的下一个数必在邻居里',
        'if g[x][0] not in used': lambda S, B, r: (f'邻居 `{S.g[S.x][0]}` 没用过 → 就是下一个' if S.g[S.x][0] not in S.used else f'邻居 `{S.g[S.x][0]}` 已用过（是来时的路）→ 看另一个邻居'),
        'res.append(g[x][0])': '把 `{g[x][0]}` 接在右边：`res = {res}`',
        'used.add(g[x][0])': '标记已使用',
        'res.append(g[x][1])': '把 `{g[x][1]}` 接在右边：`res = {res}`',
        'used.add(g[x][1])': '标记已使用',
        'return res': '还原完成 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='只出现一次的数就是端点，从它顺着邻居走一遍',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 的元素互不相同，丢失了顺序，只知道所有相邻元素对 `adjacentPairs`（顺序任意）',
                 '还原原数组，答案可以是任意一个合法结果',
                 '示例：`[[4,-2],[1,4],[-3,1]]` → `[-2,4,1,-3]`'],
        quote='对于数组中最左侧和最右侧的两个数而言，其只会在相邻元素对当中出现一次，于是可以找出只出现一次的数字，应该可以找到两个。任选一个填到数组最左侧',
        quote_src='—— yiduobo 题解原文',
        idea=['建邻接表，端点只有 1 个邻居，其余数有 2 个',
              '从端点 x 出发，下一个数是 x 的邻居',
              '之后每个数有两个邻居，其中一个是来路（已用过），另一个就是下一步',
              '若元素可重复，就要用欧拉路径，原文没展开'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：相邻对是无序的，两个方向都要加入邻接表',
                 '易错：用 `used` 排除来路，不能只看 `g[x][0]`',
                 '前提：元素互不相同，所以链是唯一的',
                 '原文代码无需修改，直接运行'],
    ),
)
