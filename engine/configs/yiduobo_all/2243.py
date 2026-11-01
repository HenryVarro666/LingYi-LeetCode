CONFIG = dict(
    num=2243, title='计算字符串的数字和', difficulty='Easy', category='模拟',
    author='yiduobo', technique='直接模拟 · 拆分求和合并', tags=[],
    code='''
class Solution(object):
    def digitSum(self, s, k):

        num_list = [int(x) for x in list(s)]
        while len(num_list) > k:
            next_list = []
            for start in range(0, len(num_list), k):
                next_list.append(0)
                for index in range(start, min(start + k, len(num_list))):
                    next_list[-1] += num_list[index]
            
            next_s = ''.join([str(x) for x in next_list])
            num_list = [int(x) for x in list(next_s)]

        return ''.join([str(x) for x in num_list])
''',
    call='Solution().digitSum("123456789", 3)',
    expect='126',
    views=[
        dict(type='array', var='num_list', pointers={'start': 'blue', 'index': 'pink'},
             color=lambda S, i, v: 'blue' if 'start' in S and S['start'] <= i < S['start'] + S['k'] else None,
             h=230, label='num_list（框 = 当前这一组）'),
        dict(type='array', var='next_list', h=200, label='next_list（各组数字和）'),
    ],
    watch=['k', ('start', 'start', 'blue'), ('index', 'index', 'pink'), ('len(num_list)', 'len(num_list)', 'green')],
    captions={
        'num_list = [int(x) for x in list(s)]': '先把字符串拆成数字列表：`{num_list}`，方便求和',
        'while len(num_list) > k': lambda S, B, r: (f'长度 `{len(S.num_list)} > {S.k}`：还要再操作一轮' if len(S.num_list) > S.k else f'长度 `{len(S.num_list)} <= {S.k}`：不用再操作，跳出循环'),
        'next_list = []': '这一轮的结果先放进新列表 `next_list`',
        'next_list.append(0)': '新的一组：开一个累加位，初值 0；组内下标到 `min(start + k, 总长)`，最后一组可能不足 k 个',
        'next_list[-1] +=': '`num_list[{index}] = {num_list[index]}` 加进这一组 → `{next_list[-1]}`',
        'next_s =': '各组的和拼成字符串 `"{next_s}"`：和可能是两位数，下一轮就变长了',
        'num_list = [int(x) for x in list(next_s)]': '再拆回一位一位的数字：`{num_list}`，回去判断长度',
        'return': '长度已不超过 k，把数字拼回字符串返回 `"{ret}"`',
    },
    cards=dict(
        one_liner='题目怎么说就怎么做：拆分、求和、合并，重复到够短',
        complexity='时间 `O(n^2)` 量级，空间 `O(n)`',
        problem=['数字串 `s`，每 `k` 位一组，每组换成数字和，再拼接',
                 '长度仍大于 `k` 就重复，直到长度不超过 `k`',
                 '示例：`"123456789", k=3` → `"126"`'],
        quote='没有什么好的思路，不过好在题目给出的字符串长度比较短，因此可以直接按照题目描述的操作进行模拟',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 最长 100，直接照做：不断重复==拆分-求和-合并==',
              '先转成整数列表，用 `range(0, n, k)` 按步长 k 取每组起点',
              '每轮结果先拼成字符串，再重新拆回数字，用 `len > k` 判断是否终止'],
        summary=['时间 `O(n^2)` 量级，空间 `O(n)`，`n ≤ 100` 足够',
                 '易错点：最后一组不足 `k` 位，要用 `min(start + k, len)` 防越界',
                 '一组的和可能是两位数，所以必须经过字符串再拆开，不能直接当一个数字',
                 '原文本身可在 Python 3 直接运行，未做修改'],
    ),
)
