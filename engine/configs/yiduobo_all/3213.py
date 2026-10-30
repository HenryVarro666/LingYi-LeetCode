TARGET = 'aba'
WORDS = ['ab', 'b', 'a']
COSTS = [1, 5, 5]


def _h(w, mod=10 ** 9 + 7):
    v = 0
    for c in w:
        v = (v * 26 + ord(c) - 97) % mod
    return v


def _groups(S):
    cd = S.get('cost_dict')
    if not cd:
        return '按长度分组：同长度的单词放一组，每组 `哈希 → 最小成本`'
    parts = []
    for length, (r, info) in cd.items():
        names = []
        for w in WORDS:
            if len(w) == length and _h(w) in info:
                names.append(f'{w}→{info[_h(w)]}')
        parts.append(f'长度 {length}：' + '，'.join(names))
    return '；'.join(parts)


def _sub(S):
    if 'f' in S and 'index' in S and 'length' in S and 'key' in S and S['index'] + 1 >= S['length']:
        i, L = S['index'] + 1, S['length']
        t = TARGET[i - L:i]
        hit = t in WORDS
        return f"窗口 `target[{i - L}:{i}]` = =={t}=={'：是单词' if hit else '：不是单词'}"
    return '`f[i]`：拼出 target 前 i 个字符的最小成本，`-1` 表示拼不出'


