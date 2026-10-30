CONFIG = dict(
    num=3323, title='通过插入区间最小化连通组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序合并区间 + 同向双指针',
    tags=['滑动窗口与双指针', '贪心与思维'],
    code='''
class Solution(object):
    def minConnectedGroups(self, intervals, k):
        
        intervals.sort()
        merged = []
        x, y = intervals[0]
        for nowx, nowy in intervals[1:]:
            if nowx <= y:
                y = max(y, nowy)
            else:
                merged.append([x, y])
                x, y = nowx, nowy
        
        merged.append([x, y])

        print(merged)

        p = 0
        res = len(merged)
        for index in range(len(merged)):
            addy = merged[index][1] + k
        
            while p < len(merged) and merged[p][0] <= addy:
                p += 1
        
            res = min(res, len(merged) - p + index + 1)
        
        return res
''',
    call='Solution().minConnectedGroups([[8,10],[1,3],[2,4],[5,6],[12,13]], 5)',
    expect=2,
    views=[
        dict(type='intervals', var='intervals', label='intervals（排序后）', h=230),
        dict(type='intervals', var='merged', label='merged（合并后的连通组，黄 = 新区间的起点所在组）', pointer='index', h=250),
        dict(type='text', fn=lambda S: (f"新区间 `[{S['merged'][S['index']][1]}, {S['addy']}]`：覆盖到第 `{S['p']-1}` 组，合并 `{S['p']-S['index']}` 组 → 剩 `{len(S['merged'])-S['p']+S['index']+1}` 组" if 'addy' in S and 'index' in S and S['p'] > S['index'] else '')),
    ],
    watch=[('index', 'index', 'yellow'), ('addy', 'addy', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'intervals.sort()': '先按起点排序，才能线性地合并相连的区间',
        'x, y = intervals[0]': '`[x, y]` 是正在扩张的当前连通组，先取第一个区间 `[{x}, {y}]`',
        'for nowx, nowy': lambda S, B, r: ('区间都看完了，循环结束' if getattr(B, 'nowx', None) == S.nowx and getattr(B, 'nowy', None) == S.nowy else f'看下一个区间 `[{S.nowx}, {S.nowy}]`'),
        'if nowx <= y': '`nowx = {nowx}` 对 当前组右端点 `y = {y}`：{"起点没超过右端点 → 相连，同一组" if nowx <= y else "出现间隙 → 这是新的一组"}',
        'y = max(y, nowy)': '合并：右端点取较大者 → `y = {y}`',
        'x, y = nowx, nowy': '当前组结束，从 `[{x}, {y}]` 开始新的一组',
        'print(merged)': '合并完成，`merged` 就是所有连通组，共 `{len(merged)}` 个',
        'p = 0': '`p` 指向「新区间还够不着的第一个组」，只增不减',
        'res = len(merged)': '不插入时就是 `{len(merged)}` 组，作为答案的初值',
        'for index in range': lambda S, B, r: ('每个 `index` 都试过了，循环结束' if getattr(B, 'index', None) == S.index else f'枚举新区间连通的==最左侧==组 `index = {S.index}`'),
        'addy = merged': '新区间起点放在第 `{index}` 组的右端点（和它重叠最小），顶着长度 `k = {k}` 向右伸 → 右端 `addy = {addy}`',
        'while p < len': lambda S, B, r: (f'第 `{S.p}` 组起点 `{S.merged[S.p][0]}` <= `addy = {S.addy}` → 能被新区间碰到，`p` 右移' if S.p < len(S.merged) and S.merged[S.p][0] <= S.addy
                                         else ('后面的组已经够不着，`p` 停下' if S.p < len(S.merged) else '组都碰完了，`p` 停下')),
        'p += 1': '`p` → {p}',
        'res = min(res': '`index` 到 `p-1` 共 `{p-index}` 组并成 1 组：`{len(merged)} - {p-index} + 1` = {len(merged)-p+index+1}，`res` = =={res}==',
        'return res': '最少连通组数 =={ret}==',
    },
    cards=dict(
        one_liner='先合并区间，再让新区间从某个组的右端点出发顶满 k',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给若干闭区间 `intervals` 和整数 `k`，再插入一个长度 `<= k` 的新区间',
                 '重叠或相接的区间属于同一个连通组，求插入后连通组的==最少个数==',
                 '本视频：`[[8,10],[1,3],[2,4],[5,6],[12,13]], k=5` → `2`'],
        quote='新添加的区间应该顶着长度 k 来设置，同时这个新区间应该和其连通的最左侧区间重叠的部分最小，……也就是说这个区间的起点应该设置在某个已有区间的终点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序合并，得到互不相连的若干组',
              '新区间起点放在第 `index` 组的右端点，终点 `addy = 右端点 + k`',
              '`index` 右移时 `addy` 不会变小，所以 `p` 只增不减，两个指针一遍扫完',
              '合并掉第 `index..p-1` 组：剩 `总数 - (p-index) + 1`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '合并时 `nowx <= y` 含相等：端点相接也算连通',
                 '原文为 Python 2 写法，`print merged` 已改为 `print(merged)`',
                 '`p` 最多走到 `len(merged)`，所以 `while` 里要先判断 `p < len(merged)`'],
    ),
)
