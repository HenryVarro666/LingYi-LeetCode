CONFIG = dict(
    num=862, title='和至少为 K 的最短子数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 双端队列',
    tags=['单调队列', '前缀和', '难度分 2307'],
    code='''
class Solution(object):
    def shortestSubarray(self, A, K):

        q = deque([[0, -1]])
        s = 0
        res = len(A) + 1
        for index, num in enumerate(A):
            s += num
            while q and s - q[0][0] >= K:
                res = min(res, index - q[0][1])
                q.popleft()
            while q and s <= q[-1][0]:
                q.pop()
            q.append([s, index])

        if res == len(A) + 1:
            res = -1
        return res
''',
    call='Solution().shortestSubarray([2,-1,2,-2,1,3], 4)',
    expect=2,
    views=[
        dict(type='array', var='A', label='A（粉箭头 = 当前 index）', pointers={'index': 'pink'}, h=260,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='queue', var='q', label='q：[前缀和, 下标]（队首最小，往右递增）', fmt=lambda x: f'{x[0]} @{x[1]}', h=140),
        dict(type='text', fn=lambda S: (f"当前前缀和 `s = {S['s']}`，队首 `{S['q'][0][0]}`：差 = =={S['s'] - S['q'][0][0]}== （K = {S['K']}）"
                                        if 'index' in S and S.get('q') else ''), h=60),
    ],
    watch=[('index', 'index', 'pink'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        'q = deque([[0, -1]])': '队列存 `[前缀和, 下标]`，一开始放 `[0, -1]`：空前缀，和为 0，下标 −1',
        's = 0': '`s` 边走边累加，就是当前前缀和',
        'res = len(A) + 1': '`res` 初始 `len(A)+1`：比任何合法长度都大，表示还没找到',
        'for index, num': '处理 `A[{index}] = {num}`',
        's += num': '前缀和 `s += {num}` → =={s}==',
        'while q and s - q[0][0] >= K': lambda S, B, r: (
            f'`{S.s} − {S.q[0][0]} = {S.s - S.q[0][0]} ≥ {S.K}`：队首到当前这段够 K' if S.q and S.s - S.q[0][0] >= S.K
            else ('队列空了，停止' if not S.q else f'`{S.s} − {S.q[0][0]} = {S.s - S.q[0][0]} < {S.K}`：不够，停止')),
        'res = min(res, index - q[0][1])': '合法子数组 `({q[0][1]}, {index}]`，长度 `{index} − ({q[0][1]})` = {index - q[0][1]}，`res` = =={res}==',
        'q.popleft()': '队首弹出：后面的 q 就算也满足，区间只会更长，这个起点不会再成为答案（性质 1）',
        'while q and s <= q[-1][0]': lambda S, B, r: (
            f'队尾 `{S.q[-1][0]} ≥ {S.s}`：起点更靠前、前缀和还不小 → 不可能比当前更优' if S.q and S.s <= S.q[-1][0]
            else '队尾比 `s` 小（或队列空）→ 保留，停止'),
        'q.pop()': '弹出队尾（性质 2）：后面任何 `q` 配当前的 `s` 都更容易满足，而且更短',
        'q.append([s, index])': '`[{s}, {index}]` 入队，队列里前缀和保持==严格递增==',
        'if res == len(A) + 1': lambda S, B, r: ('`res` 没变过 → 没有合法子数组，改成 -1' if S.res == len(S.A) + 1
                                                 else '`res` 被更新过 → 有答案，不改'),
        'return res': '返回 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='队首满足了就扔，队尾不如新来的也扔',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找和 ==至少为 `K`== 的最短连续子数组的长度，没有返回 `-1`',
                 '数组里可以有负数',
                 '本视频：`[2,-1,2,-2,1,3]`，`K = 4` → `2`'],
        quote='若存在p < index，且s[p] >= s[index]，那么对于后续的q > index，当s[q] - s[p] >= K时，必然有s[q] - s[index] >= K，而p到q这一段的长度显然大于index到q的长度',
        quote_src='—— yiduobo 题解原文',
        idea=['性质 1：`s[index] − s[p] ≥ K`，`p` 作为起点已经用完 → 从队首淘汰',
              '性质 2：`s[p] ≥ s[index]` 且 `p` 更靠前，`p` 永远不会更优 → 从队尾淘汰',
              '两头都要弹，所以用==双端队列==存 `[前缀和, 下标]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '队列里初始放 `[0, -1]`，这样从下标 0 开始的子数组也能算',
                 '用 `len(A) + 1` 当「未找到」的标记，最后换成 -1',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行（参数名 `A`、`K` 保持原样）',
                 '对比灵神：灵神先算好前缀和数组 `s` 再遍历，队列存下标；yiduobo 边走边算，队列存 `[s, 下标]`'],
    ),
)
