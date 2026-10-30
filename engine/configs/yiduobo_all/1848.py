CONFIG = dict(
    num=1848, title='到目标元素的最小距离', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从 start 向左右两侧扫描', tags=[],
    code='''
class Solution(object):
    def getMinDistance(self, nums, target, start):

        now = start
        while now >= 0 and nums[now] != target:
            now -= 1
        
        if now >= 0:
            res = start - now
        else:
            res = len(nums) + 1
        
        now = start + 1
        while now < len(nums) and nums[now] != target:
            now += 1
        
        if now < len(nums):
            res = min(res, now - start)
        
        return res
''',
    call='Solution().getMinDistance([1,5,3,4,2,5,5], 5, 4)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: ('第一步：从 start 向左找 target' if S['_line'] <= 8 else '第二步：从 start+1 向右找 target') + f"（target = {S['target']}）", size=30),
        dict(type='array', var='nums', pointers={'now': 'blue', 'start': 'pink'}, h=260,
             color=lambda S, i, v: 'green' if v == S['target'] else None),
    ],
    watch=[('now', 'now', 'blue'), ('start', 'start', 'pink'), ('res', 'res', 'green')],
    captions={
        4: '先从 `start = {start}` 出发，往左扫描',
        'while now >= 0': lambda S, B, r: (f'`nums[{S.now}] = {S.nums[S.now]}` 不是 target `{S.target}` → 继续' if S.now >= 0 and S.nums[S.now] != S.target
                                           else (f'`now = {S.now}` 出界了 → 左侧没有 target' if S.now < 0 else f'`nums[{S.now}] = {S.target}` 就是 target → 停下')),
        'now -= 1': '不是 target：`now` 左移到 {now}',
        'if now >= 0': lambda S, B, r: (f'`now = {S.now} >= 0`：左侧找到了' if S.now >= 0 else f'`now = {S.now}`：左侧没找到'),
        'res = start - now': '左侧最近的 target 距离 `{start} − {now}` = =={res}==',
        'res = len': '左侧没有 → 用一个比任何距离都大的值 `len(nums) + 1` 占位',
        13: '再往右扫：从 `start + 1 = {now}` 开始（start 自己已在左侧检查过）',
        'while now < len': lambda S, B, r: (f'`nums[{S.now}] = {S.nums[S.now]}` 不是 target → 继续' if S.now < len(S.nums) and S.nums[S.now] != S.target
                                            else (f'`now = {S.now}` 出界 → 右侧没有 target' if S.now >= len(S.nums) else f'`nums[{S.now}] = {S.target}` 就是 target → 停下')),
        'now += 1': '不是 target：`now` 右移到 {now}',
        'if now < len': lambda S, B, r: (f'`now = {S.now}` 在数组内：右侧找到了' if S.now < len(S.nums) else '右侧没找到，保留左侧结果'),
        'res = min': '对比左右两侧：`min({B.res}, {now} − {start})` = =={res}==',
        'return res': '最近的 target 距离 start 为 =={res}==',
    },
    cards=dict(
        one_liner='从 start 向两侧扫描，第一个 target 最近',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找下标 `i` 满足 `nums[i] == target`，且 `abs(i - start)` 最小',
                 '返回这个最小距离，保证 target 存在',
                 '本视频：`[1,5,3,4,2,5,5]`，`target=5`，`start=4` → `1`'],
        quote='一个自然的想法就是从start开始向左右两侧扫描，找到第一个target时停止，然后对比左右两侧当前位置与start的距离大小决定最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['向左扫：停在第一个 target，距离是 `start - now`',
              '向右扫：停在第一个 target，距离是 `now - start`',
              '每侧只看最近的一个，再取两边较小者'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一侧没找到时 `now` 会出界：左侧 `now < 0`，右侧 `now == len(nums)`，要先判断再用',
                 '左侧没找到时 `res` 设成 `len(nums) + 1`，保证后面 `min` 不被它影响',
                 '原文为 Python 2 风格，但在 Python 3 下同样可运行，代码未改动'],
    ),
)
