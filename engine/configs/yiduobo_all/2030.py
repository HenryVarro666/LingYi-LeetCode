def _top(S):
    if 'heap' not in S:
        return '先确定每一位能从哪个范围里选（右边界 bound）'
    res = S.get('res')
    if res is None:
        return f'首字符的选择范围：下标 `0 … bound`，`bound = {S.get("bound")}`'
    return f"已选 `{len(res)}` 个，还能放非 `{S['letter']}` 的名额 `other = {S.get('other')}`；可选范围到 `bound = {S.get('bound')}`"


def _color(S, i, v):
    res = S.get('res') or []
    if i in res:
        return 'green'
    if S.get('letter') == v:
        return 'orange'
    return None


def _dim(S, i, v):
    b = S.get('bound')
    return b is not None and 'heap' in S and i > b


CONFIG = dict(
    num=2030, title='含特定字母的最小子序列', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='堆 + 逐位贪心（选择范围 bound）',
    tags=['灵神题单', '单调栈', '难度分 2562'],
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
    expect='ecde', max_steps=110,
    skip=['pos_list = []', 'n = len(s)', 'heap = []', 'res = []', 'for index, char in enumerate', 'if char == letter', 'for index in range(bound + 1', 'while len(res) < k', 'if p < len(pos_list)', 'p += 1'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', pointers={'bound': 'pink'}, label='s（绿 = 已选，橙 = letter，灰 = 还不能选）', h=200, cell=70, color=_color, dim=_dim),
        dict(type='heap', var='heap', label='小根堆（字符, 下标）', h=250, fmt=lambda x: f'{x[0]}{x[1]}'),
        dict(type='array', var='pos_list', label='pos_list（letter 出现的下标）', h=150, cell=70, index=False),
    ],
    watch=[('p', 'p', 'cyan'), ('bound', 'bound', 'pink'), ('other', 'other', 'orange'), ('res', 'res', 'green')],
    captions={
        'pos_list.append': '`{letter}` 出现在下标 `{index}`，记下来：`pos_list = {pos_list}`',
        'p = len(pos_list)': '`p = {len(pos_list)} − {repetition} = {p}`：从 `pos_list[{p}]` 起恰好剩 `repetition` 个 letter，首字符不能越过 `pos_list[p]`',
        'bound = min(pos_list[p], n - k)': '首字符范围：`min(pos_list[p], n − k) = min({pos_list[p]}, {n - k})` → ==bound {bound}==',
        'heapq.heappush(heap, (s[index], index))': '`({s[index]}, {index})` 入堆（字符小的在堆顶，相同字符下标小的在前）',
        'other = k - repetition': '`other = {k} − {repetition} = {other}`：非 letter 字符最多还能选 `other` 个',
        'while len(res) < k': '`len(res) = {len(res)} < k = {k}` → {"还没选满" if len(res) < k else "选满了"}',
        'heapq.heappop': '弹出堆顶 `({char}, {index})`：当前范围内最小的字符',
        'if len(res) > 0 and index < res[-1]': '`index = {index}` {"<" if len(res) > 0 and index < res[-1] else "不小于"} 上一个已选下标 → {"在已选字符左边，失效，丢掉" if len(res) > 0 and index < res[-1] else "位置有效"}',
        'if char != letter': '`{char}` {"不是" if char != letter else "就是"} letter',
        'if other == 0': '`other = {other}` → {"名额用完，位置要留给 letter，跳过它" if other == 0 else "还有名额，可以选"}',
        'other -= 1': '用掉一个名额：`other = {other}`',
        'res.append(index)': lambda S, B, r: f'选中下标 `{S.index}`（`{S.s[S.index]}`）：`res = {S.res}`' + ('，选了 letter，后面要留的 letter 少一个，==p 后移==' if S.s[S.index] == S.letter else ''),
        'if len(res) == k': '`len(res) = {len(res)}` {"== k，选满了" if len(res) == k else "< k，继续"}',
        'next_bound = n - (k - len(res))': '剩 `{k - len(res)}` 个要选 → 最多选到下标 `n − {k - len(res)} = {next_bound}`',
        'next_bound = min(next_bound, pos_list[p])': '还要给 letter 留位置：`next_bound = min(…, pos_list[{p}]) = {next_bound}`',
        'for index in range(bound + 1, next_bound + 1)': '把下标 `{bound + 1} … {next_bound}` 的字符补进堆',
        'bound = next_bound': '`bound = {bound}`：选择范围向右扩大',
        'continue': '丢掉，重新弹堆顶',
        'break': '选满，跳出',
        "return ''.join": '答案 `{"".join([s[index] for index in res])}`',
    },
    cards=dict(
        one_liner='逐位贪心：每次从可选范围里挑最小字符，范围由堆维护',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['在 `s` 里选长为 `k` 的子序列，字典序最小，且 `letter` 至少出现 `repetition` 次',
                 '示例：`s = "leetcode"`，`k = 4`，`letter = "e"`，`repetition = 2` → `"ecde"`'],
        quote='为了使得最终答案的字典序最小，那么就应该尽可能将小的字符放在答案的前面。',
        quote_src='—— yiduobo 题解原文',
        idea=['首字符受限：后面要留 `k−1` 个位置，还要留够 `repetition` 个 letter → 右边界 `bound`',
              '用小根堆维护 `0…bound` 的字符，弹出最小的（相同字符下标小的优先）',
              '非 letter 的名额只有 `k − repetition` 个，用完就不能再选；选完一个字符，边界右移并把新字符入堆'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：堆里弹出的下标若小于上一个已选下标，已经失效，要丢掉',
                 '易错：`other == 0` 时只能选 letter，非 letter 要跳过',
                 '原文就是 Python 3 可直接运行的写法（用到 heapq），代码没有改动',
                 '对比灵神：灵神用单调队列，弹队尾前看 letter 够不够；yiduobo 用堆维护「当前可选范围」'],
    ),
)
