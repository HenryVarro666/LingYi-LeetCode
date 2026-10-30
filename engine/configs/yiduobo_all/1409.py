def _keep(name):
    last = [None]

    def f(S):
        v = S.get(name)
        if isinstance(v, (list, tuple, str)):
            last[0] = v
        return last[0]
    return f


CONFIG = dict(
    num=1409, title='查询带键的排列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='树状数组 · 用更小的下标模拟移到队首',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def processQueries(self, queries, m):

        n = len(queries)
        maxn = m + n
        suffix_array = [0] * (maxn + 1)
        now = [0] * m
        for index in range(m):
            now[index] = n + index + 1
            self.add(now[index], 1, suffix_array, maxn)
            
        res = []
        for index, pos in enumerate(queries):
            pos -= 1
            self.add(now[pos], -1, suffix_array, maxn)
            res.append(self.sum(now[pos], suffix_array))
            now[pos] = n - index
            self.add(now[pos], 1, suffix_array, maxn)
        
        return res

    def add(self, x, delta, suffix_array, maxn):
        while x <= maxn:
            suffix_array[x] += delta
            x += x & -x
        
    def sum(self, x, suffix_array):
        res = 0
        while x:
            res += suffix_array[x]
            x -= x& -x
        
        return res
''',
    call='Solution().processQueries([3,1], 4)',
    expect=[2, 1],
    views=[
        dict(type='array', var='now', label='now[k]：元素 k+1 当前的树状数组下标（越小越靠前）', cell=90, h=190,
             pointers={'pos': 'pink'},
             color=lambda S, i, v: 'pink' if S.get('pos') == i and S.get('_inner', {}).get('pos') is not None else None),
        dict(type='array', var='suffix_array', label='树状数组（下标 1..m+n，值 = 管辖区间内的元素个数）', cell=70, h=230,
             pointers={'x': 'blue'}),
        dict(type='array', var=_keep('res'), label='res（每次查询的答案）', cell=80, h=170),
    ],
    skip=['while x <= maxn', 'while x:', 'suffix_array = [0]', 'now = [0]', 'n = len', 'res = []', 'res = 0', 'x += x & -x', 'x -= x& -x'],
    max_steps=90,
    watch=[('pos', 'pos', 'pink'), ('x', 'x', 'blue'), ('delta', 'delta', 'orange'), ('res', 'res', 'green')],
    captions={
        'maxn = m + n': '下标要 `>0`：前面留出 `n` 个位置给“移到队首”用，总长 `maxn = {maxn}`',
        'now[index] = n + index + 1': '元素 {index+1} 的初始下标放在 `{now[index]}`，整体后移 `n`，给前移留空间',
        'self.add(now[index], 1': '把下标 `{now[index]}` 在树状数组里记 `+1`（这里有个元素）',
        'pos -= 1': '题目的值是 1 开始，转成 `now` 的下标：`pos = {pos}`',
        'self.add(now[pos], -1': '先把它自己从树状数组里拿掉（`-1`），免得查询时数到自己',
        'res.append': '答案 = 下标比 `now[pos] = {now[pos]}` 更小的元素个数 = 前缀和 `sum({now[pos]})`，去树状数组里查',
        'now[pos] = n - index': '“移到队首”只要换成更小的下标：`now[pos] = n - index = {now[pos]}`，比之前所有下标都小',
        'suffix_array[x] += delta': '树状数组节点 `{x}` 的计数 `{"+" if delta > 0 else "-"}1` → {suffix_array[x]}，随后 `x` 跳到 `x + lowbit(x)`',
        'res += suffix_array[x]': '前缀和累加节点 `{x}` 管辖的个数 `{suffix_array[x]}` → `res = {res}`，随后 `x` 去掉最低位',
        'return res': lambda S, B, r: (f'前缀和 = `{r}`：下标更小的元素有 {r} 个' if 'x' in S['_inner'] else f'全部查询完毕：`{r}`'),
    },
    cards=dict(
        one_liner='不真的移动元素，只给它换一个更小的下标',
        complexity='时间 `O((m+n) log(m+n))`，空间 `O(m+n)`',
        problem=['排列 `P = [1..m]`，对每个 `queries[i]`：找到它在 `P` 中的位置，作为答案，再把它移到 `P` 的最前面',
                 '示例：`queries = [3,1,2,1], m = 5` → `[2,1,2,1]`',
                 '本视频：`queries = [3,1], m = 4` → `[2,1]`'],
        quote='题目要求元素在数组中的位置，那么实际上就是要求数组中有多少元素的下标小于指定元素的下标。由于这里我们并不在意下标的绝对值，而只需要知道其相对值，因此我们在移动元素时可以通过指定更小的下标来达到移动的目的。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接模拟每次移动要搬 `O(n)` 个元素，总共 `O(n^2)`',
              '位置 = 下标比它小的元素个数 → 树状数组做前缀和',
              '移到队首 = 把下标改成比所有现存下标都小的数，下标整体后移 `n` 避免出现负数'],
        summary=['时间 `O((m+n) log(m+n))`，空间 `O(m+n)`',
                 '易错：查询前要先把自己从树状数组里删掉，再数前缀和',
                 '易错：树状数组下标必须是正数，所以初始下标整体偏移 `n`',
                 '第 `index` 次的新下标是 `n - index`，严格递减，永远排在最前',
                 '原文本身可直接在 Python 3 运行，没有改动'],
    ),
)
