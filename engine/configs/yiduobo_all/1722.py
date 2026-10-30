def _groups(S):
    f = S.get('f')
    if not f:
        return ''
    def root(c):
        while f[c] != c:
            c = f[c]
        return c
    g = {}
    for i in range(len(f)):
        g.setdefault(root(i), []).append(i)
    return '可互换的位置组（代表元：成员）  ' + '　'.join(f"[{r}: {','.join(map(str, m))}]" for r, m in sorted(g.items()))


CONFIG = dict(
    num=1722, title='执行交换操作后的最小汉明距离', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集分组 + 计数匹配',
    tags=['灵神题单', '难度分 1892'],
    code='''
class Solution(object):
    def minimumHammingDistance(self, source, target, allowedSwaps):

        n = len(source)
        f = list(range(n))
        for x, y in allowedSwaps:
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    f[fa_y] = fa_x
                else:
                    f[fa_x] = fa_y
        
        part_dict = {}
        for index in range(n):
            fa = self.find(index, f)
            if fa not in part_dict:
                part_dict[fa] = {}
            part_dict[fa][source[index]] = part_dict[fa].get(source[index], 0) + 1

        res = 0
        print(target)
        for index in range(n):
            fa = self.find(index, f)
            if part_dict[fa].get(target[index], 0) > 0:
                part_dict[fa][target[index]] -= 1
            else:
                res += 1
        
        return res
        
    def find(self, x, f):
        if f[x] != x:
            f[x] = self.find(f[x], f)
        return f[x]
''',
    call='Solution().minimumHammingDistance([1,2,3,4,5], [3,1,1,5,5], [[0,1],[1,2],[3,4]])',
    expect=2,
    views=[
        dict(type='array', var='source', label='source（蓝箭头 = 当前下标）', pointers={'index': 'blue'}, h=190),
        dict(type='array', var='target', label='target', h=130),
        dict(type='text', fn=_groups, size=22, h=70),
        dict(type='map', var='part_dict', label='part_dict：组 → {source 中的数字: 剩余个数}', h=130, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', lambda S: S.get('index'), 'blue'), ('fa', lambda S: S.get('fa'), 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len(source)': '`n = {n}`：每个位置是图中的一个点',
        'f = list(range(n))': '并查集 `f[i] = i`：每个位置先自成一组',
        'fa_x = self.find': '找 `{x}` 的代表元',
        'fa_y = self.find': '找 `{y}` 的代表元',
        'if fa_x != fa_y': lambda S, B, r: (f'代表元 {S.fa_x} ≠ {S.fa_y} → 这两个位置还没连通，要合并' if S.fa_x != S.fa_y else f'代表元相同（{S.fa_x}）→ 早已连通'),
        'if fa_x < fa_y': lambda S, B, r: (f'`{S.fa_x} < {S.fa_y}`：编号大的并到小的下面' if S.fa_x < S.fa_y else f'`{S.fa_x} > {S.fa_y}`：编号大的并到小的下面'),
        'f[fa_y] = fa_x': '`f[{fa_y}] = {fa_x}`：两组合并',
        'f[fa_x] = fa_y': '`f[{fa_x}] = {fa_y}`：两组合并',
        'part_dict = {}': '`part_dict[组][数字]`：统计每组位置上 ==source== 里各数字出现几次',
        'for index in range(n)': lambda S, B, r: (f'位置 `{S.index}`' if B.get('index') != S.index else '统计 / 匹配完毕'),
        'fa = self.find(index': '位置 `{index}` 属于哪一组？调用 `find` 求它的代表元',
        'if fa not in part_dict': lambda S, B, r: (f'组 {S.fa} 还没有计数表 → 新建一个' if S.fa not in S.part_dict else f'组 {S.fa} 已有计数表，直接累加'),
        'part_dict[fa] = {}': '为组 `{fa}` 建空计数表',
        'part_dict[fa][source[index]]': '`source[{index}] = {source[index]}` 计入组 `{fa}`：`{part_dict[fa]}`',
        'res = 0': '`res` 统计 target 里 ==配不上== 的位置数',
        'print(target)': '（原文的调试输出，不影响结果）',
        'if part_dict[fa].get': lambda S, B, r: (f'`target[{S.index}] = {S.target[S.index]}`：组 {S.fa} 里还有 {S.part_dict[S.fa].get(S.target[S.index], 0)} 个 → 能配上' if S.part_dict[S.fa].get(S.target[S.index], 0) > 0 else f'`target[{S.index}] = {S.target[S.index]}`：组 {S.fa} 里已经没有这个数 → 配不上'),
        'part_dict[fa][target[index]] -= 1': '用掉一个：`part_dict[{fa}] = {part_dict[fa]}`',
        'res += 1': '这个位置无论怎么交换都对不上，汉明距离 +1：`res = {res}`',
        'return res': '最小汉明距离 `{res}`',
    },
    cards=dict(
        one_liner='互通的位置随意排，数数 source 的数字还能配上多少 target',
        complexity='时间 `O((n + m) α(n))`，空间 `O(n)`',
        problem=['可以对 `source` 任意次交换 `allowedSwaps` 中指定的下标对',
                 '返回交换后 `source` 与 `target` 的最小汉明距离（对应位置不同的个数）',
                 '本视频：`[1,2,3,4,5]`、`[3,1,1,5,5]`，边 `[0,1],[1,2],[3,4]` → `2`'],
        quote='由于可以执行任意次数的交换，那么对于一组互相之间可以交换的位置而言，就可以按意愿任意排布这些位置上的数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['并查集找出所有可以互换的位置，分成若干组',
              '统计每组位置上 `source` 的数字各出现几次',
              '再扫 `target`：本组还有这个数就用掉一个，否则这个位置 `+1` 距离'],
        summary=['时间近似 `O(n + m)`，空间 `O(n)`',
                 '原文是 Python 2 写法：`f = range(n)` 已改为 `list(range(n))`，`print target` 已改为 `print(target)`',
                 '`part_dict` 用「用掉一个就减 1」代替灵神的正负抵消，要保证每组独立计数',
                 '对比灵神：灵神 DFS + `diff` 求对称差再 `// 2`；yiduobo 先数 source、再逐个匹配 target'],
    ),
)
