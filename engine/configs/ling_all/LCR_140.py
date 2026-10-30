CONFIG = dict(
    num='LCR 140', title='训练计划 II', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='前后指针 · 先走 k 步',
    code='''
class Solution:
    def trainingPlan(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        left = right = head
        for _ in range(k):
            right = right.next  # 右指针先向右走 k 步
        # 然后左右指针一起走，右指针走到空节点时，左指针正好就在倒数第 k 个节点
        while right:
            left = left.next
            right = right.next
        return left
''',
    call='Solution().trainingPlan(L([2, 4, 7, 8, 9, 5]), 2)',
    expect=[9, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: '尺子：`left` 到 `right` 之间始终隔 =={}== 步'.format(S['k']) if 'right' in S and S.get('_') is not None and S['_'] + 1 >= S['k'] else ''),
        dict(type='linked', label='链表（蓝 = left，粉 = right）', pointers={'left': 'blue', 'right': 'pink'}, h=360),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'k'],
    captions={
        'left = right = head': '两个指针都从头节点 `{head.val}` 出发',
        'for _ in range(k)': lambda S, B, r: (f'右指针先走 `k` = {S.k} 步：第 {S._ + 1} 步' if '_' not in B or S._ != B._
                                              else f'右指针已经走完 `k` = {S.k} 步，两个指针相距 {S.k}'),
        'right = right.next  # 右指针先': '`right` 先走一步 → ' + '{"节点 " + str(right.val) if right else "None"}',
        'while right': lambda S, B, r: (f'`right` = {S.right.val}，不是空 → 两个指针一起走' if S.right
                                        else '`right` 走到了空节点 → ==循环结束==，`left` 正好在倒数第 `k` 个'),
        'left = left.next': '`left` 右移 → 节点 `{left.val}`',
        'right = right.next': lambda S, B, r: ('`right` 右移，两者仍相距 `k`；这次走出了链表 → `None`' if S.right is None
                                               else f'`right` 右移 → 节点 `{S.right.val}`，两者仍相距 `k`'),
        'return left': '返回 `left`：倒数第 `{k}` 个节点 `{left.val}`，它和后面的节点就是答案 =={ret}==',
    },
    cards=dict(
        one_liner='右指针先走 k 步，再一起走：右到头时，左就是倒数第 k 个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表记录训练项目编号，返回==倒数第 `cnt` 个==节点',
                 '示例：`[2,4,7,8]`，`cnt = 1` → 节点 `8`',
                 '本视频：`[2,4,7,8,9,5]`，`k = 2` → 从 `9` 开始的 `[9,5]`'],
        quote='右指针先向右走 k 步，然后左右指针一起走，右指针走到空节点时，左指针正好就在倒数第 k 个节点。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`right` 先走 `k` 步，两指针之间隔 `k` 个节点',
              '一起走，间隔不变；`right` 到空节点时 `left` 离末尾恰好 `k`',
              '`while right`：走到空节点才停，所以停在倒数第 `k` 个'],
        summary=['时间 `O(n)`，空间 `O(1)`，只扫一遍',
                 '题目保证 `1 <= cnt <= 长度`，所以先走 `k` 步不会出界',
                 '`while right` 与 `while right.next` 差一个节点，别写错',
                 '题解配套视频：基础算法精讲 08'],
    ),
)
