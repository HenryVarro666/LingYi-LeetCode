def _fa_view(S):
    fa = S.get('fa')
    if not isinstance(fa, dict):
        return None
    return {k: fa[k] for k in sorted(fa)}


CONFIG = dict(
    num=952, title='按公因数计算最大组件', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='筛素数 + 并查集（按素因子合并）',
    tags=['常用数据结构', '数学算法'],
    code='''
class Solution(object):
    def largestComponentSize(self, A):

        fa = {1 : 1}
        max_num = 0
        for num in A:
            max_num = max(max_num, num)
            fa[num] = num

        prime = [True] * (max_num + 1)
        
        now = 2
        while now <= max_num:
            if prime[now]:
                if now not in fa:
                    fa[now] = now
                tmp = now + now
                while tmp <= max_num:
                    prime[tmp] = False
                    if tmp in fa:
                        self.union(now, tmp, fa)
                    tmp += now
            
            if now == 2:
                now = 3
            else:
                now += 2
        
        fa_cnt = {}
        for num in A:
            now_fa = self.get(num, fa)
            fa_cnt[now_fa] = fa_cnt.get(now_fa, 0) + 1

        return max(fa_cnt.values())
    
    def get(self, now, fa):
        if now != fa[now]:
            fa[now] = self.get(fa[now], fa)
        
        return fa[now]
    
    def union(self, x, y, fa):
        fa_x = self.get(x, fa)
        fa_y = self.get(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
''',
    call='Solution().largestComponentSize([6,10,15,7])',
    expect=3,
    views=[
        dict(type='array', var='A', label='A（原数组）', h=130, cell=70,
             color=lambda S, i, v: 'yellow' if 'num' in S and S.get('_line', 0) in (7, 8, 31, 32) and v == S['num'] else None),
        dict(type='array', var='prime', label='prime（黄 = 当前素数 now，粉 = 正在划掉的倍数 tmp）', h=190, cell=48,
             pointers={'now': 'yellow', 'tmp if tmp <= max_num and _line in (18, 19, 20, 21) else None': 'pink'},
             pointer_labels={'tmp if tmp <= max_num and _line in (18, 19, 20, 21) else None': 'tmp'}, dim=lambda S, i, v: i < 2 or not v),
        dict(type='map', var=_fa_view, label='fa：数 → 父亲（父亲相同 = 同一组件）', h=210, font=24,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='map', var='fa_cnt', label='fa_cnt：每个根下有几个数', h=110, font=24),
    ],
    watch=[('now', 'now', 'yellow'), ('tmp', 'tmp', 'pink'), ('max_num', 'max_num', 'green')],
    captions={
        'fa = {1': '并查集用字典：`fa[x]` 是 `x` 的父亲，先放一个 `1`',
        'max_num = max': '`max_num = {max_num}`：筛到最大的数就够了',
        'fa[num] = num': '`{num}` 先自成一组：`fa[{num}] = {num}`',
        'prime = [True]': '`max_num = {max_num}`：筛到最大的数就够了；`prime[i]` 记录 `i` 是否还是素数',
        'now = 2': '从素数 `2` 开始枚举',
        'while now <= max_num': lambda S, B, r: (f'`now = {S.now}` ≤ `{S.max_num}`，继续' if S.now <= S.max_num else f'`now = {S.now}` > `{S.max_num}`：素数枚举完毕'),
        'if prime[now]': lambda S, B, r: (f'`{S.now}` 还是素数 → 它的倍数都有公因数 `{S.now}`，要并到一起' if S.prime[S.now] else f'`{S.now}` 已被划掉，是合数，跳过'),
        'if now not in fa': lambda S, B, r: (f'`{S.now}` 不在数组里，先给它一个节点作为这一族的“父亲”' if S.now not in S.fa else f'`{S.now}` 自己就在数组里，直接当这一族的父亲'),
        'fa[now] = now': '`fa[{now}] = {now}`：素数自己当根',
        'tmp = now + now': '从 `2×{now} = {tmp}` 开始枚举 `{now}` 的倍数',
        'while tmp <= max_num': lambda S, B, r: (f'`{S.now}` 的倍数 `tmp = {S.tmp}` ≤ `{S.max_num}`：它是合数，下一步划掉' if S.tmp <= S.max_num else f'`{S.now}` 的倍数枚举完了'),
        'prime[tmp] = False': '`{tmp}` 是 `{now}` 的倍数 → 合数，划掉',
        'if tmp in fa': lambda S, B, r: (f'`{S.tmp}` 在数组里 → 和素数 `{S.now}` 合并' if S.tmp in S.fa else f'`{S.tmp}` 不在数组里，只划掉不合并'),
        'self.union(now, tmp, fa)': '合并 `{now}` 与 `{tmp}`：先各自找根（`get` 顺带路径压缩），根小的当新根',
        'if now == 2': '素数只需检查 2 和奇数：2 之后直接跳到 3，再每次加 2',
        'fa_cnt = {}': '合并结束，开始统计每个组件有多少个数',
        'now_fa = self.get': '`{num}` 所在组件的根是谁？',
        'fa_cnt[now_fa] =': '`fa_cnt[{now_fa}]` 加一 → `{fa_cnt[now_fa]}`',
        'return max(fa_cnt': '最大组件有 `{ret}` 个数',
        'if now != fa[now]': lambda S, B, r: (f'`{S.now}` 的父亲是 `{S.fa[S.now]}` ≠ 自己：继续往上找' if S.now != S.fa[S.now] else f'`{S.now}` 的父亲是自己：它就是根'),
        'fa[now] = self.get': '路径压缩：`fa[{now}]` 直接指向根',
        'fa_x = self.get': '先找 `x` 的根',
        'fa_y = self.get': '再找 `y` 的根',
        'if fa_x < fa_y': lambda S, B, r: (f'根 `{S.fa_x}` < `{S.fa_y}`：把大根 `{S.fa_y}` 挂到小根 `{S.fa_x}` 下' if S.fa_x < S.fa_y else f'根 `{S.fa_x}` ≥ `{S.fa_y}`：把 `{S.fa_x}` 挂到 `{S.fa_y}` 下（相等时自挂自，无影响）'),
        'fa[fa_y] = fa_x': '`fa[{fa_y}] = {fa_x}`',
        'fa[fa_x] = fa_y': '`fa[{fa_x}] = {fa_y}`',
    },
    skip=['tmp += now', 'now += 2', 'now = 3', 'return fa[now]', 'fa[num] = num', 'if now != fa[now]', 'fa[now] = self.get', 'fa_x = self.get', 'fa_y = self.get', 'fa[now] = now', 'if now == 2', 'now = 2', 'prime[tmp] = False', 'max_num = max', 'for num in A', 'tmp = now + now'],
    max_steps=130,
    cards=dict(
        one_liner='有公共素因子才连边：按素数把它的倍数并到一起',
        complexity='时间 `O(M log log M · α)`，空间 `O(M)`',
        problem=['数组 `A` 里的数互不相同；两数有大于 1 的公因数就连一条边',
                 '求最大连通组件的大小',
                 '示例：`[6,10,15,7]` → `3`（`6,10,15` 连成一组，`7` 单独一组）'],
        quote='设当前处理到x的某个倍数y，若y当前没有父亲，则设y的父亲为x，否则将y与x的父亲进行合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['两两求 gcd 要 `O(n^2)`，`n` 最多 20000，吃不消',
              '有大于 1 的公因数 ⇔ 有公共素因子：把「素数 x 的所有倍数」并成一组',
              '筛法逐个枚举素数 `x`，把 `x` 的倍数合并进同一棵树',
              '最后统计每个数的根出现的次数，取最大'],
        summary=['时间约 `O(M log log M)`（M = 最大值），空间 `O(M)`',
                 '易错点：素数本身可能不在 `A` 里，要先给它建节点再合并',
                 '`1` 在 `fa` 里预置，但不会与别的数相连',
                 '原文是 Python 2 风格代码；本题语法无需改动，可直接在 Python 3 运行'],
    ),
)
