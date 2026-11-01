CONFIG = dict(
    num=2165, title='重排数字的最小值', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='分类讨论 · 0 / 负数 / 正数',
    tags=['灵神题单', '贪心与思维', '难度分 1362'],
    code='''
class Solution(object):
    def smallestNumber(self, num):

        if num == 0:
            return 0

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num
        
        num_list = []
        while num:
            num_list.append(str(num % 10))
            num //= 10
        
        if neg_flag:
            return -int(''.join(sorted(num_list, reverse=True)))
        else:
            num_list = sorted(num_list)
            p = 0
            while num_list[p] == '0':
                p += 1
            num_list[0], num_list[p] = num_list[p], num_list[0]
            return int(''.join(num_list))
''',
    call='Solution().smallestNumber(310)',
    expect=103,
    views=[
        dict(type='array', var='num_list', label='num_list（各位数字，蓝 = p）', cell=110, h=240, pointers={'p': 'blue'}),
        dict(type='text', size=36, h=140, fn=lambda S: f"`num = {S['num']}`，`neg_flag = {S['neg_flag']}`" if 'neg_flag' in S else ''),
    ],
    watch=['num', 'neg_flag', ('p', 'p', 'blue')],
    skip=['neg_flag = False', 'num_list = []'],
    captions={
        'if num == 0': lambda S, B, r: ('`num = 0`：没有操作空间，答案就是 0' if S.num == 0 else '`num` 不是 0，继续分类'),
        'if num < 0': lambda S, B, r: ('负数：要让绝对值尽量大' if S.num < 0 else '正数：要让绝对值尽量小'),
        'num = -num': '取绝对值：`num = {num}`，`neg_flag` 记住符号',
        'while num:': lambda S, B, r: (f'`num = {S.num}` 还有数位，继续拆' if S.num else '`num = 0`：数位拆完'),
        'num_list.append': '取个位 `{num_list[-1]}` 放进 `num_list`',
        'num //= 10': '去掉个位：`num` → {num}（原文的 `/=` 在 Python 3 要写 `//=`）',
        'if neg_flag': lambda S, B, r: ('负数：较大的数字放高位，从大到小排' if S.neg_flag else '正数：较小的数字放高位，从小到大排'),
        'return -int': '降序拼接再加负号 → =={ret}==',
        'num_list = sorted': '从小到大排：`num_list = {num_list}`（可能有前导 0）',
        'while num_list[p]': lambda S, B, r: (f"`num_list[{S.p}] = '{S.num_list[S.p]}'` 是 0 → 继续找" if S.num_list[S.p] == '0' else f"`num_list[{S.p}] = '{S.num_list[S.p]}'`：首个非 0，停下"),
        'p += 1': '`p` 后移到 {p}',
        'num_list[0], num_list[p]': '把首个非 0 数字与最高位交换：`{num_list}`，==没有前导 0==',
        'return int': '拼接得到最小值 =={ret}==',
    },
    cards=dict(
        one_liner='0 直接返回；负数降序；正数升序再换掉前导 0',
        complexity='时间 `O(L log L)`，空间 `O(L)`（`L` 为位数）',
        problem=['重排 `num` 的各位数字，使值最小且没有前导零，符号不变',
                 '示例：`310` → `103`；`-7605` → `-7650`',
                 '本视频：`310` → `103`'],
        quote='正数的最小值就是绝对值最小，而负数的最小值则要求绝对值最大，因此需要分开讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num = 0`：没得排，答案 0',
              '`num < 0`：绝对值越大越小，较大的数字放高位，降序拼接',
              '`num > 0`：升序排；若首位是 0，与第一个非 0 数字交换'],
        summary=['时间 `O(L log L)`，空间 `O(L)`',
                 '原文为 Python 2 写法，整数除法 `num /= 10` 已改为 `num //= 10`',
                 '易错点：先单独处理 0，否则 `while p` 会越界；负数要先取绝对值',
                 '对比灵神：灵神转成字符串再排序；yiduobo 用 `% 10` 逐位拆数字'],
    ),
)
