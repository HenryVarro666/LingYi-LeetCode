def _chosen(S):
    return [i for i in (S.get('res') or [])]


def _idx_color(S, i, v):
    res = _chosen(S)
    if i in res:
        return 'green'
    if i in (S.get('pos_list') or []) and 'heap' in S:
        return 'purple'
    return None


def _dim(S, i, v):
    res = _chosen(S)
    return bool(res) and i < res[-1] and i not in res


def _show(S):
    if 'heap' not in S:
        return '`letter` 的位置记到 `pos_list`，后面要保证能凑够 `repetition` 个'
    res = S.get('res')
    if res is None:
        return f"首字母只能在下标 `0 ~ {S['bound']}` 里选（`bound = min(pos_list[p], n − k)`）"
    chosen = ''.join(S['s'][i] for i in res)
    return f"已选 `\"{chosen}\"`（{len(res)}/{S['k']}）　非 letter 名额 `other = {S['other']}`"


def _pop(S, B, ret):
    ch, ix = S.char, S.index
    return f'堆顶弹出 `({ch!r}, {ix})`：字符最小、下标靠前，是当前最优候选'


def _stale(S, B, ret):
    if S.index < S.res[-1]:
        return f'下标 `{S.index}` 在上一个已选下标 `{S.res[-1]}` 的左边 → ==已失效==，丢掉'
    return f'下标 `{S.index}` 在已选下标 `{S.res[-1]}` 的右边 → 有效'


def _isl(S, B, ret):
    if S.char != S.letter:
        if S.other == 0:
            return f'`{S.char}` 不是 letter，而非 letter 的名额 `other = 0` → ==不能选==，丢掉'
        return f'`{S.char}` 不是 letter，还有 `other = {S.other}` 个名额 → 可以选'
    return f'`{S.char}` 就是 letter → 选它，不占 `other` 名额'


def _nb(S, B, ret):
    s = f'下一轮边界：留出后面还要选的 `{S.k - len(S.res)}` 个位置 → `n − (k − len(res)) = {S.n - (S.k - len(S.res))}`'
    return s


