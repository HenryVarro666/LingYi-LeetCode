def _bin(S, v):
    m = S['m']
    return format(v, f'0{m}b')


def _txt(S):
    if 'f' not in S:
        return ''
    m = S['m']
    if 'x' in S and 'index' in S and 'y' in S:
        return f"`x = {_bin(S, S['x'])}` 翻转第 {S['index']} 位 → `y = {_bin(S, S['y'])}`；`f[y]` 是 y 到 nums 的最短汉明距离"
    return f"`f[v]` = v 到 nums 中最近元素的汉明距离（`m = {m}`）；`None` 表示还没算到"


CONFIG = dict(
    num=3141, title='最大汉明距离', difficulty='Hard', category='位运算',
    author='yiduobo', technique='多源 BFS · 补码转最小距离',
    tags=['灵神题单·位运算', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def maxHammingDistances(self, nums, m):

        f = [None] * (1 << m)
        q = list(set(nums))
        for v in nums:
            f[v] = 0
        
        head, tail = 0, len(q)
        while head < tail:
            for x in q[head : tail]:
                for index in range(m):
                    y = x ^ (1 << index)
                    if f[y] is None:
                        f[y] = f[x] + 1
                        q.append(y)

            head, tail = tail, len(q)
        
        return [m - f[(1 << m) - 1 - v] for v in nums]
''',
    call='Solution().maxHammingDistances([1, 2], 2)',
    expect=[2, 2],
    views=[
        dict(type='array', var='f', label='f[v]：v 到 nums 的最短汉明距离（下标 = v）', h=200,
             color=lambda S, i, v: ('yellow' if i in S.get('nums', ()) else 'green' if (v is not None and 'y' in S and i == S['y']) else None),
             pointers={'x': 'blue', 'y': 'pink'}),
        dict(type='array', var='q', label='q：BFS 队列', h=160, pointers={}),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('x', 'x', 'cyan'), ('y', 'y', 'orange')],
    captions={
        'f = [None]': '`f[v]` 记录 v 到 nums 里最近元素的汉明距离，共 `2^m = {len(f)}` 个数，先全是 `None`',
        'q = list': '队列起点是 nums 去重后的元素：`q = {q}`',
        'f[v] = 0': 'nums 里的数自己到自己距离 0：`f[{v}] = 0`（BFS 多个起点）',
        'head, tail = 0': '`q[head:tail]` 是当前这一层，初始就是所有起点',
        'while head < tail': lambda S, B, r: (f'这一层还有节点（`head={S.head} < tail={S.tail}`），继续扩展' if S.head < S.tail else '没有新节点了，BFS 结束'),
        'for x in q': '处理这一层的 `x = {x}`（二进制 `{x:0{m}b}`）',
        'y = x ^': '翻转 `x` 的第 `{index}` 位，得到相邻整数 `y = {y}`（汉明距离 1）',
        'if f[y] is None': lambda S, B, r: (f'`f[{S.y}]` 还没算过 → 它是第一次被走到，距离最短' if S.f[S.y] is None else f'`f[{S.y}] = {S.f[S.y]}` 已经有更短或相等的距离，跳过'),
        'f[y] = f[x] + 1': '`f[{y}] = f[{x}] + 1 = {f[y]}`，入队等待扩展',
        'head, tail = tail': '这一层处理完，下一层是 `q[{head}:{tail}]`',
        'return [m': lambda S, B, r: f'`v` 的补码是 `{(1 << S.m) - 1} - v`，答案 = `m - f[补码]`：得到 =={r}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='最远 = m − 补码到最近元素的距离，用多源 BFS 求最近',
        complexity='时间 `O(m·2^m)`，空间 `O(2^m)`',
        problem=['`nums` 每个元素在 `0 ~ 2^m-1` 之间，求每个 `nums[i]` 与其他元素的最大汉明距离',
                 '汉明距离 = 两数二进制不同位的个数',
                 '示例：`nums=[1,2], m=2` → `[2,2]`'],
        quote='与v汉明距离最大的整数就是v的补码，即2^m - 1 - v，二者的二进制位上全都不同，因此汉明距离为m。',
        quote_src='—— yiduobo 题解原文',
        idea=['把整数当节点，只差一位的连边，最短路 = 汉明距离',
              '要找「最远」：v 与 u 的距离 = `m −` (v 的补码与 u 的距离)',
              '于是最远 = `m −` 补码到 nums 的最近距离：用 nums 做多源 BFS 填 `f`'],
        summary=['时间 `O(m·2^m)`，空间 `O(2^m)`',
                 '`f` 下标就是整数本身，大小 `2^m`',
                 '`q[head:tail]` 分层 BFS：同层距离相同，下一层距离 +1',
                 '答案用补码下标：`(1 << m) - 1 - v`，不要写成 `-v`',
                 '原文可直接在 Python 3 运行，无需修改'],
    ),
)