CONFIG = dict(
    num=3213, title='最小代价构造字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按长度分组 RK 哈希 + DP',
    tags=['字符串', '难度分 2171'],
    code='''
class Solution(object):
    def minimumCost(self, target, words, costs):

        rank = [index for index in range(len(words))]
        rank.sort(key=lambda d:len(words[d]))
        n = len(target)

        hit = [[] for _ in range(n)]
        p = 0
        mod = 10 ** 9 + 7
        base = 26
        asc_a = ord('a')
        cost_dict = {}
        while p < len(rank):
            q = p
            while q < len(rank) and len(words[rank[p]]) == len(words[rank[q]]):
                q += 1

            length = len(words[rank[p]])
            if length > len(target):
                break

            r = 1
            for index in range(length):
                r = r * base % mod
            cost_dict[length] = [r, {}]
                
            for index in range(p, q):
                w = words[rank[index]]
                v = 0
                for c in w:
                    v = (v * base + ord(c) - asc_a) % mod
                
                if v not in cost_dict[length][1]:
                    cost_dict[length][1][v] = costs[rank[index]]
                else:
                    cost_dict[length][1][v] = min(cost_dict[length][1][v], costs[rank[index]])

            p = q

        f = [0]
        p = [1]
        v = [0]
        for index, c in enumerate(target):
            f.append(-1)
            p.append(p[-1] * base % mod)
            v.append((v[-1] * base + ord(c) - asc_a) % mod)

            for length in cost_dict:
                if index + 1 < length:
                    continue
                else:
                    r, cost_info = cost_dict[length]
                    key = (v[-1] - v[-length - 1] * p[length] % mod + mod) % mod
                    if key in cost_info and f[-length - 1] != -1 and (f[-1] == -1 or f[-1] > f[-length - 1] + cost_info[key]):
                        f[-1] = f[-length - 1] + cost_info[key]

        return f[-1]
''',
    call="Solution().minimumCost('aba', ['ab', 'b', 'a'], [1, 5, 5])",
    expect=6,
    views=[
        dict(type='text', fn=_groups, size=28, h=50),
        dict(type='text', fn=_sub, size=30, h=50),
        dict(type='string', var='target', label='target（蓝框 = 当前窗口）', h=190,
             window=('(index + 1 - length) if f else None', 'index if f else None')),
        dict(type='array', var='f', label='f[i]：前 i 个字符的最小成本', h=190, pointers={'index + 1': 'blue'},
             color=lambda S, idx, v: ('green' if v != -1 else None)),
    ],
    watch=[('length', 'length', 'pink'), ('index', 'index', 'blue'), 'key'],
    captions={
        'rank.sort': '按单词长度排序下标，同长度的单词挨在一起，方便分组',
        'while p < len': lambda S, B, r: (f'`p = {S.p}`：从 `rank[{S.p}]` 开始建下一组' if S.p < len(S.rank) else '所有长度的组都建好了'),
        'length = len': '这一组单词的长度 `length = {length}`',
        'cost_dict[length] = [r': '给长度 {length} 建一个哈希表：`哈希 → 最小成本`',
        'for index in range(p, q)': lambda S, B, r: ('这一组的单词都处理完了' if B.get('w') == S.words[S.rank[S.index]] else f'取这一组的下一个单词（`rank[{S.index}]`）'),
        'w = words': '取这一组的单词 `{w}`',
        'if v not in': '`{w}` 的 RK 哈希（逐字符 `v×base + 字符`）= `{v}`：表里已有吗？',
        'cost_dict[length][1][v] = costs': '第一次出现：成本记为 =={costs[rank[index]]}==',
        'cost_dict[length][1][v] = min': '哈希相同（同一个单词）：成本取较小者',
        'f = [0]': '`f[0] = 0`：空串成本 0。`p[i] = base^i`，`v[i]` = `target` 前 `i` 个字符的哈希，下面边走边填',
        'for index, c in enumerate': lambda S, B, r: ('target 都处理完了' if B.get('index') == S.index and B.get('c') == S.c else
                                                      f'读入第 {S.index + 1} 个字符 `{S.c}`：`f` 追加 `-1`（暂时拼不出），`p`、`v` 追加 `base^{S.index + 1}` 和前缀哈希'),
        'for length in cost_dict': lambda S, B, r: ('这个位置所有长度都试过了' if B.get('length') == S.length and B.get('index') == S.index else
                                                    f'试以长度 `{S.length}` 的单词结尾' + ('' if S.index + 1 >= S.length else f'：比已读的 {S.index + 1} 个字符还长，跳过')),
        'key = (v[-1]': lambda S, B, r: f"窗口 `target[{S.index + 1 - S.length}:{S.index + 1}]` = '{TARGET[S.index + 1 - S.length:S.index + 1]}'，哈希 = 前缀哈希之差 `v[-1] − v[-length-1] × base^length` = `{S.key}`",
        'if key in cost_info': lambda S, B, r: (f"哈希 `{S.key}` 在这一组里（是单词），而且前缀 `f[{S.index + 1 - S.length}] = {S.f[-S.length - 1]}` 能拼出 → 比较并更新"
                                                if S.key in S.cost_info and S.f[-S.length - 1] != -1 else
                                                f"哈希 `{S.key}` 不在这一组里，或前缀拼不出 → 这个长度不能用"),
        'f[-1] = f[-length - 1]': '`f[{index + 1}] = f[{index + 1 - length}] + 成本` = =={f[-1]}==',
        'return f[-1]': '`f[-1]` = 拼出整个 target 的最小成本 = =={f[-1]}==',
    },
    skip=['f.append', 'p.append', 'v.append', 'r, cost_info', 'if index + 1 < length', 'continue', 'p = [1]', 'v = [0]', 'rank = [index', 'rank.sort_x', 'rank = [index', 'n = len(target)', 'hit = [[]', 'p = 0', 'mod = ', 'base = ', 'asc_a', 'cost_dict = {}', 'q = p', 'while q <', 'q += 1',
          'if length > len(target)', 'break', 'r = 1', 'for index in range(length)', 'r = r * base', 'for c in w', 'v = (v * base', 'v = 0', 'p = q'],
    max_steps=100,
    cards=dict(
        one_liner='单词按长度分组，每组用 RK 哈希比对 target 的所有窗口',
        complexity='时间 `O(n√L)`，空间 `O(n + L)`',
        problem=['给 `words` 和 `costs`，每个单词可重复用，拼出 `target`，总代价最小',
                 '拼不出返回 `-1`',
                 '本视频：`target = aba`，`words = [ab, b, a]`，`costs = [1,5,5]` → `2`'],
        quote='将words中的单词先按长度进行分组，那么对于同一个组内的单词……只需要考察target中的所有长度为length的子串是否能与这些单词匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` = 拼出前 `index` 个字符的最小代价，枚举最后一个单词：`f[index - len] + cost`',
              '逐个单词去比对是 `O(n²)`；改为按长度分组，不同长度最多 `√L` 种',
              'RK 哈希：用==前缀哈希之差==算窗口哈希，一次比对 `O(1)`'],
        summary=['时间 `O(n√L)`，空间 `O(n + L)`',
                 '`f = -1` 表示拼不出，转移前要判断 `f[-length - 1] != -1`',
                 '同一长度的相同单词，哈希相同，取最小成本',
                 '本文单模哈希（`mod = 10^9+7`，`base = 26`），有碰撞风险',
                 '对比灵神：灵神用随机 BASE 的哈希数组，yiduobo 提前按长度分组、哈希表按组存放'],
    ),
)
