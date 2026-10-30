W0 = ['ab', 'ba']


def _states(S):
    n = S.get('n')
    return list(range(1 << n)) if n else []


def _cur(S):
    st = S.get('state')
    return st if isinstance(st, int) else None


def _scol(S, i, v):
    if i in S.get('res_state', ()):
        return 'green'
    return None


def _gtxt(S):
    ic = S.get('index2char')
    if not ic or 'g' not in S:
        return '字符 → 编号；每个 `words[i]` 是一条边：前一个字符 → 后一个字符（前者必须在前）'
    es = '，'.join(f"{ic[x]}→{ic[y]}" for x in range(len(S['g'])) for y in sorted(S['g'][x]))
    return f"边：{es}；入度 `ind = {S['ind']}`"


def _ctxt(S):
    st, n, ic = S.get('state'), S.get('n'), S.get('index2char')
    if st is None or not ic or 'cnt' not in S:
        return ''
    two = ''.join(ic[i] for i in range(n) if S['cnt'][i] == 2) or '无'
    one = ''.join(ic[i] for i in range(n) if S['cnt'][i] == 1) or '无'
    return f"`state = {st:0{n}b}`：出现 ==2 次== 的字符 `{two}`，出现 1 次的 `{one}`；`tot = {S.get('tot')}`；`best = {S.get('best')}`"


