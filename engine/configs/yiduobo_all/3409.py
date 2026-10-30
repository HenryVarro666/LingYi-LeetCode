def _color(S, i, j, v):
    vv, d = S.get('v'), S.get('diff')
    if vv is None or d is None or S.get('_line') not in (15, 19, 25) or j != d:
        return None
    if i == vv:
        return 'yellow'
    if i in (vv + d, vv - d):
        return 'blue'
    return None


def _txt(S):
    if S.get('_line', 0) >= 28:
        return f"遍历所有 `f[v][diff]` 取最大值：当前 `res` = =={S.get('res')}=="
    if 'v' not in S or 'diff' not in S:
        return '`f[v][d]` = 以 v 结尾、最后两项差恰为 d 的最长长度；`best[v][d]` = d 及以上的最大值'
    v, d = S['v'], S['diff']
    return f"`v = {v}`，`diff = {d}`：倒数第二项是 `{v+d}` 或 `{v-d}`（蓝格），从 `best[·][{d}]` + 1 转移"


CONFIG = dict(
    num=3409, title='最长相邻绝对差递减子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='f + best 后缀最大值 · 按值开表',
    tags=['灵神题单', '难度分 2500'],
    code='''
class Solution(object):
    def longestSubsequence(self, nums):
        
        f = [[0] * 5 for _ in range(5)]
        best = [[0] * 5 for _ in range(5)]

        for diff in range(5):
            f[nums[0]][diff] = 1
            best[nums[0]][diff] = 1

        for v in nums[1:]:
            for diff in range(4):
                pre_v1 = v + diff
                if pre_v1 <= 4:
                    f[v][diff] = max(f[v][diff], best[pre_v1][diff] + 1)
                
                pre_v2 = v - diff
                if pre_v2 >= 1:
                    f[v][diff] = max(f[v][diff], best[pre_v2][diff] + 1)

            f[v][4] = 1
            best[v][4] = 1

            for diff in range(3, -1, -1):
                best[v][diff] = max(best[v][diff + 1], best[v][diff], f[v][diff])
        
        res = 0
        for v in range(1, 5):
            for diff in range(4):
                res = max(res, f[v][diff])
        
        return res
''',
    call='Solution().longestSubsequence([3,1,2,1])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=80),
        dict(type='table', var='f', label='f[v][diff]（行 = 末尾值 v，列 = 最后两项差）',
             rows=lambda S: [f'v={r}' for r in range(len(S['f']))],
             cols=lambda S: [f'd={c}' for c in range(len(S['f'][0]))],
             color=_color, h=250, cell=78),
        dict(type='table', var='best', label='best[v][diff]：差 >= diff 的最大值',
             rows=lambda S: [f'v={r}' for r in range(len(S['best']))],
             cols=lambda S: [f'd={c}' for c in range(len(S['best'][0]))],
             color=_color, h=250, cell=78),
        dict(type='text', h=90, size=24, fn=_txt),
    ],
    watch=[('v', 'v', 'pink'), ('diff', 'diff', 'blue'), ('res', 'res', 'green')],
    captions={
        4: '`f[v][diff]`：以 `v` 结尾、最后两项差为 `diff` 的最长长度（演示把 301 缩成 5）',
        5: '`best[v][diff]`：`f[v][diff..]` 的后缀最大值，转移时 O(1) 取；第一个数 `{nums[0]}` 先自己成长度 1 的子序列（初始化，快进）',
        8: '第一个数 `{nums[0]}` 自己成一个子序列：长度 1，任何 `diff` 都成立',
        14: lambda S, B, r: f'前一项可以是 `v + diff = {S.pre_v1}`：{"范围内" if S.pre_v1 <= 4 else "越界"}',
        15: '`v + diff = {pre_v1}` 在范围内：接在 `{pre_v1}` 结尾、前一差 >= {diff} 的数列后：`f[{v}][{diff}] = {f[v][diff]}`',
        18: lambda S, B, r: f'前一项也可以是 `v − diff = {S.pre_v2}`：{"范围内" if S.pre_v2 >= 1 else "越界"}',
        19: '`v − diff = {pre_v2}` 在范围内：接在 `{pre_v2}` 结尾、前一差 >= {diff} 的数列后：`f[{v}][{diff}] = {f[v][diff]}`',
        21: '`diff` 取最大哨兵时，`v` 自己单独成一个子序列：`f[v][4] = 1`',
        25: '倒序更新后缀最大值：`best[{v}][{diff}] = max(best[{v}][{diff+1}], 自己, f[{v}][{diff}])` = =={best[v][diff]}==',
        30: '答案 = 所有 `f` 的最大值：`res` = =={res}==',
        27: '最后遍历所有 `f[v][diff]`，取最大的那个（共 4×4 格，这里直接快进）',
        32: '遍历完整张 `f`：最大值 `res` = =={res}==，即最长子序列长度',
    },
    skip=[7, 8, 9, 12, 13, 14, 17, 18, 21, 22, 24, 28, 29, 30],
    cards=dict(
        one_liner='f 记恰好的差，best 记「差 >= d」的最大值，转移 O(1)',
        complexity='时间 `O(nD)`，空间 `O(U^2)`，`U = 300`',
        problem=['求 `nums` 的最长子序列，使相邻项 ==绝对差单调不增==',
                 '示例：`[6,5,3,4,2,1]` → `4`',
                 '本视频：`[3,1,2,1]` → `4`（差 2,1,1）'],
        quote='可以令best[v][diff] = max(f[v][diff], f[v][diff + 1], ..., f[v][300])，那么上面的式子就可以写成 f[v][diff] = max(f[v][diff], best[pre_v1][diff] + 1)',
        quote_src='—— yiduobo 题解原文',
        idea=['状态要有「末尾值 v」和「最后两项差 diff」',
              '倒数第二项是 `v ± diff`，且再前面的差 `>= diff`，是个后缀最大值',
              '用 `best` 保存后缀最大值，倒序遍历 `diff` 更新，转移就是 O(1)'],
        summary=['时间 `O(nD)`，空间 `O(U^2)`，原题 `U = 300`',
                 '为方便演示，原文的 `301` 缩成了 `5`、`300` 缩成了 `4`（示例值都在 1..4），逻辑不变',
                 '易错：哨兵 `diff = 300` 要先置 1，倒序更新才能带出后缀最大值',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用一个变量 `fx` 带后缀最大值；yiduobo 多开一张 `best` 表'],
    ),
)
