def _loss(S):
    q = S.get('q')
    if not q:
        return []
    k = q[0]
    return [p if p <= k else 2 * k - p for p in S['prices']]


def _pc(S, idx, v):
    if 'q' not in S or 'i' not in S or S.get('_line', 0) < 23:
        return None
    i, j = S['i'], S['j']
    if idx < i:
        return 'green'
    if idx > j:
        return 'orange'
    return None


def _pc2(S, idx, v):
    if 'q' not in S:
        return None
    return 'purple' if idx < S['bound'] else 'yellow'


def _pi(S):
    return S['i'] if 'i' in S and S.get('_line', 0) >= 23 else None


def _pj(S):
    return S['j'] if 'j' in S and S.get('_line', 0) >= 23 else None


def _txt(S):
    if 'q' not in S:
        return '价格 `p ≤ k`：相对亏损 `p`；`p > k`：相对亏损 `2k − p`'
    k, m = S['q']
    if 'i' not in S or S['_line'] < 23:
        return f'当前询问 `[{k}, {m}]`：价格 ≤ {k} 的共 `bound = {S["bound"]}` 个'
    return (f'阈值 `{k}`：前缀（便宜，绿）选 `i = {S["i"]}` 个，后缀（贵，橙）选 `{len(S["prices"]) - 1 - S["j"]}` 个，'
            f'还差 `k = {S["k"]}` 个')


