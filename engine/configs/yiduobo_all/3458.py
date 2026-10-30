CODE = '''
class Solution(object):
    def maxSubstringLength(self, s, k):
        
        pos = {}
        for index, char in enumerate(s):
            if char not in pos:
                pos[char] = []
            pos[char].append(index)
        
        g = {char : set() for char in pos}
        for first in pos:
            for second in pos:
                if first == second or pos[first][0] > pos[second][-1]:
                    continue
                
                left = 0
                right = len(pos[second]) - 1
                while left < right:
                    mid = (left + right) // 2
                    if pos[second][mid] < pos[first][0]:
                        left = mid + 1
                    else:
                        right = mid
                
                if pos[second][left] < pos[first][-1]:
                    g[second].add(first)
        
        low = {}
        dfn = {}
        stack = []
        stack_set = set()
        belong = {}

        global timestamp, tot
        timestamp = 0
        tot = 0

        def dfs(now):
            global timestamp, tot
            timestamp += 1
            low[now] = timestamp
            dfn[now] = timestamp
            stack.append(now)
            stack_set.add(now)

            for nxt in g[now]:
                if nxt not in dfn:
                    dfs(nxt)
                    low[now] = min(low[now], low[nxt])
                elif nxt in stack_set:
                    low[now] = min(low[now], dfn[nxt])
            
            if low[now] == dfn[now]:
                v = -1
                while v != now:
                    v = stack.pop()
                    stack_set.remove(v)
                    belong[v] = tot
                tot += 1
        
        for char in g:
            if char not in dfn:
                dfs(char)
        
        if tot == 1:
            return k == 0

        new_g = [set() for _ in range(tot)]
        ind = [0] * tot
        for x in g:
            for y in g[x]:
                if belong[x] != belong[y] and belong[y] not in new_g[belong[x]]:
                    new_g[belong[x]].add(belong[y])
                    ind[belong[y]] += 1
        
        cnt = 0
        for index in range(tot):
            if ind[index] == 0:
                cnt += 1
        
        return cnt >= k
'''


def _s_color(S, i, v):
    if S.get('_line', 0) <= 26 and 'first' in S and 'pos' in S and S['first'] in S['pos']:
        p = S['pos'][S['first']]
        if p[0] <= i <= p[-1]:
            return 'yellow'
        return None
    if 'now' in S and S.get('pos') and S['now'] in S['pos']:
        return 'cyan' if v == S['now'] else None
    return None


_SEEN = set()


def _for_nxt(S, B, ret):
    key = (S.now, S.get('nxt'))
    if S.get('nxt') is None or key in _SEEN:
        return f'`{S.now}` 的出边都看完了'
    _SEEN.add(key)
    return f'`now = {S.now}` 的出边 `{sorted(S.g[S.now])}`，看 `nxt = {S.nxt}`'


def _top(S):
    line = S.get('_line', 0)
    if line <= 26 and 'first' in S and 'second' in S:
        p = S['pos']
        return (f"`first = {S['first']}` 的区间 `[{p[S['first']][0]}, {p[S['first']][-1]}]`：里面有没有 `second = {S['second']}` 的位置 `{p[S['second']]}`？"
                if S['second'] in p and S['first'] != S['second'] else '')
    if 'dfn' in S and 'ind' not in S and 'cnt' not in S:
        return f"Tarjan 求强连通分量：`dfn = {S['dfn']}`，`low = {S['low']}`"
    if 'cnt' in S:
        return f"入度为 0 的分量有 `{S['cnt']}` 个，要 `k = {S['k']}` 个"
    if 'ind' in S:
        return f"缩点后各分量入度 `ind = {S['ind']}`"
    return '先记每个字母的位置，再用「包含关系」建图'


