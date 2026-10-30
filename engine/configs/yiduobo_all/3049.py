CONFIG = dict(
    num=3049, title='标记所有下标的最早秒数 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='二分时间 + 堆：归零还是改标记',
    tags=['堆（优先队列）', '反悔贪心', '难度分 3125'],
    code='''
class Solution(object):
    def earliestSecondToMarkIndices(self, nums, changeIndices):

        m = len(changeIndices)
        n = len(nums)

        left = 0
        right = m
        while left < right:
            mid = (left + right) // 2
            vis = set()
            first_index_set = set()
            for index in range(mid + 1):
                if nums[changeIndices[index] - 1] > 0 and changeIndices[index] - 1 not in vis:
                    vis.add(changeIndices[index] - 1)
                    first_index_set.add(index)

            mark = 0
            need_minus = 0

            for index in range(n):
                if index not in vis:
                    need_minus += nums[index]

            heap = []
            for index in range(mid, -1, -1):
                if index in first_index_set:
                    heapq.heappush(heap, nums[changeIndices[index] - 1])

                    if len(heap) > mark:
                        mark += 1
                        need_minus += heapq.heappop(heap)
                
                elif mark < n:
                    mark += 1
                else:
                    need_minus -= 1

            if mark != n or need_minus > 0:
                left = mid + 1
            else:
                right = mid
        
        if left == m:
            return -1
        
        return left + 1
''',
    call='Solution().earliestSecondToMarkIndices([2,3], [2,1,1,1])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"二分时间区间 `[{S['left']}, {S['right']})`" + (f"，试 `mid={S['mid']}`" if 'mid' in S else '') + (f"；`mark=`==`{S['mark']}`==（已安排标记），`need_minus=`==`{S['need_minus']}`==（还要减 1 的次数）" if 'mark' in S and 'need_minus' in S else '')) if 'left' in S else '', size=24),
        dict(type='array', var='nums', label='nums', h=150, cell=96),
        dict(type='array', var='changeIndices', label='changeIndices（下标 = 时刻，从 0 开始）', h=220, cell=96,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if i in S.get('first_index_set', ()) else None,
             dim=lambda S, i, v: 'mid' in S and i > S['mid']),
        dict(type='heap', var='heap', label='heap：选择归零的 nums（堆顶最小）', h=200),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('mark', 'mark', 'green'), ('need_minus', 'need_minus', 'orange')],
    skip=['for index in range(mid + 1)', 'for index in range(n)', 'for index in range(mid, -1, -1)', 'if index not in vis', 'need_minus = 0', 'right = m', 'vis.add(changeIndices', 35, 'm = len(changeIndices)', 'n = len(nums)', 'vis = set()', 'first_index_set = set()', 'mark = 0', 'heap = []'],
    max_steps=110,
    captions={
        'left = 0': '二分最早满足的时刻：区间 `[left, right)` = `[0, m)`，m = {m}',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：继续二分' if S.left < S.right else f'`left = {S.left} = right`：二分结束'),
        'mid = (left + right)': '试时刻 `mid = {mid}`：前 `mid+1` 个时刻里能不能全部标记',
        'for index in range(mid + 1)': '正着扫前 `mid+1` 个时刻，找每门课首次出现的位置（归零只在这时用）',
        'if nums[changeIndices[index] - 1] > 0 and': lambda S, B, r: (f'正着扫：时刻 `{S.index}`：第 `{S.changeIndices[S.index]-1}` 门课（nums={S.nums[S.changeIndices[S.index]-1]}）' + ('首次出现且 nums>0 → 可以在这个时刻归零' if S.nums[S.changeIndices[S.index]-1] > 0 and S.changeIndices[S.index]-1 not in S.vis else '不用归零（为 0 或已出现过）')),
        'first_index_set.add(index)': '时刻 `{index}` 记为归零时机：{first_index_set}',
        'for index in range(n)': '没有归零机会的课只能一点点减 1，累加所需次数',
        'need_minus += nums[index]': '课 `{index}` 无法归零：`need_minus` += `{nums[index]}` → =={need_minus}==',
        'for index in range(mid, -1, -1)': lambda S, B, r: (f'倒着扫时刻 `{S.index}`：标记尽量放后面，归零尽量靠前' if S.index >= 0 else '扫完了'),
        'if index in first_index_set': lambda S, B, r: (f'倒着扫：时刻 `{S.index}` 是归零时机 → 先考虑归零，nums = `{S.nums[S.changeIndices[S.index]-1]}`' if S.index in S.first_index_set else f'倒着扫：时刻 `{S.index}` 不是归零时机'),
        'heapq.heappush(heap': '把这门课的 `nums` 放进堆：{heap}',
        'if len(heap) > mark': lambda S, B, r: (f'归零次数 `{len(S.heap)}` > 标记次数 `{S.mark}`：多了无效归零，要把其中一次换成标记' if len(S.heap) > S.mark else f'归零次数 `{len(S.heap)}` ≤ 标记次数 `{S.mark}`：没问题'),
        'mark += 1\n                        need_minus': '标记数 +1：`mark` → {mark}',
        'need_minus += heapq.heappop(heap)': '把 nums 最小的那次归零换成减 1：`need_minus` += `{B.heap[0]}` → =={need_minus}==',
        'elif mark < n': lambda S, B, r: (f'不是归零时机，且 `mark = {S.mark} < n = {S.n}` → 这个时刻用来标记' if S.mark < S.n else f'标记已够 `n = {S.n}` 次 → 这个时刻用来减 1'),
        'need_minus -= 1': '这个时刻用来减 1：`need_minus` → =={need_minus}==',
        'if mark != n or need_minus > 0': lambda S, B, r: (f'`mark = {S.mark}`，`n = {S.n}`，`need_minus = {S.need_minus}`：标记不够或减 1 不够 → ==`mid` 不可行==' if S.mark != S.n or S.need_minus > 0 else f'`mark = n`，`need_minus = {S.need_minus} ≤ 0`：全部搞定 → ==`mid` 可行=='),
        'left = mid + 1': '`mid` 不可行 → 要更晚：`left` = =={left}==',
        'right = mid': '`mid` 可行 → 试更早：`right` = =={right}==',
        'if left == m': '`left = {left}`，`m = {m}`：{"等于 m，说明所有时刻都不行 → -1" if left == m else "未到 m，找到了答案"}',
        'return left + 1': '时刻下标 `{left}`，换成第几秒要 +1：=={left + 1}==',
    },
    cards=dict(
        one_liner='二分时刻，倒着扫：归零靠前、标记靠后，多了就换成标记',
        complexity='时间 `O(m log m log n)`，空间 `O(n)`',
        problem=['`nums[i]`：下标 `i` 要减几次才到 0；`changeIndices[s]`：第 `s` 秒可把它设为任意非负数',
                 '每秒做一件事：减 1、归零、标记（值需为 0）或不动',
                 '求最早第几秒能标记完所有下标，不行返回 `-1`',
                 '本视频：`nums=[2,3]`，`changeIndices=[2,1,1,1]` → `4`'],
        quote='标记操作可以随时进行，那么就应该尽量将标记操作安排到操作序列的后面。反之，归零操作则应该尽量靠前执行，因为必须预留足够的时间给标记操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['时间越多越容易 → 二分时刻 `mid`',
              '每门课只在==首次出现==的时刻归零，放进 `first_index_set`',
              '倒着扫：归零时刻先进堆；若归零次数超过标记次数，就把 `nums` 最小的那次归零改成标记 + 减 1',
              '没有归零机会的课只能减 1，初始 `need_minus` 累加它们的 `nums`'],
        summary=['时间 `O(m log m log n)`，空间 `O(n)`',
                 '易错：`range(mid+1)` 含 `mid`；返回的是下标 + 1（秒数）',
                 '被换出的归零要用 `nums` 最小的，因为它需要补的减 1 次数最少',
                 '`left == m` 说明连最后一刻都不行 → 返回 `-1`',
                 '对比灵神：灵神把 cnt（空闲天）和 slow 合成一个比较；yiduobo 分开记 mark 与 need_minus',
                 '原文为 Python 2 风格，本题代码无需修改'],
    ),
)
