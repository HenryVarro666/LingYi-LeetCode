def _parts(S):
    res = S.get('res')
    if res is None:
        return ''
    out = []
    for h in res:
        vs, x, d = [], h, 0
        while x is not None and d < 12:
            vs.append(str(x.val)); x = x.next; d += 1
        out.append('[' + ','.join(vs) + ']')
    return '已切出的部分：`' + ' '.join(out) + '`' if out else ''

CONFIG = dict(
    num=725, title='分隔链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='先数长度，再按段切开',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def splitListToParts(self, root, k):

        now = root
        l = 0
        while now:
            l += 1
            now = now.next
        
        part_l = l // k
        l %= k

        now = root
        last = None
        res = []
        for _ in range(k):
            res.append(now)
            if last:
                last.next = None
            for _ in range(part_l):
                last = now
                now = now.next
            if l > 0:
                last = now
                now = now.next
                l -= 1
        
        return res
''',
    call='Solution().splitListToParts(L([1,2,3,4,5,6,7]), 3)',
    expect=[[1, 2, 3], [4, 5], [6, 7]],
    result_fn=lambda r: [list_vals(x) for x in r],
    views=[
        dict(type='linked', pointers={'now': 'blue', 'last': 'pink', 'root': 'green'}, h=300),
        dict(type='text', fn=_parts),
        dict(type='text', fn=lambda S: f"总长 `l`、每段至少 `part_l` = =={S['part_l']}==，前 ==`l % k`== 段多 1 个：还剩 `{S['l']}` 个多的名额" if 'part_l' in S else ''),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('last', 'last.val if last else None', 'pink'), 'l', 'part_l'],
    captions={
        'l += 1': '数节点：长度 `l` = =={l}==',
        'part_l = l': '每段基础长度：`part_l = {B.l} // {k}` = =={part_l}==',
        'l %= k': '多出来的 `{l}` 个节点，分给前 `{l}` 段各多一个',
        16: '开始第 {len(res)+1} 轮（共 `k` 轮）',
        20: '这一段还需要再走 `part_l` 步吗？',
        23: '余数 `l` = {l}：{"还有名额，这段多拿一个" if l > 0 else "名额用完，这段不多拿"}',
        'res.append(now)': '新开一段：这一段的头就是 `now`，放进答案',
        'last.next = None': '把上一段的尾巴 `last` 和这一段断开，上一段就独立了',
        'last = now': '`last` 跟着 `now` 走，始终停在当前段已走过的最后一个节点',
        'l -= 1': '这一段多拿了一个节点，多出的名额 `l` 减到 {l}',
        'return res': '`k` 段全部切好，返回各段的头节点',
    },
    cards=dict(
        one_liner='先量长度算每段几个，再边走边断开',
        complexity='时间 `O(n + k)`，空间 `O(1)`（不含答案数组）',
        problem=['把链表分成 `k` 个连续部分，长度尽量相等',
                 '任意两部分长度差 ==至多为 1==，靠前的部分长度 ≥ 靠后的',
                 '示例：`[1..7]`，`k = 3` → `[1,2,3] [4,5] [6,7]`'],
        quote='需要先从头往后走一趟，获取链表的总长度l，那么每个部分的长度就是part_l = l / k，同时还会有l % k个节点逐个被分到靠前的l % k个部分。',
        quote_src='—— yiduobo 题解',
        idea=['第一趟只数长度 `l`，得到每段基础长度 `l // k` 和余数 `l % k`',
              '第二趟每轮往答案里放一个段头，再走 `part_l` 步；余数没用完就多走一步',
              '`last` 记住上一段的尾，下一轮开头把它的 `next` 置空完成切断'],
        summary=['原文为 Python 2 写法，整数除法 `l / k` 已改为 `l // k`',
                 '`k` 大于链表长度时，后面的段是 `None`（`part_l` 为 0，不会走空指针）',
                 '切断必须在下一轮开头做，这样才不会丢掉段的最后一个节点',
                 '时间 `O(n + k)`，不额外创建节点'],
    ),
)
