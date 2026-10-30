CONFIG = dict(
    num=1538, title='找出隐藏数组中出现次数最多的元素', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='五元素分类 + 两两查询', tags=[],
    code='''
class Solution(object):
    def guessMajority(self, reader):

        n = reader.length()

        v1 = reader.query(0, 1, 2, 3)
        v2 = reader.query(0, 1, 2, 4)
        v3 = reader.query(0, 1, 3, 4)
        v4 = reader.query(0, 2, 3, 4)

        other = None
        if v1 == 4:
            #1)
            p1 = 0
            p2 = 1
            if v2 == 4:
                #1-1)
                cnt1 = 5
                cnt2 = 0
            else:
                #1-2)
                cnt1 = 4
                cnt2 = 1
        
        elif v1 == 2:
            #2)
            if v2 == 4:
                #2-1)
                p1 = 0
                p2 = 1
                cnt1 = 4
                cnt2 = 1
            elif v2 == 2:
                #2-2)
                if v3 == 0:
                    #2-2-1)
                    p1 = 0
                    p2 = 1
                    other = 4
                    cnt1 = 3
                    cnt2 = 2
                else:
                    #2-2-2)
                    p1 = 3
                    p2 = 4
                    cnt1 = 4
                    cnt2 = 1
            elif v2 == 0:
                #2-3)
                cnt1 = 3
                cnt2 = 2
                if v3 == 2:
                    #2-3-1)
                    p1 = 0
                    p2 = 1
                    other = 2
                elif v4 == 2:
                    #2-3-2)
                    p1 = 0
                    p2 = 2
                    other = 1
                else:
                    #2-3-3)
                    p1 = 1
                    p2 = 2
                    other = 0

        elif v1 == 0:
            #3)
            if v2 == 2:
                #3-1)
                cnt1 = 3
                cnt2 = 2
                if v3 == 2:
                    #3-1-1)
                    p1 = 0
                    p2 = 1
                    other = 2
                elif v4 == 2:
                    #3-1-2)
                    p1 = 0
                    p2 = 2
                    other = 1
                else:
                    #3-1-3)
                    p1 = 1
                    p2 = 2
                    other = 0
            elif v2 == 0:
                #3-2)
                p1 = 3
                p2 = 4
                cnt1 = 3
                cnt2 = 2
                if v3 == 0:
                    other = 0
                else:
                    other = 2

        i = 5
        while i + 1 < n:
            v = reader.query(p1, p2, i, i + 1)
            if v == 4:
                cnt1 += 2
            elif v == 2:
                cnt1 += 1
                cnt2 += 1
            else:
                cnt2 += 2
                other = i
            i += 2

        if other is None:
            return p1

        if i < n:
            if other < p1:
                v = reader.query(other, p1, p2, i)
            elif p1 < other < p2:
                v = reader.query(p1, other, p2, i)
            else:
                v = reader.query(p1, p2, other, i)

            if v == 2:
                cnt1 += 1
            else:
                cnt2 += 1
        
        if cnt1 > cnt2:
            return p1
        elif cnt1 == cnt2:
            return -1
        else:
            return other
''',
    setup='''
class ArrayReader(object):
    def __init__(self, a):
        self.a = a
        self.log = []
    def length(self):
        return len(self.a)
    def query(self, p, q, r, s):
        t = self.a[p] + self.a[q] + self.a[r] + self.a[s]
        res = 4 if t in (0, 4) else 2 if t in (1, 3) else 0
        self.log.append((p, q, r, s, res))
        return res
reader = ArrayReader([0, 1, 1, 0, 1, 1, 0, 1])
''',
    call='''
ans = Solution().guessMajority(reader)
ans if reader.a[ans] == 1 else None
''',
    expect=1,
    views=[
        dict(type='array', var='reader.a', h=230, label='隐藏数组（程序看不到，只能 query）',
             pointers={'p1': 'blue', 'p2': 'cyan', 'other': 'pink', 'i': 'yellow'},
             color=lambda S, i, v: ('blue' if i == S.get('p1') else 'cyan' if i == S.get('p2')
                                    else 'pink' if i == S.get('other') else None)),
        dict(type='text', h=110, size=30, fn=lambda S: (
            '已用 query：' + '  '.join(f"`({a},{b},{c},{d})→{r}`" for a, b, c, d, r in S['reader'].log[-4:]) if S['reader'].log else '还没有查询')),
        dict(type='text', h=110, size=32, fn=lambda S: (
            f"a 的数量 `cnt1 = =={S['cnt1']}==`，b 的数量 `cnt2 = =={S['cnt2']}==`" if 'cnt1' in S and 'cnt2' in S else
            '先靠前 5 个数确定两个“同种”下标 `p1`、`p2`')),
    ],
    watch=['v1', 'v2', ('p1', 'p1', 'blue'), ('p2', 'p2', 'cyan'), ('other', 'other', 'pink'), 'cnt1', 'cnt2', 'i'],
    captions={
        'n = reader': '`n = {n}`：数组长度只能通过 `reader.length()` 得到',
        'v1 = ': '`query(0,1,2,3) = {v1}`：4 = 四个都相同，2 = 3:1，0 = 2:2',
        'v2 = ': '`query(0,1,2,4) = {v2}`：把第 5 个数换进来，和 v1 比较就能看出它和被换掉的数是否同类',
        'v3 = ': '`query(0,1,3,4) = {v3}`',
        'v4 = ': '`query(0,2,3,4) = {v4}`：这四次查询足以把前 5 个数分成 a/b 两类',
        'other = None': '`other` 先置空：它之后要指向一个“已知是 b”的位置',
        'if v1 == 4': '`v1 == 4`？前四个是否全同类 → {v1 == 4}',
        'elif v1 == 2': '`v1 == 2`？前四个是否 3:1 → {v1 == 2}',
        'elif v1 == 0': '`v1 == 0`？前四个是否 2:2 → {v1 == 0}，此时第 5 个必然是 a',
        'if v2 == 2': '`v2 == 2`？ → {v2 == 2}',
        'elif v2 == 0': '`v2 == 0`？ → {v2 == 0}',
        'if v3 == 2': '`v3 == 2`？ → {v3 == 2}',
        'elif v4 == 2': '`v4 == 2`？ → {v4 == 2}',
        'p1 = 1': '确定 `p1 = {p1}`：这个位置一定是 a',
        'p2 = 2': '确定 `p2 = {p2}`：也一定是 a。有了两个 a 做“参照”',
        'other = 0': '`other = 0`：位置 0 必然是 b',
        'cnt1 = 3': '前 5 个里 a 有 3 个：`cnt1 = {cnt1}`',
        'cnt2 = 2': '前 5 个里 b 有 2 个：`cnt2 = {cnt2}`',
        'i = 5': '从下标 5 开始，两个一组处理剩下的数',
        'while i + 1 < n': '还有成对的数吗？`i + 1 < n` → {i + 1 < n}',
        'v = reader.query(p1, p2, i, i + 1)': '`query(p1,p2,i,i+1) = {v}`：p1、p2 是 a，4 → 新两个都是 a；2 → 一 a 一 b；0 → 都是 b',
        'cnt1 += 2': '`v == 4`：两个都是 a，`cnt1 = {cnt1}`',
        105: '`v == 2`？一 a 一 b → {v == 2}',
        106: '`v == 2`：一 a 一 b，`cnt1 = {cnt1}`',
        124: '`v == 2`：query 里是 3 个同类 + 1 个不同类，而 other、p1、p2 是 b a a → 落单的数是 a → {v == 2}',
        125: '落单的数是 a：`cnt1 = {cnt1}`',
        113: '`other is None`？ → {other is None}。从没见过 b 时必有 `cnt1 > cnt2`，直接返回 p1；这里见过，继续',
        'cnt2 += 1': '`cnt2 = {cnt2}`',
        'cnt2 += 2': '`v == 0`：两个都是 b，`cnt2 = {cnt2}`，顺便记下 `other = {i}`',
        'i += 2': '处理完一组，`i = {i}`',
        'if i < n': '`n` 是偶数时会剩下最后一个数：`i = {i}`，`n = {n}` → {i < n}',
        'if other < p1': '`other` 比 `p1` 小吗？只是为了把下标按升序放进 query → {other < p1}',
        'v = reader.query(other, p1, p2, i)': '拿 b（`other`）、两个 a、最后一个数查询：`v = {v}`',
        'if cnt1 > cnt2': '比较 a、b 的数量：`{cnt1}` 对 `{cnt2}` → {cnt1 > cnt2}',
        'return p1': 'a 更多，返回任意一个 a 的下标 `p1 = {ret}`',
    },
    cards=dict(
        one_liner='先用 5 个数认出两个同类下标，再两个一组去“量”',
        complexity='查询 `O(n)` 次，空间 `O(1)`',
        problem=['有一个只含 0、1 的隐藏数组，只能调用 `query(a,b,c,d)` 比较 4 个不同下标',
                 '返回 4：四个相同；2：3 个相同；0：2 对 2。`length()` 给出长度 n',
                 '求出现次数最多的值的任意一个下标，一样多则返回 -1（本题需限制查询次数）'],
        quote='每次需要使用四个不同的数，那么只有在这四个数中至少有两个数的01组合已经确定的前提下，才能确定剩下未知数的01组合。',
        quote_src='—— yiduobo 题解',
        idea=['前 5 个数用至多 4 次查询分情况，确定 a 的两个下标 `p1`、`p2` 与数量 `cnt1`、`cnt2`',
              '之后 `query(p1,p2,i,i+1)`：4/2/0 分别表示两个新数 2a / 1a1b / 2b',
              'n 为偶数时剩下最后一个，需要一个已知的 b（`other`）才能判断它'],
        summary=['查询次数约 `n/2 + 4`，空间 `O(1)`',
                 '易错：`other` 要在分类时记下，或循环中遇到 `v == 0` 时记下',
                 '`other is None` 说明没见过 b，必有 `cnt1 > cnt2`，直接返回 p1',
                 '本题为 VIP 题，这里自定义 `ArrayReader` 模拟隐藏数组，原文去掉了头部注释里的接口说明',
                 '原文已是 Python 3 可运行写法，未改动'],
    ),
)
