RIDES = [[11, 12, 2], [3, 10, 2], [10, 12, 3], [1, 6, 1]]


def _rides_txt(S):
    r = S.get('rides')
    if r is None:
        return ''
    p = S.get('p', -1)
    return '按 end 排序后：' + '  '.join((f'==[{a},{b}]+{c}==' if k == p else f'[{a},{b}]+{c}') for k, (a, b, c) in enumerate(r))


def _cur(S):
    idx = S.get('index')
    if idx is None or 'p' not in S:
        return '`f[i]` = 到位置 `i` 为止所能取得的最大收益'
    r = S['rides']
    p = S['p']
    if S['_line'] in (10, 11) and p < len(r) and r[p][1] == idx:
        l, rr, t = r[p]
        return f'区间 `[{l}, {rr}]`：`f[{l}] + {rr} - {l} + {t}` = =={S["f"][l] + rr - l + t}=='
    return f'`f[{idx}]` 先等于 `f[{idx - 1}]` = {S["f"][idx - 1]}，再看右端点为 {idx} 的区间'


CONFIG = dict(
    num=2008, title='出租车的最大盈利', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间按右端点排序 · 位置 DP + 单调指针',
    tags=['灵神题单', '难度分 1872'],
    code='''
class Solution(object):
    def maxTaxiEarnings(self, n, rides):

        rides = sorted(rides, key=lambda d:d[1])
        f = [0] * (n + 1)

        p = 0
        for index in range(1, n + 1):
            f[index] = f[index - 1]
            while p < len(rides) and rides[p][1] == index:
                f[index] = max(f[index], f[rides[p][0]] + rides[p][1] - rides[p][0] + rides[p][2])
                p += 1
        
        return f[-1]
''',
    call=f'Solution().maxTaxiEarnings(12, {RIDES!r})',
    expect=14,
    skip=['rides = sorted'],
    views=[
        dict(type='text', fn=_rides_txt, size=26, h=70),
        dict(type='array', var='f', label='f[i]：到位置 i 为止的最大收益（黄 = 正在算）', h=300, cell=62,
             pointers={'index': 'blue', 'rides[p][0] if _line == 11 and p < len(rides) else None': 'pink'},
             pointer_labels={'rides[p][0] if _line == 11 and p < len(rides) else None': 'l'},
             color=lambda S, k, v: 'yellow' if k == S.get('index') else None),
        dict(type='text', fn=_cur, size=28, h=90),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('f[index]', "f[index] if _line >= 9 else '-'", 'green')],
    captions={
        'f = [0] * (n + 1)': '`f[i]`：到位置 `i` 为止所能取得的最大收益，`f[0] = 0`',
        'p = 0': '`p` 指向下一个还没处理的区间；区间已按右端点排好，`p` 只会往后走',
        'for index in range': lambda S, B, r: ('所有位置都算完了' if S.index == B.get('index') else f'算 `f[{S.index}]`'),
        'f[index] = f[index - 1]': '最后这一段什么都没干：`f[{index}] = f[{index - 1}]` = {f[index]}',
        'while p < len': lambda S, B, r: (f'`rides[{S.p}]` 的右端点是 {S.rides[S.p][1]}，正好等于 `index` → 处理它' if S.p < len(S.rides) and S.rides[S.p][1] == S.index
                                          else (f'没有更多区间了，`index = {S.index}` 处理完' if S.p >= len(S.rides) else f'`rides[{S.p}]` 右端点 {S.rides[S.p][1]} ≠ {S.index}，留给以后')),
        'f[index] = max(f[index], f[rides': '`max({B.f[index]}, f[{rides[p][0]}] + {rides[p][1]} - {rides[p][0]} + {rides[p][2]})` = =={f[index]}==：接在 `f[l]` 后面加这个区间',
        'p += 1': '这个区间用完了，`p` → {p}（每个区间只会被处理一次 → 均摊 O(1)）',
        'return f[-1]': '答案 `f[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='区间按右端点排序，f[i] 看「什么都不干」或「以 i 结尾的区间」',
        complexity='时间 `O(m log m + n)`，空间 `O(n)`',
        problem=['一条路上 `n` 个地点，`rides[i] = [start, end, tip]`，载这位乘客盈利 `end - start + tip`',
                 '同时最多接一单，求最多盈利',
                 '示例：`n=5, rides=[[2,5,4],[1,5,1]]` → `7`'],
        quote='题目实际上是给出了若干区间，每个区间都有一个权重，要求从中选出若干不相交的区间，使得这些区间权重之和最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['这是带权的不相交区间选择：排序后用 DP',
              '作者给了两种状态：按区间编号（配树状数组），或按位置 `f[i]`',
              '这里用按位置：区间已按右端点排好，指针 `p` 单调往后走'],
        summary=['时间 `O(m log m + n)`：排序 + 每个区间只处理一次',
                 '空间 `O(n)`',
                 '易错：`f[l]` 而不是 `f[l-1]`，因为可以同地点下客再接客',
                 '原文没有 Python 2 特有写法，代码未做修改',
                 '对比灵神：灵神用字典按 end 分组，yiduobo 用排序 + 单调指针'],
    ),
)
