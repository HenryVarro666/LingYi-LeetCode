ARR, K = [1, 15, 7, 9, 2], 3


def _formula(S):
    line = S.get('_line')
    if line in (9, 13) and S.get('j') is not None:
        i, j, ma, f = S['i'], S['j'], S['ma'], S['f']
        p = i - j + 1
        return (f'分组 `arr[{j}..{i}]`（{p} 个数）：`f[{j}] + ma×{p}` = `{f[j]} + {ma}×{p}` = =={f[j] + ma * p}==')
    return '`f[i] = max(f[i-p] + max(arr[i-p..i-1]) × p)`，`p = 1..k`'


def _cap_while(S, B, ret):
    i, j = S.i, S.j
    if j > 0 and j > i - S.k + 1:
        return f'`j = {j} > 0` 且这一组只有 `{i - j + 1}` 个数 `< k` → 还能把 `arr[{j - 1}]` 也拉进这一组'
    if j == 0:
        return f'`j = 0`：已经拉到数组开头，`f[{i + 1}]` = =={S.f[i + 1]}== 定下来了'
    return f'这一组已经有 `{i - j + 1} = k` 个数，不能再扩 → `f[{i + 1}]` = =={S.f[i + 1]}=='


def _cap_first(S, B, ret):
    i = S.i
    rest = '前面没有数' if i == 0 else f'前 `{i}` 个数最大和 `f[{i}] = {S.f[i]}`'
    return f'`arr[{i}] = {S.ma}` 单独一组（`ma = arr[{i}]`）：{rest}，`f[{i + 1}] = {S.f[i]} + {S.ma}` = =={S.f[i + 1]}=='


def _cap_ma(S, B, ret):
    j = S.j
    return f'组扩成 `arr[{j}..{S.i}]`：`ma = max({B.ma}, arr[{j}]={S.arr[j]})` = =={S.ma}==（利用上一次的最大值）'


def _cap_f(S, B, ret):
    i, j, ma = S.i, S.j, S.ma
    p = i - j + 1
    cand = S.f[j] + ma * p
    old = B.f[i + 1]
    tail = f'更新 `f[{i + 1}]` = =={S.f[i + 1]}==' if S.f[i + 1] > old else f'不如 `{old}`，`f[{i + 1}]` 不变'
    return f'前 `{j}` 个数 `f[{j}] = {S.f[j]}` + `{ma}×{p}` = `{cand}` → {tail}'


CONFIG = dict(
    num=1043, title='分隔数组以得到最大和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='DP：分组往左扩，顺手维护组内最大值',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maxSumAfterPartitioning(self, arr, k):

        n = len(arr)
        f = [0] * (n + 1)
        for i in range(n):
            ma = arr[i]
            j = i
            f[i + 1] = f[j] + ma
            while j > 0 and j > i - k + 1:
                j -= 1
                ma = max(ma, arr[j])
                f[i + 1] = max(f[i + 1], f[j] + ma * (i - j + 1))

        return f[-1]
''',
    call=f'Solution().maxSumAfterPartitioning({ARR}, {K})',
    expect=63,
    skip=['ma = arr[i]', 'j = i', 'j -= 1'],
    max_steps=60,
    views=[
        dict(type='text', h=70, fn=_formula, size=26),
        dict(type='array', var='arr', h=200, label='arr（框 = 包含 arr[i] 的最后一组 arr[j..i]）', cell=96,
             window=('j', 'i'),
             pointers={'j': 'pink', 'i': 'blue'},
             dim=lambda S, k, v: S.get('i') is not None and k > S['i']),
        dict(type='array', var='f', h=210, label='f[i]：前 i 个数能得到的最大和', cell=96,
             pointers={'j': 'pink', 'i + 1': 'green'},
             color=lambda S, k, v: ('green' if k == S['i'] + 1 else 'pink' if k == S['j'] else None)
             if S.get('_line') in (9, 13) else None,
             dim=lambda S, k, v: S.get('i') is not None and S.get('_line') != 15 and k > S['i'] + 1),
    ],
    watch=['k', ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ma', 'ma', 'orange')],
    captions={
        'n = len(arr)': '`n = {n}`，`k = {k}`：每组最多 `{k}` 个数',
        'f = [0] * (n + 1)': '`f[i]` 表示==前 i 个数==能得到的最大和，`f[0] = 0`',
        'for i in range(n)': lambda S, B, r: ('所有 `f` 都算完了' if B.get('i') == S.get('i')
                                              else f'计算 `f[{S.i + 1}]`：看 `arr[{S.i}]` 和它左边的数怎么分组'),
        'f[i + 1] = f[j] + ma': _cap_first,
        'while j > 0': _cap_while,
        'ma = max(ma, arr[j])': _cap_ma,
        'f[i + 1] = max(': _cap_f,
        'return f[-1]': '`f[-1] = f[n]`：整个数组的最大和 =={ret}==',
    },
    cards=dict(
        one_liner='f[i] = 前 i 个数的最大和；最后一组往左扩，ma 跟着更新',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['把 `arr` 分隔成若干长度 ==不超过 k== 的连续子数组',
                 '每段的值都变成该段的最大值，求变换后数组的最大和',
                 '示例：`arr = [1,15,7,9,2,5,10], k = 3` → `84`',
                 '动画用前 5 个数：`arr = [1,15,7,9,2], k = 3` → `63`'],
        quote='可以发现对于随着分组的增大，arr取max的范围也是在逐渐增大，那么我们就可以按这个顺序进行计算，这样一来==每一轮计算分组中arr的最大值时就可以利用上一次的结果==。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]`：前 `i` 个数的最大和；最后一组可以是 `arr[i-1]` 单独、和 `arr[i-2]` 一组…最多 `k` 个',
              '`f[i] = max(f[i-p] + max(arr[i-p..i-1]) × p)`，`p = 1, 2, …, k`',
              '`p` 每加 1，组里只多一个数：`max_{p+1} = max(max_p, 新数)`',
              '所以 `while` 往左扩一格，`ma` 更新一次，整体 `O(nk)`'],
        result='`f[5] = 63`：`[1,15,7 | 9,2]` → `15×3 + 9×2`',
        summary=['时间 `O(nk)`，空间 `O(n)`',
                 '先单独成组初始化 `f[i+1] = f[i] + arr[i]`，再 `while` 往左扩',
                 '易错：`while` 条件 `j > i - k + 1` 保证组长 `i - j + 1 ≤ k`；`j > 0` 防越界',
                 '易错：`ma` 每轮要从 `arr[i]` 重新开始，不能沿用上一个 `i` 的',
                 '原文为 Python 2 风格写法，删去了 docstring，其余照搬'],
    ),
)
