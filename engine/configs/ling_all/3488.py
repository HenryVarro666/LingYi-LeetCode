NUMS = [1, 3, 1, 4, 1, 3, 2]
QS = [0, 3, 5]


_IP = 'i if (_line <= 5 or _line >= 14) else None'

_JP = 'j if _line in (19, 20) else None'


def _num_color(S, i, v):
    if S['_line'] >= 14 and 'i' in S and 'qi' in S:
        if i == S['i']:
            return 'yellow'
        if v == NUMS[S['i']]:
            return 'blue'
    return None


def _top(S):
    ln = S['_line']
    if ln >= 14 and 'p' in S and 'qi' in S:
        i, p = S['i'], S['p']
        if 'j' in S and ln >= 19 and S['_inner'].get('j') is not None and p[S['j'] - 1] < i <= p[S['j']]:
            j = S['j']
            return f"`i = {i}`：左边最近 `p[{j-1}] = {p[j-1]}`，右边最近 `p[{j+1}] = {p[j+1]}` → `min({i - p[j-1]}, {p[j+1] - i})`"
        return f"查询 `i = {i}`：`nums[{i}] = {NUMS[i]}` 的下标列表 `p = {p}`"
    if ln >= 8:
        return '每个下标列表==前后各加一个哨兵==：环形数组「绕一圈」的位置'
    return '先把每个数出现的下标收集起来（天然有序）'


def _if3(S, B, ret):
    p = S.p
    if len(p) == 3:
        return f'`len(p) = 3`：只有原本 1 个下标 + 2 个哨兵 → `nums[{S.i}]` ==只出现一次==，答案 -1'
    return f'`len(p) = {len(p)}`：除哨兵外还有 `{len(p) - 2}` 个下标 → 去二分'


CONFIG = dict(
    num=3488, title='距离最小相等元素查询', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='下标列表 + 哨兵 + 二分查找',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def solveQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        indices = defaultdict(list)
        for i, x in enumerate(nums):
            indices[x].append(i)

        n = len(nums)
        for p in indices.values():
            # 前后各加一个哨兵
            i0 = p[0]
            p.insert(0, p[-1] - n)
            p.append(i0 + n)

        for qi, i in enumerate(queries):
            p = indices[nums[i]]
            if len(p) == 3:
                queries[qi] = -1
            else:
                j = bisect_left(p, i)
                queries[qi] = min(i - p[j - 1], p[j + 1] - i)
        return queries
''',
    call=f'Solution().solveQueries({NUMS}, {QS})',
    expect=[2, -1, 3],
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='nums', label='nums（环形；黄 = 当前查询下标，蓝 = 相同的数）', cell=90,
             pointers={_IP: 'yellow'}, pointer_labels={_IP: 'i'}, color=_num_color, h=170),
        dict(type='map', var='indices', label='indices：每个数的下标列表',
             fmt=lambda k, v: f'{k}: {v}', h=190, font=30),
        dict(type='array', var=lambda S: S['p'] if 'p' in S else [], label='p（当前处理的下标列表）', cell=90, index=True,
             pointers={_JP: 'pink'}, pointer_labels={_JP: 'j'}, h=170),
        dict(type='array', var='queries', label='queries（答案直接写回这里）', cell=90, pointers={'qi': 'green'}, h=170),
    ],
    watch=['n', ('i', 'i', 'yellow'), ('j', 'j', 'pink'), ('qi', 'qi', 'green')],
    skip=[],
    captions={
        'indices = defaultdict': '`indices[x]`：数 `x` 出现的所有下标',
        'indices[x].append(i)': '`nums[{i}] = {x}` → `indices[{x}] = {indices[x]}`',
        'n = len': '`n = {n}`',
        'i0 = p[0]': '先记下第一个下标 `i0 = {i0}`',
        'p.insert(0': '最后一个下标 `{p[-1]}` 往左绕一圈 = `{p[-1]} − {n} = {p[0]}`：放到最前面',
        'p.append(i0': '第一个下标 `{i0}` 往右绕一圈 = `{i0} + {n} = {p[-1]}`：放到最后面',
        'p = indices[nums[i]]': '查询 `i = {i}`：取出 `nums[{i}] = {nums[i]}` 的下标列表 `{p}`',
        'if len(p) == 3': _if3,
        'queries[qi] = -1': '没有其他相同的数 → `queries[{qi}] = -1`',
        'j = bisect_left': '二分：`i = {i}` 在 `p` 中的位置 `j = {j}`（`p[{j}] = {p[j]}` 就是它自己）',
        'queries[qi] = min': '左右两侧最近：`min({i} − {p[j-1]}, {p[j+1]} − {i})` = =={queries[qi]}==',
        'return queries': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='在同值下标列表里二分自己，左右邻居就是最近的相同元素',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['环形数组 `nums`，每个查询给一个下标 `i`',
                 '求与 `nums[i]` 相等的==其他==下标到 `i` 的最小环形距离，没有则 -1',
                 '示例：`nums = [1,3,1,4,1,3,2], queries = [0,3,5]` → `[2,-1,3]`'],
        quote='在下标列表前面添加 4−n=−3，相当于认为在 −3 下标处也有一个 1。在下标列表末尾添加 0+n=7，相当于认为在 7 下标处也有一个 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二分得到 `j` 后，`p[j−1]` 是左边最近，`p[j+1]` 是右边最近',
              '环形 + 越界怎么办？==前后各加一个哨兵==，免去一堆 if-else',
              '加完哨兵长度为 3，说明这个数只出现过一次 → -1'],
        summary=['时间 `O(n + q log n)`：每次查询一次二分；空间 `O(n)`',
                 '哨兵：前面插 `p[-1] − n`，后面加 `p[0] + n`（先记下 `i0` 再 insert）',
                 '答案直接写回 `queries`，省一个数组',
                 '方法二：预处理每个下标左右最近的相同元素，可做到 `O(n + q)`'],
    ),
)
