def _ft(S):
    if 'k' not in S or 'need' not in S:
        return '`need` = 前 k 大节点的度数和；`inner + outer` = 它们最多能提供的度数'
    if S['_line'] < 17:
        return f"前 `k = {S['k']}` 个节点需要 `need = {S['need']}`"
    return ''


def _ft2(S, B):
    if 'k' not in S or 'inner' not in S or 'p' not in S or 'outer' not in S:
        return '`need` = 前 k 大节点的度数和；`inner + outer` = 最多能提供的度数'
    if S['_line'] < 21:
        return f"前 `k = {S['k']}` 个节点：`need = {S['need']}`，下面算它们最多能提供多少度"
    return (f"`need = {S['need']}`　vs　`inner + outer = {S['inner']} + {S['outer']} = {S['inner'] + S['outer']}`"
            f"　→ {'够' if S['inner'] + S['outer'] >= S['need'] else '==不够，返回 False=='}")


CONFIG = dict(
    num=3656, title='判断是否存在简单图', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='度序列排序 + 前缀和判定',
    tags=[],
    code='''
class Solution(object):
    def simpleGraphExists(self, degrees):
        
        if sum(degrees) % 2 == 1:
            return False

        degrees.sort(reverse=True)
        s = [0]
        for v in degrees:
            s.append(s[-1] + v)
        
        need = 0
        p = len(degrees)
        for k in range(1, len(degrees) + 1):
            need += degrees[k - 1]
            inner = k * (k - 1)
            while p > k and degrees[p - 1] < k:
                p -= 1
            
            outer = (p - k) * k + s[-1] - s[p]
            if inner + outer < need:
                return False

        return True
''',
    call='Solution().simpleGraphExists([1, 3, 2, 3, 1, 2])',
    expect=True,
    skip=['s = [0]', 'for v in degrees', 's.append', 'need = 0', 'p = len'],
    views=[
        dict(type='array', var='degrees', label='degrees（降序排好；蓝 = 第 k 大，橙 = p 之后的节点）', cell=80, h=170,
             pointers={'k - 1': 'blue', 'p': 'orange'},
             color=lambda S, i, v: ('blue' if 'k' in S and i < S['k'] else None)),
        dict(type='array', var='s', label='s（前缀和，s[i] = 前 i 个度数之和）', cell=80, h=170,
             pointers={'p': 'orange'}),
        dict(type='text', fn=_ft2, size=26, h=70),
    ],
    watch=[('k', 'k', 'blue'), ('p', 'p', 'orange'), ('need', 'need', 'pink'), ('inner', 'inner'), ('outer', 'outer', 'green')],
    captions={
        'if sum(degrees) % 2 == 1': '每条边贡献两个度 → 度数总和 `{sum(degrees)}` 必须是偶数：{"奇数 → 直接 False" if sum(degrees) % 2 else "偶数，继续"}',
        'degrees.sort': '==从大到小排序==：度大的节点要连更多边，优先考虑',
        'return False': lambda S, B, r: '度数不够分配 → 返回 False' if S._line == 15 or 'k' in S else '总和为奇数 → 返回 False',
        'need += degrees': '`need` += `degrees[{k-1}]` = {degrees[k-1]} → ==前 {k} 个节点共需要 {need} 个度==',
        'inner = k': '这 k 个节点两两连边，最多产生 `k×(k−1) = {inner}` 个度',
        'while p > k': lambda S, B, r: (f'`degrees[{S.p-1}] = {S.degrees[S.p-1]} < k = {S.k}`：这个节点最多只能给 `{S.degrees[S.p-1]}` 条边，全要 → `p` 左移'
                                        if S.p > S.k and S.degrees[S.p - 1] < S.k else f'`p = {S.p}`：再往前的节点度数 ≥ k 或已到 k，停止'),
        'p -= 1': '`p` → {p}：`degrees[p..]` 都比 k 小',
        'outer = (': lambda S, B, r: (f'剩余节点：前 `p−k = {S.p-S.k}` 个每个最多贡献 `k` 个度，后面的全部贡献 → `{S.p-S.k}×{S.k} + {S.s[-1]-S.s[S.p]}` = =={S.outer}=='
                                      if S.p >= S.k else f'`p = {S.p} ≤ k = {S.k}`：分界 p 已不在 k 右边，直接按原文公式算 → `outer = (p−k)×k + s[-1]−s[p]` = =={S.outer}=='),
        'if inner + outer < need': lambda S, B, r: (f'`inner + outer = {S.inner + S.outer}` ≥ `need = {S.need}`：这 {S.k} 个节点的度可以满足，继续'
                                                    if S.inner + S.outer >= S.need else
                                                    f'`inner + outer = {S.inner + S.outer}` < `need = {S.need}`：最多提供的度数不够 → ==不存在=='),
        'return True': '每个 k 都满足 → ==存在简单图==',
    },
    cards=dict(
        one_liner='度从大到小排序，逐个检查「能提供的度够不够需要的度」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`degrees[i]` 是第 `i` 个顶点的期望度数，判断是否存在==无自环、无重边==的无向图',
                 '保证 `0 <= degrees[i] <= n - 1`',
                 '本视频：`[1,3,2,3,1,2]` → `True`'],
        quote='度越大的节点需要连接的边越多，因此这些边就应该优先分配给度同样比较大的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['每条边产生两个度 → 总和必须是偶数，否则直接 False',
              '排序后看前 `k` 大的节点：内部两两连边最多 `k(k−1)` 个度',
              '其余节点每个最多给 `min(度, k)` 个度；三部分之和 `≥` 需要的度数才可能成立'],
        summary=['时间 `O(n log n)`（排序），`p` 只左移，后面是 `O(n)`',
                 '易错：别忘了先判断度数和为奇数',
                 '`p` 把剩余节点分成「度 ≥ k」和「度 < k」两段，分别用 `k` 和前缀和计算',
                 '这是 Erdős–Gallai 定理的判定形式',
                 '注意：`degrees.sort` 会原地修改传入的数组'],
    ),
)
