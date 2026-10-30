CONFIG = dict(
    num=2816, title='翻倍以链表形式表示的数字', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='进位只能是 1 · 看后继是否 ≥ 5',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def doubleIt(self, head):

        res = head
        if head.val >= 5:
            res = ListNode(1)
            res.next = head
        
        now = head
        while now:
            now.val = (now.val + now.val) % 10
            if now.next and now.next.val >= 5:
                now.val += 1
            now = now.next
        
        return res
''',
    call='Solution().doubleIt(L([5,2,9]))',
    expect=[1, 0, 5, 8],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（高位在左）', pointers={'res': 'green', 'head': 'purple', 'now': 'blue'}, h=330),
        dict(type='text', fn=lambda S: '进位只可能是 1：一位翻倍最大 18，加进位 1 也只有 19'),
    ],
    watch=[('now', 'now.val if now else None', 'blue')],
    captions={
        'res = head': '`res` 先指向原头节点，作为答案的头',
        'if head.val >= 5': lambda S, B, ret: (f'头节点 `{B.head.val}` ≥ 5：翻倍后会向更高位进位，最高位要多出一个 1' if B.head.val >= 5 else f'头节点 `{B.head.val}` < 5：不会产生新的最高位'),
        'res = ListNode(1)': '新建值为 1 的节点作为新的头部：这就是最高位的进位',
        'res.next = head': '新头接在原链表前面',
        'now = head': '`now` 从原头节点开始往后翻倍',
        'while now': lambda S, B, ret: ('`now` 不为空 → 处理这一位' if B.now else '`now` 为空 → 所有位处理完'),
        'now.val = (now.val + now.val) % 10': '本位翻倍：`{B.now.val} + {B.now.val}` 取个位 = =={now.val}==（本位的进位前驱已经加过）',
        'if now.next and now.next.val >= 5': lambda S, B, ret: (
            f'后继 `{B.now.next.val}` ≥ 5：它翻倍会进位 → 本位接受进位' if B.now.next and B.now.next.val >= 5
            else ('后继 < 5：不会进位' if B.now.next else '没有后继，没有进位')),
        'now.val += 1': '接受后继的进位：`now.val` → =={now.val}==',
        'now = now.next': '`now` 往后走',
        'return res': '返回 `res`：有新头就是新头，否则就是原头',
    },
    cards=dict(
        one_liner='翻倍就是自己加自己：进位只看后一位是否 ≥ 5',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表每个节点是数字的一位，高位在前',
                 '把这个数翻倍，返回结果链表的头节点',
                 '本视频：`[5,2,9]` → `[1,0,5,8]`（529 × 2 = 1058）'],
        quote='进位的值只能为1。……由于本题是自己加自己，因此实际上进位的1也不会对当前位是否会再次进位产生任何影响。更进一步的，只有当某一位的数值大于等于5时，该位才会发生进位。',
        quote_src='—— yiduobo 题解原文',
        idea=['用归纳法证明进位只能为 1：最大 `9 + 9 + 1 = 19`',
              '加上的进位 1 不会让本位再次进位，所以进位只取决于后继 ≥ 5',
              '头节点 ≥ 5 → 前面新建一个值为 1 的节点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先处理头：`head.val >= 5` 才需要新头，且新头值是 1',
                 '本位只需 `(v + v) % 10`，再看后继决定是否 +1，不必关心自己的进位',
                 '原文就是 Python 3 可运行的写法，无需修改',
                 '对比灵神：灵神新头值写 0，后面循环把它加到 1；yiduobo 直接建值 1 的新头'],
    ),
)
