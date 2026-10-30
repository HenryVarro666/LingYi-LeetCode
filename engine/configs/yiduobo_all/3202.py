def _txt(S):
    r, v = S.get('r'), S.get('v')
    if r is None:
        return '固定相邻两项之和模 `k` 的余数 `r`，用 `f[j]` 记录「以 j 结尾」的最长长度'
    if v is None or S.get('_line', 0) < 8:
        return f'这一轮：相邻项之和模 `{S["k"]}` == `{r}`，`f` 重新清零'
    return f'`v = {v}`：只能接在 `{(r - v) % S["k"]}` 结尾的后面（`{r} - {v}` 模 `{S["k"]}`），所以 `f[{v}] = f[{(r - v) % S["k"]}] + 1`'


CONFIG = dict(
    num=3202, title='找出有效子序列的最大长度 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举余数 r · 以结尾值为状态',
    tags=['灵神题单', '动态规划', '难度分 1974'],
    code='''
class Solution(object):
    def maximumLength(self, nums, k):

        nums = [v % k for v in nums]

        res = 0
        for r in range(k):
            f = [0] * k
            for v in nums:
                if r >= v:
                    f[v] = f[r - v] + 1
                else:
                    f[v] = f[k + r - v] + 1
            
            res = max(res, max(f))
        
        return res
''',
    call='Solution().maximumLength([1,4,2,3,1,4], 3)',
    expect=4,
    max_steps=70,
    skip=['for v in nums'],
    views=[
        dict(type='array', var='nums', label='nums（已模 k）', h=150, cell=80),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='f', label='f[j]：以 j 结尾、相邻和模 k = r 的最长长度', h=190, cell=90,
             pointers={'v': 'pink'}),
    ],
    watch=[('r', 'r', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green'), ('k', 'k', 'cyan')],
    captions={
        'nums = [v % k': '先把每个数模 `k`，不影响相邻和模 `k` 的结果：`nums = {nums}`',
        'res = 0': '`res` 记录各个 `r` 下的最优长度',
        'for r in range': '枚举相邻两项之和模 `k` 的结果 `r`',
        'f = [0] * k': '`r = {r}`：新建 `f`，`f[j]` 表示以 `j` 结尾的最长子序列',
        'if r >= v': lambda S, B, rr: (f'`r = {S.r} ≥ v = {S.v}` → 前一项是 `r - v = {S.r - S.v}`' if S.r >= S.v
                                        else f'`r = {S.r} < v = {S.v}` → 要补一个 `k`：前一项是 `r + k - v = {S.r + S.k - S.v}`'),
        'f[v] = f[r - v] + 1': '接在 `{r - v}` 结尾的子序列后：`f[{v}] = f[{r - v}] + 1` = =={f[v]}=={"" if f[v] > 1 else "（前面没有，从头算起）"}',
        'f[v] = f[k + r - v] + 1': '接在 `{k + r - v}` 结尾的子序列后：`f[{v}] = f[{k + r - v}] + 1` = =={f[v]}==',
        'res = max': '这一轮最长是 `max(f)` = `{max(f)}`，`res = max({B.res}, {max(f)})` = =={res}==',
        'return res': '所有 `r` 里最长的有效子序列长度 = =={ret}==',
    },
    cards=dict(
        one_liner='固定相邻和的余数 r，前一项就由当前项唯一确定',
        complexity='时间 `O(k(n+k))`，空间 `O(k)`',
        problem=['有效子序列：相邻两项之和对 `k` 取模，结果全部相等',
                 '求 `nums` 里最长有效子序列的长度',
                 '示例：`[1,4,2,3,1,4], k = 3` → `4`（`[1,4,1,4]`）'],
        quote='接下来可以尝试从0到k - 1枚举子序列相邻项之和对k的取模结果r。确定了这个r之后，就可以尝试用动态规划来求解了。',
        quote_src='—— yiduobo 题解原文',
        idea=['上一题（`k = 2`）可以分情况；这题余数有 `k` 种，要找普适做法',
              '枚举 `r` 后，当前项 `v` 的前一项必为 `(r - v) % k`',
              '`f[v] = f[前一项] + 1`；`v > r` 时要 +k 才不为负'],
        summary=['时间 `O(k·(n+k))`，空间 `O(k)`',
                 '易错：`r < v` 时前一项是 `k + r - v`，不能直接用负数下标',
                 '`f` 每个 `r` 都要重新清零',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神方法一不枚举余数，直接记最后两项 `f[y][x]`'],
    ),
)
