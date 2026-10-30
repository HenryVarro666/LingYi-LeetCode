CONFIG = dict(
    num=2046, title='给按照绝对值排序的链表排序', difficulty='Medium', category='链表',
    author='yiduobo', technique='一趟遍历 · 负数节点头插',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def sortLinkedList(self, head):

        if not head.next:
            return head
        
        last = head
        now = head.next
        while now:
            if now.val >= 0:
                last = now
                now = now.next
            else:
                last.next = now.next
                now.next = head
                head = now
                now = last.next
        
        return head
''',
    call='Solution().sortLinkedList(L([1, -2, 3, -4, 5]))',
    expect=[-4, -2, 1, 3, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: ('' if 'now' not in S else
              (f'`now` = {S["now"].val}：==负数==，摘下来接到表头' if S['now'] is not None and S['now'].val < 0 else
               (f'`now` = {S["now"].val}：非负，已经有序，跳过' if S['now'] is not None else '遍历结束')))),
        dict(type='linked', label='链表（last 之后的负数被摘到最前面）', pointers={'head': 'purple', 'last': 'pink', 'now': 'blue'}, h=420),
    ],
    watch=[('head', 'head.val', 'purple'), ('last', 'last.val', 'pink'), ('now', 'now.val if now else None', 'blue')],
    captions={
        'if not head.next': '只有一个节点：`head.next` 为空 → {"直接返回" if not head.next else "不止一个节点，继续"}',
        'last = head': '`last` 记录==已处理部分的末尾==，从表头开始',
        'now = head.next': '`now` 从第二个节点开始往后扫',
        'while now': lambda S, B, r: (f'`now` = {S.now.val}，还没扫完' if S.now is not None else '`now` 为空 → 全部扫完，负数已全部逆序挂到表头'),
        'if now.val >= 0': '`now.val = {now.val}`：{"非负，在绝对值有序的链表里正数本来就有序" if now.val >= 0 else "负数，要挪到表头"}',
        'last = now': '正数原地保留：`last` 前进到 {last.val}',
        'now = now.next': '`now` → {now.val if now else "空"}',
        'last.next = now.next': '把 `now`（{now.val}）从链表中摘掉：`last.next` 指向它的后一个',
        'now.next = head': '`now` 接到当前表头前面',
        'head = now': '表头更新为 `{head.val}`：==后来的负数绝对值更大，所以更小，排在更前面==',
        'now = last.next': '继续扫 `last` 之后的节点',
        'return head': '返回新表头 `{head.val}`',
    },
    cards=dict(
        one_liner='正数本来有序，负数逆序接到表头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表已按==绝对值==非降序排好，请按==实际值==非降序重新排序',
                 '示例：`[0,2,-5,5,10,-10]` → `[-10,-5,0,2,5,10]`',
                 '本视频：`[1,-2,3,-4,5]` → `[-4,-2,1,3,5]`'],
        quote='对于链表中的正数而言实际上已经是有序的，那么就只需要将其中的负数项逆序接在链表的头部。',
        quote_src='—— yiduobo 题解原文',
        idea=['按绝对值升序：负数里绝对值越大，实际值越小',
              '所以越晚遇到的负数应该越靠前 → ==头插法==',
              '一趟遍历：正数跳过，负数摘下接表头并更新 `head`'],
        summary=['时间 `O(n)`，空间 `O(1)`，一趟遍历',
                 '摘节点后用 `now = last.next` 继续，不要用 `now.next`（它已被改指向表头）',
                 '易错：`head` 会变，最后返回的是更新后的 `head`',
                 '原文就是 Python 3 可运行的写法，未做改动'],
    ),
)
