CONFIG = dict(
    num=2100, title='适合野炊的日子', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解（Go 原文转写）',
    tags=['专题：前后缀分解', '难度分 1702'],
    code='''
class Solution:
    def goodDaysToRobBank(self, security: List[int], time: int) -> List[int]:
        n = len(security)
        ans = []
        if time * 2 >= n:  # i 最小为 time，而且需要满足 i+time<n，即 time*2<n，不满足则直接返回空数组
            return ans

        suf = [0] * n  # suf[i] 表示从 security[i+1] 向后的最长连续非递减长度
        for i in range(n - 2, time - 1, -1):
            if security[i] <= security[i + 1]:
                suf[i] = suf[i + 1] + 1

        pre = 0  # pre 表示从 security[i-1] 向前的最长连续非递增长度
        for i, v in enumerate(security[:n - time]):
            if i > 0 and v <= security[i - 1]:
                pre += 1
            else:
                pre = 0
            if pre >= time and suf[i] >= time:
                ans.append(i)
        return ans
''',
    call='Solution().goodDaysToRobBank([5,3,3,3,5,6,2], 2)',
    expect=[2, 3],
    views=[
        dict(type='array', var='security', label='security', pointers={'i': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if 'ans' in S and i in S['ans'] else None),
        dict(type='array', var='suf', label='suf：向后连续非递减长度', pointers={'i': 'blue'}, h=170,
             color=lambda S, i, v: 'cyan' if v >= S['time'] else None),
        dict(type='text', h=70, fn=lambda S: f"`pre` = =={S['pre']}==（向前连续非递增长度），需要 `>= time = {S['time']}`" if 'pre' in S else f"`time = {S['time']}`：山谷两侧都至少要连续 {S['time']} 天"),
        dict(type='array', var='ans', label='ans：适合野炊的日子', h=150),
    ],
    watch=['i', ('time', 'time', 'cyan'), 'pre', ('ans', 'ans', 'green')],
    captions={
        'if time * 2 >= n': '最小的 `i` 是 `time`，还要 `i + time < n`，所以要 `time * 2 < n`：`{time * 2} >= {n}` → 不成立，继续',
        'suf = [0] * n': '`suf[i]`：从 `i` 往后能连续非递减多少天，先全设 0',
        'for i in range(n - 2': '倒着算 suf：`i` 从 `n-2` 到 `time`',
        'if security[i] <= security[i + 1]': '`security[{i}] = {security[i]}` 与 `security[{i + 1}] = {security[i + 1]}`：{"前者不大于后者，非递减链能接上" if security[i] <= security[i + 1] else "前者更大，链断了，suf 保持 0"}',
        'suf[i] = suf[i + 1] + 1': '`suf[{i}] = suf[{i + 1}] + 1` → =={suf[i]}==',
        'pre = 0  #': '`pre` 从前往后滚动记录：向前连续非递增的长度',
        'for i, v in enumerate': '正着枚举山谷 `i`，只需到 `n - time - 1`（右边要留够 time 天）',
        'if i > 0 and v <= security[i - 1]': '`{v}` 与前一天 `{security[i - 1] if i > 0 else "无"}`：{"不大于前一天，非递增链延长" if i > 0 and v <= security[i - 1] else "接不上，链重新开始"}',
        'pre += 1': '`pre` += 1 → =={pre}==',
        18: '这一天接不上，`pre` 清零，重新计数',
        'if pre >= time and suf[i] >= time': '`pre = {pre}`，`suf[{i}] = {suf[i]}`，都 `>= {time}`？→ {"成立，第 i 天适合" if pre >= time and suf[i] >= time else "不成立"}',
        'ans.append(i)': '第 `{i}` 天左右两侧都满足 → 加入答案 `{ans}`',
    },
    cards=dict(
        one_liner='前后缀分解：左边连续非递增、右边连续非递减，各算一遍长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`security[i]` 是第 i 天的出行指数；第 i 天前 time 天非递增、后 time 天非递减，就适合野炊',
                 '返回所有适合的日子下标',
                 '示例：`[5,3,3,3,5,6,2], time=2` → `[2,3]`'],
        quote='suf[i] 表示从 security[i+1] 向后的最长连续非递减长度；pre 表示从 security[i-1] 向前的最长连续非递增长度。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先倒着扫一遍，算出每天向后的连续非递减长度 `suf`',
              '再正着扫，用一个变量 `pre` 滚动算向前的非递增长度，不必开数组',
              '两个长度都 `>= time` 就是答案；`i` 只需枚举到 `n - time`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：`time * 2 >= n` 直接返回空；等号（`<=`）表示相等也算非递增/非递减',
                 '同类：前后缀分解题（如接雨水、除自身以外数组的乘积）'],
    ),
)
