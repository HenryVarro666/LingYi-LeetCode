CONFIG = dict(
    num=1535, title='找出数组游戏的赢家', difficulty='Medium', category='模拟',
    author='yiduobo', technique='修正 k 后直接模拟',
    code='''
class Solution(object):
    def getWinner(self, arr, k):

        n = len(arr)
        if k >= n - 1:
            k = n - 1
        
        q = arr[:]
        now = q[0]
        p = 1
        cnt = 0
        while p < len(q) and cnt < k:
            if now > q[p]:
                cnt += 1
                q.append(q[p])
            else:
                cnt = 1
                q.append(now)
                now = q[p]
            
            p += 1

        return now
''',
    call='Solution().getWinner([2,1,3,5,4,6,7], 2)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"`now = {S['now']}`，连胜 ==`{S['cnt']}`== / {S['k']}，下一个对手 `q[{S['p']}]`" if 'cnt' in S else ''),
        dict(type='array', var='q', pointers={'p': 'blue'}, h=300,
             color=lambda S, i, v: ('yellow' if i == S['p'] else None) if 'p' in S else None,
             dim=lambda S, i, v: 'p' in S and i < S['p'],
             label='q（队列：已比过的灰色，被淘汰的追加到末尾）'),
    ],
    watch=['n', 'k', ('now', 'now', 'green'), ('cnt', 'cnt', 'yellow'), ('p', 'p', 'blue')],
    captions={
        'n = len': '数组长度 `n = {n}`',
        'if k >= n - 1': lambda S, B, r: (f'`k = {S.k} >= n - 1 = {S.n - 1}` → 成立：某数赢 `n-1` 轮就战胜所有人，k 修正为 `{S.n - 1}`' if S.k >= S.n - 1
                                           else f'`k = {S.k} < n - 1 = {S.n - 1}`：不用修正'),
        'k = n - 1': '`k` 修正为 `{k}`：最多 `n-1` 轮就能决出，更大的 k 没有意义',
        'q = arr[:]': '复制一份当队列 `q`，输掉的数追加到末尾',
        'now = q[0]': '当前 `arr[0]` 记为 `now = {now}`',
        'p = 1': '`p` 指向下一个对手，从 `1` 开始',
        'cnt = 0': '`cnt` 统计 `now` 连胜的轮数',
        'while p < len': lambda S, B, r: (f'`p = {S.p} < {len(S.q)}` 且 `cnt = {S.cnt} < k = {S.k}` → 继续比' if (S.p < len(S.q) and S.cnt < S.k)
                                           else f'`cnt = {S.cnt}`，`k = {S.k}` → 连胜够了，结束'),
        'if now > q[p]': lambda S, B, r: (f'`{S.now} > {S.q[S.p]}`：`now` 赢 → 成立' if S.now > S.q[S.p]
                                           else f'`{S.now} < {S.q[S.p]}`：`now` 输 → 不成立'),
        'cnt += 1': '`now` 连胜 +1：`cnt = {cnt}`',
        'q.append(q[p])': '输家 `{q[p]}` 移到数组末尾',
        'cnt = 1': '新擂主刚赢下这一局，`cnt = 1`',
        'q.append(now)': '旧的 `now` 输了，追加到末尾',
        'now = q[p]': '新的 `now = {now}`',
        'p += 1': '指针后移，下一个对手：`p = {p}`',
        'return now': '连胜够 `k` 轮，赢家是 `{now}`',
    },
    cards=dict(
        one_liner='k 超过 n-1 没有意义，先修正 k 再直接模拟',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组前两个数比大小，大的留在 `0` 位，小的移到末尾',
                 '某个数连赢 `k` 回合就是赢家，求这个数',
                 '示例：`arr=[2,1,3,5,4,6,7], k=2` → `5`'],
        quote='若某个数赢了n - 1轮，那么无论对于大于等于n - 1的k，最后的赢家都会是这个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['若 `arr[0]` 是最大值，它永远不会输；是次大值时，最多赢 `n-2` 轮',
              '所以赢够 `n-1` 轮必是全局最大，`k` 先改成 `min(k, n-1)`',
              '用指针 `p` 代替真的删队首，输家追加到 `q` 末尾，边比边数 `cnt`'],
        summary=['时间 `O(n)`（`k` 修正后至多比较 `n-1` 次），空间 `O(n)`（复制了一份队列）',
                 '易错点：新擂主上台时 `cnt` 置为 `1`（它刚赢了旧擂主），不是 `0`',
                 '原文为 Python 2 风格，代码未做改动（已是 Python 3 可运行）',
                 '对比灵神：灵神不复制数组，只用 `mx` 和 `win` 一趟打擂台，空间 `O(1)`'],
    ),
)
