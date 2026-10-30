ARR, K = [3, -4, 1, 2], 3   # 元素互不相同：可以由 x 反推下标
D = ARR * 2


def _kadane(a):
    f, st, fs, starts = 0, 0, [], []
    for i, x in enumerate(a):
        if f <= 0:
            st = i
        f = max(f, 0) + x
        fs.append(f)
        starts.append(st)
    return fs, starts


FS, STARTS = _kadane(D)
POS = "_ * len(nums) + nums.index(x)"


def _pos(S):
    try:
        return S['_'] * len(S['nums']) + S['nums'].index(S['x'])
    except Exception:
        return None


def _f_line(S):
    return S.get('_line') in (L_F, L_ANS)


CODE = '''
class Solution:
    # 53. 最大子数组和（遍历 nums repeat 次）
    def maxSubArray(self, nums: List[int], repeat: int) -> int:
        ans = f = 0  # 本题允许子数组为空，ans 可以初始化成 0
        for _ in range(repeat):
            for x in nums:
                f = max(f, 0) + x
                ans = max(ans, f)
        return ans

    def kConcatenationMaxSum(self, arr: List[int], k: int) -> int:
        if k == 1:
            return self.maxSubArray(arr, 1)  # arr 的最大子数组和
        ans = self.maxSubArray(arr, 2)  # arr+arr 的最大子数组和
        ans += max(sum(arr), 0) * (k - 2)
        return ans % 1_000_000_007
'''
_LINES = CODE.strip('\n').split('\n')
L_F = [i + 1 for i, t in enumerate(_LINES) if 'f = max(f, 0) + x' in t][0]
L_ANS = [i + 1 for i, t in enumerate(_LINES) if 'ans = max(ans, f)' in t][0]
L_RET2 = [i + 1 for i, t in enumerate(_LINES) if 'ans = self.maxSubArray(arr, 2)' in t][0]
_E = FS.index(max(FS))
BEST = (STARTS[_E], _E)


def _win(k):
    def f(S):
        p = _pos(S)
        if p is None or not _f_line(S):
            return None
        return STARTS[p] if k == 0 else p
    return f


def _fvals(S):
    p = _pos(S)
    if p is None:
        # 回到 kConcatenationMaxSum 之后，f 全部算完
        return FS if 'ans' in S and 'arr' in S and S.get('_line', 0) > L_ANS else None
    upto = p if S.get('_line') in (L_F, L_ANS) else p - 1
    return [FS[i] if i <= upto else None for i in range(len(D))]


def _text(S):
    if 'nums' in S and 'x' in S:
        return '第 1 步：用 53 题的 DP 求 ==arr + arr== 的最大子数组和'
    if 'ans' in S and 'arr' in S and S.get('_line', 0) > L_ANS + 2:
        return f"第 2 步：`sum(arr) = {sum(S['arr'])} > 0` → 中间 `k − 2 = {S['k'] - 2}` 个完整 arr ==必须全部包含=="
    return '`k ≥ 2`：只需要 arr + arr 的最大子数组和，再看 `sum(arr)` 的正负'


def _fcap(S, B, r):
    if B.f <= 0:
        return f'`f = {B.f} ≤ 0`：前面的拖后腿，==从 x = {S.x} 重新开始== → `f = {S.f}`'
    xs = f'({S.x})' if S.x < 0 else S.x
    return f'`f = {B.f} > 0`：接在前面的子数组后面 → `f = {B.f} + {xs} = {S.f}`'


