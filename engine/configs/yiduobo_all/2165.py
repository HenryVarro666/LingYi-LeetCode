def _txt(S):
    if 'num_list' not in S:
        return f"`num = {S.get('num', '')}`：先看正负，再决定数字怎么排"
    return f"数字拆成 `{''.join(S['num_list']) or '（空）'}`" + ('（符号为负）' if S.get('neg_flag') else '（符号为正）')


CONFIG = dict(
    num=2165, title='重排数字的最小值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='正负分开讨论 · 排序后换掉前导零',
    tags=['灵神题单', '难度分 1362'],
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
        dict(type='text', fn=_txt, size=28, h=130),
        dict(type='array', var='num_list', pointers={'p': 'blue'}, h=300, label='num_list（各位数字）',
             color=lambda S, i, v: 'blue' if i == S.get('p') and S.get('_line', 0) >= 20 else None),
    ],
    watch=[('num', 'num', 'blue'), 'neg_flag', 'p'],
    captions={
        'if num == 0': '`num = {num}`：不是 0，还有可排的空间',
        'neg_flag = False': '`neg_flag` 记住符号，先假设是正数',
        'if num < 0': '`num = {num}`：{"负数，取绝对值" if num < 0 else "是正数，符号不用管"}',
        'num_list = []': '准备一个列表，存 `num` 的每一位',
        'while num:': '`num = {num}`：{"还有数位，继续拆" if num else "拆完了"}',
        'num_list.append': '取个位 `{num_list[-1]}` 放进列表：`{num_list}`',
        'num //= 10': '去掉个位，`num` → {num}',
        'if neg_flag': '`neg_flag = {neg_flag}`：正数要==绝对值最小==，所以从小到大排',
        'num_list = sorted': '从小到大排序：`{num_list}`',
        'p = 0': '`p` 从最高位开始，找第一个不是 0 的数字',
        'while num_list[p]': '`num_list[{p}] = {num_list[p]}`：{"是 0，不能放最高位，继续往后找" if num_list[p] == "0" else "不是 0，找到了"}',
        'p += 1': '`p` → {p}',
        'num_list[0], num_list[p]': '把第一个非零数字换到最高位：`{num_list}`，这样就没有前导 0',
        'return int': '拼起来得到 `{ret}`',
    },
    cards=dict(
        one_liner='正数从小到大排，再把第一个非零数字换到最高位',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['重排 `num` 的各位数字，使值最小且不含前导零，正负号不变',
                 '示例：`310` → `103`；`-7605` → `-7650`',
                 '本视频：`310` → `103`'],
        quote='正数的最小值就是绝对值最小，而负数的最小值则要求绝对值最大，因此需要分开讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num = 0` 没有操作空间，答案就是 0',
              '负数：绝对值越大越小，数字从大到小排',
              '正数：绝对值越小越好，从小到大排',
              '正数排好后，把第一个非零数字换到最高位，去掉前导 0'],
        summary=['时间、空间都与位数成正比，即 `O(log n)`',
                 '易错点：负数不会有前导零问题，只有正数需要换位',
                 '`num` 是 0 要先单独返回，否则后面找非零数字会越界',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`'],
    ),
)
