WORDS = ["a", "b", "ab", "cde", "ba"]


def _L(m):
    return ''.join(chr(97 + i) for i in range(26) if m >> i & 1) or '∅'


def _info(S):
    if 'cnt' not in S:
        return ''
    return f"连通分量数 ==cnt 为 {S['cnt']}==，最大分量 ==max_len 为 {S['max_len']}=="


def _qvar(S):
    q = S.get('q')
    if q is None:
        return None
    return [_L(v) for v in q]


CONFIG = dict(
    num=2157, title='字符串分组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='状态压缩 · 枚举边的 BFS 求连通分量',
    tags=['七、并查集', '§7.2 进阶', '难度分 2499'],
    code='''
class Solution(object):
    def groupStrings(self, words):

        num_list = []
        num_dict = {}
        for word in words:
            now = 0
            for char in word:
                now |= (1 << ord(char) - 97)
            num_list.append(now)
            num_dict[now] = num_dict.get(now, 0) + 1
        
        used = set()
        cnt = 0
        max_len = 0
        for num in num_list:
            if num not in used:
                cnt += 1
                q = [num]
                l = 0
                r = 1
                now_len = num_dict[num]
                used.add(num)
                while l < r:
                    now = q[l]
                    l += 1
                    for index in range(26):
                        next = now | (1 << index)
                        if next in num_dict and next not in used:
                            q.append(next)
                            used.add(next)
                            r += 1
                            now_len += num_dict[next]
                        
                        if (now & (1 << index)):
                            next = now ^ (1 << index)
                            if next in num_dict and next not in used:
                                q.append(next)
                                used.add(next)
                                r += 1
                                now_len += num_dict[next]
                            
                            tmp = next
                            for rep in range(26):
                                next = tmp | (1 << rep)
                                if next in num_dict and next not in used:
                                    q.append(next)
                                    used.add(next)
                                    r += 1
                                    now_len += num_dict[next]
                
                max_len = max(max_len, now_len)
        
        return [cnt, max_len]
''',
    call=f'Solution().groupStrings({WORDS})',
    expect=[2, 4],
    views=[
        dict(type='array', var='words', label='words', cell=90, h=160),
        dict(type='map', var='num_dict', label='num_dict：字母集合 → 出现次数（节点 = 集合）', fmt=lambda k, v: f'{_L(k)} : {v}', h=120),
        dict(type='array', var=_qvar, label='q（BFS 队列，l 指向下一个出队的；暗 = 已出队）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=200),
        dict(type='text', fn=_info, size=30),
    ],
    watch=[('cnt', 'cnt', 'green'), ('max_len', 'max_len', 'orange'), ('now_len', 'now_len', 'cyan'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    skip=['for index in range(26)', 'for rep in range(26)', 'for char in word', 'now = 0', 'num_list.append', 'used.add(next)',
          'r += 1', 'l += 1', 'used = set()', 'cnt = 0', 'l = 0', 'tmp = next', 'if (now & (1 << index))',
          'next = now | (1 << index)', 'next = now ^ (1 << index)', 'next = tmp | (1 << rep)',
          'if next in num_dict and next not in used', 'used.add(num)', 'num_list = []', 'num_dict = {}'],
    captions={
        'now |= (1 << ord(char) - 97)': lambda S, B, r: f'字母 `{S.char}` 对应第 `{ord(S.char) - 97}` 位：`now` = 集合 `{_L(S.now)}`',
        'num_dict[now] = ': lambda S, B, r: (f'集合 `{_L(S.now)}` 已出现 `{S.num_dict[S.now]}` 次：`ab` 与 `ba` 掩码相同，是同一个点' if S.num_dict[S.now] > 1 else f'集合 `{_L(S.now)}` 第一次出现，`num_dict` 记 1'),
        'max_len = 0': '`cnt` 数连通分量，`max_len` 记最大分量里的字符串数',
        'for num in num_list': '依次取每个字符串的集合，没访问过就是新分量的起点',
        'if num not in used': lambda S, B, r: (f'集合 `{_L(S.num)}` 没访问过 → 新的连通分量，从它开始 BFS' if S.num not in S.used
                                               else f'集合 `{_L(S.num)}` 已在之前的 BFS 里访问过 → 跳过'),
        'cnt += 1': '新分量：`cnt = {cnt}`',
        'q = [num]': lambda S, B, r: f'起点 `{_L(S.num)}` 入队，`now_len = {S.num_dict[S.num]}`（这个集合的字符串数）',
        'r = 1': '`l`、`r` 是数组队列的队首 / 队尾下标（左闭右开）',
        'now_len = num_dict[num]': '分量大小先记下起点的个数：`now_len = {now_len}`',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续 BFS' if B.l < B.r else f'`l == r`：队列空了，这个分量 BFS 结束，分量里共 `{B.now_len}` 个字符串'),
        'now = q[l]': lambda S, B, r: f'出队 `{_L(S.now)}`：不枚举两两关联，而是枚举 26 个字母的 加 / 删 / 换，算出邻居集合',
        30: lambda S, B, r: f'==添加== 字母：`{_L(S.now)}` → `{_L(S.next)}` 在 words 里且没访问过 → 入队',
        38: lambda S, B, r: f'==删除== 字母：`{_L(S.now)}` → `{_L(S.next)}` 在 words 里且没访问过 → 入队',
        47: lambda S, B, r: f'==替换== 字母（先删再加）：`{_L(S.now)}` → `{_L(S.next)}` 在 words 里且没访问过 → 入队',
        'now_len += num_dict[next]': lambda S, B, r: f'`{_L(S.next)}` 出现 `{S.num_dict[S.next]}` 次，加进分量大小：`now_len = {S.now_len}`',
        'max_len = max': '最大分量更新：`max_len = {max_len}`',
        'return [cnt': '分量数 `{cnt}`，最大分量 `{max_len}` → 返回 `[{cnt}, {max_len}]`',
    },
    cards=dict(
        one_liner='字符串当图上的点，加 / 删 / 换当边，BFS 数连通分量',
        complexity='时间 `O(n·U^2)`（U=26），空间 `O(n)`',
        problem=['`words` 每个字符串字母互不重复；字母集合经 ==添加 / 删除 / 替换一个字母== 能变成另一个，就「关联」',
                 '关联的字符串同组，求总组数和最大组大小',
                 '示例：`["a","b","ab","cde"]` → `[2,3]`',
                 '本视频：`["a","b","ab","cde","ba"]` → `[2,4]`'],
        quote='将每种字符串视为无向图中的一个点，两个字符串直接的关联视为无向图中的一条边的话，题目实际上就是要找出这张图中有多少个连通分量，以及最大的连通分量中有多少个节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['两两比较 2 万个字符串太慢，改成「枚举边」：每个点至多 `26+26+26^2` 条边',
              '用 `2^26` 的位掩码表示字符串，加 / 删 / 换都是位运算',
              '边的另一端是否存在，查哈希表 `num_dict`',
              '没访问过就从它 BFS：分量数 +1，队列里的点数就是分量大小'],
        summary=['时间 `O(n·U^2)`，`U = 26`；空间 `O(n)`',
                 '相同字符串的掩码相同，`num_dict` 要计数，分量大小按次数累加',
                 '用 `used` 在入队时就标记，防止重复入队',
                 '视频里 26 次枚举中没命中的不再逐步展示，只演示真正入队的邻居',
                 '对比灵神：灵神用并查集边合并边维护答案，这里用 BFS 数连通分量'],
    ),
)
