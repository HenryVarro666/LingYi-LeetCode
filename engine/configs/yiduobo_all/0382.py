def _prob(S):
    if 'now' not in S or 'cnt' not in S:
        return '一趟遍历，长度未知也没关系：走到第 `k` 个节点时，以 `1/k` 的概率让它取代答案'
    if S['now'] is None:
        return f"走完了，共 `{S['cnt']}` 个节点：每个节点最终被选中的概率都是 ==1/{S['cnt']}=="
    k = S['cnt'] + 1
    return f"当前是第 `k = {k}` 个节点（值 `{S['now'].val}`）：以 ==1/{k}== 的概率取代答案，否则保留原答案（概率 `{k - 1}/{k}`）"


CONFIG = dict(
    num=382, title='链表随机节点', difficulty='Medium', category='链表',
    author='yiduobo', technique='蓄水池抽样 · 一趟遍历',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
class Solution(object):

    def __init__(self, head):
        self.head = head

    def getRandom(self):
        cnt = 0
        ret = None

        now = self.head
        while now:
            if random.randint(0, cnt) == 0:
                ret = now.val
            cnt += 1
            now = now.next

        return ret
''',
    setup='import random\nrandom.seed(0)',
    call='''s = Solution(L([1, 2, 3, 4]))
[s.getRandom(), s.getRandom()]''',
    expect=[3, 1],
    views=[
        dict(type='text', fn=_prob, size=24, h=110, lines=2),
        dict(type='linked', pointers={'now': 'blue'}, h=300),
        dict(type='text', size=26, h=90,
             fn=lambda S: (f"当前答案 `ret = {S['ret']}`" if S.get('ret') is not None else '当前答案：还没有') if 'cnt' in S else ''),
    ],
    watch=[('cnt', 'cnt', 'cyan'), ('ret', 'ret', 'green')],
    captions={
        'self.head = head': '只记下表头：==不预先统计长度==，也不转成数组',
        'cnt = 0': '`cnt`：已经走过的节点数',
        'ret = None': '`ret`：当前选中的答案',
        'now = self.head': '从表头开始一趟遍历',
        'while now': lambda S, B, r: (f'还有节点（值 `{S.now.val}`），继续' if S.now is not None else '链表走完，`ret` 就是最终答案'),
        'if random.randint(0, cnt) == 0': lambda S, B, r: (
            f'第 `{S.cnt + 1}` 个节点：`randint(0, {S.cnt})` 共 {S.cnt + 1} 种结果，抽到 0 的概率 `1/{S.cnt + 1}`'),
        'ret = now.val': lambda S, B, r: (f'抽中了 → 用当前节点取代答案：`ret = {S.ret}`' if S.cnt > 0
                                          else '第 1 个节点概率 `1/1`，一定选中：`ret = {}`'.format(S.ret)),
        'cnt += 1': lambda S, B, r: (f'没抽中（概率 `{S.cnt - 1}/{S.cnt}`）→ 保留原答案 `{S.ret}`；`cnt` → {S.cnt}'
                                     if S.ret != S.now.val else f'`cnt` → {S.cnt}'),
        'now = now.next': '走到下一个节点',
        'return ret': '返回 =={ret}==（每个节点被返回的概率相同）',
    },
    cards=dict(
        one_liner='第 k 个节点以 1/k 的概率取代答案，一趟扫完人人机会均等',
        complexity='每次 `getRandom` 时间 `O(n)`，额外空间 `O(1)`',
        problem=['给单链表的头节点 `head`，实现 `getRandom()`：==等概率==返回链表中某个节点的值',
                 '进阶：链表很长、长度未知，且不能用额外空间',
                 '本视频：链表 `1→2→3→4`，固定随机种子，调用两次 `getRandom()`'],
        quote='于是到了这里，就可以一趟扫描，==每次按当前节点总数分之一的概率，决定是否用当前节点替代答案节点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['假设前 `k−1` 个节点里已经以 `1/(k−1)` 的概率选出了某个节点',
              '第 `k` 个节点以 `1/k` 替换；原答案留下的概率 `1/(k−1) × (k−1)/k = 1/k`',
              '归纳下去，走完时每个节点被选中的概率都是 `1/n` —— 经典==蓄水池算法=='],
        summary=['时间 `O(n)`，空间 `O(1)`；简单做法是转成数组 `O(1)` 随机取，但要 `O(n)` 空间',
                 '易错：`randint(0, cnt)` 两端都包含，共 `cnt+1` 种结果；先判断再 `cnt += 1`',
                 '同类：398 随机数索引、384 洗牌算法',
                 '原文为 Python 2 写法：删去了 `:type`/`:rtype` 文档字符串；演示中补上 `import random` 并固定随机种子'],
    ),
)
