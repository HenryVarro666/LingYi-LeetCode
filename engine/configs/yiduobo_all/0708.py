def _circle(h):
    out, x = [h.val], h.next
    while x is not h and len(out) < 20:
        out.append(x.val)
        x = x.next
    return out


CONFIG = dict(
    num=708, title='循环有序列表的插入', difficulty='Medium', category='链表',
    author='yiduobo', technique='遍历一圈找插入位置',
    tags=['循环链表'],
    code='''
class Solution(object):
    def insert(self, head, insertVal):

        if not head:
            head = Node(insertVal)
            head.next = head
            return head
        
        now = head
        while True:
            prev = now
            now = now.next
            if (prev.val <= insertVal <= now.val) or (now.val < prev.val <= insertVal) or (insertVal <= now.val < prev.val):
                tmp = Node(insertVal, now)
                prev.next = tmp
                return head
        
            if now == head:
                break
        
    
        tmp = Node(insertVal, head.next)
        head.next = tmp
        return head
''',
    setup='head = L([3,4,1], pos=0)',
    call='Solution().insert(head, 2)',
    expect=[3, 4, 1, 2],
    result_fn=_circle,
    views=[
        dict(type='linked', label='循环有序链表（尾部指回头）', pointers={'prev': 'orange', 'now': 'blue', 'head': 'purple'}, h=380),
        dict(type='text', fn=lambda S: f"要插入 `{S['insertVal']}`：看 `prev.val` = {S['prev'].val}，`now.val` = {S['now'].val}" if 'prev' in S else f"要插入 `{S['insertVal']}`", size=32),
    ],
    watch=['insertVal', ('prev', 'prev.val', 'orange'), ('now', 'now.val', 'blue')],
    captions={
        'if not head': '链表为空？这里不是，跳过空链表的特判',
        'while True': '一直转圈，直到找到位置，或回到  走完一圈',
        'now = head': '`now` 从 `head` 出发，每一轮看相邻的一对 `prev -> now`',
        'prev = now': '`prev` 记下当前节点',
        'now = now.next': '`now` 后移到 `{now.val}`，现在看这一对：`{prev.val} -> {now.val}`',
        'if (prev.val <= insertVal': lambda S, B, r: (
            f'插入值 `{S.insertVal}`，这一对 `{S.prev.val} -> {S.now.val}`：'
            + ('`prev <= v <= now` ==夹在中间== → 插这里' if S.prev.val <= S.insertVal <= S.now.val else
               '`now < prev <= v`：prev 是最大值，v 不小于它 → 插在最大值后' if S.now.val < S.prev.val <= S.insertVal else
               '`v <= now < prev`：now 是最小值，v 不大于它 → 插在最小值前' if S.insertVal <= S.now.val < S.prev.val else
               '三种情况都不满足，继续下一对')),
        'tmp = Node(insertVal, now)': '新建节点，`next` 指向 `now`',
        'prev.next = tmp': '`prev.next` 指向新节点：==插在 prev 和 now 之间==',
        'return head': '返回 `head`',
        'if now == head': lambda S, B, r: ('`now` 回到了 `head`：走完一整圈' if S.now is S.head else '`now` 还没回到 `head`，继续下一对'),
        'break': '走完一圈没找到：说明所有值都相等，随便插哪里都行',
    },
    cards=dict(
        one_liner='转一圈找相邻的 prev -> now，三种情况之一就插进去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定循环升序链表中的任意一个节点 `head`，插入 `insertVal`，保持循环有序',
                 '空链表要新建一个自环节点；可插入任意合适位置',
                 '本视频：`[3,4,1]` 循环，插入 `2` → `3,4,1,2`'],
        quote='对于上面这几种情况，就可以从head开始向后遍历直到回到head，期间每一轮操作都记录上一个节点prev以及当前节点now，若出现以上三种情况之一，则可以按照上面的处理方法完成插入操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['情况 1：`prev.val <= v <= now.val`，夹在中间',
              '情况 2：`v` 不小于最大值，插到最大值后（`now.val < prev.val <= v`）',
              '情况 3：`v` 不大于最小值，插到最小值前（`v <= now.val < prev.val`）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '空链表：新建节点并让它指向自己',
                 '==所有值相等==时三种情况都不触发，绕回 `head` 后在 head 后随便插',
                 '情况 2、3 用严格不等号才能锁定最大/最小值的位置',
                 '原文开头的 Node 类注释（docstring）是 LeetCode 提供的，已略去'],
    ),
)
