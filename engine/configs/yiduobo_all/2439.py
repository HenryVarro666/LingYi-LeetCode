def _col(S, i, v):
    if 'index' not in S:
        return None
    return 'green' if i <= S['index'] else None


def _dim(S, i, v):
    return 'index' in S and i > S['index']


def _txt(S):
    if 'index' not in S or 'now' not in S:
        return ''
    k = S['index'] + 1
    s = f"前 `{k}` 个数之和 `now = {S['now']}`"
    if 'avg' in S:
        s += f"，平均后每个堆 ==`{S['avg']}`=="
    return s


def _best(S):
    if 'res' not in S:
        return ''
    return f"目前所有前缀里最大的上取整平均数：`res = ` =={S['res']}=="


CONFIG = dict(
    num=2439, title='最小化数组中的最大值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='前缀平均数上取整的最大值',
    tags=['数学', '难度分 1965'],
    code='''
class Solution(object):
    def minimizeArrayValue(self, nums):

        res = 0
        now = 0
        for index, num in enumerate(nums):
            now += num
            avg = now // (index + 1)
            if now % (index + 1) != 0:
                avg += 1
            
            res = max(res, avg)
        
        return res
''',
    call='Solution().minimizeArrayValue([3,7,1,6,2])',
    expect=5,
    views=[
        dict(type='text', fn=_txt),
        dict(type='bars', var='nums', pointers={'index': 'blue'}, label='nums（绿色 = 当前前缀）', h=330, color=_col, dim=_dim),
        dict(type='text', fn=_best),
    ],
    watch=[('index', 'index', 'blue'), 'num', ('now', 'now', 'cyan'), 'avg', ('res', 'res', 'green')],
    max_steps=70,
    captions={
        'res = 0': '`res` 记录目前最大的前缀平均数',
        'now = 0': '`now` 是前缀和',
        'for index, num': lambda S, B, r: ('所有前缀都算过了，遍历结束' if B.get('index') == S.index
                                           else f"来到 `nums[{S.index}] = {S.num}`，前缀变成前 `{S.index + 1}` 个数"),
        'now += num': '前缀和 `now = {B.now} + {num} = {now}`',
        'avg = now //': '这 `{index + 1}` 个堆最平均能做到 `{now} // {index + 1} = {avg}`（先向下取整）',
        'if now %': lambda S, B, r: (f"`{S.now} % {S.index + 1} = {S.now % (S.index + 1)} ≠ 0` → 除不尽，必有一堆更高 → 要==向上取整==" if S.now % (S.index + 1) != 0
                                     else f"`{S.now} % {S.index + 1} = 0` → 刚好整除，不用进位"),
        'avg += 1': '向上取整：`avg = {avg}`',
        'res = max': lambda S, B, r: (f"`res = max({B.res}, {S.avg}) = {S.res}`：这个前缀成了新的瓶颈" if S.res != B.res
                                      else f"`res = max({B.res}, {S.avg}) = {S.res}`：不变，前面的瓶颈更大"),
        'return res': '最大的前缀平均数（向上取整）就是答案 `{res}`',
    },
    cards=dict(
        one_liner='答案一定是某个前缀平均数向上取整，取最大的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['可以把 `nums[i]` 的 1 个单位移到 `nums[i-1]`，次数不限',
                 '求操作后数组最大值的最小值',
                 '示例：`[3,7,1,6]` → `5`；本视频用 `[3,7,1,6,2]` → `5`'],
        quote='最终结果必然是某个前缀平均数的向上取整，于是只需一趟遍历，计算所有前缀的平均数向上取整后的结果，然后取其中最大的作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['数只能往左移，所以最大值总能「挪到」`nums[0]` 附近去摊平',
              '后面的数很小时，答案只由前缀决定：`[1,10,1]` 只看 `[1,10]`，摊成 `[6,5,1]`',
              '前缀越长，摊得越平；每个前缀都是一个下限，取最大者'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`now / (index + 1)` 已改为 `//`',
                 '易错：除不尽要 `+1`，因为总和固定，必有一堆多一点',
                 '对比灵神：他先二分答案再模拟，或者用同一个前缀平均数的公式 `(s+i)//(i+1)`'],
    ),
)
