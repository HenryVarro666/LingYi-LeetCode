CONFIG = dict(
    num=3020, title='子集中元素的最大数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 暴力枚举 x',
    code='''
class Solution(object):
    def maximumLength(self, nums):

        res = 1
        freq = Counter(nums)
        for v in freq:
            if v == 1:
                if freq[v] % 2 == 0:
                    res = max(res, freq[v] - 1)
                else:
                    res = max(res, freq[v])
                    
                continue
            
            x = v
            y = x * x
            step = 1
            while freq[x] >= 2 and freq[y] >= 1:
                step += 1
                x, y = y, y * y
            
            res = max(res, step * 2 - 1)

        return res
''',
    call='Solution().maximumLength([2,4,2,4,16,3,9,1,1])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=190),
        dict(type='map', var='freq', label='freq（出现次数）', fmt=lambda k, v: f'{k}: {v}', h=270, font=28),
        dict(type='text', h=90, size=28,
             fn=lambda S: (f"`x = {S['x']}`，`y = {S['y']}`，`step = {S['step']}` → 集合大小 `{S['step']*2-1}`" if 'step' in S else '')),
    ],
    watch=['v', 'x', 'y', 'step', ('res', 'res', 'green')],
    captions={
        'freq = Counter': '用哈希表统计每个数的次数：`{dict(freq)}`',
        'for v in freq': '枚举 `v = {v}` 作为序列最小的数',
        'if v == 1': lambda S, B, r: ('`v = 1` 是特殊情况：平方永远是 1' if S.v == 1 else f'`v = {S.v}` 不是 1，走一般情况'),
        'freq[v] % 2 == 0': '1 出现 `{freq[v]}` 次：偶数个要去掉一个才能凑成奇数长度',
        'res = max(res, freq[v] - 1)': '`res = max({B.res}, {freq[v]} − 1)` = {res}',
        'res = max(res, freq[v])': '奇数个 1 可全部放入：`res` = {res}',
        'continue': '1 处理完，换下一个数',
        'y = x * x': '`y = x^2` = {y}',
        'step = 1': '`step` 是已经通过检测的层数，只放 `x` 自己算 1 层',
        'while freq': '`x = {x}` 至少 2 个？`{freq[x]}`；`y = {y}` 至少 1 个？`{freq[y]}` → {"通过" if freq[x] >= 2 and freq[y] >= 1 else "不满足，停止"}',
        'step += 1': '通过一轮，多加入两个数：`step` → {step}',
        'x, y = y, y * y': '往外推一层：`x = {x}`，`y = {y}`',
        'res = max(res, step * 2 - 1)': '集合大小 = `step × 2 − 1` = {step*2-1}，`res = max({B.res}, {step*2-1})` = =={res}==',
        'return res': '最大集合 =={res}==',
    },
    cards=dict(
        one_liner='先计数，再暴力枚举 x：每过一轮检测，集合多两个数',
        complexity='时间 `O(n log log U)`，空间 `O(n)`',
        problem=['从 `nums` 选子集，排成 `[x, x^2, x^4, …, x^k, …, x^4, x^2, x]`',
                 '求这样的子集最大有多少个元素',
                 '本视频：`[2,4,2,4,16,3,9,1,1]` → `5`'],
        quote='因为是计算自身的乘方，因此增长的速度是非常快的，因此完全可以暴力枚举所有的x，然后检测x是否至少出现了两次同时x^2至少出现了一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表统计次数，因为要知道每个数出现几次',
              '`x = 1` 特殊：奇数次全选，偶数次去掉一个',
              '`x > 1`：x 至少 2 个且 x^2 至少 1 个，就更新为 x^2，每轮多 2 个数，大小为 `轮数×2−1`'],
        summary=['时间 `O(n log log U)`，空间 `O(n)`',
                 '易错：`x = 1` 必须单独处理，否则 `1×1=1` 会死循环',
                 '`freq[y]` 是 `Counter`，缺的键返回 0，不会报错',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神是 `while` 里累计 `res` 再看终点是否在 nums；yiduobo 边检测 x^2 边累计层数'],
    ),
)
