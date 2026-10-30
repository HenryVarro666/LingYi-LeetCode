def _q(S):
    I = S.get('_inner', {})
    if 'v' in I and 'now' in I:
        return (f"在 `[{I['left']}, {I['right']}]`（线段树结点 {I['now']}）里找第一个 ==> {I['v']}== 的位置，"
                f"只能从下标 `{I['p']}` 起；该区间最大值 `ma = {S['ma'][I['now']]}`")
    if 'a' in S and 'b' in S and 'res' in S:
        return f"询问 `({S['a']}, {S['b']})`：已回答 {S['res']}"
    return ''


def _win(S):
    I = S.get('_inner', {})
    return I.get('left'), I.get('right')


CONFIG = dict(
    num=2940, title='找到 Alice 和 Bob 可以相遇的建筑', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（区间最大值）+ 线段树上二分',
    tags=['难度分 2327'],
    code='''
class Solution(object):
    def leftmostBuildingQueries(self, heights, queries):

        n = len(heights)
        ma = [0] * (n * 4)

        def build(now, left, right):
            if left == right:
                ma[now] = heights[left]
                return

            mid = (left + right) // 2
            build(now + now + 1, left, mid)
            build(now + now + 2, mid + 1, right)
            ma[now] = max(ma[now + now + 1], ma[now + now + 2])
        
        def query(now, left, right, p, v):
            if ma[now] <= v:
                return -1
            
            if left == right:
                return left
            
            mid = (left + right) // 2
            if p <= mid:
                t = query(now + now + 1, left, mid, p, v)
                if t != -1:
                    return t

            return query(now + now + 2, mid + 1, right, p, v)
        

        build(0, 0, n - 1)
        res = []
        for a, b in queries:
            if a > b:
                a, b = b, a
            
            if a == b or heights[a] < heights[b]:
                res.append(b)
            elif b == n - 1:
                res.append(-1)
            else:
                res.append(query(0, 0, n - 1, b + 1, max(heights[a], heights[b])))
        
        return res
''',
    call='Solution().leftmostBuildingQueries([6,4,8,5,2,7], [[3,0],[2,4],[3,3]])',
    expect=[5, -1, 3],
    views=[
        dict(type='text', fn=_q, h=80, size=24),
        dict(type='array', var='heights', label='heights（蓝框 = 当前线段树结点的区间）', h=150,
             window=(lambda S: _win(S)[0], lambda S: _win(S)[1])),
        dict(type='array', var='ma', label='ma：线段树结点 now 对应区间的最大值（左孩子 2·now+1，右孩子 2·now+2）', h=130, cell=40),
        dict(type='calls', h=150),
        dict(type='array', var='res', label='res', h=100),
    ],
    watch=[('a', lambda S: S.get('a', ''), 'blue'), ('b', lambda S: S.get('b', ''), 'pink')],
    captions={
        'ma = [0]': '线段树数组 `ma`：开 `4n` 个位置，==每个结点存区间最大值==',
        'def build': '`build`：自底向上算出每个区间的最大值',
        'if left == right': lambda S, B, r: (
            f'区间 `[{S.left}, {S.right}]` 只剩一个楼，是叶子' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 还有多个楼，继续一分为二'),
        'ma[now] = heights[left]': '叶子：`ma[{now}] = heights[{left}] = {ma[now]}`',
        'mid = (left + right) // 2': '取中点 `mid = {mid}`，左半 `[{left}, {mid}]`，右半 `[{mid + 1}, {right}]`',
        'ma[now] = max(': '合并：`ma[{now}] = max(左孩子, 右孩子) = {ma[now]}`，区间 `[{left}, {right}]` 的最高楼',
        'build(0, 0, n - 1)': '建树：从根结点 0 管整个 `[0, {n - 1}]`',
        'for a, b in queries': lambda S, B, r: ('询问全部处理完' if S.get('a') == B.get('a') and S.get('b') == B.get('b') and 'res' in B and S.a == S.b and len(S.res) == 3 else f'取下一个询问 `(a, b) = ({S.a}, {S.b})`'),
        'if a > b': lambda S, B, r: f'`a = {S.a}`，`b = {S.b}`：二人等价，' + ('`a > b` → 交换，保证 `a ≤ b`' if S.a > S.b else '`a ≤ b`，不用交换'),
        'a, b = b, a': '交换后 `a = {a}`，`b = {b}`',
        'if a == b or': lambda S, B, r: (
            f'`a == b` 或 `heights[{S.a}] = {S.heights[S.a]} < heights[{S.b}] = {S.heights[S.b]}` → 在 `b` 相遇' if S.a == S.b or S.heights[S.a] < S.heights[S.b]
            else f'`heights[{S.a}] = {S.heights[S.a]} ≥ heights[{S.b}] = {S.heights[S.b]}`：谁也跳不到对方 → 找 `[b+1, n-1]` 里第一个更高的楼'),
        'res.append(b)': '答案就是 `b`：`res = {res}`',
        'elif b == n - 1': lambda S, B, r: ('`b` 已是最后一栋，右边没有楼 → 答案 `-1`' if S.b == S.n - 1 else '`b` 不是最后一栋，右边还有楼，去线段树里找'),
        'res.append(-1)': '`res = {res}`',
        'res.append(query': '目标：`[{b + 1}, {n - 1}]` 里最小的下标 `t`，满足 `heights[t] > max(heights[a], heights[b]) = {max(heights[a], heights[b])}`',
        'if ma[now] <= v': lambda S, B, r: (
            f'结点 {S.now} 区间 `[{S.left}, {S.right}]` 的最大值 `{S.ma[S.now]}` ' +
            (f'≤ `{S.v}` → ==整段都不够高==，返回 -1' if S.ma[S.now] <= S.v else f'> `{S.v}` → 这段里有更高的楼，继续看')),
        'return -1': '这一段没有答案，返回 `-1`',
        'if left == right': lambda S, B, r: (f'区间 `[{S.left}, {S.right}]`：叶子' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 不是叶子，继续拆'),
        'return left': '叶子且 `ma > v`：`heights[{left}] = {ma[now]}` 比 `{v}` 高 → 答案 =={left}==',
        'if p <= mid': lambda S, B, r: (
            f'`p = {S.p} ≤ mid = {S.mid}` → 左半 `[{S.left}, {S.mid}]` 里还有 `≥ p` 的位置，==先找左半（要最小下标）==' if S.p <= S.mid
            else f'`p = {S.p} > mid = {S.mid}` → 左半全在 `p` 左边，不用看，直接去右半'),
        't = query(now + now + 1': '递归左孩子，要最小下标所以先左后右',
        'if t != -1': lambda S, B, r: (f'左半找到了 `t = {S.t}` → 直接返回' if S.t != -1 else '左半没找到 → 再去右半找'),
        'return t': '返回 `t = {t}`',
        'return query(now + now + 2': '去右孩子 `[{mid + 1}, {right}]` 找，结果直接返回',
        'return res': '全部询问答完：`{ret}`',
    },
    skip=[8, 10, 12, 13, 14, 21, 24],
    max_steps=140,
    cards=dict(
        one_liner='线段树存区间最大值，在 b 右边「找第一个比 max(a,b) 高的楼」',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['`heights[i]` 是楼高，只能从低楼走到右边更高的楼；每个询问 `(a, b)`，求二人能相遇的==最左==楼',
                 '不能相遇答 `-1`',
                 '本视频：`heights=[6,4,8,5,2,7]`，询问 `[[3,0],[2,4],[3,3]]` → `[5,-1,3]`'],
        quote='需要在区间[b + 1, n - 1]之间寻找一个最小的下标t，满足heights[t] > max(heights[a], heights[b])。这是一个后缀区间询问问题，需要要寻找的是满足条件的最小坐标，因此需要用到线段树。',
        quote_src='—— yiduobo 题解原文',
        idea=['Alice 和 Bob 等价：`a > b` 就交换；`a == b` 或 `heights[a] < heights[b]` 直接在 `b` 相遇',
              '否则找 `[b+1, n-1]` 里第一个 `> max(heights[a], heights[b])` 的下标：线段树维护区间最大值 `ma`',
              '自顶向下：最大值 `≤ v` 无解；叶子即答案；`b+1 ≤ mid` 先左后右'],
        summary=['时间：建树 `O(n)`，每个询问 `O(log n)`；空间 `O(n)`',
                 '易错点：左半没找到才找右半；`p > mid` 时左半整个在 `p` 左边，必须跳过',
                 '`b == n - 1` 时右边没有楼，要单独返回 `-1`',
                 '原文本身是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神主推离线 + 最小堆；yiduobo 在线用线段树二分，思路等同灵神的方法三'],
    ),
)
