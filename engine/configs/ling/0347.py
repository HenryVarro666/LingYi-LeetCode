def _bidx(S):
    b = S.get('bucket')
    for i, x in enumerate(S.get('buckets') or []):
        if x is b:
            return i
    return None


def _for_xc(S, B, ret):
    if 'x' in B and (B.x, B.c) == (S.x, S.c):
        return '所有元素都放进桶了'
    pre = f'先建 `max_cnt + 1 = {len(S.buckets)}` 个空桶。' if 'x' not in B else ''
    return pre + f'元素 `{S.x}` 出现了 `{S.c}` 次 → 放进 `buckets[{S.c}]`'


CONFIG = dict(
    num=347, title='前 K 个高频元素', difficulty='Medium', category='堆',
    author='灵茶山艾府', technique='哈希表计数 + 桶排序',
    code='''
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 第一步：统计每个元素的出现次数
        cnt = Counter(nums)
        max_cnt = max(cnt.values())

        # 第二步：把出现次数相同的元素，放到同一个桶中
        buckets = [[] for _ in range(max_cnt + 1)]  # 也可以用 defaultdict(list)
        for x, c in cnt.items():
            buckets[c].append(x)

        # 第三步：倒序遍历 buckets，把出现次数前 k 大的元素加入答案
        ans = []
        for bucket in reversed(buckets):
            ans += bucket
            # 注意题目保证答案唯一，一定会出现恰好等于 k 的情况
            if len(ans) == k:
                return ans
''',
    call='Solution().topKFrequent([4, 4, 4, 1, 1, 2, 2, 3], 3)',
    expect=[4, 1, 2],
    skip=['buckets = [[] for _ in range'],
    views=[
        dict(type='array', var='nums', cell=80, index=False),
        dict(type='map', var='cnt', label='cnt（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}次', h=100),
        dict(type='table', var='buckets', label='buckets（第 c 行 = 出现 c 次的元素；绿 = 当前桶）', cell=64, h=320,
             rows=lambda S: [f'{i}次' for i in range(len(S['buckets']))],
             color=lambda S, i, j, v: 'green' if S.get('bucket') is S['buckets'][i] else 'blue'),
        dict(type='array', var='ans', label='ans', cell=72, index=False, min_slots=3),
    ],
    watch=[('k', 'k', 'orange'), ('max_cnt', 'max_cnt'), ('len(ans)', lambda S: len(S['ans']), 'green')],
    captions={
        'cnt = Counter(nums)': '第一步：用哈希表 `cnt` ==统计每个元素的出现次数==',
        'max_cnt = max': '出现次数的最大值 `max_cnt = {max_cnt}`（`≤ n`，保证桶的个数是 `O(n)`）',
        'for x, c in cnt.items()': _for_xc,
        'buckets[c].append(x)': lambda S, B, ret: (f'`buckets[{S.c}]` 加入 `{S.x}`' +
                                                   ('：==同一个桶内的元素出现次数相同，无需排序==' if len(S.buckets[S.c]) > 1 else '')),
        'ans = []': '第三步：倒序遍历桶，出现次数大的先进答案',
        'for bucket in reversed(buckets)': lambda S, B, ret: f'倒序来到 `buckets[{_bidx(S)}]` = `{S.bucket}`（出现 {_bidx(S)} 次的元素）',
        'ans += bucket': '整桶加入答案：`ans = {ans}`',
        'if len(ans) == k': lambda S, B, ret: (f'`len(ans) = {len(S.ans)} == k`：==恰好凑够 k 个==' if len(S.ans) == S.k
                                               else f'`len(ans) = {len(S.ans)} < k = {S.k}`，继续看下一个桶'),
        'return ans': '返回 `{ret}`（题目保证答案唯一，一定会恰好等于 k）',
    },
    max_steps=70,
    cards=dict(
        one_liner='按出现次数分桶，从次数最大的桶往下拿，拿够 k 个就停',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['返回数组中出现频率前 `k` 高的元素，可以按任意顺序返回',
                 '进阶：时间复杂度必须优于 `O(n log n)`',
                 '本视频示例：`[4,4,4,1,1,2,2,3], k = 3` → ==[4,1,2]=='],
        quote='把出现次数相同的元素，放到同一个桶中。同一个桶内的元素出现次数相同，无需对桶内元素排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一步：哈希表 `cnt` 统计次数，问题变成“前 k 大的出现次数对应哪些元素”',
              '第二步：`buckets[c]` 存出现 `c` 次的元素；`max_cnt ≤ n`，所以桶只有 `O(n)` 个',
              '第三步：==倒序遍历桶==，答案长度一旦等于 `k` 就立刻返回'],
        summary=['时间 `O(n)`：计数、分桶、倒序遍历都是线性的，比堆的 `O(n log k)` 更优',
                 '注意倒序：要先拿出现次数==大==的桶',
                 '答案唯一保证 `len(ans)` 会恰好等于 `k`，不会跨过去',
                 '`buckets` 也可以用 `defaultdict(list)`'],
    ),
)
