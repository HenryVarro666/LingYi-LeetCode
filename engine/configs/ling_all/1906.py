CONFIG = dict(
    num=1906, title='查询差绝对值的最小值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二分元素位置 · 枚举值域 1..100（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def minDifference(self, a: List[int], qs: List[List[int]]) -> List[int]:
        ans = [0] * len(qs)
        pos = [[] for _ in range(101)]
        for i, v in enumerate(a):
            pos[v].append(i)
        for i, q in enumerate(qs):
            l, r, d, pre = q[0], q[1] + 1, int(1e9), int(-1e9)
            for v, ps in enumerate(pos):
                if not ps:
                    continue
                cnt = bisect_left(ps[bisect_left(ps, l):], r)  # 二分查询 v 的个数
                if cnt == r - l:  # 所有元素都相同
                    ans[i] = -1
                    break
                if cnt > 0:  # 子数组包含元素 v
                    if v - pre < d:
                        d = v - pre
                    pre = v
            else:
                ans[i] = d
        return ans
''',
    call='Solution().minDifference([4,5,2,2,7], [[2,3],[0,4]])',
    expect=[-1, 1],
    skip=['for v, ps in enumerate(pos)', 'if not ps', 'continue'],
    views=[
        dict(type='array', var='a', h=200, cell=90, label='a（下标 → 元素）',
             window=('l', lambda S: S['r'] - 1 if 'r' in S else None)),
        dict(type='map', var=lambda S: {v: ps for v, ps in enumerate(S['pos']) if ps}, h=240, label='pos：每个值出现的下标（有序）',
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"查询 `[{S['l']}, {S['r'] - 1}]`：已见最小差 `d = {S['d'] if S['d'] < 10**8 else '∞'}`，上一个出现的值 `pre = {S['pre'] if S['pre'] > -10**8 else '无'}`"
            if 'l' in S and 'd' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('v', 'v', 'cyan'), ('cnt', 'cnt', 'yellow'), ('d', 'd', 'green'), 'ans'],
    captions={
        'ans = [0]': '`ans` 先占位，每个查询填一个答案',
        'pos = [[]': '`pos[v]` 记录值 `v` 出现的所有下标（从小到大）',
        'pos[v].append': '值 `{v}` 出现在下标 `{i}`：`pos[{v}]` = {pos[v]}',
        'l, r, d, pre': '第 {i} 个查询，半开区间 `[{l}, {r})`（长度 `{r - l}`）；`d` 取很大、`pre` 取很小，使第一个值不会更新 `d`',
        'cnt = bisect_left': '值 `{v}` 在 `[{l}, {r})` 里有 =={cnt}== 个：在 `{pos[v]}` 中二分出落在区间内的个数',
        'if cnt == r - l': lambda S, B, r: (f'`cnt = {S.cnt} == 区间长度 {S.r - S.l}` → ==区间内全是同一个值== → 答案 -1，直接结束这个查询'
                                          if S.cnt == S.r - S.l else f'`cnt = {S.cnt}` ≠ 区间长度 `{S.r - S.l}` → 不是全相同，继续'),
        'ans[i] = -1': '这个查询的答案是 =={ans[i]}==，`break` 跳出值域枚举（不走 `else`）',
        'if cnt > 0': lambda S, B, r: (f'`cnt = {S.cnt} > 0` → 区间包含值 `{S.v}`' if S.cnt > 0 else f'`cnt = 0` → 区间里没有值 `{S.v}`，跳过'),
        'if v - pre < d': lambda S, B, r: (f'`{S.v} - {S.pre if S.pre > -10**8 else "-∞"} < {S.d if S.d < 10**8 else "∞"}`' + (' → ==更新最小差==' if S.v - S.pre < S.d else ' → 不更小')),
        'd = v - pre': '相邻两个存在的值之差 `{v} − {pre}` → `d = ` =={d}==',
        'pre = v': '`pre = {pre}`：下次与它比较（值是从小到大枚举的，只有相邻值才可能产生最小差）',
        'ans[i] = d': '枚举完 1..100，没有提前 break → 答案 `d = ` =={ans[i]}==',
        'return ans': '所有查询答案：=={ans}==',
    },
    cards=dict(
        one_liner='值域只有 100：从小到大枚举值，只看相邻存在的两个值',
        complexity='时间 `O(n + q·U·log n)`，空间 `O(n)`（U = 100）',
        problem=['每个查询 `[l, r]`：求子数组里任意两个不同元素差的绝对值的最小值',
                 '元素全相同时答案是 `-1`；`nums[i] <= 100`',
                 '本视频：`nums=[4,5,2,2,7]`，查询 `[2,3]`、`[0,4]` → `[-1, 1]`'],
        quote='func minDifference(a []int, qs [][]int) []int { ... cnt := ps[ps.Search(l):].Search(r) // 二分查询 v 的个数 ... if cnt == r-l { // 所有元素都相同',
        quote_src='—— 灵茶山艾府题解代码（原文为 Go，方法二）',
        idea=['值域小（≤100）：每次查询从 1 枚举到 100',
              '对每个值 `v`，在它的下标列表 `pos[v]` 里二分，得到区间里有几个 `v`',
              '存在就与上一个存在的值 `pre` 作差，更新最小差；若某值个数等于区间长度，全部相同，答案 -1'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`continue outer` 改写为 `break` + `for ... else`',
                 '`sort.IntSlice.Search` 对应 `bisect_left`；原文还有方法一（每个值一份个数前缀和），这里选空间更省的方法二',
                 '时间 `O(n + q·U·log n)`，空间 `O(n)`',
                 '易错点：区间 `[l, r]` 要转成半开 `[l, r+1)`；`pre` 初值取很小，避免第一个值产生假差',
                 '视频里为了简洁，枚举值域时跳过了没出现的值（代码里是 `if not ps: continue`）'],
    ),
)
