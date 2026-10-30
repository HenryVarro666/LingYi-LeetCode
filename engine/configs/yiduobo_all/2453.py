CONFIG = dict(
    num=2453, title='摧毁一系列目标', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='余数哈希 · 记最小值下标与个数',
    tags=['灵神题单', '数学算法', '难度分 1762'],
    code='''
class Solution(object):
    def destroyTargets(self, nums, space):

        rest = {}
        for index, num in enumerate(nums):
            r = num % space
            if r not in rest:
                rest[r] = [index, 0]
            elif nums[rest[r][0]] > num:
                rest[r][0] = index

            rest[r][1] += 1
        
        res = None
        max_cnt = 0
        for index, cnt in rest.values():
            if cnt > max_cnt or (cnt == max_cnt and nums[index] < res):
                max_cnt = cnt
                res = nums[index]
        
        return res
''',
    call='Solution().destroyTargets([6,2,5,3,4,1], 3)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（space = 3）', pointers={'index': 'blue'}, h=170),
        dict(type='map', var='rest', label='rest：余数 → [最小值下标, 个数]', fmt=lambda k, v: f'{k}: {v}', h=200, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"目前最多 ==%d== 个，输入值 ==%s==" % (S['max_cnt'], S['res'])) if 'max_cnt' in S else '余数相同的数，输入其中最小的就能全部摧毁'),
    ],
    watch=['index', 'num', 'r', ('max_cnt', 'max_cnt', 'orange'), ('res', 'res', 'green'), 'cnt'],
    captions={
        'rest = {}': '`rest[余数] = [最小值的下标, 个数]`',
        'r = num % space': '`{num} % {space}` = `{r}`：它属于余数 {r} 这一组',
        'if r not in rest': lambda S, B, ret: (f'余数 {S.r} 第一次出现 → 新建这一组' if S.r not in S.rest
                                                else f'余数 {S.r} 已有一组，继续看谁更小'),
        'rest[r] = [index, 0]': '新建：最小值下标 = `{index}`，个数先记 0',
        'elif nums[rest[r][0]] > num': lambda S, B, ret: (f'组内记录的最小值 `{S.nums[S.rest[S.r][0]]}` > `{S.num}` → 换成更小的' if S.nums[S.rest[S.r][0]] > S.num
                                                         else f'组内最小值 `{S.nums[S.rest[S.r][0]]}` 不比 `{S.num}` 大，保持'),
        'rest[r][0] = index': '更新这一组的最小值下标为 `{index}`',
        'rest[r][1] += 1': '这一组个数加一 → `{rest[r][1]}`',
        'res = None': '`res` 保存答案，`max_cnt` 保存最大个数',
        'max_cnt = 0': '`max_cnt = 0`：还没有任何一组',
        'for index, cnt in rest.values()': lambda S, B, r: ('各组都比较完了' if 'index' in B and B.index == S.index
                                                           else f'逐组比较：这一组有 `{S.cnt}` 个，最小值 `{S.nums[S.index]}`'),
        'if cnt > max_cnt': lambda S, B, ret: (f'`{S.cnt} > {S.max_cnt}`：个数更多 → 更新' if S.cnt > S.max_cnt else
            (f'个数相同（{S.cnt}），最小值 `{S.nums[S.index]} < {S.res}` → 取较小者' if S.cnt == S.max_cnt and S.nums[S.index] < S.res
             else f'`cnt = {S.cnt}` 不比 `max_cnt = {S.max_cnt}` 更优 → 跳过')),
        'max_cnt = cnt': '`max_cnt` → {max_cnt}',
        'res = nums[index]': '`res` → {res}',
        'return res': '最多目标的一组中最小的数：`{res}`',
    },
    cards=dict(
        one_liner='先按余数聚合，再挑个数最多的组，并列取最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['输入 `nums[i]` 会摧毁 `nums[i] + c*space` 位置的所有目标',
                 '求摧毁最多目标时，可输入的最小值',
                 '本视频：`nums=[6,2,5,3,4,1], space=3` → `1`（三组都是 2 个）'],
        quote='对于一组余数相同的nums，输入其中最下的nums，就可以将这一组余数相同的nums全部摧毁。',
        quote_src='—— yiduobo 题解原文',
        idea=['满足 `nums[j] >= nums[i]` 且余数相同的目标都会被摧毁',
              '用字典存每个余数：最小值的==下标==和==个数==',
              '再遍历各组：个数多者胜；个数相同取各自最小值较小的'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '字典里存下标而不是值，比较时用 `nums[index]`',
                 '并列时用 `nums[index] < res`；`res` 初始为 `None`，因 `max_cnt=0` 时 `cnt > max_cnt` 必先成立，不会比较 None',
                 '原文无需改动 Python 3（本来就兼容）'],
    ),
)