CONFIG = dict(
    num=2030, title='含特定字母的最小子序列', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='最小堆 + 可选范围边界',
    tags=['最小字典序', '难度分 2562'],
    code='''
class Solution(object):
    def smallestSubsequence(self, s, k, letter, repetition):

        pos_list = []
        n = len(s)
        for index, char in enumerate(s):
            if char == letter:
                pos_list.append(index)

        p = len(pos_list) - repetition
        heap = []
        n = len(s)
        bound = min(pos_list[p], n - k)
        for index in range(bound + 1):
            heapq.heappush(heap, (s[index], index))

        res = []
        other = k - repetition
        while len(res) < k:
            char, index = heapq.heappop(heap)
            if len(res) > 0 and index < res[-1]:
                continue
            if char != letter:
                if other == 0:
                    continue
                other -= 1
                res.append(index)
            else:
                res.append(index)
                if p < len(pos_list):
                    p += 1

            if len(res) == k:
                break

            next_bound = n - (k - len(res))
            if p < len(pos_list):
                next_bound = min(next_bound, pos_list[p])

            for index in range(bound + 1, next_bound + 1):
                heapq.heappush(heap, (s[index], index))
            bound = next_bound
        
        return ''.join([s[index] for index in res])
''',
    call='Solution().smallestSubsequence("leetcode", 4, "e", 2)',
    expect='ecde',
    skip=['for index, char in enumerate', 'if char == letter', 'n = len(s)', 'for index in range(bound', 'bound = next_bound'],
    max_steps=100,
    views=[
        dict(type='string', var='s', label='s（绿 = 已选，紫 = letter，灰 = 已失效，橙箭头 = bound）', cell=76, h=200,
             pointers={'bound': 'orange'},
             color=_idx_color, dim=_dim),
        dict(type='heap', var='heap', label='heap（候选：(字符, 下标)，堆顶最小）', fmt=lambda x: f'{x[0]}{x[1]}', h=190),
        dict(type='text', fn=_show, size=26, h=80),
    ],
    watch=[('pos_list', 'pos_list', 'purple'), ('p', 'p', 'cyan'), ('bound', 'bound', 'orange'),
           ('other', 'other', 'yellow'), ('res', 'res', 'green')],
    captions={
        'pos_list.append(index)': '记下 letter 出现的下标：`pos_list = {pos_list}`',
        'p = len(pos_list) - repetition': '首字母之后还得有 `repetition` 个 letter：`pos_list[{p}]` 是最晚能选首字母的 letter 位置',
        'heap = []': '用最小堆装候选字符，字符相同下标小的在前',
        'bound = min(pos_list': lambda S, B, ret: f'首字母范围：既要给后面留 `k − 1` 个位，又要保住 letter → `bound = min({S.pos_list[S.p]}, {S.n} − {S.k}) = {S.bound}`',
        'heapq.heappush(heap, (s[index], index))': '`({s[index]!r}, {index})` 入堆',
        'res = []': '`res` 里存选中字符的==下标==',
        'other = k - repetition': '`k` 个位置里 `repetition` 个留给 letter，其余最多 `other = {other}` 个给别的字符',
        'while len(res) < k': lambda S, B, ret: (f'已选 `{len(S.res)}` 个，还差 `{S.k - len(S.res)}` 个' if len(S.res) < S.k else '选满了'),
        'heapq.heappop': _pop,
        'if len(res) > 0 and index < res[-1]': _stale,
        'if char != letter': _isl,
        'if other == 0': lambda S, B, ret: ('`other = 0`：非 letter 的名额用完 → 跳过它' if S.other == 0 else f'`other = {S.other}` > 0 → 还可以选'),
        'other -= 1': '用掉一个名额：`other = {other}`',
        'res.append(index)': lambda S, B, ret: f'选下标 `{S.index}`（`{S.s[S.index]}`）→ 已选 `"{"".join(S.s[i] for i in S.res)}"`',
        30: lambda S, B, ret: ('后面还有 letter 要留 → `p` 后移' if S.p < len(S.pos_list) else 'letter 已全部用完'),
        'p += 1': '选了一个 letter，需预留的 letter 少一个：`p = {p}`',
        'if len(res) == k': lambda S, B, ret: ('选满 `k` 个 → 结束' if len(S.res) == S.k else f'才选了 `{len(S.res)}` 个，继续'),
        'break': '提前结束循环',
        'next_bound = n - (k - len(res))': _nb,
        37: lambda S, B, ret: ('还有 letter 要预留 → 边界不能越过 `pos_list[p]`' if S.p < len(S.pos_list) else '不再需要给 letter 预留位置'),
        'next_bound = min(': '`next_bound = {next_bound}`',
        'return': '按下标取字符拼起来：`"{ret}"`',
    },
    cards=dict(
        one_liner='每次只在「还能选完」的范围内取最小字符',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['从 `s` 取长为 `k` 的子序列，要求 `letter` 至少出现 `repetition` 次',
                 '在满足条件的子序列里，字典序最小',
                 '示例：`"leetcode"`，`k=4`，`letter="e"`，`repetition=2` → `"ecde"`'],
        quote='首字母的选择范围在0到bound = min(n - k, pos_list[p])之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案越靠前的字符越小越好 → 逐位选最小的字符，同字符取下标小的',
              '选首字符有两个限制：后面要留 `k − 1` 个位置；后面要留够 `repetition` 个 letter',
              '合起来是下标上界 `bound`；还有 `other` 限制非 letter 的数量，用堆维护候选，边选边扩大边界'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：弹出的候选下标若在已选下标左边，已失效要丢掉',
                 '易错：非 letter 名额 `other = k − repetition`，用完就只能选 letter',
                 '原文本来就是 Python 3 可运行的写法，代码未改动（`heapq` 由引擎预置）',
                 '灵神题解仅供参考，这里按 yiduobo 的堆做法演示；灵神的做法是单调栈/队列'],
    ),
)
