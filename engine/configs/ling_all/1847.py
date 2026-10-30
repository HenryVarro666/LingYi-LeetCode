SETUP = '''
import bisect as _bs


class SortedList:  # sortedcontainers.SortedList 的最小替代：只含 add / bisect_left / 下标 / len
    def __init__(self):
        self._a = []

    def add(self, x):
        _bs.insort(self._a, x)

    def bisect_left(self, x):
        return _bs.bisect_left(self._a, x)

    def __getitem__(self, i):
        return self._a[i]

    def __len__(self):
        return len(self._a)
'''


def _rooms(S):
    if 'rooms' not in S:
        return ''
    j = S.get('j')
    parts = []
    for i, (a, b) in enumerate(S['rooms']):
        parts.append(f'`[{a},{b}]`' if (j is None or i <= j) else f'==[{a},{b}]==')
    return '房间 [id,面积]（按面积从小到大，强调 = 已加入有序集合）：' + ' '.join(parts)


def _queries(S):
    if 'queries' not in S:
        return ''
    cur = S.get('i')
    parts = [(f'==[{a},{b}]==' if k == cur else f'`[{a},{b}]`') for k, (a, b) in enumerate(S['queries'])]
    return '询问 [preferred,minSize]：' + ' '.join(parts) + (f'　当前第 {cur} 个' if cur is not None else '')


CONFIG = dict(
    num=1847, title='最近的房间', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离线 · 询问排序 + 有序集合二分',
    tags=['灵神题单·常用数据结构', '难度分 2082'],
    setup=SETUP,
    code='''
class Solution:
    def closestRoom(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        rooms.sort(key=lambda r: r[1])  # 按照 size 从小到大排序
        q = len(queries)
        ans = [-1] * q
        room_ids = SortedList()  # sortedcontainers
        j = len(rooms) - 1
        for i in sorted(range(q), key=lambda i: -queries[i][1]):  # 按照 minSize 从大到小排序
            preferred_id, min_size = queries[i]
            while j >= 0 and rooms[j][1] >= min_size:
                room_ids.add(rooms[j][0])
                j -= 1

            diff = inf
            k = room_ids.bisect_left(preferred_id)
            if k:
                diff = preferred_id - room_ids[k - 1]  # 左边的差
                ans[i] = room_ids[k - 1]
            if k < len(room_ids) and room_ids[k] - preferred_id < diff:  # 右边的差更小
                ans[i] = room_ids[k]
        return ans
''',
    call='Solution().closestRoom([[1,4],[2,3],[3,5]], [[2,3],[2,4],[2,5]])',
    expect=[2, 1, 3],
    views=[
        dict(type='text', h=90, size=26, fn=_rooms),
        dict(type='text', h=90, size=26, fn=_queries),
        dict(type='array', var='room_ids._a', label='room_ids（有序集合：面积够大的房间 id）', cell=84, h=170,
             color=lambda S, i, v: ('blue' if 'k' in S and S.get('_line', 0) >= 14 and i == S['k'] - 1 else 'pink' if 'k' in S and S.get('_line', 0) >= 14 and i == S['k'] else None)),
        dict(type='array', var='ans', label='ans（按原询问下标写入）', cell=70, h=140, color=lambda S, i, v: ('green' if i == S.get('i') and S.get('_line') in (16, 19) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('preferred_id', 'preferred_id', 'yellow'), 'min_size', ('j', 'j', 'pink'), 'k', 'diff', ('ans', 'ans', 'green')],
    captions={
        'rooms.sort': '房间按面积从小到大排；`j` 从最大的开始往回走',
        'ans = [-1]': '`ans` 先全填 `-1`（没有满足条件的房间）',
        'room_ids = ': '`room_ids` 是有序集合，只存“面积够大”的房间号',
        'j = len': '`j` 指向下一个还没加入集合的房间（面积最大的在最后）',
        'for i in sorted': lambda S, B, r: ('所有询问都回答完了' if getattr(B, 'i', None) == S.i and 'j' in B else f'下标数组按 `minSize` 从大到小：先答第 `{S.i}` 个询问'),
        'preferred_id, min_size': '这个询问：想要 `preferred_id = {preferred_id}`，面积至少 `min_size = {min_size}`',
        'while j >= 0': lambda S, B, r: (f'`rooms[{S.j}]` 面积 {S.rooms[S.j][1]} ≥ {S.min_size}：它也能满足这个询问（以及之后 minSize 更小的所有询问）→ 加入集合' if S.j >= 0 and S.rooms[S.j][1] >= S.min_size else '面积够大的房间都已在集合里了；之前加入的不用重复处理'),
        'room_ids.add': '房间号 `{rooms[j][0]}` 加入有序集合 → `{room_ids._a}`',
        'j -= 1': '`j = {j}`',
        'diff = inf': '`diff` 记录当前最近的差；先设成无穷大',
        'bisect_left': '在集合里二分：第一个 ≥ `{preferred_id}` 的位置 `k = {k}`；`k-1` 是左边最近，`k` 是右边最近',
        'if k:': lambda S, B, r: ('`k > 0`：左边有房间' if S.k else '`k = 0`：左边没有房间，只能看右边'),
        'diff = preferred_id': '左边最近 `{room_ids[k-1]}`，差 `{diff}`，先暂定为答案',
        'ans[i] = room_ids[k - 1]': '暂定 `ans[{i}] = {ans[i]}`',
        'if k < len': lambda S, B, r: (f'右边 `{S.room_ids[S.k]} − {S.preferred_id} = {S.room_ids[S.k] - S.preferred_id}` 与左边差 `{S.diff}` 比：' + ('==严格更小，换成右边==' if S.room_ids[S.k] - S.preferred_id < S.diff else '不更小（平局取小的 id，保留左边）')) if S.k < len(S.room_ids) else '`k` 已到末尾：右边没有房间',
        'ans[i] = room_ids[k]': '换成右边：`ans[{i}] = {ans[i]}`',
        'return ans': '答案 `{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='先答 minSize 大的询问：候选房间只增不减',
        complexity='时间 `O(n log n + q log q + q log n)`，空间 `O(n + q)`',
        problem=['`rooms[i] = [id, size]`，询问 `[preferred, minSize]`：找面积 ≥ `minSize` 且 id 离 `preferred` 最近的房间',
                 '差相等取小 id，没有则 `-1`',
                 '本视频：`rooms=[[1,4],[2,3],[3,5]]`，`queries=[[2,3],[2,4],[2,5]]` → `[2,1,3]`'],
        quote='把询问排序，通过改变回答询问的顺序，使问题更容易处理。由于面积 ≥ 6 的房间编号已经添加到有序集合中了，所以后续只需把面积在 [3,5] 中的房间号添加到有序集合中，不需要重复处理面积 ≥ 6 的房间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接排序 `queries` 会打乱答案顺序：改成排下标数组 `queryIds`',
              '双指针：`minSize` 从大到小，房间面积也从大到小，满足的房间号加进有序集合',
              '集合里二分找 `preferred` 左右两个邻居，取更近的（平局取左边小的）'],
        summary=['时间 `O(n log n + q log q + q log n)`，空间 `O(n + q)`',
                 '原文用 `sortedcontainers.SortedList`；本视频里用最小替代实现（`add / bisect_left / 下标 / len`），逻辑不变',
                 '易错：必须按下标排序再写回 `ans[i]`；右边必须“严格更小”才替换，保证平局取小 id',
                 '同类：离线算法——排序询问，让候选集合单调增长'],
    ),
)
