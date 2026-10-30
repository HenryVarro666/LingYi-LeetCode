def _txt(S):
    line = S.get('_line')
    if 'f' not in S:
        return '先数一数：每个数字出现了几次'
    f = S['f']
    if 'res' not in S:
        return f"统计：数字 ==`{S['num']}`== 出现了 ==`{f[S['num']]}`== 次"
    x = S['num']
    k = f[x]
    if line == 9:
        return f'从小到大扫描：现在处理数字 ==`{x}`==（共 39999 个，只演示前面一段）'
    if k > 1:
        return f'`{x}` 有 `{k}` 个 → 留 1 个，其余 ==`{k - 1}`== 个各 +1 变成 `{x + 1}`，花 `{k - 1}` 次操作'
    return f'`{x}` 至多 1 个 → 已经唯一，什么都不用做'


def _col(S, i, v):
    if 'res' not in S:
        return 'blue' if v else None
    x = S.get('num')
    if i == x:
        return 'orange' if v > 1 else 'green'
    if i < x:
        return 'green' if v else None
    return 'blue' if v else None


CONFIG = dict(
    num=945, title='使数组唯一的最小增量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='计数 + 从小到大逐格进位',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def minIncrementForUnique(self, A):

        f = [0] * 40000
        for num in A:
            f[num] += 1

        res = 0
        for num in range(39999):
            if f[num] > 1:
                res += f[num] - 1
                f[num + 1] += f[num] - 1

        if f[-1] > 1:
            res += (f[-1] - 1) * f[-1] // 2

        return res
''',
    call='Solution().minIncrementForUnique([3,2,1,2,1,7])',
    expect=6,
    trace_limit=39, snap_maxlen=12,
    truncated_caption='…… 数组共 39999 格，后面的 `num` 同理：没有重复就什么也不做，快进到结束 ……',
    views=[
        dict(type='array', var='A', label='A（输入数组）', cell=70, h=170),
        dict(type='array', var='f', label='f[x] = 数字 x 有几个（绿 = 已处理，橙 = 有重复；只画前 12 格）',
             pointers={'num': 'blue'}, color=_col, cell=76, h=250),
        dict(type='text', fn=_txt, size=30, h=120),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [0] * 40000': '开一个 40000 格的计数数组 `f`：`f[x]` = 数字 `x` 出现的次数（值域是 0 ~ 39999）',
        'f[num] += 1': '数字 `{num}` 又出现了一次：`f[{num}]` = =={f[num]}==',
        'for num in A': lambda S, B, r: ('数完了：`f` 里记好了每个数出现的次数' if sum(S.f) == len(S.A)
                                         else f'取下一个数 `num = {S.num}`'),
        'res = 0': '`res` 累计操作次数',
        'for num in range(39999)': '从 0 到 39998 逐个处理：现在轮到 `num = {num}`',
        'if f[num] > 1': lambda S, B, r: (f'`f[{S.num}] = {S.f[S.num]}` 大于 1 → 有重复，多出来的要往上推' if S.f[S.num] > 1
                                          else f'`f[{S.num}] = {S.f[S.num]}` 不大于 1 → 没有重复，跳过'),
        'res += f[num] - 1': '`{num}` 有 `{f[num]}` 个，留 1 个，多出的 `{f[num] - 1}` 个各加 1 → `res` += {f[num] - 1} → =={res}=='
                             ,
        'f[num + 1] += f[num] - 1': '这 `{f[num] - 1}` 个变成了 `{num + 1}`：并入 `f[{num + 1}]` → =={f[num + 1]}==，下一轮还要继续处理它们',
    },
    cards=dict(
        one_liner='先数每个数出现几次，从小到大把多出来的往上推一格',
        complexity='时间 `O(V)`，空间 `O(V)`（`V = 40000` 是值域）',
        problem=['每次操作可以把数组里的某个数 `+1`',
                 '要让数组里的数==两两不同==，最少要操作几次',
                 '示例：`[3,2,1,2,1,7]` → `6`（变成 `[3,4,1,2,5,7]`）'],
        quote='对于当前处理的x，若目前存在k个x且k大于1，那么就执行k - 1次操作，将k - 1个x变为x + 1，同时更新答案，并将dict中x + 1出现的次数加上k - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['数 `x` 出现 `k` 次：至少要把 `k − 1` 个推到 `x + 1`，花 `k − 1` 次',
              '推上去的数会和 `x + 1` 原有的数碰到一起，所以==从小到大==处理，把它们并入 `f[x + 1]`',
              '值域只有 0 ~ 39999，数组大小固定，所以直接扫 39999 格'],
        after=[dict(heading='扫完之后：最后一格 39999', lines=[
            '扫到 39998 后，0 ~ 39998 每个数都只有 1 个了',
            '39999 可能还有 `k` 个，推上去是 40000，没有下一格可并入',
            '依次推：`(k − 1) + (k − 2) + … + 1`',
            '= `(k − 1) × k / 2`，对应代码 `res += (f[-1] - 1) * f[-1] // 2`',
        ])],
        summary=['时间 `O(V)`、空间 `O(V)`，`V = 40000`；与数组长度无关',
                 '循环固定扫 39999 格，视频只演示前面一段，其余快进',
                 '易错：只扫到 39998，最后一格 39999 要用等差数列公式收尾',
                 '原文为 Python 2 写法，公式里的整数除法 `/` 已改为 `//`',
                 '`f[num + 1]` 累加的是被推上来的个数，处理它时要把这些一起算上'],
    ),
)
