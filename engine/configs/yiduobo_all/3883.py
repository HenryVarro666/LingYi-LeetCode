def _fm(S):
    s = S.get('s')
    if s is None or 'candidate' not in S:
        return '`candidate[s]` = 值域内数位和为 `s` 的所有数；`f[v]` = 当前位填 `v` 的方案数；`pre` = `f` 的前缀和'
    c = S['candidate'].get(s, [])
    return f'本轮 `digitSum = {s}`：候选 `{c}`；`f[v] = pre[v]`（上一位 `<= v` 的方案数之和）'


CONFIG = dict(
    num=3883, title='统计满足数位和数组的非递减数组数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP 滚动 + 前缀和 + 候选表',
    tags=['灵神题单·动态规划', '难度分 2172'],
    code='''
class Solution(object):
    def countArrays(self, digitSum):
        
        candidate = {}
        for v in range(12):
            s = 0
            x = v
            while x:
                s += x % 10
                x //= 10
            
            if s not in candidate:
                candidate[s] = []
            candidate[s].append(v)

        pre = [1] * 12
        mod = 10 ** 9 + 7
        for s in digitSum:
            f = [0] * 12
            if s in candidate:
                for v in candidate[s]:
                    f[v] = pre[v]
            pre[0] = f[0]
            for v in range(1, 12):
                pre[v] = pre[v - 1] + f[v]
                if pre[v] >= mod:
                    pre[v] -= mod

        return pre[-1]
''',
    call='Solution().countArrays([1, 2])',
    expect=3,
    skip=['for v in range(12)', 's = 0', 'x = v', 'while x', 's += x % 10', 'x //= 10', 'if s not in candidate',
          'candidate[s] = []', 'candidate[s].append(v)', 'if pre[v] >= mod', 'pre[v] -= mod', 24],
    views=[
        dict(type='text', h=70, size=24, fn=_fm),
        dict(type='array', var='f', label='f[v]：本位填 v 的方案数（黄 = 刚填的候选）', h=240, cell=80,
             pointers={'v': 'blue'},
             color=lambda S, i, x: 'yellow' if x else None),
        dict(type='array', var='pre', label='pre[v] = f[0] + … + f[v]（前缀和；下一轮用它）', h=240, cell=80,
             pointers={'v': 'pink'}),
    ],
    watch=[('s', 's', 'blue'), ('v', 'v', 'cyan'), ('pre[-1]', 'pre[-1]', 'green')],
    captions={
        4: '`candidate[s]`：值域内数位和为 `s` 的数。下面一个循环给 0..11 逐个算数位和并归类（太碎，不逐步展示）',
        16: '`pre`：上一位的前缀和。还没放任何数时，任何值都能接 → 全是 1',
        17: '答案要取模',
        18: lambda S, B, r: (f'处理 `digitSum` 的下一项：`s = {S.s}`' if S.s != B.get('s') else '`digitSum` 都处理完了'),
        19: '新开一行 `f` 全 0：数位和不合格的值，方案数就是 0',
        20: '数位和 `{s}` 的候选：`{candidate[s]}`',
        21: lambda S, B, r: (f'候选 `v = {S.v}`' if S.v != B.get('v') or B.get('v') is None else '这一位的候选都填完了'),
        22: '`f[{v}] = pre[{v}] = {f[v]}`：前一位取 `<= {v}` 的所有方案数之和',
        23: '`pre[0] = f[0] = {f[0]}`：前缀和从第 0 位开始',
        25: lambda S, B, r: f'`pre[{S.v}] = pre[{S.v - 1}] + f[{S.v}]` = {S.pre[S.v - 1]} + {S.f[S.v]} = =={S.pre[S.v]}==',
        29: '`pre[-1]` 是最后一位所有取值的方案数之和 = =={ret}==',
    },
    cards=dict(
        one_liner='f 只在数位和合格的位置有值，前缀和 pre 负责「前一个数 ≤ v」',
        complexity='时间 `O(n·U)`，空间 `O(U)`，`U = 5001`',
        problem=['`arr` 长 `n`，每项在 `[0, 5000]`，非递减，且 `arr[i]` 的数位和等于 `digitSum[i]`',
                 '数出不同的有效数组，对 `10^9+7` 取模；示例：`[1]` → `4`',
                 '本视频把值域 `5001` 缩成 `12`（只含 0..11），`digitSum = [1, 2]` → `3`'],
        quote='f[index][v] = f[index - 1][0] + f[index - 1][1] + ... + f[index - 1][v]',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index][v]`：前 `index+1` 个数有效、末位是 `v`；数位和不对就是 0',
              '否则前一个数 `<= v` 即可 → 上一轮 `f` 的前缀和 `pre[v]`',
              '先按数位和给 0..5000 分组 `candidate`，只遍历合格的候选；`f` 与 `pre` 滚动复用'],
        summary=['时间 `O(n·U)`，空间 `O(U)`',
                 '`pre` 初值全 1：空前缀，任何值都能接',
                 '`pre[0] = f[0]` 后再往右累加：别漏掉第 0 位',
                 '为了能在视频里看清数组，原文所有 `5001` 改成了 `12`，其余逐字不变；原文已是 Python 3 可运行写法',
                 '对比灵神：灵神只对同数位和的候选做双指针，不必扫整个值域'],
    ),
)
