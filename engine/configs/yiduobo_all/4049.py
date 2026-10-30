CONFIG = dict(
    num=4049, title='统计等间距出现整数数目 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='四个哈希表一趟遍历',
    code='''
class Solution(object):
    def countSpecialIntegers(self, nums):
        
        pre = {}
        diff = {}
        cnt = {}
        flag = {}

        for index, v in enumerate(nums):
            if v not in pre:
                pre[v] = index
                diff[v] = None
                cnt[v] = 1
                flag[v] = True
            
            else:
                if diff[v] is not None and diff[v] != index - pre[v]:
                    flag[v] = False
                diff[v] = index - pre[v]
                pre[v] = index
                cnt[v] += 1
        
        res = 0
        for v in flag:
            if cnt[v] >= 3 and flag[v]:
                res += 1
        
        return res
''',
    call='Solution().countSpecialIntegers([1,8,1,5,1,5,8,5,8,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, h=150, cell=70,
             color=lambda S, k, v: 'green' if 'index' in S and k == S['index'] and 'res' not in S else None),
        dict(type='map', var='pre', label='pre[x]：上次出现的下标', fmt=lambda k, v: f'{k}: {v}', h=95, font=30),
        dict(type='map', var='diff', label='diff[x]：约定的下标差', fmt=lambda k, v: f'{k}: {v}', h=95, font=30),
        dict(type='map', var='cnt', label='cnt[x]：出现次数', fmt=lambda k, v: f'{k}: {v}', h=95, font=30),
        dict(type='map', var='flag', label='flag[x]：下标差是否一直合法', fmt=lambda k, v: f'{k}: {v}', h=95, font=30),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v'), ('res', 'res', 'green')],
    captions={
        'pre = {}': '`pre`：记录每个数上一次出现的下标',
        'diff = {}': '`diff`：记录约定好的下标差，第二次出现时才定下来',
        'cnt = {}': '`cnt`：记录每个数出现了几次',
        'flag = {}': '`flag`：记录这个数的下标差有没有出过问题',
        'for index, v in enumerate': lambda S, B, ret: (f'看 `nums[{S.index}] = {S.v}`' if 'index' not in B or S.index != B.index else '遍历结束，开始统计答案'),
        'if v not in pre': lambda S, B, ret: (f'`{S.v}` 以前没见过 → 首次出现，初始化' if S.v not in B.pre else f'`{S.v}` 以前见过 → 要检查下标差'),
        'pre[v] = index': lambda S, B, ret: (f'`pre[{S.v}] = {S.pre[S.v]}`：记住这次的下标' ),
        'diff[v] = None': '只有一个 `{v}`，还没有下标差 → `diff[{v}] = None`',
        'cnt[v] = 1': '出现次数 `cnt[{v}] = 1`',
        'flag[v] = True': '目前没有矛盾 → `flag[{v}] = True`',
        'if diff[v] is not None': lambda S, B, ret: (
            f'本次间隔 `{S.index} - {B.pre[S.v]} = {S.index - B.pre[S.v]}`，已约定 `{B.diff[S.v]}` → ==不一致，flag 置 False=='
            if B.diff[S.v] is not None and B.diff[S.v] != S.index - B.pre[S.v] else
            (f'这是第二次出现，还没有约定的差，不用比较' if B.diff[S.v] is None else
             f'本次间隔 `{S.index - B.pre[S.v]}` 与已约定的 `{B.diff[S.v]}` 相同 → 没问题')),
        'flag[v] = False': '`flag[{v}] = False`：下标差不一致，这个数不可能特别',
        'diff[v] = index': '更新约定的下标差：`diff[{v}] = {index} - {B.pre[v]} = {diff[v]}`',
        'pre[v] = index': '`pre[{v}]` 更新为当前下标 `{index}`',
        'cnt[v] += 1': '`cnt[{v}]` 加一 → `{cnt[v]}`',
        'res = 0': '遍历完了，再看每个出现过的数是否合法；`res = 0`',
        'for v in flag': lambda S, B, ret: ('每个数都检查完了' if 'v' in B and S.v == B.v and S.v == list(S.flag)[-1] and 'res' in B else f'检查 `{S.v}`'),
        'if cnt[v]': lambda S, B, ret: (
            f'`cnt[{S.v}] = {S.cnt[S.v]}`，`flag[{S.v}] = {S.flag[S.v]}` → ==至少 3 次且等间隔，特别整数=='
            if S.flag[S.v] and S.cnt[S.v] >= 3 else
            f'`cnt[{S.v}] = {S.cnt[S.v]}`，`flag[{S.v}] = {S.flag[S.v]}` → 不合格'),
        'res += 1': '又找到一个特别整数 → `res = {res}`',
        'return res': '返回特别整数的个数 =={ret}==',
    },
    skip=['pre = {}', 'diff = {}', 'cnt = {}', 'flag = {}'],
    max_steps=90,
    cards=dict(
        one_liner='记住上次下标和约定的差，差变了就作废',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['特别整数：在 `nums` 中==至少出现三次==，且所有出现下标等间隔','返回不同的特别整数个数','本视频：`[1,8,1,5,1,5,8,5,8,3,3,3]` → `3`（1、5、3；8 的间隔不等）'],
        quote='对于等间隔出现这个条件，则需要记录每个元素上一次出现的位置，以及已经约定好的下标差才方便判断。除此之外，还需要标记每种元素的下标差是否合法。',
        quote_src='—— yiduobo 题解',
        idea=['`pre` 记上次下标，`diff` 记约定的差，`cnt` 记次数，`flag` 记差是否一直合法',
              '首次出现：初始化；再次出现：和约定的差比较，不同就把 `flag` 置 False，再更新 `diff`、`pre`、`cnt`',
              '遍历完后，`flag` 为真且 至少 3 次且等间隔 的数就是特别整数'],
        summary=['时间 `O(n)`，空间 `O(n)`（四个哈希表）',
                 '易错点：第二次出现时 `diff` 还是 None，不能拿来比较',
                 '和 I 题的区别只在最后一处判断：`cnt[v] >= 3`，出现更多次也行',
                 '一旦 `flag` 为 False 就不会再变回 True',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行'],
    ),
)
