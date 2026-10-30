CONFIG = dict(
    num=3109, title='查找排列的索引', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='康托展开 + 树状数组', tags=['常用数据结构'],
    code='''
class Solution(object):
    def getPermutationIndex(self, perm):
        
        fac = [1]
        mod = 10 ** 9 + 7
        n = len(perm)
        for index in range(1, n):
            fac.append(fac[-1] * index % mod)

        f = [0] * (n + 1)

        def add(x, delta):
            while x <= n:
                f[x] += delta
                x += x & -x
        
        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n + 1):
            add(index, 1)
        
        res = 0
        for index, v in enumerate(perm[:n - 1]):
            res = (res + get(v - 1) * fac[n - 1 - index]) % mod
            add(v, -1)
        
        return res
''',
    call='Solution().getPermutationIndex([3,1,2])',
    expect=4,
    views=[
        dict(type='array', var='perm', pointers={'index if index < len(perm) else None': 'blue'}, label='perm（index 指向正在确定的位置）', h=170),
        dict(type='array', var='fac', label='fac：fac[i] = i!', h=150),
        dict(type='array', var='f', label='树状数组 f（下标 0 不用）：f[x] 管 x 往前 lowbit(x) 个数', pointers={'x if 0 < x < len(f) else None': 'pink'}, h=190),
        dict(type='text', h=70, fn=lambda S: f"康托展开：排名 = Σ ==后面比 v 小的个数== × (剩余位数)! ，累计 `res` = =={S['res']}==" if 'res' in S else '先备好阶乘，再让树状数组里每个数都记 1（表示“还没用过”）'),
    ],
    watch=['index', 'v', 'x', ('res', 'res', 'green')],
    captions={
        'fac.append': '`fac` 追加 `{index}!`：`fac[{index}] = {fac[-1]}`',
        'f = [0]': '建树状数组 `f`，下标 1..n，初始全 0',
        'f[x] += delta': '`f[{x}]` 加上 `{delta}` → {f[x]}（x 这一格负责一段区间）',
        'x += x & -x': '`x += lowbit(x)`：跳到管着它的上一格 → `{x}`',
        's += f[x]': '累加 `f[{x}]` → `s` = {s}',
        'x -= x & -x': '`x -= lowbit(x)`：去掉最低位，跳到下一段 → `{x}`',
        'return s': '前缀和 `get` 返回 =={s}==：1..x 中还没用过的数有 {s} 个',
        'for index in range(1, n + 1)': '把 1..n 逐个 `add(index, 1)`：表示每个数都还没被用掉',
        'for index, v in enumerate': '处理第 `{index}` 位，`v = {v}`',
        'res = (res': '后面比 `{v}` 小的个数 = `get({v}-1)`（先去树状数组查），再乘 `fac[{n-1-index}]` = {fac[n-1-index]}，累加进 `res`',
        'add(v, -1)': '`{v}` 已经放在前面，从树状数组里删掉：`add({v}, -1)`',
        'return res': '排名（从 0 开始）是 =={res}==',
    },
    skip=['mod = ', 'n = len'],
    max_steps=110,
    cards=dict(
        one_liner='康托展开：每一位数「后面有几个比它小」乘阶乘，用树状数组数个数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一个 1..n 的排列 `perm`，求它在所有排列的字典序中排第几（从 0 开始），结果对 `10^9+7` 取模',
                 '示例：`[3,1,2]` → `10`'],
        quote='对于当前遍历到的perm[index]，首先找出后续有多少个元素小于perm[index]，不妨记为k，那么此时就只需将k * (n - index - 1)!累加到答案中',
        quote_src='—— yiduobo 题解原文',
        idea=['以更小的数开头的排列都排在前面，每个有 `(剩余位数)!` 个',
              '“后面比 v 小的个数” = 还没用过且小于 v 的数 → 前缀和',
              '用过的数 `add(v, -1)` 删除，动态前缀和交给树状数组'],
        summary=['时间 `O(n log n)`，阶乘取模预处理 `O(n)`',
                 '`get(v - 1)` 统计的是“还没用过且比 v 小”的数，不是整个数组里小的',
                 '最后一位恒为 0，所以只枚举 `perm[:n-1]`',
                 '`fac` 每步取模，防止溢出；排名从 0 开始'],
    ),
)
