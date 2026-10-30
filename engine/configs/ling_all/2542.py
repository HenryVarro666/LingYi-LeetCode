def _cur(S):
    return f"{S['x']}·{S['y']}" if 'x' in S and 'y' in S else None


def _pairs(S):
    return [f'{p[0]}·{p[1]}' for p in S['a']] if 'a' in S else None


CONFIG = dict(
    num=2542, title='最大子序列的分数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='按 nums2 排序 + 大小为 k 的最小堆',
    tags=['灵神题单', '堆', '难度分 2056'],
    code='''
class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        a = sorted(zip(nums1, nums2), key=lambda p: -p[1])
        h = [x for x, _ in a[:k]]
        heapify(h)
        s = sum(h)
        ans = s * a[k - 1][1]
        for x, y in a[k:]:
            if x > h[0]:
                s += x - heapreplace(h, x)
                ans = max(ans, s * y)
        return ans
''',
    call='Solution().maxScore([4,2,3,1,5,2], [1,6,3,5,2,4], 3)',
    expect=21,
    views=[
        dict(type='array', var=_pairs, label='a（nums1·nums2，按 nums2 从大到小；黄 = 当前枚举）', cell=100, h=170,
             color=lambda S, i, v: "yellow" if v == _cur(S) else None),
        dict(type='heap', var='h', label='h：最小堆，只留 nums1 最大的 k 个', top_color='pink', h=200),
        dict(type='text', fn=lambda S: (f"堆和 `s = {S['s']}`，当前最小值 `y = {S['y']}` → 分数 `{S['s']} × {S['y']}` = =={S['s']*S['y']}==" if 'y' in S and 's' in S and S['_line'] == 11 else (f"前 k 个：堆和 `s = {S['s']}`" if 's' in S else '')), h=60),
    ],
    watch=[('s', 's', 'blue'), ('x', 'x', 'orange'), ('y', 'y', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'a = sorted': '按 `nums2` 从大到小排：往后枚举时，==当前 y 一定是已选元素里最小的 nums2==',
        'h = [x for': '先拿前 `k` 个，它们的 nums2 都 ≥ 第 k 个的 `{a[k-1][1]}`',
        'heapify(h)': '建成最小堆，堆顶 `{h[0]}` 是这 k 个 nums1 里最小的',
        's = sum(h)': '`s = {s}`：堆里 k 个 nums1 之和',
        'ans = s *': '最小值就是第 k 个的 `nums2 = {a[k-1][1]}`：`ans = {s} × {a[k-1][1]}` = =={ans}==',
        'for x, y in a[k:]': '枚举下一个：`nums2 = {y}` 成为新的最小值，`nums1 = {x}` 可以参选',
        'if x > h[0]': lambda S, B, r: (f'`x = {S.x}` > 堆顶 `{S.h[0]}`：换掉堆顶能让和变大 → 成立' if S.x > S.h[0]
                                        else f'`x = {S.x}` ≤ 堆顶 `{S.h[0]}`：换了只会变小 → 跳过（这个 y 不能让答案更大）'),
        's += x -': '用 `x` 顶替堆里最小的数：`s` 变为 =={s}==',
        'ans = max(ans': '`ans = max({B.ans}, {s} × {y})` = =={ans}==',
        'return ans': '枚举完，最大分数 `{ans}`',
    },
    cards=dict(
        one_liner='有序是好性质：按 nums2 降序，再用堆保留最大的 k 个 nums1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选 `k` 个下标，分数 = ==nums1 之和 × nums2 最小值==，求最大分数',
                 '示例：`[1,3,3,2]`、`[2,1,3,4]`、`k=3` → `12`',
                 '本视频：`[4,2,3,1,5,2]`、`[1,6,3,5,2,4]`、`k=3`'],
        quote='请记住：有序是一个非常好的性质。……枚举 nums2[i] 作为序列的最小值，那么 nums1 就只能在下标 ≤ i 的数中选了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按 `nums2` 降序后，枚举到的 `y` 就是最小值，前面的数都能选',
              '要选 nums1 最大的 `k` 个：大小固定为 `k` 的最小堆（同 703 题）',
              '新元素比堆顶大就替换堆顶，和只增不减'],
        summary=['时间 `O(n log n)`（排序 + 堆），空间 `O(n)`',
                 '先用前 `k` 个算一次答案，再从第 `k` 个之后开始枚举',
                 '`x <= h[0]` 时不更新：和没变，而 y 更小，分数不会更大',
                 '同类：703 数据流中的第 K 大元素'],
    ),
)
