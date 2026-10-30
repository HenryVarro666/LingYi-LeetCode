CONFIG = dict(
    num=1335, title='工作计划的最低难度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前 i 天的 DP + 倒序枚举求区间最大值',
    tags=['灵神题单', '动态规划', '难度分 2035'],
    code='''
class Solution(object):
    def minDifficulty(self, jobDifficulty, d):

        n = len(jobDifficulty)
        if n < d:
            return -1

        g = [jobDifficulty[0]]
        for j in range(1, n):
            g.append(max(jobDifficulty[j], g[-1]))

        for i in range(1, d):
            f = [0] * i
            for j in range(i, n):
                f.append(g[j - 1] + jobDifficulty[j])
                ma = max(jobDifficulty[j], jobDifficulty[j - 1])
                for k in range(j - 2, i - 2, -1):
                    f[-1] = min(f[-1], g[k] + ma)
                    ma = max(ma, jobDifficulty[k])
            
            g = f[:]
        
        return g[-1]
''',
    call='Solution().minDifficulty([7, 1, 7, 1, 4], 3)',
    expect=12,
    skip=['for k in range', 'for j in range(i'],
    views=[
        dict(type='array', var='jobDifficulty', label='jobDifficulty（蓝 = 今天最后一项 j，粉 = 今天从 k+1 开始）', h=200, cell=80,
             pointers={'j': 'blue', 'k': 'pink'},
             color=lambda S, i, v: 'blue' if i == S.get('j') else None),
        dict(type='array', var='g', label='g：前一天的结果（g[j] = 前 i 天做完前 j+1 项）', h=150, cell=80, color=lambda S, i, v: 'pink' if i == S.get('k') else None),
        dict(type='array', var='f', label='f：今天正在算的结果', h=150, cell=80, color=lambda S, i, v: 'green' if i == S.get('j') else None),
        dict(type='text', fn=lambda S: (f"今天最后一段 `a[{S['k'] + (0 if S.get('_line') == 19 else 1)}..{S['j']}]`，最大值 `ma` = =={S['ma']}==" if 'k' in S and 'ma' in S and 'j' in S and S['k'] < S['j'] else ''), size=26, h=50),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), ('ma', 'ma', 'orange')],
    captions={
        'if n < d': '`n = {n}`，`d = {d}`：每天至少一项，`n < d` 排不满 → 返回 -1',
        'g = [jobDifficulty[0]]': '`g[j]`：只用 1 天做完前 `j+1` 项，难度 = 前缀最大值。先放 `g[0]`',
        'g.append': '`g[{j}] = max(jobDifficulty[{j}], g[{j-1}])` = =={g[-1]}==：1 天只能整段一起做，取最大',
        'for i in range': '开始算第 `{i+1}` 天：`f` 只依赖前一天的 `g`（滚动掉 i 这一维）',
        'f = [0] * i': '前 `{i}` 项工作凑不满 `{i+1}` 天，状态不合法，占位 0（后面不会用到）',
        'f.append': '初始化：今天只做 `jobDifficulty[{j}]` 一项 → `{g[j-1]} + {jobDifficulty[j]}` = =={f[-1]}==',
        'ma = max(jobDifficulty': '今天做 `{j-1}..{j}` 两项，最大值 `ma = {ma}`；向前枚举起点',
        'f[-1] = min': '今天从 `{k+1}` 做到 `{j}`，前面 `g[{k}] = {g[k]}`，加 `ma = {ma}` = {g[k]+ma} → `f[{j}]` = =={f[-1]}==',
        'ma = max(ma,': '起点再往前扩一项 `jobDifficulty[{k}]`，`ma` 更新为 =={ma}==（倒序遍历顺便求区间最大）',
        'g = f[:]': '第 `{i+1}` 天算完，`g` 换成这一天的 `f` = `{f}`',
        'return g[-1]': '答案 `g[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] = 前 i 天做完前 j 项；今天的段倒着扩，顺便求最大值',
        complexity='时间 `O(dn^2)`，空间 `O(n)`',
        problem=['`d` 天按顺序做完所有工作，==每天至少一项==，一天难度 = 当天最大难度',
                 '求 `d` 天总难度最小值；`n < d` 时返回 -1',
                 '本视频：`[7,1,7,1,4]`，`d = 3`'],
        quote='首先，由于每天都必须完成至少一个工作，因此当j < i时，f[i][j]都是不合法的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先让今天只做第 `j` 项：`f[j] = g[j-1] + job[j]`',
              '再从 `j-1` 往前枚举今天的起点 `k`，`ma` 边走边更新，不用重算区间最大',
              '`g` 是前一天、`f` 是今天，用滚动数组去掉天数这一维'],
        summary=['时间 `O(dn^2)`，空间 `O(n)`',
                 '前 `i` 项里 `f` 用 0 占位，下标必须与 `j` 对齐',
                 'yiduobo 提到可以用单调栈优化到 `O(dn)`，原文没有实现',
                 '代码在 Python 3 下无需修改即可运行',
                 '对比灵神：灵神方法二用单调栈把转移降到均摊 `O(1)`'],
    ),
)
