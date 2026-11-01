CONFIG = dict(
    num=1903, title='字符串中的最大奇数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='倒序找最后一个奇数位',
    tags=['贪心与思维', '难度分 1249'],
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
    call='Solution().largestOddNumber("2718460")',
    expect='271',
    views=[
        dict(type='string', var='num', label='num（从右往左找第一个奇数）', cell=90,
             pointers={'index': 'pink', 'p': 'blue'}, window=None,
             color=lambda S, k, v: ('green' if k <= S['p'] else None) if S.get('p', len(S['num'])) < len(S['num'])
             else ('pink' if k == S.get('index') else None),
             dim=lambda S, k, v: S.get('p', len(S['num'])) < len(S['num']) and k > S['p']),
        dict(type='text', fn=lambda S: (f"`p = {S['p']}`：前缀 `num[:{S['p']+1}]` = `{S['num'][:S['p']+1]}`" if 'p' in S and S['p'] < len(S['num'])
                                        else ''), size=28),
    ],
    watch=[('n', 'n'), ('index', 'index', 'pink'), ('p', 'p', 'blue')],
    captions={
        'n = len': '数字串长度 `n = {n}`',
        'p = n': '`p = n` 表示“还没找到奇数位”',
        'for index': '从最低位往高位看，当前 `index = {index}`，数字 `{num[index]}`',
        'if int(num[index])': lambda S, B, r: (f"`{S.num[S.index]} % 2 = {int(S.num[S.index]) % 2}` → ==是奇数=="
                                                if int(S.num[S.index]) % 2 == 1
                                                else f"`{S.num[S.index]}` 是偶数，这一位不能当末位，继续往左"),
        'p = index': '最后一个奇数位在 `p = {p}`',
        'break': '找到了，不用再往前看',
        'if p == n': lambda S, B, r: ('`p == n`：一个奇数位都没有 → 返回空串' if S.p == S.n
                                       else f'`p = {S.p} ≠ n`：有奇数位 → 返回前缀 `num[:{S.p + 1}]`'),
        "return ''": '没有奇数，返回 `""`',
        'return num': '返回 `"{ret}"`',
    },
    cards=dict(
        one_liner='位数越多越大，奇数的末位必是奇数：找最后一个奇数位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个大整数字符串 `num`，求所有子串中==最大的奇数==',
                 '没有奇数就返回空串',
                 '本视频：`"2718460"` → `"271"`'],
        quote='为了使得最终结果最大，那么就需要位数尽可能多。由于一个奇数的最低位必然也是奇数，只需要从后向前找到字符串中的最后一个奇数所在的位置p。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想最大：位数要尽可能多，所以子串从头开始',
              '再想奇数：末位是奇数，所以从后往前找第一个奇数位 `p`',
              '答案就是前缀 `num[:p + 1]`；`p` 一直等于 `n` 说明没找到'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`p = n` 用来标记“没找到”，最后据此返回空串',
                 '原文是 Python 2 风格，只删去了类型说明文档字符串，其余不变'],
    ),
)
