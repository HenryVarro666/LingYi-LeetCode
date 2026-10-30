def _done(S):
    r = S.get('res')
    return sum(len(x) for x in r) if r else 0


CONFIG = dict(
    num=2022, title='将一维数组转变成二维数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 行计数器 p',
    tags=[],
    code='''
class Solution(object):
    def construct2DArray(self, original, m, n):

        res = []
        if len(original) != m * n:
            return res

        p = 0
        for num in original:
            if p == 0:
                res.append([])
            res[-1].append(num)
            p += 1
            if p == n:
                p = 0
        
        return res
''',
    call='Solution().construct2DArray([1, 2, 3, 4, 5, 6], 2, 3)',
    expect=[[1, 2, 3], [4, 5, 6]],
    views=[
        dict(type='text', fn=lambda S: f"`m = {S['m']}`，`n = {S['n']}`：需要 `{S['m']} × {S['n']} = {S['m'] * S['n']}` 个数，`original` 有 `{len(S['original'])}` 个" + (f"　当前行已填 `p = {S['p']}` 个" if 'p' in S else ''), size=26, h=60),
        dict(type='array', var='original', label='original（绿 = 已放进 res）', cell=90, h=190,
             color=lambda S, i, v: 'green' if i < _done(S) else None),
        dict(type='grid', var='res', label='res（每行最多 n 个，黄框 = 刚放入）', cell=90, h=260),
    ],
    watch=['p', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 是答案矩阵，一开始没有任何一行',
        'if len(original) != m * n': '元素个数 `{len(original)}` 对 `m * n = {m * n}`：' + '必须==恰好相等==，多了少了都铺不满',
        'return res': lambda S, B, r: ('个数对不上，返回空数组 `[]`' if S.get('p') is None else f'全部放完，返回 `{r}`'),
        'p = 0': '`p` 是当前行已经填了几个数，从 0 开始',
        'for num in original': '取出下一个数 `num = {num}`',
        'if p == 0': lambda S, B, r: ('`p == 0`：当前行是空的，说明这个数要==另起一行==' if S.p == 0 else f'`p = {S.p}`：当前行还没填满，接着往这一行放'),
        'res.append([])': '`res` 末尾新开一行，现在有 `{len(res)}` 行',
        'res[-1].append(num)': '把 `{num}` 放到==最后一行==的末尾：`{res[-1]}`',
        'p += 1': '这一行又多了一个数：`p = {p}`',
        'if p == n': lambda S, B, r: (f'`p = {S.p}` 等于 `n = {S.n}`：这一行填满了' if S.p == S.n else f'`p = {S.p}` < `n = {S.n}`：这一行还没满'),
        'p = 0': lambda S, B, r: '行满了，`p` 清零，下一个数会另起一行' if 'num' in S else '`p = 0`：`p` 是当前行已经填了几个数',
    },
    skip=[],
    cards=dict(
        one_liner='一趟遍历：行满了就另起一行',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计答案）',
        problem=['把长度为 `len` 的一维数组 `original`，按行优先填成 `m` 行 `n` 列的二维数组',
                 '元素个数不等于 `m * n` 时无法构成，返回空数组',
                 '示例：`[1,2,3,4,5,6]`，`m=2, n=3` → `[[1,2,3],[4,5,6]]`'],
        quote='首先判断original的长度是否等于m * n，若不等于，说明无法转换，直接返回空。……使用一个行计数器p计算当前行已经填充了多少个数……当p等于n时，则在答案矩阵中另起一行，并将p置为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先判长度：`len(original) != m * n` 就直接返回空',
              '行计数器 `p`：`p == 0` 时先给 `res` 追加一个空行',
              '每个数放进 `res[-1]`，`p` 加一；`p == n` 就清零，下一个数换行'],
        summary=['时间 `O(mn)`，空间 `O(1)`（答案不计）',
                 '易错：必须==先判长度==，否则会得到最后一行不满的矩阵',
                 '作者提到 Python 也有内置的转换方式，这里手写了一遍计数器',
                 '原文已是 Python 3 可运行写法，仅删去了类型说明文档字符串'],
    ),
)
