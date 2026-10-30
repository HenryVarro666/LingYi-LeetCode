CONFIG = dict(
    num=46, title='全排列', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯（append / pop + used 数组）',
    code='''
class Solution(object):
    def permute(self, nums):
        res = []
        used = [False for index in range(len(nums))]
        self.dfs(nums, 0, res, [], used)
        return res

    def dfs(self, nums, level, res, now, used):
        if level == len(nums):
            res.append([x for x in now])
            return

        for index, num in enumerate(nums):
            if not used[index]:
                now.append(num)
                used[index] = True
                self.dfs(nums, level + 1, res, now, used)
                used[index] = False
                now.pop()
''',
    call='Solution().permute([1, 2, 3])',
    expect=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
    views=[
        dict(type='array', var='nums', label='nums（绿 = used）', cell=64, h=150, pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if S['used'][i] else None),
        dict(type='stack', var='now', label='now', h=108),
        dict(type='calls', h=218),
        dict(type='stack', var='res', label='res', h=108),
    ],
    watch=[('level', 'level', 'blue'), ('index', 'index', 'pink'), ('num', 'num', 'pink'), 'used'],
    skip=['for index, num in enumerate', 'used = [False'],
    captions={
        'self.dfs(nums, 0': '`used[index]` 表示 `nums[index]` 是否用过（初始全 `False`）；从第 `0` 层开始，`now` 为空',
        'if level == len(nums)': lambda S, B, ret: (
            f'`level == len(nums)`（{S.level} == {len(S.nums)}）→ ==成立==：全部处理完了'
            if S.level == len(S.nums) else
            f'`level = {S.level}`：还没处理完，在 `now` 末尾再放一个数'),
        'res.append': lambda S, B, ret: (
            f'`[x for x in now]` 逐个复制 now 的元素：`x = {S.x}`' if len(S.res) == len(B.res) else
            f'复制好的 `{S.res[-1]}` 加入 res；==不能直接放 now==，它之后还会变' if len(S.res) == 1 else
            f'复制好的 `{S.res[-1]}` 加入 res'),
        '            return': '这一支到头了 → 回到上一层',
        'if not used[index]': lambda S, B, ret: (
            f'`nums[{S.index}] = {S.num}` 未使用 → 可以放进 now'
            if not S.used[S.index] else
            f'`nums[{S.index}] = {S.num}` ==已经用过== → 跳过'),
        'now.append(num)': '每次在 list 末尾加入一个未使用的数：`now` 末尾加入 `{num}`',
        'used[index] = True': '标记 `used[{index}] = True`，下一层不会再选 `{num}`',
        'self.dfs(nums, level + 1': '然后进行下一步：进入第 `{level}` 层',
        'used[index] = False': '第 `{level + 1}` 层处理完了，取消标记：`used[{index}] = False`',
        'now.pop()': '弹出数组末尾的 `{B.now[-1]}`，==回到放它之前的状态==，好去试下一个未使用的数',
        'return res': '搜索结束，返回全部 `{len(ret)}` 个排列',
    },
    max_steps=56,
    cards=dict(
        one_liner='末尾加入一个未使用的数，处理完再把它弹出来',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（不计返回值）',
        problem=['给一个==不含重复数字==的数组 `nums`，返回它的所有全排列',
                 '示例：`[1,2,3]` → `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`'],
        quote='经典的搜索回溯问题，==每次在 list 末尾加入一个未使用的数，然后进行下一步==，当全部处理完之后==弹出数组末尾的数并加入下一个未使用的数==。',
        quote_src='—— yiduobo 题解',
        idea=['`now` 当栈用：选一个数 `append`，下一层回来后 `pop`',
              '`used[index]` 记录 `nums[index]` 是否已在 `now` 里',
              '`level == len(nums)` 时 now 装满 → 复制进 `res`'],
        result='6 个排列全部找到 ✓（中间分支已快进，过程同理）',
        summary=['原文说复杂度「应该是指数级」：准确地说叶子有 `n!` 个，总计 `O(n·n!)`',
                 '`append` / `pop`、`used = True / False` 必须==成对出现==',
                 '易错：`res.append(now)` 存的是引用，最后全变成空 list',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
