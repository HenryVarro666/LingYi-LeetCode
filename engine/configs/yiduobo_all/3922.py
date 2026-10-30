CONFIG = dict(
    num=3922, title='使二进制字符串连贯的最少翻转次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按 1 的个数分情况',
    tags=['灵神题单', '难度分 1759'],
    code='''
class Solution(object):
    def minFlips(self, s):
        
        one = 0
        for c in s:
            if c == '1':
                one += 1
        
        if one == len(s) or one <= 1:
            return 0
        
        res = len(s) - one
        if s[0] == '1' and s[-1] == '1':
            res = min(res, one - 2)
        else:
            res = min(res, one - 1)
        
        return res
''',
    call='Solution().minFlips("1010101")',
    expect=2,
    views=[
        dict(type='string', var='s', label='s', h=170,
             color=lambda S, i, v: ('green' if v == '1' else None)),
        dict(type='text', fn=lambda S: (f"1 的个数 `one = {S['one']}`，长度 `{len(S['s'])}`" if 'one' in S else ''), h=60),
        dict(type='text', fn=lambda S: (f"候选：全变 1 → `{S['res']}`" if 'res' in S else ''), h=60),
    ],
    watch=['one', ('res', 'res', 'green')],
    captions={
        "if c == '1'": lambda S, B, r: f"`c = '{S.c}'`" + ('，是 1 → 计数' if S.c == '1' else '，是 0 → 跳过'),
        'one += 1': '`one` = =={one}==',
        'if one == len(s)': lambda S, B, r: (f'`one = {S.one}`：全是 1 或至多一个 1，已经连贯 → 答案 0' if (S.one == len(S.s) or S.one <= 1)
                                           else f'`one = {S.one}`：1 有 2 个以上且有 0 → 需要翻转'),
        'res = len(s) - one': '先考虑变成全 1：翻掉所有 0，代价 `{len(s)} - {one}` = =={res}==',
        "if s[0] == '1'": lambda S, B, r: ('两端都是 1 → 可以变成 `1000…0001`，只留两端的 1' if S.s[0] == '1' and S.s[-1] == '1'
                                         else '端点有 0 → 只能留一个 1'),
        'res = min(res, one - 2)': '变成 `1000..0001`：代价 `one - 2` = {one - 2}；`res = min({B.res}, {one - 2})` = =={res}==',
        'res = min(res, one - 1)': '仅留一个 1：代价 `one - 1` = {one - 1}；`res = min({B.res}, {one - 1})` = =={res}==',
        'return res': '最少翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='0 的左右两侧至多各一个 1，所以 1 最多留两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s` 不含子序列 `011`、`110` 才算连贯',
                 '可以翻转任意字符，求最少翻转次数',
                 '示例：`"1010"` → `1`；`"1000"` → `0`'],
        quote='如果最终的s中存在0，那么这个0的左侧和右侧至多只能有一个1，那么这样就可以推导出一个条件：s中如果有0，那么其中1的数量不能大于等于3个。',
        quote_src='—— yiduobo 题解原文',
        idea=['数 1 的个数 `one`：没有 0、没有 1 或只有一个 1 → 已经连贯',
              '否则先算「全变 1」的代价 `len(s) - one`',
              '再看两端：都是 1 → 留 `1000…0001`，代价 `one - 2`；否则留一个 1，代价 `one - 1`',
              '全变 0 一定不比留 1 更省，不用考虑'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先处理 `one <= 1` 直接返回 0，后面才能放心用 `one - 2`',
                 '两端都是 1 时才有资格留两个 1，否则只能留一个',
                 '对比灵神：灵神用 `c0` 和 `c1` 直接取 min；yiduobo 按 1 的个数拆开讨论'],
    ),
)
