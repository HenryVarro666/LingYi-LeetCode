CONFIG = dict(
    num=501, title='二叉搜索树中的众数', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='非递归中序遍历 · 一趟统计',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findMode(self, root):

        if not root:
            return []

        now = root
        val = None
        cnt = 0
        max_cnt = 0
        res = []
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                tmp = now.left
                now.left = None
                now = tmp
            else:
                if val == now.val:
                    cnt += 1
                else:
                    val = now.val
                    cnt = 1
                if cnt == max_cnt:
                    res.append(val)
                elif cnt > max_cnt:
                    res = [val]
                    max_cnt = cnt
                now = now.right

        return res
''',
    call='Solution().findMode(Tr([3,2,4,1,2]))',
    expect=[2],
    views=[
        dict(type='tree', label='BST（左子树被一层层「拆」成链）', pointers={'now': 'blue', 'rightest': 'pink'}, path=False, h=300),
        dict(type='text', h=56, fn=lambda S: f"正在统计的值 `val = {S.get('val')}`，已连续出现 `cnt = {S.get('cnt')}` 次；最多 `max_cnt = {S.get('max_cnt')}`" if 'cnt' in S else ''),
        dict(type='array', var='res', label='res（当前的众数）', h=130),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'),
           ('val', 'val', 'cyan'), ('cnt', 'cnt', 'orange'), ('max_cnt', 'max_cnt', 'green')],
    captions={
        'if not root': '空树没有众数 → 返回 `[]`',
        'now = root': '从根节点开始，边走边把中序遍历「拉直」',
        'val = None': '`val` 是当前正在统计的值，`cnt` 是它连续出现的次数',
        'max_cnt = 0': '`max_cnt` 记录目前最大的出现次数',
        'while now': lambda S, B, r: (f"`now = {S.now.val}`，还有节点没处理" if S.now is not None else '`now` 为空：中序遍历走完了'),
        'if now.left': lambda S, B, r: (f"`{S.now.val}` 有左子树 → 要先处理完左边，才轮到它" if S.now.left else f"`{S.now.val}` 没有左子树 → 它就是中序遍历的下一个值"),
        'rightest = now.left': '找左子树里最大的节点：从 `now.left` 出发一路向右',
        'while rightest.right': '`rightest.right` 还有节点 → 继续向右',
        'rightest = rightest.right': '`rightest` 往右走到 `{rightest.val}`',
        'rightest.right = now': '`{rightest.val}` 是左子树最后访问的节点，把它的右指针接到 `{now.val}`：左子树走完就回到当前节点',
        'tmp = now.left': '先记住左儿子 `{tmp.val}`',
        'now.left = None': '断开 `now.left`：这棵左子树已经「接好」，下次不会重复进入',
        'now = tmp': '`now` 下降到左儿子 `{now.val}`，继续往最左走',
        'if val == now.val': lambda S, B, r: (f"轮到 `{S.now.val}`：和 `val = {S.val}` 相等 → 同一个数的又一次出现" if S.val == S.now.val
                                              else f"轮到 `{S.now.val}`：和 `val = {S.val}` 不同 → 换了一个新数"),
        'cnt += 1': '`cnt` + 1 → `{cnt}`',
        'val = now.val': '换新数：`val = {val}`',
        'cnt = 1': '新数第一次出现，`cnt = 1`',
        'if cnt == max_cnt': lambda S, B, r: (f"`cnt = {S.cnt}` == `max_cnt = {S.max_cnt}` → 与当前最大并列，也是众数" if S.cnt == S.max_cnt else f"`cnt = {S.cnt}` ≠ `max_cnt = {S.max_cnt}`"),
        'res.append(val)': '并列 → `{val}` 加入 `res`：`{res}`',
        'elif cnt > max_cnt': lambda S, B, r: (f"`cnt = {S.cnt}` > `max_cnt = {S.max_cnt}` → 出现了更多次，旧答案作废" if S.cnt > S.max_cnt else f"`cnt = {S.cnt}` < `max_cnt = {S.max_cnt}` → 不够多，不是众数"),
        'res = [val]': '`res` 重置为 `[{val}]`',
        'max_cnt = cnt': '`max_cnt` 更新为 `{max_cnt}`',
        'now = now.right': '处理完 `{B.now.val}`，沿右指针走：左子树的最后一个会接回根，所以中序顺序不乱',
        'return res': '一趟中序统计完毕，众数是 `{res}`',
    },
    cards=dict(
        one_liner='中序遍历天然有序，相同的数挨在一起，一趟就能数完',
        complexity='时间 `O(n)`，空间 `O(1)`（不计结果；会改动树）',
        problem=['给一棵含重复值的 BST，找出其中出现次数最多的数（可能有多个）',
                 '示例：`root = [3,2,4,1,2]`，中序 `1,2,2,3,4` → `[2]`'],
        quote='由于二叉搜索树的中序遍历是天然有序的，那么直接对二叉搜索树的中序遍历进行一趟扫描，统计每个数出现的次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通数组求众数：先排序，再一趟扫描计数',
              'BST 的中序遍历已经有序，省掉排序',
              '遍历用非递归写法（前面 94 题）：把左子树的最右节点接到当前节点上，边走边拆'],
        summary=['时间 `O(n)`，额外空间 `O(1)`',
                 '计数三种情况：`cnt == max_cnt` 追加，`cnt > max_cnt` 重置，否则忽略',
                 '这种遍历会把 `now.left` 置空，==树被破坏==；需要保留树时要另行恢复',
                 '换数时 `cnt` 重置为 1，不要忘了 `val = now.val`'],
    ),
)
