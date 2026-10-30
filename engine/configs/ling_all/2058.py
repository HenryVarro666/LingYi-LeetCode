CONFIG = dict(
    num=2058, title='找出临界点之间的最小和最大距离', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='一次遍历 · 三指针滑动',
    tags=['灵神题单', '链表树与回溯', '遍历链表'],
    code='''
class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        first, pre = 0, -inf
        min_dis = inf
        a, b, c = head, head.next, head.next.next
        i = 1

        while c:
            if a.val < b.val > c.val or a.val > b.val < c.val:
                if first == 0:
                    first = i
                min_dis = min(min_dis, i - pre)
                pre = i
            a, b, c = b, c, c.next
            i += 1

        if first >= pre:  # 临界点少于两个
            return [-1, -1]
        return [min_dis, pre - first]
''',
    setup='head = L([5,3,1,2,5,1,2])',
    call='Solution().nodesBetweenCriticalPoints(head)',
    expect=[1, 3],
    views=[
        dict(type='text', fn=lambda S: (f"当前中间节点 b = `{S['b'].val}`，下标 `i = {S['i']}`，左右邻居 `{S['a'].val}` 和 `{S['c'].val}`" if S.get('c') is not None and S.get('b') is not None else '')),
        dict(type='linked', label='链表（a、b、c 三个相邻节点一起右移）', pointers={'a': 'blue', 'b': 'pink', 'c': 'green'}, h=300),
        dict(type='text', fn=lambda S: f"first = `{S.get('first')}`　pre = `{S.get('pre')}`　min_dis = `{S.get('min_dis')}`" if 'first' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('first', 'first', 'yellow'), ('pre', 'pre', 'orange'), ('min_dis', 'min_dis', 'green')],
    captions={
        'first, pre = 0, -inf': '`first` 记第一个临界点位置，`pre` 记上一个临界点；`pre = -inf` 让第一次算距离不影响最小值',
        'min_dis = inf': '`min_dis` 先设为无穷大，等着被相邻临界点距离更新',
        'a, b, c = head': '三个指针 `a, b, c` 指向前三个节点：==b 是被检查的中间节点==，下标 `i = 1`',
        'while c': lambda S, B, r: (f'`c` 不为空：`b` 后面还有节点，b 有资格成为临界点' if S.get('c') is not None else '`c` 为空：b 已是最后一个节点，不可能是临界点 → 结束'),
        'if a.val < b.val > c.val': lambda S, B, r: (f'`{S.a.val}, {S.b.val}, {S.c.val}`：b 比两边都大或都小 → ==是临界点==' if (S.a.val < S.b.val > S.c.val or S.a.val > S.b.val < S.c.val) else f'`{S.a.val}, {S.b.val}, {S.c.val}`：b 不是严格的峰或谷 → 不是临界点'),
        'if first == 0': lambda S, B, r: ('`first == 0`：这是==第一个==临界点，记下位置' if S.first == 0 else '`first` 已记录，不是第一个临界点'),
        'first = i': '`first = {first}`：最大距离的左端点',
        'min_dis = min': lambda S, B, r: ('第一个临界点：`i - pre` 是无穷大，`min_dis` 不变' if B.pre == -inf else f'与上一个临界点的距离 `{S.i} - {B.pre}` = {S.i - B.pre}，`min_dis = {S.min_dis}`'),
        'pre = i': '`pre = {pre}`：更新「上一个临界点」',
        'a, b, c = b, c, c.next': '三指针整体右移一格，`i` 即将 +1',
        'i += 1': '`i = {i}`',
        'if first >= pre': lambda S, B, r: ('`first >= pre`：临界点少于两个 → 返回 [-1, -1]' if S.first >= S.pre else f'`first = {S.first} < pre = {S.pre}`：至少有两个临界点'),
        'return [min_dis, pre - first]': '最小距离 `{min_dis}`；最大距离 = 最后一个临界点 `{pre}` − 第一个 `{first}` = =={pre - first}==',
    },
    cards=dict(
        one_liner='一次遍历：相邻临界点距离取最小，首尾临界点距离就是最大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['临界点：严格大于或严格小于==前后两个邻居==的节点（首尾节点不算）',
                 '返回任意两个临界点之间的 `[最小距离, 最大距离]`，少于两个返回 `[-1,-1]`',
                 '示例：`[5,3,1,2,5,1,2]` → `[1,3]`'],
        quote='遍历链表的过程中，维护第一个临界点的位置 first、上一个临界点的位置 pre。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `a, b, c` 三个相邻节点，检查中间的 `b` 是否是峰或谷',
              '最小距离只可能出现在相邻两个临界点之间：每次用 `i - pre` 更新',
              '最大距离 = 最后一个临界点 − `first`，遍历结束后的 `pre` 就是最后一个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`first` 用 0 表示未设置：临界点下标从 1 开始，不会冲突',
                 '`pre = -inf` 巧妙地避免了「第一个临界点」的特判',
                 '结尾判断 `first >= pre`：临界点不足两个时，`pre` 没有超过 `first`',
                 '同类题：遍历链表专题（§1.1）'],
    ),
)
