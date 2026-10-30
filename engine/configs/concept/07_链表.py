def _vals(node, lim=8):
    out = []
    while node is not None and len(out) < lim:
        out.append(str(node.val))
        node = node.next
    return ' → '.join(out) if out else '空'


def _formula(S):
    if 'dummy' in S:
        if 'left' in S:
            d, a = 0, S['left']
            while a is not None and a is not S['right'] and d < 10:
                a, d = a.next, d + 1
            return f"尺子：`left` 到 `right` 相距 =={d}== 步；`right` 到尾时 `left` 在倒数第 {S['n'] + 1} 个"
        return '哨兵 `dummy` 在头节点前面：==头节点也有前驱了=='
    if 'cur' in S:
        return f"已反转（`pre` 开头）：`{_vals(S['pre'])}`　待反转（`cur` 开头）：`{_vals(S['cur'])}`"
    return ''


_cnt = {'nxt': 0}


def _nxt_cap(S, B, ret):
    _cnt['nxt'] += 1
    if _cnt['nxt'] == 1:
        return f"先用 `nxt` 记住 `{S.cur.val}` 的下一个节点——==改指针前必须先存==，否则后面就断了"
    return f"`nxt` 记住 `{S.cur.val}` 的下一个：`{S.nxt.val if S.nxt else 'None'}`"


