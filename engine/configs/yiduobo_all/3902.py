def _qvals(S):
    return [n.val for n in S['q']] if 'q' in S else []


def _info(S):
    if 'level' not in S or 'res' not in S:
        return ''
    side = '从左到右' if S['level'] % 2 == 1 else '从右到左'
    ok = '==有效==' if S.get('flag', True) else '==已失效（本层后续节点不累加）=='
    return f"第 `{S['level']}` 层（{side}）：本层累加 {ok}；`res = {S['res']}`"


def _cap_for(S, B, ret):
    return '`index` 从 `tail-1` 倒着扫到 `head`：每层都从后往前取节点'


def _cap_now(S, B, ret):
    return f'`index` 从队尾往队头倒着走：取出 `q[{S.index}]` = 节点 `{S.now.val}`'


def _cap_cond(S, B, ret):
    n = S.now
    if S.level % 2 == 1:
        return f'第 `{S.level}` 层是奇数层：先入队左孩子再入队右孩子，并检查==左孩子==是否存在'
    return f'第 `{S.level}` 层是偶数层：先入队右孩子再入队左孩子，并检查==右孩子==是否存在'


def _cap_flag(S, B, ret):
    side = '左' if S.level % 2 == 1 else '右'
    return f'节点 `{S.now.val}` 没有{side}孩子 → ==`flag = False`==：它和本层后面的节点都不再累加'


def _cap_add(S, B, ret):
    return f'`flag` 仍为 True → 本层和加上 `{S.now.val}`：`res[-1] = {S.res[-1]}`'


def _cap_next(S, B, ret):
    return f'本层处理完：下一层是 `q[{S.head}:{S.tail}]`，层号 `{S.level}` → `{S.level + 1}`'


CONFIG = dict(
    num=3902, title='二叉树的Z字形层级和', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BFS · 从队尾往队头扫',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def zigzagLevelSum(self, root):
        
        q = [root]
        head, tail = 0, 1
        level = 1
        res = []

        while head < tail:
            flag = True
            res.append(0)

            for index in range(tail - 1, head - 1, -1):
                now = q[index]
                if level % 2 == 1:
                    if now.left:
                        q.append(now.left)
                    else:
                        flag = False
                    if now.right:
                        q.append(now.right)
                else:
                    if now.right:
                        q.append(now.right)
                    else:
                        flag = False
                    if now.left:
                        q.append(now.left)

                if flag:
                    res[-1] += now.val
            
            head, tail = tail, len(q)
            level += 1
    
        return res
''',
    call='Solution().zigzagLevelSum(Tr([1,2,3,4,5,6,7,8]))',
    expect=[1, 5, 4, 0],
    views=[
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, path=False, h=300),
        dict(type='array', var=_qvals, label='队列 q（q[head:tail] 是当前层）',
             pointers={'head': 'green', 'tail': 'pink'}, cell=64, h=130),
        dict(type='array', var='res', label='res（每层的和）', cell=64, h=110),
    ],
    watch=[('level', 'level', 'blue'), ('head', 'head', 'green'), ('tail', 'tail', 'pink'),
           ('flag', 'flag', 'yellow'), ('res', 'res', 'cyan')],
    captions={
        'q = [root]': '队列用列表实现：`q = [root]`，用 `head/tail` 圈出当前层',
        'head, tail = 0, 1': '当前层 = `q[head:tail]`，现在只有根节点',
        'level = 1': '层号从 1 开始：==奇数层左到右，偶数层右到左==',
        'while head < tail': '`head < tail` → 当前层非空，继续' ,
        'res.append(0)': '本层开始：`flag = True`（还没遇到缺孩子的节点），并准备本层的和 `0`',
        'for index in range': _cap_for,
        'now = q[index]': _cap_now,
        'if level % 2 == 1': _cap_cond,
        'flag = False': _cap_flag,
        'res[-1] += now.val': _cap_add,
        'head, tail = tail, len(q)': _cap_next,
        'return res': '队列扫完，每层的和：`{ret}`',
    },
    skip=['if flag:', 'level += 1', 'flag = True', 'res = []', 'for index in range'],
    cards=dict(
        one_liner='BFS 每层从队尾扫到队头，用 `flag` 截断累加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按 Z 字形逐层遍历二叉树：奇数层左到右，偶数层右到左，求每层的节点值之和',
                 '奇数层：首个没有==左孩子==的节点及本层后续节点，不计入层和',
                 '偶数层：首个没有==右孩子==的节点及本层后续节点，不计入层和',
                 '本视频：`root = [1,2,3,4,5,6,7,8]` → `[1,5,4,0]`'],
        quote='所以每一层都是从后往前遍历。需要注意的是，奇数层是先将左孩子入队再将右孩子入队，形成正常的序，而偶数层因为是反序，所以要先将右孩子入队再将左孩子入队。',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数层要逆序遍历，所以整个队列从后往前扫',
              '偶数层从后往前扫时，下一层节点也是倒着入队的 → 再反一次，每层都从后往前扫',
              '奇数层先左后右入队；偶数层先右后左入队，使队列保持正确的顺序',
              '`flag` 一旦变 False，本层后面的节点都不再累加'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个节点入队、出队各一次',
                 '易错：`flag` 要在==累加之前==更新，缺孩子的节点自己也不计入',
                 '易错：奇偶层判断缺孩子的方向相反（奇数看左，偶数看右）',
                 '原文为 Python 2 风格，本题代码无需修改，已直接在 Python 3 运行'],
    ),
)
