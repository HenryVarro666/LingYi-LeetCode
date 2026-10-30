ARR, K = [1, 15, 7, 9, 2], 3


def _in_inner(S):
    return S.get('_line') in (8, 9) and S.get('j') is not None


def _formula(S):
    if S.get('_line') == 9:
        i, j, mx, f = S['i'], S['j'], S['mx'], S['f']
        return (f'最后一段 `arr[{j}..{i}]` 全变成 `{mx}`：`f[{j}] + {i - j + 1}×{mx}` = '
                f'`{f[j]} + {(i - j + 1) * mx}` = =={f[j] + (i - j + 1) * mx}==')
    return '`f[i+1] = max{ f[j] + (i-j+1)×max(arr[j..i]) }`，`j` 从 `i` 往左最多 `k` 个'


def _cap_mx(S, B, ret):
    i, j = S.i, S.j
    tail = '' if j == i else f'（`max({B.mx}, arr[{j}]={S.arr[j]})`，一边往左扩一边维护）'
    return f'最后一段扩到 `arr[{j}..{i}]`，长度 `{i - j + 1}`：段内最大值 `mx` = =={S.mx}=={tail}'


def _cap_f(S, B, ret):
    i, j, mx = S.i, S.j, S.mx
    cand = S.f[j] + (i - j + 1) * mx
    old = B.f[i + 1]
    verdict = f'更新 `f[{i + 1}]` = =={S.f[i + 1]}==' if S.f[i + 1] > old else f'不如之前的 `{old}`，`f[{i + 1}]` 不变'
    rest = '前面没有数了，`f[0] = 0`' if j == 0 else f'剩下的前缀 `arr[0..{j - 1}]` 最大和 `f[{j}] = {S.f[j]}`'
    return f'{rest}，加上 `{i - j + 1}×{mx}` = `{cand}` → {verdict}'


def _cap_i(S, B, ret):
    if B.get('i') == S.get('i'):
        return '所有 `f[i+1]` 都算完了'
    i = S.i
    lo = max(i - K + 1, 0)
    return f'计算 `f[{i + 1}]`：`arr[0..{i}]` 的最大和；最后一段起点 `j` 从 `{i}` 枚举到 `{lo}`'


CONFIG = dict(
    num=1043, title='分隔数组以得到最大和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP：枚举最后一段的起点',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maxSumAfterPartitioning(self, arr: List[int], k: int) -> int:
        n = len(arr)
        f = [0] * (n + 1)
        for i in range(n):
            mx = 0
            for j in range(i, max(i - k, -1), -1):
                mx = max(mx, arr[j])  # 一边枚举 j，一边计算子数组的最大值
                f[i + 1] = max(f[i + 1], f[j] + (i - j + 1) * mx)
        return f[n]
''',
    call=f'Solution().maxSumAfterPartitioning({ARR}, {K})',
    expect=63,
    skip=['mx = 0', 'for j in range'],
    max_steps=60,
    views=[
        dict(type='text', h=70, fn=_formula, size=26),
        dict(type='array', var='arr', h=200, label='arr（框 = 最后一段 arr[j..i]，会变成段内最大值 mx）', cell=96,
             window=('j', 'i'),
             pointers={'j': 'pink', 'i': 'blue'},
             dim=lambda S, k, v: S.get('i') is not None and k > S['i']),
        dict(type='array', var='f', h=210, label='f[i+1]：arr[0..i] 分隔后的最大和（f[0] = 0 是边界）', cell=96,
             pointers={'j': 'pink', 'i + 1': 'green'},
             color=lambda S, k, v: ('green' if k == S['i'] + 1 else 'pink' if k == S['j'] else None)
             if S.get('_line') == 9 else None,
             dim=lambda S, k, v: S.get('i') is not None and S.get('_line') != 10 and k > S['i'] + 1),
    ],
    watch=['k', ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('mx', 'mx', 'orange')],
    captions={
        'n = len(arr)': '`n = {n}`，`k = {k}`：每段长度最多 `{k}`',
        'f = [0] * (n + 1)': '`f[i+1]` 对应 `dfs(i)`；左边多插一个 `f[0] = 0`，对应递归边界 `dfs(-1) = 0`',
        'for i in range(n)': _cap_i,
        'mx = max(mx, arr[j])': _cap_mx,
        'f[i + 1] = max(': _cap_f,
        'return f[n]': '`f[n]` 就是 `dfs(n-1)`：整个数组分隔后的最大和 =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一段的起点 j，剩下的前缀是子问题',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['把 `arr` 分隔成若干长度 ==不超过 k== 的连续子数组',
                 '每段的值都变成该段的最大值，求变换后数组的最大和',
                 '示例：`arr = [1,15,7,9,2,5,10], k = 3` → `84`（`[15,15,15,9,10,10,10]`）',
                 '动画用前 5 个数：`arr = [1,15,7,9,2], k = 3` → `63`'],
        quote='去掉这段子数组，例如去掉 [2,5,10]，剩余的要解决的问题是 [1,15,7,9] 在分隔变换后能够得到的元素最大和。由于这是一个和原问题==相似的子问题==，所以可以用递归解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i)`：`arr[0..i]` 的最大和；枚举最后一段起点 `j ∈ [max(i-k+1,0), i]`',
              '`dfs(i) = max{ dfs(j-1) + (i-j+1)×max(arr[j..i]) }`，边界 `dfs(-1) = 0`',
              '`j` 从 `i` ==倒着==枚举，`mx` 顺手维护，段内最大值 `O(1)` 得到',
              '1:1 翻译成递推：`f` 整体右移一位，`f[i+1]` 对应 `dfs(i)`'],
        result='`f[5] = 63`：`[1,15,7 | 9,2]` → `[15,15,15,9,9]`，`45 + 18`',
        summary=['时间 `O(nk)`：`n` 个状态，每个枚举 `k` 个起点；空间 `O(n)`',
                 '易错：`j` 的下界是 `max(i-k+1, 0)`，`range` 写成 `max(i-k, -1)`（开区间）',
                 '易错：`mx` 要在每个 `i` 开始时重置，且必须倒序枚举 `j` 才能递推维护',
                 '记忆化搜索写法等价；只依赖前 `k` 个状态 → 可滚动成 `f[(i+1)%k]`，空间 `O(k)`'],
    ),
)