CONFIG = dict(
    num=1191, title='K 次串联后最大子数组之和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='复用 53 题 · arr+arr 的最大子数组和',
    tags=['字节30天'],
    code=CODE,
    call=f'Solution().kConcatenationMaxSum({ARR}, {K})',
    expect=8,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='array', var=lambda S: D, label='arr + arr（蓝框 = f 对应的子数组，即以 x 结尾的最优子数组）', cell=84,
             pointers={POS: 'blue'}, pointer_labels={POS: 'x'}, window=(_win(0), _win(1)), h=210),
        dict(type='array', var=_fvals, label='f：以该位置结尾的最大子数组和（绿 = 当前 ans）', cell=84, h=150,
             color=lambda S, i, v: 'green' if v is not None and v == S.get('ans') and v > 0 else None),
        dict(type='array', var=lambda S: ARR * K if S.get('_line', 0) > L_RET2 else None,
             label=f'arr 重复 k = {K} 次：答案 = arr+arr 的最优子数组中间插入 k − 2 个完整 arr', cell=60, h=150,
             window=(lambda S: BEST[0] if S.get('_line', 0) > L_RET2 else None,
                     lambda S: BEST[1] + len(ARR) * (K - 2) if S.get('_line', 0) > L_RET2 else None),
             window_color='green'),
    ],
    watch=[('_', '_'), ('x', 'x', 'blue'), ('f', 'f'), ('ans', 'ans', 'green'), ('k', 'k')],
    captions={
        'if k == 1': '`k = {k}` ≠ 1：k = 1 时就是 53 题本身',
        'ans = self.maxSubArray(arr, 2)': '先求 ==arr + arr== 的最大子数组和：直接调用 53 题的代码，遍历两遍',
        'ans = f = 0': '`ans = f = 0`：本题允许子数组为空，答案最小是 0',
        'for _ in range(repeat)': lambda S, B, r: (f'第 `{S._ + 1}` 遍 arr' if S.get('_') != B.get('_') or '_' not in B else '两遍都走完了'),
        'for x in nums': lambda S, B, r: (f'`x = {S.x}`（arr + arr 的第 `{_pos(S)}` 个）' if S.get('x') != B.get('x') or 'x' not in B
                                          else '这一遍走完了'),
        'f = max(f, 0) + x': _fcap,
        'ans = max(ans, f)': '`ans = max({B.ans}, {f}) = {ans}`',
        'ans += max(sum(arr), 0)': '`sum(arr) = {sum(arr)}` > 0：插入 `k − 2 = {k - 2}` 个完整 arr → `ans += {sum(arr)} × {k - 2}` = =={ans}==',
        'return ans % 1_000_000_007': '别忘了取模：返回 =={ret}==',
        'return ans': lambda S, B, r: f'arr + arr 的最大子数组和是 =={r}==',
    },
    cards=dict(
        one_liner='只需算 arr+arr 的最大子数组和；sum(arr) > 0 时再补上中间 k−2 份',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把整数数组 `arr` 重复 `k` 次，求修改后数组的==最大子数组和==',
                 '子数组可以为空（和为 0）；结果对 `10^9 + 7` 取模',
                 '示例：`[1,2], k = 3` → `9`；`[1,-2,1], k = 5` → `2`',
                 '示例：`[-1,-2], k = 7` → `0`（取空子数组）',
                 '本视频：`arr = [3,-4,1,2]`，`k = 3` → `8`'],
        quote='定理：设 s 是 arr 的元素和。如果 s>0，那么 arr+arr 的最大子数组和==必然横跨两个 arr==。……这中间的 (k−2) 的 arr ==必须全部包含==。',
        quote_src='—— 灵茶山艾府题解：复用 53 题代码',
        idea=['`k = 1`：就是 53 题；`k ≥ 2`：先求 arr + arr 的最大子数组和',
              '`s < 0`：最优子数组不会包含完整的 arr（去掉它反而更大）',
              '`s > 0`：在中间插入 `k − 2` 个完整 arr，答案 `+ s·(k−2)`'],
        summary=['时间 `O(n)`：arr + arr 只遍历两遍，不用真的拼接',
                 '53 题的 DP：`f = max(f, 0) + x`，`ans` 初始化为 0（允许空子数组）',
                 '易错：别忘了取模；其他语言要小心 `s·(k−2)` 乘法溢出',
                 '`s = 0` 时包不包含中间的 arr 都一样'],
    ),
)
