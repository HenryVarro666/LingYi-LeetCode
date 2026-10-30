def _info(S):
    if 'i' not in S:
        return '`arr[i-k] <= arr[i]` → 下标差 `k` 的元素连成一条链，==各组互不影响=='
    i, k = S['i'], S['k']
    return f"第 {i} 组（下标 ≡ {i} mod {k}）：`{S['arr'][i::k]}`，要让它==非降=="


def _color(S, idx, v):
    if 'i' not in S:
        return None
    if idx % S['k'] == S['i']:
        j = S.get('j')
        return 'orange' if (j == idx and S['_line'] in (7, 8, 9, 10, 11, 13)) else 'cyan'
    return None


def _dim(S, idx, v):
    return 'i' in S and idx % S['k'] < S['i']


def _for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return f'`{S.k}` 组都处理完了，`save = {S.save}` 个元素不用改'
    return f"第 {S.i} 组：下标 `{S.i}, {S.i}+{S.k}, …` 的元素 `{S.arr[S.i::S.k]}`，==各自求最长非降子序列=="


def _for_j(S, B, ret):
    if 'j' in B and B.j == S.j:
        return f'这一组取完了：`f = {S.f}`，长度 `{len(S.f)}`'
    return f'取这一组的下一个数：`arr[{S.j}] = {S.arr[S.j]}`'


def _if(S, B, ret):
    if S.p < len(S.f):
        return f'`p = {S.p} < len(f) = {len(S.f)}`：`f[{S.p}] = {S.f[S.p]}` 比 `v = {S.v}` 大 → 用 `v` 把它换掉'
    return f'`p = {S.p} == len(f)`：`f` 里没有比 `v = {S.v}` 大的数 → `v` 可以接在末尾'


CONFIG = dict(
    num=2111, title='使数组 K 递增的最少操作次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按下标模 k 分组 · 每组最长非降子序列（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1941'],
    code='''
class Solution:
    def kIncreasing(self, arr: List[int], k: int) -> int:
        save = 0
        n = len(arr)
        for i in range(min(k, n)):
            f = []
            for j in range(i, n, k):
                v = arr[j]
                p = bisect_left(f, v + 1)
                if p < len(f):
                    f[p] = v
                else:
                    f.append(v)
            save += len(f)
        return len(arr) - save
''',
    call='Solution().kIncreasing([5, 2, 3, 2, 4, 1], 2)',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='arr', label='arr（青 = 当前这一组，橙 = 正在处理的 arr[j]，暗 = 已处理的组）', cell=100,
             pointers={'j if _line in (7, 8, 9, 10, 11, 13) else None': 'pink'}, pointer_labels={'j if _line in (7, 8, 9, 10, 11, 13) else None': 'j'},
             color=_color, dim=_dim, h=200),
        dict(type='array', var='f', label='f（这一组当前最长非降子序列的「末尾」；长度 = 能保留的个数）', cell=100, min_slots=3,
             pointers={'p if _line in (9, 10, 11, 13) else None': 'yellow'}, pointer_labels={'p if _line in (9, 10, 11, 13) else None': 'p'},
             color=lambda S, idx, v: 'green', h=200),
        dict(type='text', fn=lambda S: f"已保留 `save = {S['save']}` 个，需要修改 `len(arr) − save = {len(S['arr']) - S['save']}` 个" if 'save' in S else '', size=24, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'v', ('p', 'p', 'yellow'), ('save', 'save', 'green')],
    captions={
        'save = 0': '`save` 记录==不用修改==的元素总数 = 每一组最长非降子序列的长度之和',
        'n = len(arr)': '`n = len(arr) = {n}`，一共有 `k = {k}` 组',
        'for i in range': _for_i,
        'f = []': '新开一组：`f = []`。`f[x]` 是长度为 `x+1` 的非降子序列的==最小末尾==',
        'for j in range': _for_j,
        'v = arr[j]': '`v = arr[{j}] = {v}`：看它能接在 `f = {f}` 的哪里',
        'p = bisect_left': '在 `f = {f}` 里二分，找第一个 `>= v + 1`（即第一个 ==大于 v==）的位置：`p = {p}`',
        'if p < len(f)': _if,
        'f[p] = v': '`f[{p}]` 由 `{B.f[p]}` 换成 `{v}`：长度不变，==末尾更小==，后面的数更容易接上',
        'f.append(v)': '`f` 末尾加入 `{v}`：这一组的非降子序列变长了，`len(f) = {len(f)}`',
        'save += len(f)': '这一组最长非降子序列长度 `{len(f)}`，这些数不用改：`save = {B.save} + {len(f)} = {save}`',
        'return len(arr)': '需要修改的个数 = 总数 − 保留的 = `{len(arr)} − {save} = {ret}`',
    },
    cards=dict(
        one_liner='下标模 k 分成 k 组，每组留下最长非降子序列，其余都要改',
        complexity='时间 `O(n log n)`，空间 `O(n / k)`（每组一个 `f`）',
        problem=['`arr` 是 K 递增：对每个 `i >= k`，都有 `arr[i-k] <= arr[i]`',
                 '一次操作可把任意一个数改成任意正整数',
                 '求把 `arr` 变成 K 递增的==最少操作次数==',
                 '本视频：`arr = [5,2,3,2,4,1]`，`k = 2` → `2`'],
        quote='将 arr 每 k 个数取一个元素，分为若干组……组与组之间是互不影响的，我们需要让每一组内的元素单调不降。题目要求需要修改的最少元素个数，这可以通过求不需要修改的最多元素个数来求出，也就是该组元素的最长不降子序列的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`arr[i-k] <= arr[i]` 只把下标差 `k` 的元素连起来 → 按下标模 `k` ==分成 k 组==，每组独立',
              '每组要非降：最少改动 = 组长 − ==最长非降子序列长度==',
              '求 LNDS 用二分：在 `f` 里找==第一个大于 v 的位置==替换或追加',
              '所有组保留的个数加起来是 `save`，答案 = `len(arr) - save`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.SearchInts(f, v+1)` → `bisect_left(f, v + 1)`，`if p := …; p < len(f)` 拆成两行）',
                 '时间 `O(n log n)`：每个数一次二分；空间 `O(n / k)`',
                 '易错：不降要找「第一个 ==大于== v」，所以二分 `v + 1`（整数）；严格递增则二分 `v`',
                 '`for i in range(min(k, n))`：`k` 可能大于 `n`，组数不能超过 `n`',
                 '同类：300. 最长递增子序列（严格递增）'],
    ),
)
