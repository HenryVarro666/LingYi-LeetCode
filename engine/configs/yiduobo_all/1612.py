CONFIG = dict(
    num=1612, title='检查两颗二叉树表达式是否等价', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层次遍历 + 哈希表计数',
    tags=['灵神题单', '链表树与回溯'],
    setup='''
class Node(TreeNode):
    def __init__(self, val=" ", left=None, right=None):
        super().__init__(val, left, right)
def P(l, r):
    return Node('+', l, r)
root1 = P(P(Node('a'), Node('b')), P(Node('a'), Node('c')))
root2 = P(P(Node('a'), P(Node('c'), Node('a'))), Node('b'))
''',
    code='''
class Solution(object):
    def checkEquivalence(self, root1, root2):

        cnt = {}
        head, tail = 0, 1

        q = [root1]
        while head < tail:
            now = q[head]
            head += 1
            if now.val == '+':
                q.append(now.left)
                q.append(now.right)
                tail += 2
            else:
                cnt[now.val] = cnt.get(now.val, 0) + 1

        head, tail = 0, 1
        q = [root2]
        while head < tail:
            now = q[head]
            head += 1
            if now.val == '+':
                q.append(now.left)
                q.append(now.right)
                tail += 2
            elif cnt.get(now.val, 0) == 0:
                return False
            else:
                cnt[now.val] -= 1

        for v in cnt.values():
            if v > 0:
                return False
        
        return True
''',
    call='Solution().checkEquivalence(root1, root2)',
    expect=True,
    views=[
        dict(type='tree', var='root1', label='root1：蓝 = 当前节点 now', pointers={'now': 'blue'}, path=False, h=200),
        dict(type='tree', var='root2', label='root2', pointers={'now': 'blue'}, path=False, h=200),
        dict(type='map', var='cnt', label='cnt（变量出现次数）', h=120),
        dict(type='text', fn=lambda S: f"队列 `q = {[x.val for x in S['q']]}`，`head = {S['head']}`" if 'q' in S and 'head' in S else '', size=24, h=50),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('now', lambda S: S['now'].val if 'now' in S else None, 'yellow')],
    captions={
        'cnt = {}': '`cnt` 统计 root1 里每个变量被累加了几次',
        5: '`head` 是队首下标，`tail` 是队列长度：队列里只有根一个节点',
        18: '`head`、`tail` 重置：队列重新只有 root2 的根',
        'q = [root1]': '从 root1 开始层次遍历',
        'q = [root2]': '换成 root2：这次是==扣除==，而不是计数',
        'now = q[head]': '取出队首 `{now.val}`',
        'if now.val ==': lambda S, B, r: (f'`{S.now.val}` 是加号 → 内部节点，把左右孩子都放进队列' if S.now.val == '+' else f'`{S.now.val}` 是变量（叶子）→ 它会被累加到结果里'),
        'cnt[now.val] = cnt.get': '变量 `{now.val}` 计数 +1 → `cnt = {cnt}`',
        'elif cnt.get(now.val, 0) == 0': lambda S, B, r: (f'`cnt[{S.now.val}] = {S.cnt.get(S.now.val, 0)}` 已经用完 → root2 里多出一个 `{S.now.val}` → ==不等价==' if S.cnt.get(S.now.val, 0) == 0 else f'`cnt[{S.now.val}] = {S.cnt.get(S.now.val, 0)} > 0` → 还有名额，可以扣'),
        'cnt[now.val] -= 1': '扣掉一个 `{now.val}` → `cnt = {cnt}`',
        'for v in cnt.values()': lambda S, B, r: f'检查剩余次数：`v = {S.v}`' + (' > 0 → root1 里还有没被 root2 用掉的变量 → ==不等价==' if S.v > 0 else '，已经扣光'),
        'return True': '两边变量的出现次数完全一致 → ==等价==',
    },
    skip=['head += 1', 'tail += 2', 'q.append', 'if v > 0'],
    max_steps=120,
    cards=dict(
        one_liner='树里只有加法：每个叶子都加一次，比一比每个变量出现的次数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两棵表达式树：叶子是变量（小写字母），内部节点只有 `+`',
                 '判断两棵树表示的表达式是否==等价==（无论变量取何值结果都相同）',
                 '本视频：`(a+b)+(a+c)` 与 `(a+(c+a))+b`',
                 '都是 `2a + b + c` → `True`'],
        quote='题目的树中只存在加法操作，换言之树中每个叶子节点的值都将被累加到最终结果中，于是可以分别遍历这两棵树，使用哈希表统计每个变量被累加的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['加法满足交换律、结合律：形状无关，只看每个变量出现几次',
              '遍历 root1，叶子计数进 `cnt`；遍历 root2，叶子来一个扣一个',
              '扣不到（次数为 0）或最后有剩余，都说明两边不一样'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：要双向检查——root2 多出来（扣到 0）和 root1 多出来（最后剩余）都要判',
                 '用 `head/tail` 手写队列层次遍历，`tail += 2` 对应加了两个孩子',
                 '题目给的节点类 `Node(val, left, right)` 由 setup 提供',
                 '原文可直接在 Python 3 运行，代码未改'],
    ),
)
