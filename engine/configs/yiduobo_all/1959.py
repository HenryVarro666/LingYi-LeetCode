def _fview(S):
    f = S.get('f')
    n = len(S['nums'])
    if f is None:
        return None
    return [None] * (n - len(f)) + f[::-1]


def _w0(S):
    return S['cut_pos'] if 'cut_pos' in S and 'i' in S and S.get('_line') == 26 else None


def _formula(S):
    if 'i' not in S:
        return '`f[j]`：把 `nums[0..j]` 浪费的空间（不 resize 时 = 前缀最大 × 长度 − 前缀和）'
    i = S['i']
    if 'j' in S and 'cut_pos' in S:
        return f'最后一段 `[{S["cut_pos"]}..{S["j"]}]` 的浪费 = ==段内最大== × 段长 − 段内和'
    return f'第 `{i}` 轮：最多 resize `{i}` 次；`g` = 上一轮的 `f`'


def _cap_cut(S, B, ret):
    L = S.j - S.cut_pos + 1
    seg = S.s[S.j] - S.s[S.cut_pos - 1]
    cand = S.g[S.cut_pos - 1] + S.ma * L - seg
    return (f'`nums[{S.cut_pos}..{S.j}]` 作为最后一段：最大 `{S.ma}` × 长 `{L}` − 和 `{seg}` = `{S.ma * L - seg}`，'
            f'加前面 `g[{S.cut_pos - 1}] = {S.g[S.cut_pos - 1]}` → =={cand}==，' + (f'比当前 `{B.f[-1]}` 小 → 更新' if cand < B.f[-1] else f'不比当前 `{B.f[-1]}` 小 → 保持'))


CONFIG = dict(
    num=1959, title='K次调整数组大小浪费的最小空间', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分型 DP · 倒序枚举切分点维护区间最大',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minSpaceWastedKResizing(self, nums, k):

        f = [0]
        s = [nums[0]]
        ma = nums[0]
        n = len(nums)
        for index in range(1, n):
            ma = max(ma, nums[index])
            s.append(s[-1] + nums[index])
            f.append(ma * (index + 1) - s[-1])

        res = f[-1]

        for i in range(1, k + 1):
            g = f[:]
            f = []
            for j in range(n - 1, -1, -1):
                if j + 1 <= i:
                    f.append(0)
                else:
                    f.append(g[j - 1])
                    ma = nums[j]
                    for cut_pos in range(j - 1, i - 1, -1):
                        ma = max(nums[cut_pos], ma)
                        f[-1] = min(f[-1], g[cut_pos - 1] + ma * (j - cut_pos + 1) - s[j] + s[cut_pos - 1])

            f.reverse()
            res = min(res, f[-1])

        return res
''',
    call='Solution().minSpaceWastedKResizing([10, 20, 15, 30, 20], 1)',
    expect=25,
    skip=[4, 5, 6, 7, 8, 9, 10, 16, 17, 18, 23, 24, 25],
    views=[
        dict(type='text', fn=_formula, size=22, h=50),
        dict(type='array', var='nums', label='nums', window=(_w0, 'j'), pointers={'j': 'blue'}, h=150, cell=64),
        dict(type='array', var='s', label='s（前缀和）', h=110, cell=64, index=False),
        dict(type='array', var='g', label='g（上一轮：最多 i-1 次）', pointers={'cut_pos - 1': 'pink'}, h=165, cell=64),
        dict(type='array', var=_fview, label='f（本轮：按下标 j 对齐，倒序填入）', h=110, cell=64, index=False),
    ],
    watch=[('i', 'i', 'purple'), ('j', 'j', 'blue'), 'cut_pos', 'ma', ('res', 'res', 'green')],
    captions={
        11: '`f[{index}]` = 前 `{index + 1}` 个数一个容量不变：最大 `{ma}` × `{index + 1}` − 和 `{s[-1]}` = =={f[-1]}==',
        13: '`res = f[-1]` = =={res}==：一次都不 resize 的浪费，先当答案',
        15: lambda S, B, r: (f'第 `{S.i}` 轮（最多 resize `{S.i}` 次）：`g = f[:]` 存下上一轮，再从 `j = n-1` 倒着重算 `f`' if B.get('i') != S.i else '`k` 轮都做完了'),
        19: lambda S, B, r: (f'`j + 1 = {S.j + 1} <= i = {S.i}`：段数够，每个数自成一段，浪费 0' if S.j + 1 <= S.i
                             else f'`j = {S.j}`：`j + 1 = {S.j + 1} > i = {S.i}`，需要真正分段'),
        20: '`f` 末尾加入 `0`：每个数自成一段，没有浪费',
        22: '先假设最后一段只有 `nums[{j}]`（浪费 0）：`f` 末尾加入 `g[{j - 1}] = {g[j - 1]}`',
        26: _cap_cut,
        28: '`f` 是从 `j = n-1` 倒着填的 → `reverse()` 后 `f[j]` 才和下标 `j` 对齐',
        29: '`res = min(res, f[-1])` = =={res}==：用第 `{i}` 轮的整串结果更新答案',
        31: '最少浪费空间 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一段的起点，倒着扫顺手维护段内最大值',
        complexity='时间 `O(k·n²)`，空间 `O(n)`',
        problem=['数组 `nums[t]` 是第 `t` 秒的元素个数，容量可以随时调整，一共最多调整 `k` 次',
                 '某一刻容量必须 ≥ 元素个数，浪费 = 容量 − 元素个数，求总浪费的最小值',
                 '示例：`[10,20,15,30,20], k=2` → `15`；本视频取 `k=1` → `25`'],
        quote='因此可以调换一下求解的顺序，从j开始从后向前枚举cut_pos，这样一来就可以边求解f边更新max值',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[j]`：把前 `j+1` 个数分成若干段，每段容量取段内最大值，浪费最小是多少',
              '枚举最后一段的起点 `cut_pos`：浪费 = 前面的 `g` + 段最大 × 段长 − 段内和',
              '段内和用前缀和 `s`；`cut_pos` 从 `j` 往前走，段最大值 `ma` 边走边更新',
              '`i` 这一维只依赖上一轮，用 `g` 滚动'],
        summary=['时间 `O(k·n²)`，空间 `O(n)`',
                 '`f` 是倒着 `append` 的，每轮结束要 `f.reverse()` 才和下标对齐',
                 '`j + 1 <= i` 时每个数自成一段，浪费 `0`；`res` 取每一轮 `f[-1]` 的最小值（resize 次数不必用满）',
                 '原文为 Python 2 风格，本题无需改动，只是去掉了空行里的空格'],
    ),
)
