CONFIG = dict(
    num=1721, title='交换链表中的节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='求长度 + 假头 + 交换 next',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def swapNodes(self, head, k):

        p_head = ListNode()
        p_head.next = head
        now = p_head
        l = 0
        while now.next:
            now = now.next
            l += 1

        if l & 1 and k == (l + 1) // 2:
            return head
        
        if k > (l + 1) // 2:
            k = l + 1 - k

        cnt1 = k - 1
        cnt2 = l - k
        cnt = 0
        now = p_head
        while now.next:
            if cnt == cnt1:
                p1 = now
            if cnt == cnt2:
                p2 = now
                break
            
            cnt += 1
            now = now.next
        
        tmp = p1.next
        p1.next = p2.next
        p2.next = tmp

        p1 = p1.next
        p2 = p2.next
        tmp = p1.next
        p1.next = p2.next
        p2.next = tmp
        return p_head.next
''',
    call='Solution().swapNodes(L([1, 2, 3, 4, 5, 6]), 2)',
    expect=[1, 5, 3, 4, 2, 6],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: (f'链表长度 `l` = =={S["l"]}==，交换第 {S["k"]} 个和第 `l-k+1` = {S["l"]-S["k"]+1} 个' if 'l' in S and 'k' in S and S['l'] > 0 and 'cnt1' not in S else
              (f'要交换第 =={S["k"]}== 个和第 =={S["l"]-S["k"]+1}== 个：先找它们的==前驱== `p1`（第 {S["k"]-1} 个）、`p2`（第 {S["l"]-S["k"]} 个）' if 'cnt1' in S else ''))),
        dict(type='linked', label='链表（最左边是假头 p_head）', pointers={'now': 'blue', 'p1': 'pink', 'p2': 'orange', 'p_head': 'purple'}, h=420),
    ],
    watch=[('k', 'k', 'yellow'), ('l', 'l', 'cyan'), ('cnt', 'cnt', 'blue'), ('p1', 'p1.val if "p1" in globals() else None', 'pink')],
    captions={
        'p_head = ListNode()': '建一个==假头== `p_head`：这样第 1 个节点也有前驱，`k = 1` 不用特判',
        'p_head.next = head': '假头接到真正的表头前面',
        'now = p_head': '`now` 站在假头，准备走一趟',
        'l = 0': '`l` 用来数链表长度',
        'while now.next': lambda S, B, r: (('`now.next` 不为空，继续数' if 'cnt1' not in S else '`now.next` 不为空，继续找 p1 / p2') if B.now.next else '走到末尾：长度已经确定'),
        'now = now.next': '`now` 走到 {now.val}',
        'l += 1': '长度 `l` = {l}',
        'if l & 1 and': '`l = {l}`，`k = {k}`：{"奇数长度且 k 正好在正中间，交换自己，直接返回" if (l & 1 and k == (l + 1) // 2) else "不是正中间，需要交换"}',
        'if k > (l + 1)': '`k = {k}` {"大于" if B.k > (B.l + 1) // 2 else "不大于"} 中点 `{(l + 1) // 2}`：{"用 l+1-k 代替，结果不变" if B.k > (B.l + 1) // 2 else "保持 k 不变"}',
        'cnt1 = k - 1': '第 k 个节点的前驱下标：`cnt1 = k - 1` = {cnt1}',
        'cnt2 = l - k': '第 l-k+1 个节点的前驱下标：`cnt2 = l - k` = {cnt2}',
        'now = p_head': '从假头出发，找 `p1` / `p2`',
        'if cnt == cnt1': '`cnt = {cnt}`，`cnt1 = {cnt1}` → {"==找到 p1==" if cnt == cnt1 else "还没到"}',
        'p1 = now': '`p1` = 节点 {p1.val}（第 k 个节点的前驱）',
        'if cnt == cnt2': '`cnt = {cnt}`，`cnt2 = {cnt2}` → {"==找到 p2==" if cnt == cnt2 else "还没到"}',
        'p2 = now': '`p2` = 节点 {p2.val}（第 l-k+1 个节点的前驱），找齐，`break`',
        'cnt += 1': '`cnt` → {cnt}',
        'tmp = p1.next\n': '先暂存 `p1.next`（第一个要交换的节点）',
        'p1.next = p2.next': '`p1.next` 改指向 `p2.next`：第 k 个位置换成后面那个节点',
        'p2.next = tmp': '`p2.next` 指向原先的 `p1.next`：两个节点对调位置',
        'p1 = p1.next': '`p1` 向后一步，现在就是换过来的节点 {p1.val}',
        'p2 = p2.next': '`p2` 向后一步，现在是换过来的节点 {p2.val}',
        'return p_head.next': '返回 `p_head.next`：头节点可能被换掉，所以不能直接返回 `head`',
    },
    cards=dict(
        one_liner='交换两个节点：找到各自的前驱，再交换两次 next',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交换链表中==正数第 k 个==节点和==倒数第 k 个==节点，返回头节点',
                 '示例：`head = [1,2,3,4,5], k = 2` → `[1,4,3,2,5]`',
                 '本视频：`[1,2,3,4,5,6], k = 2` → `[1,5,3,4,2,6]`'],
        quote='要交换第k个节点以及第l - k + 1个节点，实际上就是要找到第k - 1个节点和第l - k个节点，然后对这两个节点的next进行操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['单向链表：先扫一趟得到长度 `l`，倒数第 k 个就是第 `l-k+1` 个',
              '加==假头== `p_head`，让 `k = 1` 也有前驱',
              '找到前驱 `p1`、`p2`，先交换它们的 `next`，再往后一步交换两个节点的 `next`'],
        summary=['时间 `O(n)`，空间 `O(1)`，扫两趟',
                 '`k` 大于中点时换成 `l+1-k`，两个位置对称，结果不变',
                 '易错：两节点相邻时 `p1.next` 与 `p2` 相同，先换前驱的 next、再换节点的 next 仍然正确',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
