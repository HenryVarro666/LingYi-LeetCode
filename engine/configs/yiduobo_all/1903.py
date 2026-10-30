CONFIG = dict(
    num=1903, title='字符串中的最大奇数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='从后找最后一个奇数位', tags=['灵神题单', '贪心与思维', '难度分 1249'],
    code='''
class Solution(object):
    def largestOddNumber(self, num):

        n = len(num)
        p = n
        for index in range(n - 1, -1, -1):
            if int(num[index]) % 2 == 1:
                p = index
                break
        
        if p == n:
            return ''
        else:
            return num[:p + 1]
''',
    call="Solution().largestOddNumber('4235468')",
    expect='4235',
    views=[
        dict(type='text', fn=lambda S: ('从后往前找最后一个奇数位：当前看下标 `' + str(S['index']) + '`，数字 `' + S['num'][S['index']] + '`') if 'index' in S else '`p = n` 表示还没找到奇数位'),
        dict(type='string', var='num', label='num', h=300, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if S.get('p', len(S['num'])) < len(S['num']) and i <= S['p'] else None)),
        dict(type='text', fn=lambda S: ('找到！答案是前缀 `num[:' + str(S['p'] + 1) + ']` = ==' + S['num'][:S['p'] + 1] + '==') if 'p' in S and S['p'] < len(S['num']) else '绿色 = 最终答案的前缀', size=30),
    ],
    watch=['n', ('p', 'p', 'orange'), 'index'],
    captions={
        'n = len': '`n = len(num) = {n}`',
        'p = n': '`p = n = {p}`：先假设没有奇数位，`p == n` 代表「没找到」',
        'for index': '从最后一位往前看，下标 `index = {index}`',
        'if int(num[index])': lambda S, B, r: f'`num[{S.index}] = {S.num[S.index]}`：' + ('是奇数 → 它可以当答案的末位' if int(S.num[S.index]) % 2 else '是偶数，不能当末位 → 继续往前'),
        'p = index': '找到最靠后的奇数位 `p = {p}`：位数尽量多，所以取最靠后的',
        'break': '已经是最后一个奇数位，不用再往前找，==break==',
        'if p == n': '`p = {p}`，`n = {n}`：`p == n` 吗？不成立说明找到了奇数位',
        "return ''": '没有任何奇数位 → 返回空串',
        'return num[:p + 1]': '前缀 `num[:{p} + 1]` 最长且以奇数结尾 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='末位是奇数才是奇数：取到最后一个奇数位为止的前缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`num` 是表示大整数的字符串，在所有非空子串中找值最大的奇数',
                 '没有奇数就返回空串 `""`',
                 '示例：`"52"` → `"5"`；`"4206"` → `""`；本视频：`"4235468"` → `"4235"`'],
        quote='为了使得最终结果最大，那么就需要位数尽可能多。由于一个奇数的最低位必然也是奇数，只需要从后向前找到字符串中的最后一个奇数所在的位置p。',
        quote_src='—— yiduobo 题解原文',
        idea=['位数越多值越大 → 子串要尽量长，直接取前缀',
              '奇数的最低位是奇数 → 前缀必须停在一个奇数位上',
              '从后往前找第一个奇数位 `p`，答案就是 `num[:p + 1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`p = n` 当哨兵，表示没找到；别和有效下标混淆',
                 '前缀一定从下标 0 开始，因为 `num` 没有前导零',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
