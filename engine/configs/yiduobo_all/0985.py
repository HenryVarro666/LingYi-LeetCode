CONFIG = dict(
    num=985, title='查询后的偶数和', difficulty='Medium', category='模拟',
    author='yiduobo', technique='维护偶数和 · 分四种奇偶情况', tags=[],
    code='''
class Solution(object):
    def sumEvenAfterQueries(self, A, queries):

        now = 0
        for num in A:
            if num % 2 == 0:
                now += num
        
        res = []
        for delta, index in queries:
            if A[index] % 2 == 0:
                if delta % 2 == 0:
                    now += delta
                else:
                    now -= A[index]
                
                res.append(now)
                A[index] += delta
            
            else:
                A[index] += delta
                if A[index] % 2 == 0:
                    now += A[index]
                
                res.append(now)

        return res
''',
    call='Solution().sumEvenAfterQueries([1, 2, 3, 4], [[1, 0], [-3, 1], [-4, 0], [2, 2], [2, 3]])',
    expect=[8, 6, 2, 2, 4],
    views=[
        dict(type='text', fn=lambda S: (f"当前偶数和 `now` = =={S['now']}==" if 'now' in S else ''), size=34),
        dict(type='array', var='A', label='A（偶数高亮，奇数灰）', h=250, cell=100,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v % 2 == 0 else None,
             dim=lambda S, i, v: v % 2 != 0),
        dict(type='array', var='res', label='res：每次查询后的偶数和', h=150, cell=100),
    ],
    watch=['num', ('delta', 'delta', 'orange'), ('index', 'index', 'blue'), ('now', 'now', 'green')],
    captions={
        'now = 0': '`now` 记录 A 中所有==偶数的和==，后面每次查询只改一个数，增量更新即可',
        'for num in A': '预处理：扫一遍 A，统计偶数之和',
        'if num % 2 == 0': lambda S, B, r: f'`{S.num}` 是' + ('偶数 → 计入 now' if S.num % 2 == 0 else '奇数 → 不计'),
        'now += num': '`now` 加上偶数 `{num}` → {now}',
        'res = []': '预处理完成：`now = {now}`',
        'for delta, index in queries': '查询：`A[{index}] += {delta}`',
        11: lambda S, B, r: f'`A[{S.index}] = {S.A[S.index]}` 是' + ('偶数：它已经算在 now 里' if S.A[S.index] % 2 == 0 else '奇数：它没算在 now 里'),
        'if delta % 2 == 0': lambda S, B, r: f'`delta = {S.delta}` 是' + ('偶数：偶数加偶数还是偶数' if S.delta % 2 == 0 else '奇数：偶数加奇数变奇数'),
        'now += delta': '情况 1：偶 + 偶 仍是偶数，`s\' = s + val` → `now = {now}`',
        'now -= A[index]': '情况 2：偶 + 奇 变奇数，它要从 now 里==扣掉==旧值 `{A[index]}` → `now = {now}`',
        'res.append(now)': '记录答案 `{now}`',
        18: lambda S, B, r: f'更新 `A[{S.index}]`：{B.A[S.index]} → {S.A[S.index]}',
        21: lambda S, B, r: f'先更新 `A[{S.index}]`：{B.A[S.index]} → {S.A[S.index]}，再看它现在是不是偶数',
        22: lambda S, B, r: f'新值 `{S.A[S.index]}` 是' + ('偶数：奇 + 奇 变偶数，要计入 now（情况 4）' if S.A[S.index] % 2 == 0 else '奇数：奇 + 偶 仍是奇数，now 不变（情况 3）'),
        'now += A[index]': '情况 4：新出现一个偶数，`now += {A[index]}` → `now = {now}`',
    },
    cards=dict(
        one_liner='先存下偶数和，每次只看被改的那一个数',
        complexity='时间 `O(n + q)`，空间 `O(1)`（不含答案）',
        problem=['数组 `A`，每次查询 `[val, index]`：先 `A[index] += val`，再求 A 中所有偶数的和',
                 '返回每次查询之后的偶数和',
                 '本视频：`A=[1,2,3,4]`，查询 `[[1,0],[-3,1],[-4,0],[2,2],[2,3]]` → `[8,6,2,2,4]`'],
        quote='由于每一次操作最多只会影响一个数的奇偶性，那么我们可以首先预先计算出A中所有偶数的和s，然后依次遍历queries。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次只改一个数，所以不用重算整个数组，只维护偶数和 `now`',
              '原文分四种情况：偶+偶 → `s + val`；偶+奇 → `s - A[index]`',
              '奇+偶 → 无变化；奇+奇 → 变成偶数，`s + (A[index] + val)`'],
        summary=['时间 `O(n + q)`，每次查询 `O(1)`',
                 '易错：偶 + 奇 要扣掉的是==修改前==的 `A[index]`，所以先 `now -= A[index]` 再更新',
                 '易错：奇 + 奇 要加的是修改后的新值，所以先更新再判断',
                 '查询里是 `[val, index]`，顺序别写反',
                 '原文已是 Python 3 可运行写法，未做改动'],
    ),
)
