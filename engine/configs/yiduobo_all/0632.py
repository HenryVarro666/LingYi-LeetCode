COLS = ['blue', 'pink', 'green']

CONFIG = dict(
    num=632, title='最小区间', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='多路归并 + 滑动窗口',
    tags=['滑动窗口与双指针', '常用数据结构'],
    code='''
import heapq

class Solution(object):
    def smallestRange(self, nums):

        q = []
        heap = []
        pos_dict = {}
        cnt_dict = {}
        part_cnt = 0
        k = len(nums)
        l = r = 0
        res = None

        for index, part in enumerate(nums):
            heapq.heappush(heap, [part[0], index])
            pos_dict[index] = 1
            cnt_dict[index] = 0

        while heap:
            while heap and part_cnt < k:
                now, source = heap[0]

                while heap and heap[0][0] == now:
                    now, source = heapq.heappop(heap)
                    q.append([now, source])
                    r += 1
                    cnt_dict[source] += 1
                    if cnt_dict[source] == 1:
                        part_cnt += 1
                    if pos_dict[source] < len(nums[source]):
                        heapq.heappush(heap, [nums[source][pos_dict[source]], source])
                        pos_dict[source] += 1

            while l < r and part_cnt == k:
                if res is None or q[r - 1][0] - q[l][0] < res[1] - res[0]:
                    res = [q[l][0], q[r - 1][0]]
                remove_num = q[l][0]
                for remove_pos in range(l, r):
                    if q[remove_pos][0] != remove_num:
                        break
                if q[remove_pos][0] == remove_num:
                    remove_pos += 1
                for index in range(l, remove_pos):
                    cnt_dict[q[index][1]] -= 1
                    if cnt_dict[q[index][1]] == 0:
                        part_cnt -= 1

                l = remove_pos
        return res
''',
    call='Solution().smallestRange([[1,5],[2,6],[3,7]])',
    expect=[1, 3],
    views=[
        dict(type='array', var=lambda S: [x for x, _ in S['q']] or [''], label='q：归并出的有序序列（颜色 = 来源列表，框 = 窗口 [l, r)）', cell=84, h=190,
             window=('l', lambda S: S['r'] - 1),
             color=lambda S, i, v: COLS[S['q'][i][1]] if i < len(S['q']) else None,
             dim=lambda S, i, v: i < len(S['q']) and not (S['l'] <= i < S['r'])),
        dict(type='heap', var='heap', label='heap（每个列表的下一个候选：值, 来源）', fmt=lambda x: f'{x[0]}/列表{x[1]}', h=190),
        dict(type='map', var='cnt_dict', label='cnt_dict（窗口内各列表的个数）', fmt=lambda k, v: f'列表{k}: {v}', h=130, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"已覆盖 ==`{S['part_cnt']}`== / {S['k']} 个列表；当前最小区间 ==`{S['res']}`==" if 'part_cnt' in S and 'k' in S else ''),
    ],
    skip=['q = []', 'heap = []', 'pos_dict = {}', 'cnt_dict = {}', 'part_cnt = 0', 'k = len', 'l = r = 0', 'res = None', 'pos_dict[index] = 1', 'cnt_dict[index] = 0', 'q.append', 'pos_dict[source] += 1', 'r += 1', 'part_cnt += 1', 'part_cnt -= 1', 'for remove_pos', 'break', 'for index in range'],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('part_cnt', 'part_cnt', 'purple'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for index, part in enumerate': lambda S, B, rr: ('初始化：`q` 存归并出的有序序列，`cnt_dict` 记窗口内各列表的个数，`part_cnt` 记已覆盖的列表数；先把每个列表的头元素入堆' if S.get('index') == 0 else ('三个列表的头元素都入堆了，初始化完成' if B.get('index') == S.get('index') else f'下一个列表：`index = {S.index}`')),
        'heapq.heappush(heap, [part[0]': '每个列表的第一个元素入堆：`{part[0]}`（列表 {index}）',
        'while heap:': lambda S, B, rr: (f'堆里还有元素（{len(S.heap)} 个）：归并还没完成' if S.heap else '堆空了：归并结束'),
        'while heap and part_cnt < k': lambda S, B, rr: (f'`part_cnt = {S.part_cnt} < k = {S.k}`：窗口还没覆盖所有列表 → 继续从堆里取' if S.heap and S.part_cnt < S.k else f'`part_cnt = {S.part_cnt}`：已覆盖所有列表（或堆空），转去收缩'),
        'now, source = heap[0]': '偷看堆顶：最小值 `now = {now}`（列表 {source}）',
        'while heap and heap[0][0] == now': lambda S, B, rr: (f'堆顶还等于 `{S.now}`：把所有相同值一起入窗口（同值必须同进同出）' if S.heap and S.heap[0][0] == S.now else '没有相同值了'),
        'now, source = heapq.heappop': '弹出最小的 `{now}`（来自列表 {source}）',
        'q.append': '放进 `q` 末尾，也就是窗口右端',
        'r += 1': '`r` → {r}',
        'cnt_dict[source] += 1': '列表 {source} 在窗口里的个数：`{cnt_dict[source]}`',
        'if cnt_dict[source] == 1': lambda S, B, rr: (f'`cnt_dict[{S.source}] == 1`：列表 {S.source} 第一次出现，覆盖数加一' if S.cnt_dict[S.source] == 1 else '这个列表之前就有了，覆盖数不变'),
        'part_cnt += 1': '`part_cnt` → {part_cnt}',
        'if pos_dict[source] <': lambda S, B, rr: (f'列表 {S.source} 还有下一个元素：补入堆，保持每个列表一个候选' if S.pos_dict[S.source] < len(S.nums[S.source]) else f'列表 {S.source} 没有下一个元素了，不再补'),
        'heapq.heappush(heap, [nums': '补入 `{nums[source][pos_dict[source]]}`',
        'pos_dict[source] += 1': '`pos_dict[{source}]` → {pos_dict[source]}',
        'while l < r and part_cnt == k': lambda S, B, rr: (f'`part_cnt == k`：窗口 `q[{S.l}:{S.r}]` 覆盖所有列表，合法 → 收缩左边界并更新答案' if S.l < S.r and S.part_cnt == S.k else f'`part_cnt = {S.part_cnt} < k`：窗口不再合法，回去归并扩右边界'),
        'if res is None or': lambda S, B, rr: (f'窗口 `[{S.q[S.l][0]}, {S.q[S.r - 1][0]}]` 宽 `{S.q[S.r - 1][0] - S.q[S.l][0]}`' + ('，还没有答案 → 更新' if S.res is None else f' < 当前 `{S.res[1] - S.res[0]}` → 更新' if S.q[S.r - 1][0] - S.q[S.l][0] < S.res[1] - S.res[0] else f' 不比当前 `{S.res[1] - S.res[0]}` 小 → 不更新')),
        'res = [q[l][0]': '`res = {res}`',
        'remove_num = q[l][0]': '要移出的值 `{remove_num}`：和它相同的值要一起移出',
        'for remove_pos in range(l, r)': '从 l 往右找第一个不等于 `{remove_num}` 的位置',
        'if q[remove_pos][0] == remove_num': '`remove_pos` 修正为 {remove_pos}：窗口左边界将跳到这里',
        'for index in range(l, remove_pos)': '依次移出 `q[{l}:{remove_pos}]` 里的元素',
        'cnt_dict[q[index][1]] -= 1': '列表 {q[index][1]} 在窗口里的个数：`{cnt_dict[q[index][1]]}`',
        'if cnt_dict[q[index][1]] == 0': lambda S, B, rr: (f'列表 {S.q[S.index][1]} 在窗口里没有了：覆盖数减一' if S.cnt_dict[S.q[S.index][1]] == 0 else '窗口里还有这个列表的数，覆盖数不变'),
        'part_cnt -= 1': '`part_cnt` → {part_cnt}',
        'l = remove_pos': '`l` → {l}：左边界右移',
        'return res': '最小区间 `{res}`',
    },
    cards=dict(
        one_liner='右边界靠多路归并推进，左边界照常收缩',
        complexity='时间 `O(L log k)`，空间 `O(L)`（L 为元素总数）',
        problem=['`k` 个非递减列表，找最小区间，使每个列表至少有一个数落在其中',
                 '示例：`[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]` → `[20,24]`',
                 '本视频：`[[1,5],[2,6],[3,7]]` → `[1,3]`'],
        quote='实际上就是右边界不再是简单的往右扩展，而是需要通过执行多路归并来获取到有序的序列，然后再往右扩展。左边界的缩减操作则维持不变。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想简化版：有序数组、每个数带来源标记，求包含所有来源的最短区间 → 标准滑窗',
              '这里的有序数组是现算的：用最小堆对 k 个列表做多路归并',
              '扩：不断弹堆顶入窗口直到覆盖所有列表；缩：左边界右移直到不再覆盖，同时更新答案'],
        summary=['时间 `O(L log k)`，空间 `O(L)`；`q` 保存了归并出的全部元素',
                 '相同值要整批进、整批出，这样窗口边界不会落在一串相同值中间',
                 '`part_cnt` 记已覆盖的列表数，等于 k 才合法',
                 '对比灵神：灵神是先整体排序再滑窗，这里边归并边滑窗，省掉了全排序',
                 '代码在 Python 3 下无需修改'],
    ),
)
