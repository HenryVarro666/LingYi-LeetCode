def _present(S, idx):
    i = S.get('index')
    return i is not None and idx in S['removeQueries'][i:]


def _txt(S):
    if 'new_right' not in S or 'index' not in S:
        return '倒推：把删掉的数一个个加回来，只记录子段的左右边界'
    return f'新子段 `[{S["new_left"]}, {S["new_right"]}]`'


CONFIG = dict(
    num=2382, title='删除操作后的最大子段和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='倒序加回 + 边界字典 + 前缀和',
    tags=['灵神题单', '常用数据结构', '难度分 2136'],
    code='''
class Solution(object):
    def maximumSegmentSum(self, nums, removeQueries):

        left = {}
        right = {}
        res = [0]
        
        n = len(nums)
        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        for index in range(n - 1, 0, -1):
            remove = removeQueries[index]
            if remove - 1 in left:
                new_left = left[remove - 1]
            else:
                new_left = remove
            
            if remove + 1 in right:
                new_right = right[remove + 1]
            else:
                new_right = remove
            
            left[new_right] = new_left
            right[new_left] = new_right

            new_s = s[new_right]
            if new_left > 0:
                new_s -= s[new_left - 1]
            
            res.append(max(res[-1], new_s))

        return res[::-1]
''',
    call='Solution().maximumSegmentSum([1,2,5,6,1], [0,3,2,4,1])',
    expect=[14, 7, 2, 2, 0],
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='array', var='nums', pointers={'remove': 'blue'}, window=('new_left', 'new_right'),
             label='nums（绿 = 已加回；灰 = 仍被删除；框 = 新子段）', h=170,
             color=lambda S, i, v: 'blue' if i == S.get('remove') else ('green' if _present(S, i) else None),
             dim=lambda S, i, v: not _present(S, i)),
        dict(type='array', var='s', label='s：前缀和，子段和 = s[右] - s[左-1]', h=120),
        dict(type='map', var='left', label='left：右边界 → 左边界', h=120),
        dict(type='map', var='right', label='right：左边界 → 右边界', h=120),
        dict(type='array', var='res', label='res（倒序存放，最后反转）', h=120,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 and len(S['res']) > 1 else None),
    ],
    skip=['right = {}', 'n = len'],
    watch=['index', 'remove', 'new_left', 'new_right', 'new_s'],
    captions={
        'left = {}': '只维护子段的==边界==：`left[右端]` = 左端，`right[左端]` = 右端',
        'res = [0]': '`res[0] = 0`：全部删光后的答案；之后每加回一个数追加一项',
        'n = len': '`n = {n}`',
        's.append(s[-1] + num)': '累加前缀和 → `s = {s}`',
        'for index in range': '倒推：第 `index` 次删除的位置在下一步被「加回」',
        'remove = removeQueries': '加回位置 `remove = {removeQueries[index]}`',
        'if remove - 1 in left': lambda S, B, r: (f'左邻 `{S.remove - 1}` 是某子段的右端 → 能向左接上' if S.remove - 1 in S.left
                                                   else f'左邻 `{S.remove - 1}` 不是子段右端 → 左边没有紧挨的子段'),
        'new_left = left[remove - 1]': '新子段左端 = 左邻子段的左端 `left[{remove - 1}] = {left[remove - 1]}`',
        'new_left = remove': '左边没有子段，左端就是自己 `{remove}`',
        'if remove + 1 in right': lambda S, B, r: (f'右邻 `{S.remove + 1}` 是某子段的左端 → 能向右接上' if S.remove + 1 in S.right
                                                    else f'右邻 `{S.remove + 1}` 不是子段左端 → 右边没有紧挨的子段'),
        'new_right = right[remove + 1]': '新子段右端 = 右邻子段的右端 `right[{remove + 1}] = {right[remove + 1]}`',
        'new_right = remove': '右边没有子段，右端就是自己 `{remove}`',
        'left[new_right] = new_left': '四种情况统一：新子段 `[{new_left}, {new_right}]`，在两端互相登记边界',
        'right[new_left] = new_right': '`right[{new_left}] = {new_right}`，中间位置不用管',
        'new_s = s[new_right]': '用前缀和求新子段和：先取 `s[{new_right}] = {s[new_right]}`',
        'new_s -= s[': '减去 `s[{new_left - 1}] = {s[new_left - 1]}` → 新子段和 `{new_s}`',
        'res.append(max': lambda S, B, r: f'当前最大 = max(上一轮 `{S.res[-2]}`，新子段 `{S.new_s}`) = ==`{S.res[-1]}`==：其他子段没变，只有新子段可能更大',
        'return res': '`res` 是倒序的：`{res}` 反转后就是答案',
    },
    cards=dict(
        one_liner='倒着把删掉的数加回来，只记录子段两端，用前缀和算和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['依次删除 `nums[removeQueries[i]]`，数组被切成连续的子段',
                 '求每次删除后的最大子段和',
                 '示例：`nums=[1,2,5,6,1]`，`removeQueries=[0,3,2,4,1]` → `[14,7,2,2,0]`'],
        quote='对于这类不断删东西并要求找出删除过程中的中间结果的问题，一种常见的做法是从最终态开始往前倒推，逐个将删去的东西加回来。',
        quote_src='—— yiduobo 题解原文',
        idea=['加回一个数，会遇到四种情况：孤立 / 并入左 / 并入右 / 连起两段',
              '只有区间两端有用：`left[i]` 记右端 i 的左边界，`right[i]` 反过来',
              '新左右端算出来，互相登记即可；和用前缀和 `s[r] - s[l-1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`new_left == 0` 时不能减 `s[-1]`，要单独判断',
                 '最大子段和只会被新合并的子段刷新，故取 `max(res[-1], new_s)`',
                 '`res` 是倒序追加的，返回前反转',
                 '对比灵神：灵神用并查集累加 `sum`；yiduobo 用边界字典 + 前缀和',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
