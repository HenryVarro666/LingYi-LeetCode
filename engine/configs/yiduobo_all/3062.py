CONFIG = dict(
    num=3062, title='链表游戏的获胜者', difficulty='Easy', category='链表',
    author='yiduobo', technique='步长为 2 遍历 · 两两比较',
    tags=[],
    code='''
class Solution(object):
    def gameResult(self, head):

        now = head
        diff = 0
        while now:
            if now.val > now.next.val:
                diff += 1
            elif now.val < now.next.val:
                diff -= 1
            
            now = now.next.next
        
        if diff > 0:
            return "Even"
        elif diff < 0:
            return "Odd"
        else:
            return "Tie"
''',
    setup='head = L([2,1,3,5,4,4,1,7])',
    call='Solution().gameResult(head)',
    expect='Odd',
    views=[
        dict(type='text', fn=lambda S: ('当前这一对：`%d` vs `%d`' % (S['now'].val, S['now'].next.val) if S.get('now') is not None and S['now'].next is not None else '') + (('　　差值 diff = ==%d==（正：Even 领先，负：Odd 领先）' % S['diff']) if 'diff' in S else '')),
        dict(type='linked', label='链表（偶数下标 = Even 队，奇数下标 = Odd 队）', pointers={'now': 'blue'}, h=420),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('diff', 'diff', 'green')],
    captions={
        'now = head': '从链表头开始，`now` 指向第 0 个节点（Even 队）',
        'diff = 0': '`diff` = Even 队得分 − Odd 队得分，先记 0',
        'while now': lambda S, B, r: ('`now` 不为空 → 还有一对没比' if S.now else '`now` 走到末尾 → 所有对都比完了'),
        'if now.val > now.next.val': lambda S, B, r: (f'`{S.now.val} > {S.now.next.val}` → ==成立==：Even 队这一对赢，`diff` 加 1' if S.now.val > S.now.next.val
                                                      else f'`{S.now.val} > {S.now.next.val}` → 不成立，看下一个条件'),
        'elif now.val < now.next.val': lambda S, B, r: (f'`{S.now.val} < {S.now.next.val}` → ==成立==：Odd 队这一对赢，`diff` 减 1' if S.now.val < S.now.next.val
                                                        else f'`{S.now.val} < {S.now.next.val}` → 也不成立：==相等的一对不得分=='),
        'diff += 1': '`diff` → {diff}',
        'diff -= 1': '`diff` → {diff}',
        'now = now.next.next': '链表长度是偶数，所以 `now.next` 一定存在；==一次跳两步==到下一对：`now` → {now.val if now else "None（结束）"}',
        'if diff > 0': lambda S, B, r: ('`diff > 0` → Even 队总分更高' if S.diff > 0 else f'`diff = {S.diff}`，不大于 0，看下一个条件'),
        'elif diff < 0': lambda S, B, r: ('`diff < 0` → Odd 队总分更高' if S.diff < 0 else '`diff` 也不小于 0 → 平局'),
        'return "Odd"': '`diff` 为负 → 返回 `Odd`',
        'return "Even"': '`diff` 为正 → 返回 `Even`',
        'return "Tie"': '`diff` 为 0 → 平局',
    },
    cards=dict(
        one_liner='链表长度为偶数：一次跳两步，两两比大小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['链表长度为偶数，偶数下标节点属于 ==Even== 队，奇数下标属于 ==Odd== 队',
                 '每一对 (下标 `2k`，`2k+1`) 值大的一队得 1 分，相等不得分',
                 '总分高者获胜，返回 `"Even"` / `"Odd"`；分数相同返回 `"Tie"`',
                 '本视频：`[2,1,3,5,4,4,1,7]` → `"Odd"`'],
        quote='题目保证的链表长度为偶数，那么只需从链表头开始以步长为2向后移动，每次对比当前节点与下一个节点的值的大小即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度为偶数 → 每个 `now` 后面一定有 `now.next`，不用判空',
              '用一个 `diff` 代替两个计分：Even 赢加 1，Odd 赢减 1',
              '最后只看 `diff` 的正负'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`now = now.next.next` 靠“长度为偶数”才安全',
                 '相等的一对不动 `diff`',
                 '原文只有 Python 2 风格的类声明，无需改动'],
    ),
)
