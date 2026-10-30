NUMS = [7, 9, 5, 8, 1, 3]


def _i(S):
    return S['i'] if 'i' in S and S.get('_line') in (10, 11, 18, 19, 20) else None


def _col(S, k, v):
    i, ln = _i(S), S.get('_line', 0)
    if i is None:
        return None
    if ln <= 11:
        return 'green' if k >= i else None
    return 'cyan' if k <= i else None


def _dim(S, k, v):
    i, ln = _i(S), S.get('_line', 0)
    if i is None:
        return False
    return (k < i) if ln <= 11 else (k > i)


def _suf(S, B, r):
    i, v = S.i, S.nums[S.i]
    top = B['min_h'][0]
    if v > top:
        return f'从右往左看 `nums[{i}] = {v}`：和堆顶 `{top}` 比，更大 → 踢掉 `{top}`、放进 `{v}`，后缀和 `{S.suf_max[i + 1]}` → ==`{S.suf_max[i]}`==' if False else f'`nums[{i}] = {v}` > 堆顶 `{top}`：踢掉 `{top}`、放进 `{v}` ，后缀和 `{S.suf_max[i + 1]}` → ==`{S.suf_max[i]}`=='
    return f'`nums[{i}] = {v}` ≤ 堆顶 `{top}`：不如堆里最小的，==堆不变==，`suf_max[{i}] = {S.suf_max[i]}`'


def _pre(S, B, r):
    i, v = S.i, S.nums[S.i]
    top = -B['max_h'][0]
    if v < top:
        return f'`nums[{i}] = {v}` < 堆顶（最大）`{top}`：踢掉 `{top}`、放进 `{v}` → 前缀最小和 ==`{S.pre_min}`=='
    return f'`nums[{i}] = {v}` ≥ 堆顶 `{top}`：不如堆里最大的，==堆不变==，`pre_min` 仍是 `{S.pre_min}`'


def _ans(S, B, r):
    i = S.i
    return (f'分割在 `{i}` 之后：`pre_min − suf_max[{i + 1}]` = {S.pre_min} − {S.suf_max[i + 1]} = {S.pre_min - S.suf_max[i + 1]}，'
            f'`ans` → =={S.ans}==')


def _fm(S):
    ln = S.get('_line', 0)
    if 'i' in S and ln in (18, 19, 20):
        i = S['i']
        return f"分割点：前 `{i + 1}` 个里选 {len(S['max_h'])} 个最小（`pre_min = {S['pre_min']}`），后面选 {len(S['min_h'])} 个最大（`suf_max[{i + 1}] = {S['suf_max'][i + 1]}`）"
    if 'i' in S and ln in (10, 11):
        return f"后缀 `nums[{S['i']}:]` 里最大的 {len(S['min_h'])} 个数之和 → `suf_max[{S['i']}]`"
    return '答案 = 所有分割点上 `最小前缀和 − 最大后缀和` 的最小值'


CONFIG = dict(
    num=2163, title='删除元素后和的最小差值', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前后缀分解 + 堆',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2225'],
    code='''
class Solution:
    def minimumDifference(self, nums: List[int]) -> int:
        m = len(nums)
        n = m // 3
        min_h = nums[-n:]
        heapify(min_h)

        suf_max = [0] * (m - n + 1)  # 后缀最大和
        suf_max[-1] = sum(min_h)
        for i in range(m - n - 1, n - 1, -1):
            suf_max[i] = suf_max[i + 1] + nums[i] - heappushpop(min_h, nums[i])

        max_h = [-x for x in nums[:n]]  # 所有元素取反，表示最大堆
        heapify(max_h)

        pre_min = -sum(max_h)  # 前缀最小和
        ans = pre_min - suf_max[n]  # i=n-1 时的答案
        for i in range(n, m - n):
            pre_min += nums[i] + heappushpop(max_h, -nums[i])
            ans = min(ans, pre_min - suf_max[i + 1])
        return ans
''',
    call=f'Solution().minimumDifference({NUMS})',
    expect=1,
    skip=['for i in range(m - n - 1', 'for i in range(n, m - n)'],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 后缀已纳入，青 = 前缀已纳入）', h=200, cell=84,
             pointers={'i if _line in (10, 11, 18, 19, 20) else None': 'blue'}, pointer_labels={'i if _line in (10, 11, 18, 19, 20) else None': 'i'},
             color=_col, dim=_dim),
        dict(type='heap', var='min_h', label='min_h：后缀最大的 n 个', h=150),
        dict(type='heap', var=lambda S: [-x for x in S['max_h']] if 'max_h' in S else None,
             label='max_h：前缀最小的 n 个（取反显示）', h=150),
        dict(type='array', var='suf_max', label='suf_max[i]：nums[i:] 中最大 n 个数之和', h=190, cell=84),
        dict(type='text', fn=_fm, size=24, h=90),
    ],
    watch=['n', 'pre_min', ('ans', 'ans', 'green')],
    captions={
        'n = m // 3': '数组共 `{m}` 个数，`n = {n}`：留下 `2n` 个，==删除只是障眼法==，关键是选哪些数',
        'min_h = nums[-n:]': '后缀先放进最后 `n` 个数，它们就是 `nums[{m - n}:]` 里最大的 `n` 个',
        'heapify(min_h)': '建成最小堆：堆顶是这 `n` 个里最小的，==随时可以被更大的数替换==',
        'suf_max[-1] = sum': '`suf_max[{m - n}] = {suf_max[-1]}`：只有 `n` 个数，全选',
        'suf_max[i] = suf_max[i + 1]': _suf,
        'max_h = [-x': '前缀同理，Python 只有最小堆 → ==所有数取反==当最大堆用',
        'pre_min = -sum': '`pre_min = {pre_min}`：前 `n` 个全选',
        'ans = pre_min - suf_max[n]': '分割点在 `n-1` 之后：`{pre_min} − {suf_max[n]}` = ==`{ans}`==',
        'pre_min += ': _pre,
        'ans = min(ans': _ans,
        'return ans': '最小差值 = ==`{ans}`==',
    },
    cards=dict(
        one_liner='枚举分割点：前缀选最小 n 个，后缀选最大 n 个',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 有 `3n` 个数，恰好删掉 `n` 个，剩下 `2n` 个按顺序分成前后两半',
                 '求 `sum_first − sum_second` 的==最小值==',
                 '示例：`[7,9,5,8,1,3]` → `1`'],
        quote='删除元素是障眼法，把重点放在怎么选 2n 个数上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两半互相独立：前半和越小越好，后半和越大越好',
              '枚举分割位置：前缀选最小的 `n` 个，后缀选最大的 `n` 个',
              '后缀用 ==最小堆==（Top K 套路）从右往左算 `suf_max`，前缀用最大堆边算边更新答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（这里 n 是 `len(nums)/3`）',
                 '`heappushpop` = 先入堆再弹堆顶，一步完成「替换」',
                 '最大堆用「元素取反 + 最小堆」，注意 `pre_min` 的符号',
                 '分割点范围：`i` 从 `n-1` 到 `2n-1`，保证两侧各至少 `n` 个数',
                 '同类题：703 数据流中的第 K 大元素（同一个 Top K 堆）'],
    ),
)
