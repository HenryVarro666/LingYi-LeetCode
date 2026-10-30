CONFIG = dict(
    num=2181, title='合并零之间的节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='假头节点 · 删 0 再吞并',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def mergeNodes(self, head):

        phead = ListNode()
        phead.next = head

        now = phead
        while now.next:
            while now.next and now.next.val == 0:
                now.next = now.next.next
            
            if now.next:
                now = now.next
                while now.next and now.next.val != 0:
                    now.val += now.next.val
                    now.next = now.next.next
        
        return phead.next
''',
    setup='''
head = L([0,3,1,0,4,5,2,0])
import tracer, itertools
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
''',
    call='Solution().mergeNodes(head)',
    expect=[4, 11],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（最左边是假头 phead）', pointers={'now': 'blue', 'phead': 'purple'}, h=300),
        dict(type='text', fn=lambda S: f"当前合并目标 `now.val` = =={S['now'].val}==" if S.get('now') is not None and S['now'] is not S.get('phead') else ''),
    ],
    watch=[('now.val', 'now.val', 'blue')],
    captions={
        'phead = ListNode()': '先建假头节点 `phead`：要删节点（尤其是开头的 0），有假头就不用特判',
        'phead.next = head': '`phead.next` 指向原链表',
        'now = phead': '`now` 从假头出发',
        'while now.next:': lambda S, B, r: ('`now.next` 存在：还有节点没处理' if S.now.next is not None else '`now.next` 为空：全部处理完'),
        'while now.next and now.next.val == 0': lambda S, B, r: ('`now.next` 的值是 0 → 要删掉' if (S.now.next is not None and S.now.next.val == 0) else '`now.next` 不是 0（或已无节点）：找到了这一轮的目标节点'),
        'now.next = now.next.next': lambda S, B, r: ('删掉值为 0 的节点：`now.next` 跳过它' if B.now.next.val == 0 else f'把 `{B.now.next.val}` 吞并进 now 后，删掉这个节点：`now.next` 跳过它'),
        'if now.next:': lambda S, B, r: ('后面还有非 0 节点：它就是本轮合并的目标' if S.now.next is not None else '后面没有节点了 → 外层循环结束'),
        'now = now.next': '`now` 走到目标节点：之后往它里面累加',
        'while now.next and now.next.val != 0': lambda S, B, r: (f'`now.next.val = {S.now.next.val}` 不是 0 → 合并到 now' if (S.now.next is not None and S.now.next.val != 0) else '遇到 0 或链表末尾：本轮合并完成'),
        'now.val += now.next.val': '`now.val += {B.now.next.val}` → =={now.val}==',
        'return phead.next': '返回 `phead.next`：链表变成 `[4, 11]`',
    },
    cards=dict(
        one_liner='先删掉 now 后面的 0，再把后面连续非 0 节点全吞进 now',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表由 `0` 分隔，首尾都是 `0`，相邻两个 `0` 之间的节点合并为一个（值为和）',
                 '合并后不能含有 `0`，返回头节点',
                 '示例：`[0,3,1,0,4,5,2,0]` → `[4,11]`'],
        quote='由于涉及到删除节点，为了最后处理方便，可以按照常规做法，先设置一个假头节点phead，将phead.next置为head，然后从phead开始向后遍历处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 1 步：删掉 `now` 后面所有值为 0 的节点，剩下的第一个非 0 节点就是目标',
              '第 2 步：只要 `now.next` 非 0，就把它的值累加进 `now` 并删除它',
              '第 3 步：这一轮完成，回到第 1 步；末尾一定是 0，所以必然在第 1 步结束'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '假头节点 `phead` 让删除开头的 0 不需要特判',
                 '外层 `while now.next` 里面两个内层循环，每个节点只会被删或被吞并一次',
                 '原文已是 Python 3 可运行，未做改动；假头在视频里画在最左边',
                 '对比灵神：灵神原地复用已走过的节点；这里用「删 0、吞后继」直接改指针'],
    ),
)
