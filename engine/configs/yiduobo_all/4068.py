M = [[3, 5, 4], [4, 7, 8], [8, 10, 3], [1, 3, 2]]


def _txt(S):
    if 'f' not in S:
        return '`f[k]`：前 k+1 场里 「收益 + 空闲 − 最后一场的结束时间」的最大值（把 end 带进状态）'
    if S['_line'] >= 30:
        return f'答案 `res` = =={S["res"]}==（`f` 里减过 end，所以答案不直接取 `f`）'
    return f'`res` = =={S["res"]}==；`f` = {S["f"]}'


CONFIG = dict(
    num=4068, title='考虑空闲时间的会议最大收益', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='排序 + 二分 · 把 end 带进 f', tags=[],
    code='''
class Solution(object):
    def maxEarnings(self, meetings):
        
        meetings.sort(key=lambda d:d[1])

        f = []
        res = 0

        for index, (start, end, rev) in enumerate(meetings):
            if start < meetings[0][1]:
                res = max(res, rev)
                if not f:
                    f.append(rev - end)
                else:
                    f.append(max(f[-1], rev - end))
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right + 1) // 2
                    if meetings[mid][1] <= start:
                        left = mid
                    else:
                        right = mid - 1
                
                v = f[left] + rev + start
                res = max(res, v)
                f.append(max(f[-1], v - end))
        
        return res
''',
    call=f'Solution().maxEarnings({M!r})',
    expect=15,
    views=[
        dict(type='table', var='meetings', label='meetings（按结束时间排序；黄 = 当前第 index 场）', rows=lambda S: [f'#{k}' for k in range(len(S['meetings']))],
             cols=['开始', '结束', '收益'], h=250, cell=110,
             color=lambda S, i, j, v: 'yellow' if i == S.get('index') else None),
        dict(type='array', var='f', label='f[k]：前 k+1 场里 收益 + 空闲 − end 的最大值', pointers={'left': 'blue', 'right': 'pink', 'mid': 'cyan'}, h=210, cell=110),
        dict(type='text', h=90, size=27, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'cyan'), ('res', 'res', 'green')],
    captions={
        'meetings.sort': '先按==结束时间==从小到大排序',
        'f = []': '`f` 逐场追加：它是个单调不降的「带着 end 的最优值」',
        'res = 0': '`res` 是真正的答案（不减 end）',
        'for index, (start': lambda S, B, r: ('会议都处理完了，`res` 就是答案' if 'index' in B and B['index'] == S['index'] else f'第 `{S.index}` 场：`[{S.start}, {S.end})`，收益 {S.rev}'),
        'if start < meetings[0][1]': lambda S, B, r: (
            f'`start = {S.start} < {S.meetings[0][1]}`（最早的结束时间）：左边放不下会议，它只能是第一场'
            if S.start < S.meetings[0][1] else f'`start = {S.start} >= {S.meetings[0][1]}`：左边至少能放第一场，要找前一场'),
        'res = max(res, rev)': '第一场没有空闲收益：`res = max(.., {rev})` = {res}',
        'f.append(rev - end)': '`f` 里先减去 `end`：`{rev} − {end} = {rev - end}`（下一场接上时再加回 start）',
        'f.append(max(f[-1], rev - end))': '`f` 取 `max(前一个, {rev} − {end})` = =={f[-1]}==，保持单调',
        'left = 0': '二分找最大的 `p`，满足 `end[p] <= start`：左边界 `left = 0`',
        'right = len(f) - 1': '右边界 `right = {right}`（只在已处理的前面会议里找）',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：还没收敛，继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：找到了 `p = {S.left}`'),
        'mid = (left': '取偏右的中点 `mid = {mid}`（`left = mid` 时不会死循环）',
        'if meetings[mid][1] <= start': lambda S, B, r: (
            f'`end[{S.mid}] = {S.meetings[S.mid][1]} <= start = {S.start}`：它放得下 → `left = mid`' if S.meetings[S.mid][1] <= S.start
            else f'`end[{S.mid}] = {S.meetings[S.mid][1]} > start = {S.start}`：放不下 → `right = mid − 1`'),
        'left = mid': '`left` → {left}',
        'right = mid - 1': '`right` → {right}',
        'v = f[left]': '`v = f[{left}] + rev + start = {f[left]} + {rev} + {start}` = =={v}==：`start` 抵掉 f 里减去的 end，剩下的差就是空闲收益',
        'res = max(res, v)': '`v` 里没有再减 end，可以直接更新答案：`res` = =={res}==',
        'f.append(max(f[-1], v - end))': '存回 `f` 时又要减掉自己的 end：`v − end = {v - end}` → `f` = {f}',
        'return res': '最大总收益 =={res}==',
    },
    cards=dict(
        one_liner='f 里提前减去 end，转移时加上 start 就等于加了空闲时间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选互不重叠的会议，得到收益；相邻两场之间每单位空闲时间多加 1',
                 '首场之前、末场之后的空闲不算；只选一场没有空闲收益',
                 '本视频：`[[3,5,4],[4,7,8],[8,10,3],[1,3,2]]` → `15`'],
        quote='对于f[index]而言……就需要直到f[p]中真正召开的最后一场会议q是哪一场……可以在更新f[index]时直接将end[q]的信息带上去，这样一来就不需要考虑这个q到底是哪一场会议了。',
        quote_src='—— yiduobo 题解原文',
        idea=['空闲时间 = `start − end[q]`，q 是前一场；不想记下 q',
              '于是 `f` 里存 `收益 − end`：接下一场时 `f[p] + rev + start` 自动包含空闲',
              '按结束时间排序，用二分找到最大的 `p`（`end[p] <= start`）'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`f` 的定义里减过 `end`，答案 `res` 要用没减 `end` 的 `v`',
                 '第一场用 `rev` 更新答案、不加 `start`，但存进 `f` 时仍要减 `end`',
                 '对比灵神：灵神把 `pre_max` 对齐到 `bisect_right`，这里手写二分'],
    ),
)
