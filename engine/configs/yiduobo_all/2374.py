CONFIG = dict(
    num=2374, title='边积分最高的节点', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='数组累加积分 · 再扫一遍取最大',
    tags=[],
    code='''
class Solution(object):
    def edgeScore(self, edges):

        n = len(edges)
        scores = [0] * n
        for x, y in enumerate(edges):
            scores[y] += x
        
        res = 0
        ma = scores[0]
        for x in range(1, n):
            if scores[x] > ma:
                res = x
                ma = scores[x]
        
        return res
''',
    call='Solution().edgeScore([1,0,0,0,0,7,7,5])',
    expect=7,
    views=[
        dict(type='array', var='edges', label='edges（边 x → edges[x]）', pointers={'x': 'blue'}, h=190),
        dict(type='array', var='scores', label='scores（粉 = 刚加分的节点，绿 = 当前最大）', pointers={'y': 'pink', 'res': 'green'}, h=230),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green'), 'ma'],
    captions={
        'n = len': '`n = {n}` 个节点，也是 `n` 条边',
        'scores = [0]': '`scores[i]` 记录节点 i 的积分，初始都是 0',
        'scores[y] += x': '边 `({x}, {y})`：把 `x = {x}` 累加到 `scores[{y}]` → =={scores[y]}==',
        'res = 0': '积分累加完毕。再从头找最大值：先假设答案是节点 0',
        'ma = scores[0]': '`ma` 是目前最大积分 `{ma}`',
        'if scores[x] > ma': lambda S, B, r: (f'`scores[{S.x}] = {S.scores[S.x]} > ma = {S.ma}` → 更新' if S.scores[S.x] > S.ma
                                              else f'`scores[{S.x}] = {S.scores[S.x]} <= ma = {S.ma}` → 不更新（相等也不换，保证编号小）'),
        'res = x': '`res = {res}`',
        'ma = scores[x]': '`ma = {ma}`',
        'return res': '最大积分对应的节点是 `{res}`',
    },
    cards=dict(
        one_liner='遍历每条边累加积分，再取最大积分的节点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个节点恰有一条出边 `i → edges[i]`',
                 '节点的边积分 = 指向它的所有节点的编号之和',
                 '求积分最高的节点，相同取编号最小；示例 `[1,0,0,0,0,7,7,5]` → `7`'],
        quote='对于边(x, y)，按照题目中对积分的定义就应该是将x累加到score[y]当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟遍历所有边，`scores[y] += x`',
              '再一趟从小到大扫节点，只有严格更大才更新',
              '严格大于，自然让相同积分时编号最小的留下'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：第二趟要用严格 `>`，否则相同积分会取到编号更大的',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
