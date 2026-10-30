S0 = 'ABB'
QS = [[2, 0, 2], [1, 2], [2, 0, 2]]


def _bs(S):
    b = S.get('b')
    return b


def _txt(S):
    q = S.get('q')
    if q is None:
        return '树状数组 `f[v][x]`：前 `x` 个位置里，“`v` 后面紧跟 `1-v`”的相邻对数（0 = A，1 = B）'
    if q[0] == 1:
        return f'翻转下标 `{q[1]}`：它和左右邻居形成的相邻对都要更新'
    if 'ma' in S and 'v' in S:
        return f"查询 `[{q[1]}, {q[2]}]`：枚举以 `v = {S['v']}` 开头的交替串，`ma` = 当前最长保留长度 `{S['ma']}`"
    return f'查询 `[{q[1]}, {q[2]}]`：最少删除 = 长度 − 最长能保留的交替子序列'


CONFIG = dict(
    num=3777, title='使子字符串变交替的最少删除次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按相邻对计数 · 两棵树状数组',
    tags=['灵神题单', '常用数据结构', '难度分 2202'],
    code='''
class Solution(object):
    def minDeletions(self, s, queries):
        
        n = len(s)
        b = [ord(c) - 65 for c in s]

        f = [[0] * (n + 1) for _ in range(2)]

        def add(x, delta, v):
            while x <= n:
                f[v][x] += delta
                x += x & -x
        
        def get(x, v):
            cnt = 0
            while x:
                cnt += f[v][x]
                x -= x & -x
            return cnt

        for index in range(1, n):
            if b[index] != b[index - 1]:
                add(index, 1, b[index - 1])

        res = []
        for q in queries:
            if q[0] == 2:
                left, right = q[1], q[2]
                
                ma = 0
                for v in range(2):
                    pair = get(right, v) - get(left, v)
                    if left > 0 and b[left - 1] == v and b[left] == 1 - v:
                        pair -= 1
                    length = pair + pair
                    if b[right] == v:
                        length += 1
                    ma = max(ma, length)

                res.append(right - left + 1 - ma)
            
            else:
                p = q[1]
                if p > 0:
                    if b[p - 1] != b[p]:
                        add(p, -1, b[p - 1])
                    else:
                        add(p, 1, b[p - 1])

                if p + 1 < n:
                    if b[p] != b[p + 1]:
                        add(p + 1, -1, b[p])
                    else:
                        add(p + 1, 1, 1 - b[p])
                
                b[p] ^= 1

        return res
''',
    call=f'Solution().minDeletions({S0!r}, {QS})',
    expect=[1, 0],
    views=[
        dict(type='text', fn=_txt, h=80, size=26),
        dict(type='array', var='b', label='b（A = 0，B = 1）', cell=84, h=220,
             color=lambda S, i, v: 'cyan' if v == 0 else 'purple',
             pointers={'left': 'green', 'right': 'orange', 'p': 'pink'}),
        dict(type='array', var=lambda S: S['f'][0] if 'f' in S else None, label='f[0]：A 后面紧跟 B 的相邻对（树状数组）', cell=84, h=175),
        dict(type='array', var=lambda S: S['f'][1] if 'f' in S else None, label='f[1]：B 后面紧跟 A 的相邻对（树状数组）', cell=84, h=175),
        dict(type='array', var='res', label='res', cell=84, h=130),
    ],
    watch=[('x', 'x', 'blue'), ('v', 'v', 'purple'), ('pair', 'pair', 'orange'), ('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    skip=['n = len(s)', 'res = []', 'cnt = 0', 'while x', 'x += x & -x', 'x -= x & -x', 'for q in queries', 'def ', 'f = [[0]', 'left, right = q[1], q[2]', 'ma = 0', 'else:'],
    max_steps=90,
    captions={
        'b = [ord(c)': '`A` → 0，`B` → 1：这样 `f[v]` 的 `v` 可以直接用数值当下标',
        'if b[index] != b[index - 1]': lambda S, B, r: (f'`b[{B.index-1}]={B.b[B.index-1]}`、`b[{B.index}]={B.b[B.index]}`：' + ('不同 → 是一个相邻对，记到位置 `%d`' % B.index if B.b[B.index] != B.b[B.index-1] else '相同 → 不是交替对，跳过')),
        'add(index, 1, b[index - 1])': '位置 `{index}` 有一个“`{b[index-1]}` 后接 `{1-b[index-1]}`”的对：`f[{b[index-1]}]` 的 `{index}` 加 1',
        'f[v][x] += delta': '`f[{v}]` 的节点 `{B.x}` 加 `{delta}` → {f[v][B.x]}，随后 `x` 跳到 `x + lowbit(x)`',
        'cnt += f[v][x]': '前缀和累加 `f[{v}]` 的节点 `{B.x}` = `{f[v][B.x]}` → `cnt = {cnt}`，随后 `x` 去掉最低位',
        'return cnt': lambda S, B, r: f'`f[{S.v}]` 的前缀和 = `{r}`',
        'if q[0] == 2': lambda S, B, r: (f'`q = {B.q}`：类型 2 → 查询' if B.q[0] == 2 else f'`q = {B.q}`：类型 1 → 翻转 `b[{B.q[1]}]`'),
        'for v in range(2)': lambda S, B, r: ('两种开头都试过了' if 'v' in B and B.v == S.v else f'枚举保留下来的交替串以 `v = {S.v}` 开头（{"A" if S.v == 0 else "B"}）'),
        'pair = get(right, v)': '`[left, right]` 里“`{v}` 后接 `{1-v}`”的相邻对数 = `get({right}) − get({left})`，前缀差',
        'if left > 0 and b[left - 1] == v': lambda S, B, r: ('跨过左边界的对：`b[left-1]=v` 且 `b[left]=1-v`，这对只有一半在区间内 → ==减 1==，`pair = %d`' % S.pair
                                                                if B.left > 0 and B.b[B.left - 1] == B.v and B.b[B.left] == 1 - B.v
                                                                else '没有跨过左边界的对，`pair` 不变'),
        'length = pair + pair': '每个对贡献 2 个字符（`v` 和 `1-v`）：`length = {length}`',
        'if b[right] == v': lambda S, B, r: (f'`b[{B.right}] = {B.b[B.right]} = v`：右端还能多接一个 `v` → `length += 1`' if B.b[B.right] == B.v else f'`b[{B.right}] ≠ v`：右端没有多余字符，`length` 不变'),
        'ma = max(ma, length)': '取最长保留长度：`ma = max({B.ma}, {length}) = {ma}`',
        'res.append': '答案 = 区间长度 − 最长保留长度 = `{right} − {left} + 1 − {ma}` = =={right - left + 1 - ma}==',
        'p = q[1]': '要翻转的下标 `p = {p}`',
        'if p > 0': lambda S, B, r: ('`p > 0` → 先更新左边的对 `(p-1, p)`' if B.p > 0 else '`p = 0` 没有左邻居'),
        'if b[p - 1] != b[p]': lambda S, B, r: ('原来 `b[p-1] ≠ b[p]`，翻转后会相同 → 这个对消失，`-1`' if B.b[B.p-1] != B.b[B.p] else '原来 `b[p-1] = b[p]`，翻转后会不同 → 新增一个对，`+1`'),
        'if p + 1 < n': lambda S, B, r: ('`p + 1 < n` → 再更新右边的对 `(p, p+1)`' if B.p + 1 < B.n else '`p` 是最后一个，没有右邻居'),
        'if b[p] != b[p + 1]': lambda S, B, r: ('原来 `b[p] ≠ b[p+1]`，翻转后会相同 → 对消失，`-1`' if B.b[B.p] != B.b[B.p+1] else '原来 `b[p] = b[p+1]`，翻转后会不同 → 新增一个对，`+1`'),
        'b[p] ^= 1': '先改树状数组，最后翻转 `b[{p}]`：`0 ↔ 1`',
        'return res': '全部答案：`{res}`',
    },
    cards=dict(
        one_liner='相邻的 AB、BA 对越多，能保留的越长；其余全删',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含 `A/B`；`[1, p]` 翻转 `s[p]`，`[2, left, right]` 问 `s[left..right]` 变成交替串最少删几个',
                 '示例（本视频）：`s = "ABB"`，`queries = [[2,0,2],[1,2],[2,0,2]]` → `[1,0]`'],
        quote='连续出现的相同字符是需要全部删掉的。例如AAABBB，如果考虑得到ABAB形式的子串，那么前面的两个A以及后面的两个B都应该删除掉。问题实际上就是询问一组[left, right]之间，相邻的AB以及相邻的BA的数量是多少，尽量保留下这些字符对。',
        quote_src='—— yiduobo 题解原文',
        idea=['保留的字符数 = `2 × 相邻对数`，若右端字符对得上还能多接 1 个',
              '`f[v]` 是树状数组：数“`v` 后面紧跟 `1-v`”的相邻对，区间对数 = 前缀差',
              '跨过左边界的那一对只在前缀里算了一半，要扣 1；翻转时只改左右两个位置的对'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '易错：`get(right) - get(left)` 之后要处理跨过左边界的对（`pair -= 1`）',
                 '易错：只需考虑右端字符 `== v` 的情形才多算 1',
                 '翻转时先按 `b[p-1], b[p], b[p+1]` 的旧值改树状数组，最后才 `b[p] ^= 1`',
                 '对比灵神：灵神把“相等对”标成 b[i] 单树；yiduobo 把“相异对”按起始字母分两棵树'],
    ),
)
