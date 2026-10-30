CONFIG = dict(
    num=2243, title='计算字符串的数字和', difficulty='Easy', category='模拟',
    author='yiduobo', technique='直接模拟 拆分-求和-合并',
    tags=[],
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
    call="Solution().digitSum('11111222223', 3)",
    expect='135',
    views=[
        dict(type='array', var='num_list', label='当前数字 num_list（黄框 = 正在求和的这一组）', h=180, cell=64,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'yellow' if 'start' in S and S['start'] <= i < S['start'] + S['k'] and S.get('_line') not in (None,) and 'next_list' in S else None),
        dict(type='array', var='next_list', label='这一轮每组的和 next_list', h=150, cell=64),
        dict(type='text', fn=lambda S: (f"本轮：长度 `{len(S['num_list'])}` > `k = {S['k']}`，继续拆分" if 'num_list' in S else ''), size=26),
    ],
    watch=['k', 'start', 'index', ('num_list', 'num_list', 'cyan'), ('next_list', 'next_list', 'green')],
    skip=['next_list = []', 'next_list.append(0)', 'for start in range', 'for index in range', 'next_s = '],
    max_steps=100,
    captions={
        'list(s)]': lambda S, B, r: f'把字符串变成数字列表：`{S.num_list}`',
        'while len(num_list) > k': lambda S, B, r: (f'长度 `{len(S.num_list)}` > `k = {S.k}` → 再来一轮' if len(S.num_list) > S.k
                                                     else f'长度 `{len(S.num_list)}` ≤ `k = {S.k}` → 不用再拆了'),
        'next_list[-1] += num_list[index]': '这一组累加 `num_list[{index}] = {num_list[index]}` → 本组和 =={next_list[-1]}==',
        'list(next_s)]': lambda S, B, r: f'每组的和拼成字符串 `{S.next_s}`，再拆成新的数字列表 `{S.num_list}`（和可能是两位数）',
        'return': '长度已经 ≤ k，返回 `{ret}`',
    },
    cards=dict(
        one_liner='长度还大于 k 就拆组、求和、拼回去，照着题意模拟',
        complexity='时间约 `O(n)`（每轮长度大幅缩短），空间 `O(n)`',
        problem=['数字串 `s`，只要长度 `> k` 就做一轮：每 `k` 个分一组，组内数字求和，再把和拼成新串',
                 '直到长度 `≤ k`，返回结果',
                 '示例：`s = "11111222223"`，`k = 3` → `"135"`'],
        quote='因此可以直接按照题目描述的操作进行模拟，不断重复拆分-求和-合并，直到字符串的长度小于等于k为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把字符串转成数字列表 `num_list`，方便求和',
              '`range(0, len, k)` 每次跳 k 个，得到每组的起点 `start`',
              '每组和放进 `next_list`，拼成字符串再转回数字（和可能有两位）'],
        summary=['数据范围只有 100，直接模拟就够',
                 '易错点：和可能是多位数，==必须先拼字符串再拆成单个数字==',
                 '最后一组可以不足 k，所以用 `min(start + k, len(num_list))` 防越界',
                 '原文本身是 Python 3 可运行写法，未改动代码'],
    ),
)
