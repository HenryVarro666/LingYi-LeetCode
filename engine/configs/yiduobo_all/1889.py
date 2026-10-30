CONFIG = dict(
    num=1889, title='装包裹的最小浪费空间', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='排序 + 前缀和 + 单调指针',
    tags=['灵神题单', '双序列配对', '难度分 2214'],
    code='''
class Solution(object):
    def minWastedSpace(self, packages, boxes):

        box_info = []
        m = len(boxes)
        for index in range(m):
            for v in boxes[index]:
                box_info.append([v, index])
        
        box_info = sorted(box_info, key=lambda d:d[0])
        
        n = len(packages)
        sorted_packages = sorted(packages)
        s = [sorted_packages[0]]
        for package in sorted_packages[1:]:
            s.append(s[-1] + package)
        
        dealed = [-1] * m
        cost = [0] * m
        p = -1
        mod = 10 ** 9 + 7
        for v, index in box_info:
            while p + 1 < n and sorted_packages[p + 1] <= v:
                p += 1
            
            if p > dealed[index]:
                cnt = p - dealed[index]
                cost[index] += cnt * v - s[p]
                if dealed[index] >= 0:
                    cost[index] += s[dealed[index]]
                dealed[index] = p

        res = -1
        for index in range(m):
            if dealed[index] == n - 1 and (res == -1 or res > cost[index]):
                res = cost[index]
        
        if res != -1:
            res %= mod

        return res
''',
    call='Solution().minWastedSpace([3,5,8,10,11,12], [[12],[11,9],[10,5,14]])',
    expect=9,
    views=[
        dict(type='array', var='sorted_packages', label='sorted_packages（蓝框 = 已被处理的包裹，p = 最大可装下标）', h=200, cell=80,
             pointers={'p': 'blue'}, window=('0', 'p') if False else None,
             color=lambda S, i, v: 'blue' if 'p' in S and i <= S['p'] else None),
        dict(type='array', var='box_info', label='box_info：[箱子尺寸, 供应商]，按尺寸排序', h=150, cell=122,
             fmt=lambda v: f'{v[0]}|{v[1]}' if isinstance(v, list) else str(v),
             color=lambda S, i, v: 'yellow' if 'v' in S and 'index' in S and isinstance(v, list) and v[0] == S['v'] and v[1] == S['index'] else None),
        dict(type='array', var='dealed', label='dealed[供应商]：已能处理到第几个包裹', h=120, cell=100,
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and 'p' in S else None),
        dict(type='array', var='cost', label='cost[供应商]：浪费空间累计', h=100, cell=100, index=False,
             color=lambda S, i, v: 'green' if S.get('dealed') and i < len(S['dealed']) and S['dealed'][i] == len(S['sorted_packages']) - 1 else None),
    ],
    watch=['v', 'index', ('p', 'p', 'blue'), 'cnt', ('res', 'res', 'green')],
    skip=['box_info = []', 'p += 1', 'dealed[index] = p', 'if dealed[index] >= 0', 'res = -1', 'if res != -1', 'res %= mod', 'm = len', 'n = len', 'mod = ', 'p = -1', 'cost = [0]', 'for index in range(m)', 'for v in boxes', 'box_info.append', 'for package in', 's.append'],
    max_steps=90,
    captions={
        'box_info = sorted': '所有箱子打上供应商编号，按尺寸排序：`{box_info}`',
        'sorted_packages = sorted': '包裹按大小排序：`{sorted_packages}`',
        's = [sorted': '`s` 是包裹的前缀和，用来 O(1) 求一段包裹的总尺寸',
        'dealed = ': '`dealed[k]`：供应商 k 的箱子目前已能装下到第几个包裹（-1 = 还没有）',
        'for v, index in box_info': lambda S, B, r: ('所有箱子都看完了' if B.get('v') == S['v'] and B.get('index') == S['index'] and 'cnt' in S else f"按尺寸从小到大看箱子：尺寸 `v = {S['v']}`，属于供应商 `{S['index']}`"),
        'while p + 1 < n': lambda S, B, r: (f'包裹 `{S.sorted_packages[S.p + 1]} <= {S.v}`：这个箱子装得下它，`p` 前进到 {S.p + 1}（`p` 只增不减，整体 O(n)）' if S.p + 1 < S.n and S.sorted_packages[S.p + 1] <= S.v
                                            else f'下一个包裹放不进尺寸 `{S.v}` 的箱子（或已到头）→ `p = {S.p}`：包裹 `0..{S.p}` 都装得下'),
        'if p > dealed': lambda S, B, r: (f'`p = {S.p} > dealed[{S.index}] = {S.dealed[S.index]}`：有新的包裹归这个箱子' if S.p > S.dealed[S.index]
                                          else f'`p = {S.p}` 没超过 `dealed[{S.index}]`：这个箱子装不到新包裹，跳过'),
        'cnt = p': '包裹 `{dealed[index] + 1}..{p}` 共 `{cnt}` 个，由尺寸 `{v}` 的箱子来装',
        'cost[index] += cnt': lambda S, B, r: f"`cnt × v − s[p]` = `{S.cnt} × {S.v} − {S.s[S.p]}` → `cost[{S.index}] = {S.cost[S.index]}`" + ('（这是该供应商第一批包裹，不用补）' if S.cnt == S.p + 1 else '：减掉的是整段前缀和 `0..p`，多减了前面已算过的部分，下一行补回'),
        'cost[index] += s[': '补回多减的前缀和 `s[{dealed[index]}] = {s[dealed[index]]}`：`cost[{index}]` → =={cost[index]}==（供应商 {index} 现已处理到第 {p} 个包裹）',
        'for index in range(m):': lambda S, B, r: ('供应商都检查完了' if B.get('index') == S['index'] and 'res' in B and B.get('res') == S['res'] and S['index'] == S['m'] - 1 else f"检查供应商 `{S['index']}`"),
        'if dealed[index] == n - 1': lambda S, B, r: (f"`dealed[{S.index}] = {S.dealed[S.index]}`：{'装得下全部包裹' if S.dealed[S.index] == S.n - 1 else '有包裹装不下 → 忽略'}"
                                                      + (f'，浪费 `{S.cost[S.index]}`' + ('，比当前最优更小 → 更新' if (S.res == -1 or S.res > S.cost[S.index]) else '，不比当前最优小') if S.dealed[S.index] == S.n - 1 else '')),
        'res = cost[index]': '最优浪费更新为 `{res}`',
        'res %= mod': '`res % mod = {res}`',
        'return res': '最少浪费空间 `{res}`',
    },
    cards=dict(
        one_liner='每个包裹选刚好装得下的最小箱子，按箱子尺寸扫一遍',
        complexity='时间 `O(n log n + M log M)`，空间 `O(n + M)`',
        problem=['每个箱子装一个包裹，包裹尺寸 ≤ 箱子尺寸才能放入',
                 '选一个供应商（箱子尺寸有若干种、数量无限），使总浪费最小',
                 '示例：包裹 `[3,5,8,10,11,12]`，供应商 `[[12],[11,9],[10,5,14]]` → `9`'],
        quote='为了使浪费的空间最小，很明显就应该选择容量最小的，但大于等于包裹大小的箱子。',
        quote_src='—— yiduobo 题解原文',
        idea=['包裹排序、箱子打上供应商编号后排序；`p` 随箱子变大只增不减',
              '`dealed[k]` 记录供应商 k 已经处理到的包裹，新的一段包裹由当前箱子来装',
              '一段包裹的浪费 = `个数 × 箱子尺寸 − 包裹之和`，和用前缀和求'],
        summary=['时间 `O(n log n + M log M)`，`M` 是箱子总数；空间 `O(n + M)`',
                 '易错：`dealed[index] == n-1` 才说明该供应商装得下最大的包裹',
                 '前缀和相减的写法：`cost += cnt*v − s[p]`，再补 `+ s[dealed]`',
                 '最后才取模：比较大小要用真实值，不要先取模'],
    ),
)
