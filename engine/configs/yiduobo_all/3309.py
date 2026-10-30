def _txt(S):
    if S.get('_line') in (19, 20) and 'v' in S:
        n = S['nums']
        s = ''.join(bin(n[t])[2:] for t in (S['i'], S['j'], S['k']))
        return f'顺序 `[{n[S["i"]]}, {n[S["j"]]}, {n[S["k"]]}]` → ==`{s}`==，值 {int(s, 2)}'
    return '只有 3 个数：枚举全部 6 种排列'


CONFIG = dict(
    num=3309, title='连接二进制表示可形成的最大数值', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='暴力枚举排列',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maxGoodNumber(self, nums):

        length = [0] * 3
        for index, v in enumerate(nums):
            x = v
            while x:
                length[index] += 1
                x >>= 1
        
        res = 0
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                for k in range(3):
                    if i == k or j == k:
                        continue
                    v = (nums[i] << (length[j] + length[k])) + (nums[j] << length[k]) + nums[k]
                    res = max(res, v)
        
        return res
''',
    call='Solution().maxGoodNumber([1,2,3])',
    expect=30,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='nums', cell=130, h=290, label='nums', pointers={'i': 'blue', 'j': 'pink', 'k': 'orange'}),
        dict(type='array', var='length', cell=130, h=230, label='length：每个数的二进制位数'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), ('res', 'res', 'green')],
    captions={
        'length = [0]': '`length[i]` 记录 `nums[i]` 的二进制位数，拼接时要用它来移位',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还没移空，继续数位' if S.x else f'`x` 移空了：`nums[{S.index}]` 共 `{S.length[S.index]}` 位'),
        'length[index] += 1': '位数加一：`length[{index}]` = {length[index]}',
        'x >>= 1': '右移一位，丢掉最低位：`x` = {x}',
        'res = 0': '`res` 保存最大值',
        'if i == j': lambda S, B, r: (f'`i = j = {S.i}`，同一个数不能重复用 → 跳过' if S.i == S.j else f'`i = {S.i}, j = {S.j}` 不同，继续选第三个'),
        'if i == k or j == k': lambda S, B, r: (f'`k = {S.k}` 已被选过 → 跳过' if S.i == S.k or S.j == S.k else f'`k = {S.k}` 是剩下那个数'),
        'v = (nums[i]': '`nums[i]` 左移 `length[j]+length[k]` 位，`nums[j]` 左移 `length[k]` 位，再加 `nums[k]` → ==`{v}`==',
        'res = max': '`res = max({B.res}, {v}) = {res}`',
        'return res': '所有排列里最大的拼接值：`{res}`',
    },
    skip=['continue', 'x = v', 'length[index] += 1', 'x >>= 1', 'while x'],
    max_steps=90,
    cards=dict(
        one_liner='数组只有 3 个，直接枚举 6 种顺序取最大',
        complexity='时间 `O(1)`（固定 3 个数），空间 `O(1)`',
        problem=['长度为 3 的数组，二进制表示按任意顺序连接',
                 '求最大数值',
                 '示例：`[1,2,3]` → `30`（顺序 3,1,2）'],
        quote='由于题目中数组的大小只有3，那么完全可以暴力枚举出所有的排列方式，计算出形成的数值，取其中的最大值作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数出每个数的二进制位数 `length`',
              '三重循环选 i、j、k 互不相同，就是一个排列',
              '拼接值 = 前面的数左移后面所有位数，逐个相加'],
        summary=['时间 `O(1)`，只有 3! = 6 个排列',
                 '易错点：左移的位数是==它后面所有数==的位数之和',
                 '原文已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神把本题当作 179 最大数，用自定义比较排序，数组再大也能做'],
    ),
)
