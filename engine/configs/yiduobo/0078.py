CONFIG = dict(
    num=78, title='子集', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · now 单调递增（从 last_pos + 1 枚举）',
    code='''
class Solution(object):
    def subsets(self, nums):
        res = []
        now = []

        self.dfs(nums, -1, now, res)
        return res

    def dfs(self, nums, last_pos, now, res):
        res.append(now[:])
        for index in range(last_pos + 1, len(nums)):
            now.append(nums[index])
            self.dfs(nums, index, now, res)
            now.pop()
''',
    call='Solution().subsets([1, 2, 3])',
    expect=[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]],
    views=[
        dict(type='array', var='nums', label='nums（暗 = 下标 ≤ last_pos，不能再选）', cell=64, h=150,
             pointers={'last_pos': 'blue', 'index': 'pink'}, dim=lambda S, i, v: i <= S['last_pos']),
        dict(type='stack', var='now', label='now', h=108),
        dict(type='calls', h=218),
        dict(type='stack', var='res', label='res', h=108),
    ],
    watch=[('last_pos', 'last_pos', 'blue'), ('index', 'index', 'pink'), ('now', 'now', 'yellow')],
    captions={
        'self.dfs(nums, -1': '从 `last_pos = -1` 开始：第一个数可以从下标 `0` 选起',
        'res.append(now[:])': lambda S, B, ret: (
            f'==每一个 now 都是解的一种==：把 `{S.res[-1]}` 复制进 res'
            + ('（`now[:]` 是拷贝）' if len(S.res) == 1 else '')),
        'for index in range': lambda S, B, ret: (
            (f'从 `last_pos + 1 = {S.last_pos + 1}` 开始往后枚举：`index = {S.index}`，试着放 `{S.nums[S.index]}`'
             if S.index == S.last_pos + 1 else
             f'继续往后枚举：`index = {S.index}`，试着放 `{S.nums[S.index]}`')
            if 'index' in S and S.index != B.get('index') else
            f'`range({S.last_pos + 1}, {len(S.nums)})` 枚举完了 → 这一层结束，返回上一层'),
        'now.append': '`now` 末尾加入 `nums[{index}] = {nums[index]}` → `{now}`，保持 now ==单调递增==',
        'self.dfs(nums, index': '递归：把 `last_pos` 设为 `{last_pos}`，下一个数只能从 `{last_pos + 1}` 往后选',
        'now.pop()': '回溯：弹出 `{B.now[-1]}`，now 回到 `{now}`，准备试下一个 `index`',
        'return res': '搜索结束，共 `{len(ret)}` 个子集',
    },
    max_steps=60,
    cards=dict(
        one_liner='让 now 单调递增，每个 now 都是一个子集',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['数组 `nums` 的元素==互不相同==，返回它的所有子集（幂集）',
                 '示例：`[1,2,3]` → `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`'],
        quote='为了去除重复情况，同样可以用上一题中==保证 now 单调递增==的做法，然后在每次操作时==从 last_pos + 1 开始往后枚举==。每一个 now 都是解的一种。',
        quote_src='—— yiduobo 题解',
        idea=['`[1,2]` 和 `[2,1]` 是同一个子集 → 只按下标从小到大放，就不会重复',
              '`last_pos`：now 最后一个数的下标，下一个数从 `last_pos + 1` 选起',
              '每进入一次 dfs，当前 now 就是一个新子集 → 直接加入 res'],
        summary=['一共 `2^n` 次 dfs，每次复制 now `O(n)` → `O(n·2^n)`',
                 '和全排列的区别：不需要 used 数组，下标递增天然去重',
                 '易错：`res.append(now)` 不复制，最后全是空 list',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