CONFIG = dict(
    num=None, title='链表 · 通用思想与模板', author='概念讲解', category='链表',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def remove_nth_from_end(head, n):    # 19. 哨兵 + 前后指针
    dummy = ListNode(0, head)        # 哨兵：头节点也有前驱
    left = right = dummy
    for _ in range(n):               # right 先走 n 步
        right = right.next
    while right.next:                # 一起走，直到 right 是尾节点
        left, right = left.next, right.next
    left.next = left.next.next       # 删除 left 的下一个
    return dummy.next

def reverse(head):                   # 206. 反转链表（头插法）
    pre, cur = None, head
    while cur:
        nxt = cur.next               # ① 先存下一个
        cur.next = pre               # ② cur 插到新链表头部
        pre, cur = cur, nxt          # ③ 两个指针都前进
    return pre
''',
    call='reverse(remove_nth_from_end(L([1, 2, 3, 4, 5, 6]), 2))',
    result_fn=list_vals,
    expect=[6, 4, 3, 2, 1],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='linked', label='链表（先删除倒数第 2 个，再整体反转）',
             pointers={'pre': 'pink', 'cur': 'blue', 'nxt': 'green', 'dummy': 'purple', 'left': 'cyan',
                       'right': 'orange'}, h=420),
    ],
    watch=[('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('nxt', 'nxt', 'green'), ('left', 'left', 'cyan'),
           ('right', 'right', 'orange')],
    captions={
        'pre, cur = None, head': '`pre` = 已反转部分的头（一开始是空链表），`cur` = 下一个要处理的节点',
        'while cur:': lambda S, B, ret: ('`cur` 不为空 → 还有节点没反转' if S.get('cur') is not None
                                         else '`cur` 为空：所有节点都反转完了'),
        'nxt = cur.next': _nxt_cap,
        'cur.next = pre': lambda S, B, ret: (f"头插法：`{S.cur.val}.next` 指向 `pre`"
                                             f"（{S.pre.val if S.pre else 'None'}）→ `{S.cur.val}` 成为新链表的头"),
        'pre, cur = cur, nxt': lambda S, B, ret: (f"`pre` → {S.pre.val}，`cur` → {S.cur.val if S.cur else 'None'}："
                                                  f"已反转 `{_vals(S.pre)}`"),
        'return pre': lambda S, B, ret: f'返回新的头节点 `{ret.val}`：`{_vals(ret)}`，`O(n)` 时间、`O(1)` 空间',
        'dummy = ListNode': '在头节点前面接一个哨兵 `dummy`：==要删的是头节点也不用特判==',
        'left = right = dummy': '`left`、`right` 都从 `dummy` 出发——想象一把长度为 n 的尺子',
        'for _ in range': lambda S, B, ret: (f'`right` 先走第 {S["_"] + 1} 步' if B.get('_') != S.get('_') or '_' not in B
                                             else f'`right` 已经领先 `left` {S.n} 步'),
        'right = right.next': '`right` → {right.val}',
        'while right.next': lambda S, B, ret: ('`right.next` 不为空 → 尺子整体右移一格' if S.right.next is not None
                                               else f'`right` 是尾节点了：`left` 恰好在倒数第 {S.n + 1} 个（`{S.left.val}`）'),
        'left, right = left.next': '`left` → {left.val}，`right` → {right.val}，两者距离保持 {n}',
        'left.next = left.next.next': '`{left.val}.next` 跳过下一个节点 → ==倒数第 {n} 个被删除==',
        'return dummy.next': lambda S, B, ret: f'返回 `dummy.next`：==哨兵后面才是真正的头==，`{_vals(ret)}`',
    },
    cards=dict(
        one_liner='画图 + 先存后改；哨兵省特判，双指针找位置',
        complexity='大多 `O(n)` 时间、`O(1)` 空间',
        problem_heading='什么时候用？',
        problem=['要改指针：反转、交换、删除、合并 → 先存 `nxt` 再改',
                 '可能动到头节点 → 加哨兵 `dummy`，最后返回 `dummy.next`',
                 '倒数第 k 个、中点、环、相交 → 前后指针 / 快慢指针',
                 '要 `O(1)` 查找又要维护顺序 → 哈希表 + 双向链表（146）'],
        before=[dict(heading='核心概念：三个基本动作', lines=[
            '反转（头插法）：存 `nxt` → `cur.next = pre` → `pre, cur = cur, nxt`',
            '哨兵：`dummy = ListNode(0, head)`，删除 / 插入头节点不用特判',
            '前后指针：`right` 先走 `n` 步再一起走；快慢指针：两步 vs 一步',
            '`while node` 走到最后一个，`while node.next` 走到倒数第二个']),
        ],
        idea_heading='两位作者怎么说',
        quote='链表位置相关的问题的一个经典处理方法就是双指针法，简单来说就是一个从头开始正常走，另一个按特定的方法走，==当一个走到头时另一个就是要找的节点==。',
        quote_src='—— yiduobo · 19. 删除链表的倒数第 N 个结点',
        idea=['灵神：==要删除头节点时，加哨兵节点==；yiduobo 21 题叫它「假头」',
              '灵神 206：迭代是 ==头插法==、递归是尾插法；25 题就是 k 个一组的反转',
              '141 / 142 / 160：两人都用 ==步数差== 证明双指针的正确性'],
        after=[dict(heading='本类 Hot100 题目 & 学习顺序（1/2）', chapter='④ 小结', lines=[
            '`206` 反转链表：头插法三步',
            '`21` 合并两个有序链表：哨兵 + 谁小接谁',
            '`2` 两数相加：哨兵 + 进位',
            '`19` 删除倒数第 N 个：哨兵 + 前后指针',
            '`141` 环形链表：快慢指针会相遇',
            '`142` 环形链表 II：相遇后一个回头，再遇即入口',
            '`160` 相交链表：走完自己走对方',
            '`234` 回文链表：快慢找中点 + 反转后半'])],
        summary_heading='本类 Hot100 题目 & 学习顺序（2/2）',
        summary=['`24` 两两交换：哨兵 + 每轮改 3 个指针',
                 '`25` K 个一组翻转：数够 k 个再反转，接回前后',
                 '`138` 随机链表的复制：交错复制 / 哈希映射',
                 '`148` 排序链表：快慢找中点 + 归并',
                 '`23` 合并 K 个升序链表：最小堆 / 分治',
                 '`146` LRU 缓存：哈希表 + 双向链表 + 哨兵',
                 '易错：先存 `nxt` 再改指针；返回 `dummy.next` 而不是 `head`'],
    ),
)