CONFIG = dict(
    num=3435, title='最短公共超序列的字母出现频率', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='枚举状态 + 拓扑排序判环',
    tags=['难度分 3028'],
    code='''
class Solution(object):
    def supersequences(self, words):
        
        char2index = {}
        index2char = {}
        n = 0
        for w in words:
            if w[0] not in char2index:
                char2index[w[0]] = n
                index2char[n] = w[0]
                n += 1
            if w[1] not in char2index:
                char2index[w[1]] = n
                index2char[n] = w[1]
                n += 1

        g = [set() for x in range(n)]
        ind = [0] * n
        for w in words:
            x = char2index[w[0]]
            y = char2index[w[1]]
            g[x].add(y)
            ind[y] += 1

        best = None
        res_state = set()
        for state in range(1 << n):
            cnt = [1] * n
            tot = n
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cnt[index] += 1
                    tot += 1

            if best is not None and tot > best:
                continue

            part_ind = ind[:]
            q = []
            head = 0
            tail = 0
            for index in range(n):
                if cnt[index] == 2 or part_ind[index] == 0:
                    q.append(index)
                    tail += 1

            while head < tail:
                x = q[head]
                head += 1
                for y in g[x]:
                    if cnt[y] == 2:
                        continue
                    part_ind[y] -= 1
                    if part_ind[y] == 0:
                        q.append(y)
                        tail += 1

            if len(q) == n:
                if best is None or tot < best:
                    best = tot
                    res_state = set([state])
                else:
                    res_state.add(state)
        
        res = []
        for state in res_state:
            cnt = [0] * 26
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cnt[ord(index2char[index]) - 97] = 2
                else:
                    cnt[ord(index2char[index]) - 97] = 1
            res.append(cnt[:])
        
        return res
''',
    call=f'Solution().supersequences({W0!r})',
    expect=[[2, 1] + [0] * 24, [1, 2] + [0] * 24],
    views=[
        dict(type='text', h=90, size=28, fn=_gtxt),
        dict(type='array', var=_states, label='state：第 i 位为 1 = 第 i 个字符出现 2 次（绿 = 目前最优）', cell=90, h=210,
             pointers={_cur: 'pink'}, pointer_labels={_cur: 'state'}, color=_scol),
        dict(type='text', h=100, size=28, fn=_ctxt),
        dict(type='queue', var='q', label='拓扑排序队列 q', h=100),
        dict(type='array', var='part_ind', label='part_ind（剩余入度）', cell=80, h=130),
    ],
    watch=['state', 'tot', ('best', 'best', 'green'), ('res_state', 'res_state', 'cyan')],
    skip=['char2index = {}', 'index2char = {}', 'n = 0', 'for w in words', 'if w[0] not in', 'if w[1] not in', 'char2index[w[', 'index2char[n] =',
          'x = char2index', 'y = char2index', 'ind[y] += 1', 'g = [set()', 'ind = [0]', 'best = None', 'res_state = set()',
          'cnt = [1] * n', 'tot = n', 'for index in range(n)', 'cnt[index] += 1', 'tot += 1', 'part_ind = ind[:]', 'q = []', 'head = 0',
          'tail = 0', 'head += 1', 'tail += 1', 'x = q[head]', 'if part_ind[y] == 0', 'continue', 'if (state & (1 << index)) == (1 << index):\n',
          67, 69, 70, 72, 'res = []'],
    max_steps=110,
    captions={
        'n += 1': '给新出现的字符编号，目前共 `n = {n}` 个不同字符；每个字符在超序列里出现 1 或 2 次',
        'g[x].add(y)': '`words[i]` 的前字符 `{index2char[x]}` 必须在后字符 `{index2char[y]}` 前面 → 建边 `{index2char[x]} → {index2char[y]}`，`{index2char[y]}` 入度 +1',
        'for state in range': lambda S, B, r: ('所有状态枚举完毕，答案在 `res_state` 里' if S.get('state') == B.get('state') else
                                               f'枚举 2^n 种状态：第 i 位为 1 表示第 i 个字符出现 2 次。这是 `state = {S.state}`（二进制 `{S.state:0{S.n}b}`）'),
        'if (state & (1 << index))': lambda S, B, r: (f'`state` 的第 `{S.index}` 位是 `{S.state >> S.index & 1}` → 字符 `{S.index2char[S.index]}` 出现 '
                                                      + ('2' if S.state >> S.index & 1 else '1') + ' 次'),
        'if best is not None and tot > best': lambda S, B, r: (
            f'这个状态超序列长度 `tot = {S.tot}`' + ('，比最优 `best` 还长 → 直接跳过' if S.best is not None and S.tot > S.best else '，不比最优差 → 判断它能不能排出来')),
        'if cnt[index] == 2 or part_ind[index] == 0': lambda S, B, r: (
            f'字符 `{S.index2char[S.index]}`：' + ('出现 2 次 → 放在两端，约束已满足，直接入队' if S.cnt[S.index] == 2
                                                  else ('入度为 0 → 没有人要求它在后面，入队' if S.part_ind[S.index] == 0 else '入度不为 0，要等前面的字符处理完'))),
        'q.append(index)': '`{index}` 入队，作为拓扑排序的起点',
        'while head < tail': lambda S, B, r: (f'队列里还有 `{S.tail - S.head}` 个字符待处理' if S.head < S.tail else '队列空了，拓扑排序结束'),
        'for y in g[x]': lambda S, B, r: f'处理字符 `{S.index2char[S.x]}` 的出边：它指向 `{"、".join(S.index2char[y] for y in sorted(S.g[S.x]))}`',
        'if cnt[y] == 2': lambda S, B, r: (f'`{S.index2char[S.y]}` 出现 2 次：两端已满足，这条边不用管' if S.cnt[S.y] == 2
                                           else f'`{S.index2char[S.y]}` 只出现 1 次：这条边要算入度'),
        'part_ind[y] -= 1': '前面的 `{index2char[x]}` 已处理 → `{index2char[y]}` 的剩余入度减 1，变成 `{part_ind[y]}`',
        'q.append(y)': '入度归零 → `{index2char[y]}` 可以排了，入队',
        'if len(q) == n': lambda S, B, r: (f'`len(q) = {len(S.q)}`，`n = {S.n}`：' + ('所有字符都出了队 → 没有环，这个状态可行' if len(S.q) == S.n else '有字符进不了队 → 有环，这个状态不可行')),
        'if best is None or tot < best': lambda S, B, r: ('第一个可行状态，或比最优更短 → 更新最优' if S.best is None or S.tot < S.best else '和最优一样短 → 并列'),
        'best = tot': '最短长度 `best = {tot}`',
        'res_state = set([state])': '旧的作废，`res_state` 只保留这个状态 `{state}`',
        'res_state.add(state)': '和最优并列，加入 `res_state`',
        'for state in res_state': '把每个最优状态转成 26 位频率数组',
        'res.append(cnt[:])': '这个状态的频率：`a..z` 里出现 2 次的是 2，出现 1 次的是 1 → `{cnt[:2]}…`',
        'return res': '返回所有最优状态的频率数组（共 `{len(ret)}` 个）',
    },
    cards=dict(
        one_liner='每个字符出现 1 或 2 次：枚举状态，拓扑排序判环',
        complexity='时间 `O(2^n·(n+m))`，空间 `O(n+m)`',
        problem=['`words` 里每个字符串长 2，求所有最短公共超序列的字母频率（互为排列的只算一个）',
                 '`["ab","ba"]` → `aba` 和 `bab` 两种频率',
                 f'本视频：`words = {W0}`'],
        quote='最少出现一次很好理解，而最多出现两次则可以通过words中字符串的长度分析得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['多于两次时，中间那个多余的 x 总能被第一个或最后一个 x 替代 → 每种字符只出现 1 或 2 次',
              '暴力枚举每种字符是 1 次还是 2 次（最多 `2^16`）；出现 2 次的放两端，相关字符串自动满足',
              '剩下出现 1 次的字符只建边、做拓扑排序：能全出队 = 无环 = 可行'],
        summary=['时间约 `O(2^n·(n+m))`，空间 `O(n+m)`',
                 '不用每次建图：图只建一次，出现 2 次的字符直接当“起点”入队，并忽略指向它的边',
                 '`tot > best` 直接剪枝；`tot < best` 才清空 `res_state`',
                 '本题原文为 Python 2 风格，没有需要改的语法',
                 '对比灵神：灵神用三色 DFS 判环并用位运算枚举子集，这里用入度 + 队列的拓扑排序'],
    ),
)
