def _fq(p):
    return f'{p[0].val}|{p[1]:b}'


def _info(S):
    st = S.get('state')
    if st is None:
        return '队列里每项是 `[节点, 路径奇偶编码]`；编码第 `v-1` 位 = 数字 `v` 出现次数的奇偶'
    t = S.get('tmp')
    extra = f'，lowbit 循环：`tmp = {t:b}`，已数出 `cnt = {S.get("cnt")}` 个 1' if t is not None and 'cnt' in S else ''
    return f'当前编码 `state = {st:b}`（9 位：{st:09b}）{extra}'


def _node(S, B, ret):
    return f'`{S.now.val}`'


CONFIG = dict(
    num=1457, title='二叉树中的伪回文路径', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS + 9 位二进制编码 + lowbit',
    tags=['灵神题单', '链表树与回溯', '难度分 1405'],
    code='''
class Solution(object):
    def pseudoPalindromicPaths (self, root):

        q = [[root, 0]]
        l = 0
        r = 1
        res = 0
        while l < r:
            now, state = q[l]
            l += 1
            state ^= (1 << (now.val - 1))
            if now.left is None and now.right is None:
                tmp = state
                cnt = 0
                while tmp:
                    cnt += 1
                    tmp -= tmp & - tmp
                
                if cnt <= 1:
                    res += 1
            else:
                if now.left:
                    q.append([now.left, state])
                    r += 1
                if now.right:
                    q.append([now.right, state])
                    r += 1
        
        return res
''',
    call='Solution().pseudoPalindromicPaths(Tr([2,3,1,3,1,None,1]))',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=290, path=False),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='stack', var='q', label='队列 q（节点|编码，绿 = 刚入队）', fmt=_fq, h=130),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('state', lambda S: f"{S['state']:b}" if 'state' in S else None, 'yellow'),
           ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'q = [[root, 0]]': '队列里放 `[节点, 编码]`：根节点出发时编码 `0`（还没数字）',
        'l = 0': '`l` 是队头，`r` 是队尾后一格：不用 pop，只移动下标',
        'res = 0': '`res` 统计伪回文路径条数',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：队里还有节点' if S.l < S.r else f'`l = r = {S.l}`：队列空了 → 结束'),
        'now, state = q[l]': lambda S, B, r: f'取出队头：节点 `{S.now.val}`，从根带来的编码 `state = {S.state:b}`',
        'l += 1': '队头后移：`l` → {l}',
        'state ^= ': lambda S, B, r: f'把 `{S.now.val}` 加入编码：翻转第 `{S.now.val - 1}` 位 → `state = {S.state:b}`（==出现奇数次的数字对应位为 1==）',
        'if now.left is None and now.right is None': lambda S, B, r: (
            f'`{S.now.val}` 是==叶子==：根到它的路径完整了，数一数编码里有几个 1' if S.now.left is None and S.now.right is None
            else f'`{S.now.val}` 不是叶子 → 把孩子连同编码入队'),
        'tmp = state': '复制一份 `tmp`，用 lowbit 一个个拆掉 1，`state` 不能破坏',
        'cnt = 0': '`cnt` 记录 1 的个数 = 出现奇数次的数字个数',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp:b}` 还有 1 → 继续拆' if S.tmp else '`tmp = 0`：1 全拆完 → 退出'),
        'cnt += 1': '又拆到一个 1：`cnt` → {cnt}',
        'tmp -= tmp & - tmp': '`tmp & -tmp` 是最低位的 1（==lowbit==），减掉它 → `tmp = {tmp:b}`',
        'if cnt <= 1': lambda S, B, r: (f'`cnt = {S.cnt} ≤ 1` → 至多一个数字奇数次，==可重排成回文==' if S.cnt <= 1
                                        else f'`cnt = {S.cnt} > 1` → 至少两个数字奇数次，排不成回文'),
        'res += 1': '这条根到叶的路径是伪回文：`res` → {res}',
        'q.append([now.left': '左孩子 `{now.left.val}` 带着编码 `{state:b}` 入队，`r` 再 +1',
        'q.append([now.right': '右孩子 `{now.right.val}` 带着编码 `{state:b}` 入队，`r` 再 +1',
        'return res': '队列处理完，共 `{res}` 条伪回文路径',
    },
    skip=['r += 1', 'if now.left:', 'if now.right:', 'cnt = 0'],
    max_steps=90,
    cards=dict(
        one_liner='数字只有 1~9：用 9 位二进制记奇偶，lowbit 数 1 的个数',
        complexity='时间 `O(n)`，空间 `O(n)`（队列）',
        problem=['二叉树节点值 `1~9`；根到叶路径的节点值能重排成回文，就叫伪回文',
                 '返回根到叶的伪回文路径条数',
                 '示例：`[2,3,1,3,1,null,1]` → `2`'],
        quote='需要满足路径中出现次数为奇数次的数字数目小于等于1。由于这里只有9个数字，因此可以进行二进制编码，即使用一个9位二进制数来表示当前路径中数字的奇偶性。',
        quote_src='—— yiduobo 题解',
        idea=['做一次 ==BFS==，队列里每个节点携带「根到它的路径编码」',
              '进节点用异或更新编码；到叶子用 ==lowbit== 数 1 的个数',
              '个数 `≤ 1` 就答案 +1；非叶子则把孩子和编码入队'],
        summary=['时间 `O(n)`，空间 `O(n)`：队列存放整层节点',
                 '编码第 `val-1` 位对应数字 `val`，注意减 1；叶子才判断',
                 '`tmp -= tmp & -tmp` 每次去掉最低位的 1，循环次数 = 1 的个数',
                 '对比灵神：灵神用递归 DFS 把 `mask` 当参数传，判断用 `mask & (mask-1) == 0`；yiduobo 用 BFS + lowbit 计数',
                 '原文为 Python 2 风格，仅多一个 `def pseudoPalindromicPaths (self, root)` 的空格，未改动代码'],
    ),
)