CONFIG = dict(
    num=2819, title='购买巧克力后的最小相对损失', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='离线排序 · 前缀和 · 两端找第 m 小',
    tags=['题单·二分算法', '题单·常用数据结构'],
    code='''
class Solution(object):
    def minimumRelativeLosses(self, prices, queries):

        prices.sort()
        s = [0]
        for p in prices:
            s.append(s[-1] + p)

        bound = 0
        res = [0] * len(queries)

        for index, q in sorted(enumerate(queries), key=lambda d:d[1][0]):
            while bound < len(prices) and prices[bound] <= q[0]:
                bound += 1

            if bound == 0:
                res[index] = q[0] * q[1] * 2 - (s[-1] - s[-q[1] - 1])
            elif bound == len(prices):
                res[index] = s[q[1]]
            else:
                i = 0
                j = len(prices) - 1
                k = q[1]
                while True:
                    if i == bound:
                        res[index] = s[bound] + q[0] * (q[1] - bound) * 2 - (s[-1] - s[-q[1] + bound - 1])
                        break
                    elif j == bound - 1:
                        res[index] = q[0] * (len(prices) - bound) * 2 - (s[-1] - s[bound]) + s[q[1] + bound - len(prices)]
                        break
                    elif k == 1:
                        if prices[i] < q[0] * 2 - prices[j]:
                            i += 1
                        else:
                            j -= 1
                        
                        res[index] = s[i] + q[0] * (q[1] - i) * 2 - (s[-1] - s[j + 1])
                        break

                    else:
                        mid = k // 2
                        if i + mid - 1 >= bound:
                            j -= mid
                        elif j - mid + 1 < bound:
                            i += mid
                        elif prices[i + mid - 1] < q[0] * 2 - prices[j - mid + 1]:
                            i += mid
                        else:
                            j -= mid
                        
                        k -= mid

        return res
''',
    call='Solution().minimumRelativeLosses([1,9,22,10,19], [[18,4],[5,2]])',
    expect=[34, -21],
    views=[
        dict(type='array', var='prices', label='prices（排序后；绿 = 已选的便宜前缀，橙 = 已选的贵后缀）', cell=76, h=210,
             pointers={_pi: 'blue', _pj: 'pink', 'bound': 'yellow'}, pointer_labels={_pi: 'i', _pj: 'j'}, color=_pc),
        dict(type='array', var=_loss, label='每件的相对亏损（紫 = p ≤ k，黄 = p > k）', cell=76, h=150,
             color=_pc2),
        dict(type='array', var='s', label='s（prices 的前缀和）', cell=76, h=140),
        dict(type='text', h=100, size=26, fn=_txt),
    ],
    watch=[('q', 'q', 'orange'), ('bound', 'bound', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'cyan'), ('res', 'res', 'green')],
    skip=['bound = 0', 'res = [0]', 'while True', 'break', 'for p in prices', 'i = 0', 'j = len(prices) - 1'],
    captions={
        'prices.sort()': '价格先排序：`{prices}`，询问离线处理',
        's.append': '`s` 是前缀和：`s[x]` = 最便宜的 x 件的价格和 → 末尾 `{s[-1]}`',
        'for index, q in sorted': lambda S, B, r: (f'按 `k` 从小到大取询问 `{S.q}`（原下标 `{S.index}`）：这样 `bound` 只增不减'
                                                    if 'q' not in B or S.q != B.q else '所有询问处理完了'),
        'while bound < len': lambda S, B, r: (
            f'`prices[{S.bound}] = {S.prices[S.bound]} ≤ k = {S.q[0]}`：属于“便宜”部分 → `bound` 右移' if S.bound < len(S.prices) and S.prices[S.bound] <= S.q[0]
            else (f'价格全都 ≤ {S.q[0]}' if S.bound >= len(S.prices) else f'`prices[{S.bound}] = {S.prices[S.bound]} > k = {S.q[0]}`：从这里起是“贵”部分 → `bound = {S.bound}` 即分界')),
        'bound += 1': '`bound = {bound}`',
        'if bound == 0': lambda S, B, r: ('价格全都 > k：亏损都是 `2k − p`，直接取最贵的 m 件（后缀和）' if S.bound == 0
                                          else f'`bound = {S.bound} ≠ 0`：有便宜的，也有贵的 → 需要比较'),
        'elif bound == len': lambda S, B, r: ('价格全都 ≤ k：亏损就是 `p`，取最便宜的 m 件 `s[m]`' if S.bound == len(S.prices)
                                              else '既有便宜的又有贵的，进入二分'),
        'k = q[1]': '`i = 0`（便宜侧起点），`j = {j}`（贵侧终点），`k = {k}` = 还要挑的件数',
        'if i == bound': lambda S, B, r: (f'`i = {S.i} = bound`：便宜的全选完了，剩下 {S.q[1] - S.bound} 件从贵的里挑最大的' if S.i == S.bound
                                          else f'`i = {S.i} ≠ bound = {S.bound}`：便宜侧还没选完'),
        'res[index] = s[bound]': '便宜的全选：`s[{bound}]`，贵的取最大的 `{q[1] - bound}` 件 → `res[{index}] = {res[index]}`',
        'elif j == bound - 1': lambda S, B, r: (f'`j = {S.j} = bound − 1`：贵的全选完了，剩下的从便宜里挑最小的' if S.j == S.bound - 1
                                                else f'`j = {S.j}`：贵侧还没选完'),
        'res[index] = q[0] * (len': '贵的全选，再从便宜里取最小的 → `res[{index}] = {res[index]}`',
        'elif k == 1': lambda S, B, r: ('只差最后 1 件：比较两端各一个，取亏损小的' if S.k == 1 else f'还差 `k = {S.k}` 件，二分排除一半'),
        'if prices[i] < q[0] * 2 - prices[j]': lambda S, B, r: (
            f'便宜端亏损 `{S.prices[S.i]}`，贵端亏损 `2×{S.q[0]} − {S.prices[S.j]} = {S.q[0] * 2 - S.prices[S.j]}`：'
            + ('便宜端更小 → 选它' if S.prices[S.i] < S.q[0] * 2 - S.prices[S.j] else '贵端更小（或相等） → 选它')),
        'i += 1': '多选便宜端一件：`i = {i}`',
        'j -= 1': '多选贵端一件：`j = {j}`',
        'res[index] = s[i]': '前缀 `s[{i}]` + 后缀亏损合计 → `res[{index}] = {res[index]}`',
        'mid = k // 2': '还差 `k = {k}` 件：每侧先看各自的第 `mid = {mid}` 件（`k // 2`）',
        'if i + mid - 1 >= bound': lambda S, B, r: (
            f'便宜侧取 {S.mid} 件会越过 bound，便宜侧不够 → 这 {S.mid} 件取自贵侧，`j` 左移' if S.i + S.mid - 1 >= S.bound
            else '便宜侧还够 mid 件'),
        'elif j - mid + 1 < bound': lambda S, B, r: (
            f'贵侧取 {S.mid} 件会越过 bound，贵侧不够 → 取便宜侧，`i` 右移' if S.j - S.mid + 1 < S.bound else '两侧都够 mid 件，比较它们的边界亏损'),
        'elif prices[i + mid - 1]': lambda S, B, r: (
            f'便宜侧第 mid 件亏损 `{S.prices[S.i + S.mid - 1]}` < 贵侧第 mid 件 `{S.q[0] * 2 - S.prices[S.j - S.mid + 1]}`：便宜侧的 mid 件一定都入选 → `i += {S.mid}`'
            if S.prices[S.i + S.mid - 1] < S.q[0] * 2 - S.prices[S.j - S.mid + 1]
            else f'贵侧第 mid 件亏损更小（`{S.q[0] * 2 - S.prices[S.j - S.mid + 1]}`）：贵侧的 mid 件都入选 → `j -= {S.mid}`'),
        'i += mid': '`i = {i}`：便宜侧选定 {mid} 件',
        'j -= mid': '`j = {j}`：贵侧选定 {mid} 件',
        'k -= mid': '确定了 {mid} 件，还差 `k = {k}` 件',
        'return res': '`res = {res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='亏损在 k 处拐弯：先便宜的、后贵的，两头往中间挑',
        complexity='时间 `O(n log n + q log m)`，空间 `O(n)`',
        problem=['Bob 买 `m` 件，每件价格 `p`：Bob 先付 `k`，超出部分 Alice 付。求 Bob 的最小相对损失',
                 '相对损失 = Bob 付的 − Alice 付的：`p ≤ k` 时是 `p`，`p > k` 时是 `2k − p`',
                 '本视频：`prices=[1,9,22,10,19]`，`queries=[[18,4],[5,2]]` → `[34,-21]`'],
        quote='当商品价格不超过当前的k[i]时，价格越贵bob越亏，但是当商品价格超过当前的k[i]时，价格越贵bob越赚，因为超出k[i]的这部分是alice出的。',
        quote_src='—— yiduobo 题解原文',
        idea=['价格排序后，亏损在 `k` 处先升后降：便宜部分挑小的（前缀），贵部分挑大的（后缀）',
              '于是答案 = 一个前缀 + 一个后缀的亏损和，用前缀和 `s` 一次算出',
              '像第 4 题那样二分找第 `m` 小：每轮比较两端各 `mid` 个，排除一半'],
        summary=['时间 `O(n log n + q log m)`，空间 `O(n)`',
                 '询问按 `k` 排序后，`bound` 只增不减，不用每次重新找',
                 '易错：前缀、后缀和下标（`s[-q[1]+bound-1]` 等）很容易差一；先判三种边界再二分',
                 '原文为 Python 2 写法，整数除法 `k / 2` 已改为 `k // 2`',
                 '灵神归类到二分题单，本写法用的是“两个有序序列中找第 m 小”的二分思路'],
    ),
)
