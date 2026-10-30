CONFIG = dict(
    num=3063, title='链表频率', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='哈希表计数 + 建新链表',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def frequenciesOfElements(self, head):

        freq = Counter()
        now = head
        while now:
            freq[now.val] += 1
            now = now.next
        
        res = ListNode()
        now = res
        for f in freq.values():
            now.next = ListNode(f)
            now = now.next
        
        return res.next
''',
    setup='head = L([1,1,2,1,2,3])',
    call='Solution().frequenciesOfElements(head)',
    expect=[3, 2, 1],
    result_fn=list_vals,
    views=[
        dict(type='linked', label='链表（上排 = 输入，下排 = 新建的答案链）', pointers={'now': 'blue', 'res': 'purple'}, h=330),
        dict(type='map', var='freq', label='freq（值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('f', 'f', 'orange')],
    captions={
        'freq = Counter()': '`freq`：统计每个值出现了几次（保持首次出现的顺序）',
        'now = head': '`now` 从头节点出发',
        'while now': lambda S, B, r: ('`now` 不为空 → 还有节点要统计' if S.now else '`now` 为空 → ==第一趟遍历结束==，频率都统计好了'),
        'freq[now.val] += 1': '节点值 `{now.val}` 出现次数 +1 → `freq[{now.val}]` = =={freq[now.val]}==',
        8: lambda S, B, r: ('`now` 后移到下一个节点' if S.now else '`now` 移出链尾'),
        'res = ListNode()': '建一个哨兵头节点 `res`，答案链接在它后面',
        'now = res': '`now` 改作答案链的尾指针',
        'for f in freq.values()': lambda S, B, r: ('频率都处理完，循环结束' if 'f' in B and B.f == S.f else f'第二趟：遍历所有==频率== `f` = {S.f}'),
        'now.next = ListNode(f)': '在答案链尾接上新节点 `{f}`',
        14: '尾指针移到新节点',
        'return res.next': '返回 `res.next`：跳过哨兵，答案链 `{list_vals(res.next)}`',
    },
    cards=dict(
        one_liner='先数每个值出现几次，再把次数串成新链表',
        complexity='时间 `O(n)`，空间 `O(k)`（`k` 为不同值的个数）',
        problem=['给一个链表 `head`，返回一个新链表：每个节点的值是原链表中==某个元素出现的次数==',
                 '每种值只对应一个节点，顺序任意',
                 '示例：`[1,1,2,1,2,3]` → 频率 `[3,2,1]`'],
        quote='先对链表进行一趟遍历，使用哈希表统计链表中每种数出现的频率，接下来再对这些频率进行一趟遍历，构造出答案链表即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：沿 `now.next` 走完链表，`Counter` 数各值的出现次数',
              '第二趟：遍历 `freq.values()`，每个频率接成一个新节点',
              '用哨兵 `res` 开头，最后返回 `res.next`'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '要返回 `res.next`，不是 `res`（哨兵）',
                 '答案只含频率，不含原值；顺序任意，示例按首次出现顺序',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
