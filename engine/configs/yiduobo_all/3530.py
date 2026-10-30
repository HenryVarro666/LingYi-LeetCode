_IDX = lambda S: S['_inner'].get('index')


def _scores(S):
    d = {i: s for s, i in S.get('score_info', [])}
    return [d.get(k, 0) for k in range(max(d) + 1)] if d else [3, 1, 2]


def _txt(S):
    I = S['_inner']
    if 'now' not in I:
        return '`calc(now)`：已处理节点集合为 `now` 时，处理剩余节点的最大利润'
    n = len(S['depend'])
    now = I['now']
    done = [k for k in range(n) if now >> k & 1]
    s = f'`now = {now:0{n}b}`（已处理节点 {done}）'
    if 'cnt' in I and 'candidate' in I:
        s += f'，已处理 `cnt = {I["cnt"]}` 个'
    return s


CONFIG = dict(
    num=3530, title='有向无环图中合法拓扑排序的最大利润', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 记忆化 + 无依赖时贪心',
    tags=['灵神题单', '动态规划', '难度分 2353'],
    code='''
class Solution(object):
    def maxProfit(self, n, edges, score):
        
        f = {}
        n = len(score)
        score_info = [[s, index] for index, s in enumerate(score)]
        score_info.sort()

        max_state = (1 << n) - 1
        depend = [0] * n
        for x, y in edges:
            depend[y] |= (1 << x)

        def calc(now):
            if now == max_state:
                return 0
            if now not in f:
                f[now] = 0
                tmp = now
                cnt = 0
                while tmp:
                    cnt += 1
                    tmp -= tmp & -tmp
                
                candidate = []
                flag = True
                for score, index in score_info:
                    if now & (1 << index) == 0:
                        if now & depend[index] == depend[index]:
                            candidate.append((score, index))
                        else:
                            flag = False

                if flag:
                    for score, index in candidate:
                        f[now] += score * (cnt + 1)
                        cnt += 1
                else:
                    for score, index in candidate:
                        f[now] = max(f[now], calc(now | (1 << index)) + score * (cnt + 1))
            
            return f[now]
        
        return calc(0)
''',
    call='Solution().maxProfit(3, [[0, 1]], [3, 1, 2])',
    expect=11,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var=_scores, label='score（蓝 = 当前枚举的节点 index）', cell=70, h=210,
             pointers={_IDX: 'blue'}, pointer_labels={_IDX: 'index'}),
        dict(type='array', var='depend', label='depend[i]：节点 i 的前置节点集合', cell=70, h=140),
        dict(type='map', var='f', label='f：已算过的 now → 最大利润', fmt=lambda k, v: f'{k:03b} → {v}', h=130),
        dict(type='calls', h=150),
    ],
    watch=[('now', "_inner.get('now')"), ('cnt', "_inner.get('cnt')"), ('flag', "_inner.get('flag')"), ('candidate', "_inner.get('candidate')")],
    skip=['score_info = ', 'score_info.sort', 'max_state = ', 'depend = [0]', 'for x, y in edges',
          'while tmp', 'cnt += 1', 'tmp -= ', 'tmp = now', 'for score, index in score_info', 'for score, index in candidate', 'flag = True', 'candidate = []', 'f[now] = 0', 'candidate.append', 'flag = False'],
    captions={
        'f = {}': '`f` 是记忆化字典：`now` → 最大利润',
        'n = len(score)': '`n = {n}`（形参 n 被重新赋值，结果一样）',
        'depend[y] |= ': lambda S, B, r: f'边 `{S.x} → {S.y}`：`depend[{S.y}]` 加入节点 {S.x}，现在是 `{S.depend[S.y]:03b}`',
        'if now == max_state': lambda S, B, r: ('全部节点都处理完了，利润 0' if B.now == B.max_state else f'`now = {B.now:03b}` 还没处理完，继续'),
        'return 0': '返回 0',
        'if now not in f': lambda S, B, r: ('第一次遇到 `now`：先占位 `f[now] = 0`，再计算' if B.now not in B.f else f'`f[{B.now}]` 已经算过 → 直接返回 `{B.f[B.now]}`'),
        'f[now] = 0': '先占位 `f[now] = 0`，下面开始计算',
        'cnt = 0': '循环 `tmp -= tmp & -tmp` 每次去掉最低位的 1，数出 `now` 里有 `cnt = {bin(now).count("1")}` 个 1：已处理 {bin(now).count("1")} 个，下一个是第 `{bin(now).count("1") + 1}` 个',
        'if now & (1 << index) == 0': lambda S, B, r: (
            f'节点 {B.index} 已处理 → 跳过' if B.now >> B.index & 1 else f'节点 {B.index}（得分 {B.score}）还没处理，判断依赖'),
        'if now & depend[index]': lambda S, B, r: (
            f'`depend[{B.index}] = {B.depend[B.index]:03b}` 都在 `now` 里 → ==能处理==，加入 `candidate`（按得分升序）'
            if B.now & B.depend[B.index] == B.depend[B.index] else
            f'`depend[{B.index}] = {B.depend[B.index]:03b}` 还有前置没处理 → ==不能处理==，`flag = False`（剩下的节点有依赖，不能直接贪心）'),
        'if flag': lambda S, B, r: ('`flag` 为真：剩下的节点==全都没有依赖==，可以任意顺序 → 贪心' if B.flag
                                    else '`flag` 为假：有依赖的存在，要逐个枚举下一个处理谁'),
        'f[now] += score * (cnt + 1)': '贪心：按得分从小到大处理，==大分数留给大系数==：`f[now]` += `{score} × {cnt + 1}` → {f[now]}',
        'f[now] = max(': lambda S, B, r: f'枚举先处理节点 `{B.index}`（得分 {B.score}）：先递归算 `calc({B.now | (1 << B.index)})`，再加本节点 `{B.score} × {B.cnt + 1}`，取最大',
        'return f[now]': '`calc({now})` 返回 =={ret}==',
        'return calc(0)': '入口：什么都没处理，`calc(0)`；`candidate` 收集现在能处理的节点，`flag` 记剩下的节点是否都无依赖',
    },
    max_steps=60,
    cards=dict(
        one_liner='f[now] 记已处理集合的最大利润；无依赖时贪心一步算完',
        complexity='时间 `O(2^n · n)`，空间 `O(2^n)`',
        problem=['DAG 有 `n` 个节点（`n ≤ 22`），`edges` 里 `[u, v]` 表示 `u` 要排在 `v` 前面',
                 '拓扑序里第 `p` 个节点的利润 = `score × p`，总利润取和，求最大',
                 '本视频：`n=3, edges=[[0,1]], score=[3,1,2]`'],
        quote='令f[now]表示已经处理了状态为now的节点时，处理剩余节点可以得到的最大利润，那么对于f[now]，可以先分离出now的二进制表示中1的数量cnt，也就是已经处理了cnt个任务。',
        quote_src='—— yiduobo 题解原文',
        idea=['`depend[y]` 存 y 的所有直接前置节点；`now & depend[i] == depend[i]` 表示 i 可以处理',
              '可以处理的节点逐个试作下一个：`f[now] = max(calc(now | 1<<i) + score[i] × (cnt+1))`',
              '贪心优化：如果剩下的节点==都没有依赖==，按得分从小到大排，直接累加，不再递归'],
        summary=['时间 `O(2^n · n)`，空间 `O(2^n)`，n = 22 时靠贪心优化减少状态',
                 '`now` 二进制里 1 的个数 `cnt` 用 `tmp -= tmp & -tmp` 逐个去掉最低位 1 数出来',
                 '`candidate` 按得分升序，所以贪心时分数小的先处理、系数小',
                 '函数里 `for score, index` 会遮住参数 `score`，不影响结果',
                 '原文为 Python 2 风格写法，Python 3 下可直接运行，未改动'],
    ),
)