CONFIG = dict(
    num=3458, title='选择 K 个互不重叠的特殊子字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='包含关系建图 + 强连通分量 + 入度为 0',
    tags=['灵神题单·贪心与思维', '贪心算法', '难度分 1520'],
    code=CODE,
    call='Solution().maxSubstringLength("ababc", 2)',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=22, h=80),
        dict(type='string', var='s', label='s（黄 = first 的区间；青 = 当前 DFS 字母）', cell=70, h=140, color=_s_color),
        dict(type='map', var='g', label='g[second] = {first}：first 的首尾区间包住了 second', h=100, fmt=lambda k, v: f'{k} → {sorted(v)}'),
        dict(type='stack', var='stack', label='Tarjan 栈', h=90),
        dict(type='map', var='belong', label='belong：字母所属的强连通分量', h=90, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='calls', h=100),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'cyan'), ('now', 'now', 'orange'), ('分量数', 'len(set(belong.values()))', 'purple'), ('cnt', 'cnt', 'green'), ('k', 'k', 'pink')],
    skip=['for index, char in enumerate', 'if char not in pos', 'pos[char] = []', 'pos[char].append', 'for second in pos', 'if first == second or', 'continue',
          'left = 0', 'right = len', 'while left < right', 'mid = (left', 'if pos[second][mid]', 'left = mid + 1', 'right = mid', 'else:',
          'dfn = {}', 'stack = []', 'stack_set = set()', 'belong = {}', 'tot = 0', 'timestamp = 0', 'for x in g', 'for y in g[x]', 'for char in g', 'for index in range(tot)', 'ind = [0]', 'low[now] = timestamp', 'dfn[now] = timestamp', 'stack_set.add', 'stack_set.remove', 'v = -1', 'while v != now', 'global timestamp'],
    max_steps=80,
    captions={
        'pos = {}': '遍历 s，记录每个字母出现的所有下标 `pos[c]`（升序）',
        'g = {char': lambda S, B, ret: f'`pos = {S.pos}`。建有向图 `g`：对每对字母 `first, second`，若 `second` 出现在 first 的首尾之间，则 first 要包含 second',
        'for first in pos': lambda S, B, ret: ('所有 `first` 都枚举完了' if B.get('first') == S.first else f'枚举 `first = {S.first}`，它的首尾区间 `[{S.pos[S.first][0]}, {S.pos[S.first][-1]}]`'),
        'if pos[second][left] < pos[first][-1]': lambda S, B, ret: (
            f'二分找 `second = {S.second}` 的位置 `{S.pos[S.second]}` 中第一个 `>= {S.pos[S.first][0]}` 的：`{S.pos[S.second][S.left]}`，'
            + (f'`< {S.pos[S.first][-1]}` → ==second 被 first 包含==' if S.pos[S.second][S.left] < S.pos[S.first][-1] else f'`>= {S.pos[S.first][-1]}` → 不包含')),
        'g[second].add(first)': '连边 `g[{second}] = {g[second]}`：想选 `{first}` 就必须选 `{second}`；反过来不一定（有向）',
        'low = {}': '接下来：把互相包含的字母缩成一个点 —— 求==强连通分量==（Tarjan）。`dfn` 是访问序号，`low` 是能回溯到的最早序号，`tot` 是分量个数',
        'timestamp += 1': '访问 `{now}`：`dfn = low = {timestamp}`，入栈',
        'stack.append(now)': '`{now}` 入栈：`stack = {stack}`',
        'for nxt in g[now]': _for_nxt,
        'dfs(nxt)': '进入 `dfs({nxt})`',
        'low[now] = min(low[now], low[nxt])': '子节点回来：`low[{now}] = min({B.low[now]}, {low[nxt]}) = {low[now]}`',
        'elif nxt in stack_set': lambda S, B, ret: (f'`{S.nxt}` 还在栈里 → 它和 `{S.now}` 在同一个环上' if S.nxt in S.stack_set else f'`{S.nxt}` 已出栈，属于别的分量，忽略'),
        'low[now] = min(low[now], dfn[nxt])': '环！`low[{now}] = min({B.low[now]}, dfn[{nxt}] = {dfn[nxt]}) = {low[now]}`',
        'if low[now] == dfn[now]': lambda S, B, ret: (f'`low[{S.now}] = dfn[{S.now}] = {S.dfn[S.now]}` → `{S.now}` 是一个强连通分量的根，把栈里它之上的全弹出来' if S.low[S.now] == S.dfn[S.now]
                                                      else f'`low[{S.now}] = {S.low[S.now]} < dfn[{S.now}] = {S.dfn[S.now]}` → 它连着更早的点，分量根在别处，先不弹栈'),
        'v = stack.pop()': '弹出 `{v}`',
        'belong[v] = tot': '`belong[{v}] = {belong[v]}`：`{v}` 归入分量 {belong[v]}',
        'tot += 1': '这个分量弹完了，分量编号 `tot` 加一',
        'if nxt not in dfn': lambda S, B, ret: (f'`{S.nxt}` 还没访问 → 递归 `dfs({S.nxt})`' if S.nxt not in S.dfn else f'`{S.nxt}` 已经访问过'),
        'if char not in dfn': lambda S, B, ret: (f'`{S.char}` 没访问过 → 以它为根做 Tarjan' if S.char not in S.dfn else f'`{S.char}` 已经访问过，跳过'),
        'dfs(char)': '从 `{char}` 出发',
        'if tot == 1': lambda S, B, ret: (f'只有 {len(set(S.belong.values()))} 个分量：所有字母必须一起选，就是整个 s → 只有 `k == 0` 才成立' if len(set(S.belong.values())) == 1 else f'有 {len(set(S.belong.values()))} 个分量，往下数入度为 0 的'),
        'new_g = ': '缩点后建新图 `new_g`，枚举每条边 x → y，统计每个分量的入度 `ind`',
        'if belong[x] != belong[y]': lambda S, B, ret: (f'`belong[{S.x}] = {S.belong[S.x]}`，`belong[{S.y}] = {S.belong[S.y]}`：' + ('同一分量内部的边，忽略' if S.belong[S.x] == S.belong[S.y] else '跨分量的边 → 记入新图')),
        'new_g[belong[x]].add': '`new_g = {new_g}`',
        'ind[belong[y]] += 1': '`ind = {ind}`',
        'cnt = 0': '入度为 0 的分量 = 可以独立选取的最小块，数它们的个数',
        'if ind[index] == 0': lambda S, B, ret: (f'`ind[{S.index}] = 0` → 没有别的分量要求带上它，==可以独立选取==' if S.ind[S.index] == 0 else f'`ind[{S.index}] = {S.ind[S.index]}` → 选它要牵扯别的分量，不优'),
        'cnt += 1': '`cnt = {cnt}`',
        'return cnt >= k': '`cnt = {cnt}`，`k = {k}`：`{cnt} >= {k}` → =={ret}==',
        'return k == 0': '`k == 0`？=={ret}==',
    },
    cards=dict(
        one_liner='「包含」建有向图，缩环成点，数入度为 0 的点',
        complexity='时间 `O(n + 26² log n)`，空间 `O(n)`',
        problem=['判断能否在 `s` 里选 `k` 个互不重叠的==特殊子串==：子串里的字母不出现在子串之外，且子串不是整个 `s`',
                 '`k = 0` 直接成立',
                 '本视频：`s = "ababc"`，`k = 2` → `true`'],
        quote='对于两种不同的字符串first和second，若second出现在pos[first][0]以及pos[first][-1]之间，那么如果子串中包含了字符first，那么就必须包含所有的second，可以发现这是一种有向关系。',
        quote_src='—— yiduobo 题解原文',
        idea=['字母当点，「想包含 first 就必须包含 second」当有向边；包含关系用二分判断',
              '想选一个点，就要把它牵扯的点全选上；==入度为 0 的点牵扯最少==，优先选它们',
              '互相包含的字母构成环（如 `ababc` 里的 a、b）：先求强连通分量，缩成一个点',
              '缩点后是 DAG，数入度为 0 的分量个数，`>= k` 就是答案'],
        summary=['时间 `O(n + 26² log n)`，空间 `O(n)`',
                 '`tot == 1` 说明所有字母缠成一团，只能选整个 `s`，不合法 → 只有 `k == 0` 成立',
                 'Tarjan 里 `low[now] == dfn[now]` 才是分量的根，弹栈给 `belong`',
                 '二分判断「second 是否在 first 区间里」：找第一个 `>= pos[first][0]` 的位置再比较',
                 '对比灵神：灵神从每个字母 DFS 合并区间，再按右端点排序做区间贪心；yiduobo 用 SCC 缩点后数入度为 0 的点'],
    ),
)
