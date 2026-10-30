def _qphase(S):
    return 'q' in S


def _ncol(S, i, v):
    if _qphase(S):
        return 'green' if v <= S['q'] else 'red'
    if 'i' in S and S['_line'] in (4, 5):
        if i == S['i'] and S['_line'] == 5:
            return 'yellow'
        if i < S['i'] or i == S['i'] and S['_line'] == 5:
            return 'cyan'
    return None


def _top(S):
    if _qphase(S):
        q = S['q']
        k = sum(1 for v in S['nums'] if v <= q)
        return f"`q = {q}`：前缀和 `≤ {q}` 的有 =={k}== 个 → 最多选 `{k}` 个最小的数"
    if 'i' in S:
        return '`nums[i]` 原地变成前缀和：前 `i + 1` 个最小数之和'
    return '和有上限 → 为了选得多，==优先选小的==；位置无关，可以排序'


CONFIG = dict(
    num=2389, title='和有限的最长子序列', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='排序 + 前缀和 + 二分',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()
        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]  # 原地求前缀和
        for i, q in enumerate(queries):
            queries[i] = bisect_right(nums, q)  # 复用 queries 作为答案
        return queries
''',
    call='Solution().answerQueries([4,5,2,1,6], [3,10,21,1])',
    expect=[2, 3, 5, 1],
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='nums', label='nums（排序 → 原地前缀和；绿 = ≤ q，红 = > q）', color=_ncol,
             pointers={'queries[i] if _line == 7 else None': 'green'},
             pointer_labels={'queries[i] if _line == 7 else None': '第一个 > q'}, cell=96, h=280),
        dict(type='array', var='queries', label='queries（逐个改成答案）', cell=96,
             color=lambda S, i, v: 'yellow' if _qphase(S) and i == S['i'] else None, h=200),
    ],
    watch=[('i', 'i', 'cyan'), ('q', 'q', 'yellow')],
    captions={
        'nums.sort()': '排序：`{nums}`，==选前缀==就是选最小的若干个数',
        'for i in range(1': lambda S, B, r: ('前缀和算完' if B.get('i') == S.i else f'`i = {S.i}`：前 {S.i + 1} 个数的和 = 前 {S.i} 个的和 + `nums[{S.i}]`'),
        'nums[i] += nums[i - 1]': '原地求前缀和：`nums[{i}]` = `{B.nums[i]} + {nums[i - 1]}` = =={nums[i]}==',
        'for i, q in enumerate': lambda S, B, r: ('询问都回答完了' if 'q' in B and B.i == S.i
                                                  else f'询问 `q = {S.q}`'),
        'queries[i] = bisect_right': '前缀和严格递增 → 二分找第一个 `> {q}` 的下标 =={queries[i]}==，它就是最长前缀的长度',
        'return queries': '复用 `queries` 作为答案：`{ret}`',
    },
    cards=dict(
        one_liner='贪心选最小的数：排序求前缀和，二分找第一个大于询问值的位置',
        complexity='时间 `O((n + m) log n)`，空间 `O(1)`',
        problem=['对每个 `queries[i]`，求 nums 中元素和 `≤ queries[i]` 的==子序列的最大长度==',
                 '示例：`nums = [4,5,2,1], queries = [3,10,21]` → `[2,3,4]`',
                 '本视频：`[4,5,2,1,6], [3,10,21,1]` → `[2,3,5,1]`'],
        quote='贪心：由于元素和有上限，为了能让子序列尽量长，子序列中的==元素值越小越好==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['元素位置不影响和 → 排序后选一个==前缀==',
              'nums 都是正数，前缀和严格递增，可以二分',
              '`bisect_right(前缀和, q)` = 前缀和 `≤ q` 的个数 = 最长长度'],
        summary=['时间 `O((n + m) log n)`；前缀和存进 nums、答案存进 queries，额外空间 `O(1)`',
                 '要找 `≤ q` 的个数，用 `bisect_right`，不是 `bisect_left`',
                 '子序列可以不连续，所以才能排序；改成子数组就不行了（思考题）'],
    ),
)
