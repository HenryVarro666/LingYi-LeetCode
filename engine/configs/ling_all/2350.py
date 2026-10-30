def _segs(rolls, k):
    seen, out, cur = set(), [], 0
    for x in rolls:
        out.append(cur)
        seen.add(x)
        if len(seen) == k:
            seen = set()
            cur += 1
    return out


_PAL = ['blue', 'purple', 'cyan', 'orange']


def _rcol(S, i, v):
    if 'ans' not in S:
        return None
    seg = _segs(S['rolls'], S['k'])
    if seg[i] >= S['ans'] - 1:
        return None
    return _PAL[seg[i] % 4]


def _text(S):
    if 'ans' not in S:
        return '把 `rolls` 切成若干段，每段是「刚好凑齐 1..k」的最短段'
    k = S['k']
    return (f'当前第 =={S["ans"]}== 段：还差 =={S["left"]}== 种数没出现（共 `k = {k}`）；'
            f'`mark[v] = ans` 表示 v 已在本段出现')


def _mcol(S, i, v):
    if i == 0 or 'ans' not in S:
        return None
    return 'green' if v == S['ans'] else None


CONFIG = dict(
    num=2350, title='不可能得到的最短骰子序列', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='贪心分段 · 每段凑齐 1..k',
    tags=['灵神题单', '难度分 1961'],
    code='''
class Solution:
    def shortestSequence(self, rolls: List[int], k: int) -> int:
        mark = [0] * (k + 1)  # mark[v] 标记 v 属于哪个子段
        ans, left = 1, k
        for v in rolls:
            if mark[v] < ans:
                mark[v] = ans
                left -= 1
                if left == 0:
                    left = k
                    ans += 1
        return ans
''',
    call='Solution().shortestSequence([4,2,1,2,3,3,2,4,1], 4)',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='rolls', label='rolls（同色 = 已切好的一段）', color=_rcol, h=200),
        dict(type='array', var='mark', label='mark[v]：v 属于第几段', color=_mcol, h=200),
    ],
    watch=[('ans', 'ans', 'green'), ('left', 'left', 'yellow'), ('v', 'v', 'blue'), 'k'],
    captions={
        'mark = [0]': '`mark[v]` 记录 v 最近一次在==第几段==出现，初始 0',
        'ans, left = 1, k': '从第 1 段开始：还需要凑齐 `k = {k}` 种数',
        'for v in rolls': '看下一个数 `v = {v}`',
        'if mark[v] < ans': lambda S, B, r: (f'`mark[{S.v}] = {S.mark[S.v]} < ans = {S.ans}`：`{S.v}` 在本段还没出现过 → 记下' if S.mark[S.v] < S.ans
                                              else f'`mark[{S.v}] = {S.mark[S.v]} = ans`：`{S.v}` 本段已经有了，跳过'),
        'mark[v] = ans': '标记 `mark[{v}] = {ans}`：`{v}` 属于第 {ans} 段',
        'left -= 1': '本段又凑到一种数，还差 `left = {left}` 种',
        'if left == 0': lambda S, B, r: (f'`left = 0`：1..{S.k} 全齐了 → 这一段结束，开新的一段' if S.left == 0
                                          else f'`left = {S.left}`：还没凑齐，继续'),
        'left = k': '重新开始：下一段又要凑齐 `{k}` 种',
        'ans += 1': '又切出一段，`ans` → {ans}（目前答案 = 段数 + 1）',
        'return ans': '剩余部分凑不齐 1..k，说明有长为 `{ans}` 的序列不在 rolls 中 → `{ret}`',
    },
    cards=dict(
        one_liner='切出 m 段「刚好凑齐 1..k」，答案就是 m+1',
        complexity='时间 `O(n+k)`，空间 `O(k)`',
        problem=['`k` 面骰子扔 `n` 次得到 `rolls`；求==不是 rolls 子序列==的最短骰子序列的长度',
                 '子序列不要求连续',
                 '示例：`rolls=[4,2,1,2,3,3,2,4,1], k=4` → `3`'],
        quote='考虑包含 1 到 k 的最短前缀，无法得到的子序列的第一个数必然在里面。这个前缀的最后一个数 x，在前缀中只会出现一次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：每次取「刚好包含 1..k」的最短前缀当一段，取它的最后一个数',
              '设切出 `m` 段，每段各选一个数就能得到任意长为 `m` 的序列 → 答案至少 `m+1`',
              '各段最后一个数 + 剩余部分缺的数，构造出长 `m+1` 的不可得序列 → 答案 `m+1`'],
        summary=['时间 `O(n+k)`，空间 `O(k)`',
                 '`mark[v]` 存段号而不是布尔值：换段时不用清空，省掉哈希表重建',
                 '`ans` 从 1 开始：它既是当前段号，最后也是答案',
                 '易错：`left` 要在凑齐后重置为 `k`'],
    ),
)
