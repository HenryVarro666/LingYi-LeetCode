CONFIG = dict(
    num=1395, title='统计作战单位数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间 + 树状数组正反扫描',
    tags=['树状数组'],
    code='''
class Solution(object):
    def numTeams(self, rating):

        n = len(rating)
        new_rating = [0] * n
        cnt = 1
        for num, index in sorted([[x, index] for index, x in enumerate(rating)], key=lambda d:d[0]):
            new_rating[index] = cnt
            cnt += 1

        suffix_array = [0] * (n + 1)
        left = []
        for num in new_rating:
            left.append(self.sum(num - 1, suffix_array))
            self.add(num, n, suffix_array)
        
        suffix_array = [0] * (n + 1)
        right = []
        for num in new_rating[::-1]:
            right.append(self.sum(num - 1, suffix_array))
            self.add(num, n, suffix_array)
        right.reverse()

        res = 0
        for index in range(1, n - 1):
            res += left[index] * (n - index - 1 - right[index]) + right[index] * (index - left[index])
        
        return res

    def sum(self, x, suffix_array):
        res = 0
        while x:
            res += suffix_array[x]
            x -= x & -x
        
        return res

    def add(self, x, n, suffix_array):
        while x <= n:
            suffix_array[x] += 1
            x += x & -x
''',
    call='Solution().numTeams([2,5,3,4])',
    expect=1,
    views=[
        dict(type='array', var='rating', label='rating（身高各不相同）', h=150),
        dict(type='array', var='new_rating', label='new_rating：按大小重排成 1..n 的名次', h=150),
        dict(type='array', var='suffix_array', label='suffix_array：树状数组（下标 1..n）', h=150),
        dict(type='array', var='left', label='left[i]：i 前面比它矮的人数', h=150),
        dict(type='array', var='right', label='right[i]：i 后面比它矮的人数', h=150),
    ],
    watch=['num', 'x', 'cnt', ('res', 'res', 'green')],
    captions={
        'new_rating[index] = cnt': '`rating[{index}] = {num}` 排第 `{cnt}` 小 → `new_rating[{index}] = {cnt}`（名次 1..n，树状数组好用）',
        'left.append': '`num = {num}`：前面已出现的人里比它矮的有 `sum({num}-1)` = =={left[-1]}== 个，记入 left',
        'right.append': '倒着扫：`num = {num}` 后面比它矮的有 =={right[-1]}== 个，记入 right',
        'self.add(num, n, suffix_array)': '把名次 `{num}` 登记进树状数组，后面的人就能数到它',
        'right.reverse()': '倒着存的，翻回来：`right[i]` 对应第 i 个人',
        'res += left[index]': '以第 `{index}` 人当中间：前矮 `{left[index]}` × 后高 `{n-index-1-right[index]}` + 后矮 `{right[index]}` × 前高 `{index-left[index]}`，`res` = =={res}==',
        'res += suffix_array[x]': '累加 `suffix_array[{x}]`，`res` = {res}',
        'x -= x & -x': '`x -= x & -x` → {x}：去掉最低位的 1',
        'suffix_array[x] += 1': '`suffix_array[{x}]` += 1',
        'x += x & -x': '`x += x & -x` → {x}：跳到下一个管着它的格子',
        'return res': '`return res`：{res}',
    },
    skip=['while x', 'res = 0', 'n = len', 'cnt += 1', 'cnt = 1', 'left = []', 'right = []', 'suffix_array = [0]'],
    max_steps=72,
    cards=dict(
        one_liner='三连不等式先下手中间人：前矮×后高 + 前高×后矮',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`rating` 里每个人评分不同，选 3 人 `i<j<k`',
                 '要求评分严格递增或严格递减，求方案数',
                 '示例：`[2,5,3,4]` → `1`：只有 (2,3,4)'],
        quote='一般这种三连不等式的问题，都是先从中间这个人下手，因为这样就可能将问题分割成两个相同的子问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['中间人前方矮 `l1`、高 `t1`；后方矮 `l2`、高 `t2`',
              '递增：`l1 × t2`；递减：`t1 × l2`',
              '分数各不同 → 高的人数 = 总数 − 矮的人数；只需正反两趟用树状数组数「比我矮的人」'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先把评分排序成名次 1..n：评分范围大时也能用树状数组',
                 '`sum(num-1)` 查比自己矮的个数；两趟之间要重置树状数组',
                 '只枚举 `1..n-2` 的中间人，首尾不能当中间',
                 '原文代码无需改动即可在 Python 3 运行'],
    ),
)
