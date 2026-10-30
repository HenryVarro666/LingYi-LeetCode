CONFIG = dict(
    num=2058, title='找出临界点之间的最小和最大距离', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='一次遍历 · last 记前驱',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def nodesBetweenCriticalPoints(self, head):

        first_pos = last_pos = None

        last = head
        now = head.next
        pos = 1

        res = [100000, -1]
        while now.next:
            if (now.val > last.val and now.val > now.next.val) or (now.val < last.val and now.val < now.next.val):
                if first_pos is None:
                    first_pos = pos
                else:
                    res[0] = min(res[0], pos - last_pos)
                    res[1] = max(res[1], pos - first_pos)

                last_pos = pos

            last, now = now, now.next
            pos += 1

        if res[0] == 100000:
            res[0] = -1
        
        return res
''',
    setup='head = L([5,3,1,2,5,1,2])',
    call='Solution().nodesBetweenCriticalPoints(head)',
    expect=[1, 3],
    views=[
        dict(type='linked', label='链表（last 是 now 的前驱，单链表自己找不到前驱）', pointers={'last': 'blue', 'now': 'pink'}, h=300),
        dict(type='text', fn=lambda S: f"first_pos = `{S.get('first_pos')}`　last_pos = `{S.get('last_pos')}`　res = `{S.get('res')}`" if 'res' in S else ''),
    ],
    watch=[('pos', 'pos', 'blue'), ('first_pos', 'first_pos', 'yellow'), ('last_pos', 'last_pos', 'orange'), ('res', 'res', 'green')],
    captions={
        'first_pos = last_pos = None': '`first_pos` 第一个极值点下标，`last_pos` 上一个极值点下标，都还没有',
        'last = head': '单链表只能往后找，所以用 `last` 记住 `now` 的前一个节点',
        'now = head.next': '`now` 从第二个节点出发：首节点没有前驱，不可能是极值点',
        'pos = 1': '`pos` 是 `now` 在链表中的下标，从 1 开始',
        'res = [100000': '`res = [最小距离, 最大距离]`：最小先放一个很大的数，最大先放 -1',
        'while now.next': lambda S, B, r: ('`now.next` 存在：`now` 有前驱也有后继，可以判断' if S.now.next is not None else '`now.next` 为空：`now` 是最后一个节点，不能是极值点 → 结束'),
        'if (now.val': lambda S, B, r: (f'`{S.last.val}, {S.now.val}, {S.now.next.val}`：now 比前后都大或都小 → ==是极值点==' if ((S.now.val > S.last.val and S.now.val > S.now.next.val) or (S.now.val < S.last.val and S.now.val < S.now.next.val)) else f'`{S.last.val}, {S.now.val}, {S.now.next.val}`：不是峰也不是谷 → 跳过'),
        'if first_pos is None': lambda S, B, r: ('还没有极值点：这是==第一个==，只记录位置' if S.first_pos is None else '已有极值点：可以和之前的算距离了'),
        'first_pos = pos': '`first_pos = {first_pos}`',
        'res[0] = min': '与上一个极值点相邻：`{pos} - {last_pos}` = {pos - last_pos}，最小距离 → =={res[0]}==',
        'res[1] = max': '与第一个极值点的距离 `{pos} - {first_pos}` = {pos - first_pos}，最大距离 → =={res[1]}==',
        'last_pos = pos': '`last_pos = {last_pos}`：这个极值点成为「上一个」',
        'last, now = now, now.next': '两个指针一起右移：`last` 追上 `now`，`now` 前进一个节点',
        'pos += 1': '`pos = {pos}`',
        'if res[0] == 100000': lambda S, B, r: ('最小距离没被更新过：极值点不足两个 → 改成 -1' if S.res[0] == 100000 else '最小距离被更新过，保持不变'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='last 记前驱，边走边判极值点；最小看相邻，最大看首尾',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['极值点：严格大于或严格小于前后两个节点的值（首尾节点不算）',
                 '返回任意两个极值点之间的 `[最小距离, 最大距离]`，不足两个返回 `[-1,-1]`',
                 '示例：`[5,3,1,2,5,1,2]` → `[1,3]`'],
        quote='在单链表中，找到某个节点的后继节点是很容易的，但是没有办法直接找到某个节点的前驱节点，因此需要使用一个遍历last记录当前节点的上一个节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：对比 `last、now、now.next` 三者的值判断 `now` 是不是极值点',
              '最小距离必然出现在==相邻==的两个极值点之间，用 `pos - last_pos` 更新',
              '最大距离必然是==第一个==和==最后一个==极值点，每次用 `pos - first_pos` 更新'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`first_pos` 为空时只记位置，不更新距离；之后才用距离更新 `res`',
                 '`res[0]` 用 100000 当哨兵，结束时没被改过就说明极值点不足两个',
                 '原文已是 Python 3 可运行，未做改动',
                 '对比灵神：灵神用 `a,b,c` 三指针 + `pre=-inf`；这里用 `last/now` 两指针 + None 判断'],
    ),
)
