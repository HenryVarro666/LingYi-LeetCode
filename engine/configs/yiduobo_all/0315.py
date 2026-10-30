CONFIG = dict(
    num=315, title='计算右侧小于当前元素的个数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离散化 rank + 树状数组',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def countSmaller(self, nums):

        last = None
        rank = 1
        rank_dict = {}

        for num in sorted(nums):
            if num == last:
                continue

            rank_dict[num] = rank
            rank += 1
            last = num
        
        res = []
        sum_list = [0] * rank

        for index in range(len(nums) - 1, -1, -1):
            now = rank_dict[nums[index]] - 1

            tmp = 0
            while now > 0:
                tmp += sum_list[now]
                now -= now & -now
            res.append(tmp)

            now = rank_dict[nums[index]]
            while now < rank:
                sum_list[now] += 1
                now += now & -now
            
        res.reverse()
        return res
''',
    call='Solution().countSmaller([5, 2, 6, 1])',
    expect=[2, 1, 1, 0],
    max_steps=120,
    skip=['rank += 1', 'last = num', 'last = None', 'rank_dict = {}', 'tmp = 0', 'if num == last', 'continue', 'now -= now & -now', 'now += now & -now'],
    views=[
        dict(type='array', var='nums', label='nums（青色箭头 = 当前从右往左扫描到的位置）', h=215,
             pointers={'index': 'cyan'}),
        dict(type='map', var='rank_dict', label='rank_dict：数值 → rank（1 到 n）', h=150,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='sum_list', label='sum_list（树状数组，下标 = rank，下标 0 不用）', h=215,
             pointers={'now': 'pink'}),
        dict(type='array', var='res', label='res（从右往左收集，最后翻转）', h=130),
    ],
    watch=['index', 'now', 'tmp'],
    captions={
        'rank = 1': '`rank` 从 1 开始：树状数组的下标不能是 0',
        'rank_dict[num] = rank': '按从小到大编号：`{num}` 的 rank 是 `{rank_dict[num]}`，值被压缩到 `1..n`',
        'sum_list = [0] * rank': '树状数组 `sum_list`：记录每个 rank 已出现的个数，初始全 0',
        'for index in range': lambda S, B, r: f'从右往左扫：`index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`',
        'now = rank_dict[nums[index]] - 1': '求 rank 在 `1..{now}` 之间的个数，即右侧比 `{nums[index]}` 小的数的个数；先从 `now = {now}` 开始',
        'while now > 0': lambda S, B, r: (f'`now = {S.now}` > 0：这一格还管着一段 rank，继续往前查（每次去掉最低位 `now & -now`）' if S.now > 0 else '`now = 0`：前缀查完了'),
        'while now < rank': lambda S, B, r: (f'`now = {S.now}` < `rank`：还有节点覆盖这个 rank，继续更新（每次加上最低位 `now & -now`）' if S.now < S.rank else f'`now = {S.now}` 超出范围：树状数组更新完毕'),
        'tmp += sum_list[now]': '把 `sum_list[{now}]` 累加进 `tmp` → =={tmp}==',
        'now -= now & -now': '`now & -now` 去掉最低位的 1：往前跳到 `now = {now}`（树状数组的前缀查询）',
        'res.append(tmp)': '`nums[{index}]` 右侧比它小的有 =={tmp}== 个，追加到 `res`',
        'now = rank_dict[nums[index]]': '查完后把它自己加入树状数组：从 `now = {now}` 开始更新',
        'sum_list[now] += 1': '`sum_list[{now}]` 加 1 → {sum_list[now]}',
        'now += now & -now': '`now & -now` 加上最低位：往后跳到 `now = {now}`，更新所有覆盖它的节点',
        'res.reverse()': '`res` 是从右往左收集的，翻转后才和 `nums` 一一对应',
    },
    cards=dict(
        one_liner='排序得到 rank，再用树状数组动态数「比我小的个数」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['对每个 `nums[i]`，求它右侧有多少个数比它小，返回数组',
                 '示例：`[5,2,6,1]` → `[2,1,1,0]`',
                 '本视频：同示例，一步步看树状数组怎么算'],
        quote='求解动态的区间和，很自然就联想到了使用树状数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序，把每个数映射成 rank（`1` 到 `n`），值域缩小后就能开数组',
              '从右往左扫：右侧 rank 在 `1..rank-1` 之间的个数就是答案，用树状数组求前缀和',
              '查完把自己的 rank 加进去；最后翻转 `res`'],
        summary=['时间 `O(n log n)`：排序 + 每个元素两次树状数组操作',
                 '`rank` 从 1 开始，树状数组下标 0 不能用；重复的数 rank 相同（`continue` 跳过）',
                 '先查询再插入，这样不会数到自己；别忘了翻转',
                 '原文为 Python 2 写法，已无需修改，直接运行'],
    ),
)
