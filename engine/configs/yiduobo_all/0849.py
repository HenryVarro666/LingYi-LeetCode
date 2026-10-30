CONFIG = dict(
    num=849, title='到最近的人的最大距离', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='扫描连续空位段',
    code='''
class Solution(object):
    def maxDistToClosest(self, seats):

        l = None
        res = 0
        for index, num in enumerate(seats):
            if num == 0:
                if l is None:
                    l = index
            else:
                if l is not None:
                    if l == 0:
                        res = max(res, index)
                    else:
                        res = max(res, (index - l + 1) // 2)
                l = None
        
        if l is not None:
            res = max(res, len(seats) - l)

        return res
''',
    call='Solution().maxDistToClosest([1,0,0,0,1,0,0])',
    expect=2,
    views=[
        dict(type='array', var='seats', label='seats（0 = 空位，1 = 有人；蓝 = 空位段起点 l）', cell=90, h=230,
             pointers={'index': 'pink', 'l': 'blue'},
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', size=30, h=90,
             fn=lambda S: f"当前最大距离 res = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'pink'), 'num', ('l', 'l', 'blue'), ('res', 'res', 'green')],
    captions={
        4: '`l` 记录当前连续空位段的起点，现在没有',
        'if num == 0': '`seats[{index}] = {num}`：{"空位" if num == 0 else "有人，一段空位到此结束"}',
        'l = index': '空位段从 `{index}` 开始：`l = {l}`',
        'if l == 0': lambda S, B, r: ('空位段从 0 开始，左侧没人：坐在最左边，到最近的人距离 = `index`' if S.l == 0
                                      else f'空位段在中间（`l = {S.l}`）：坐正中间'),
        'res = max(res, index)': '靠边的段：距离 = `{index}`，`res = max({B.res}, {index}) = {res}`',
        'res = max(res, (index': '中间的段：长 `{index - l}`，坐中间距离 `({index} - {l} + 1) // 2 = {(index - l + 1) // 2}`，`res = {res}`',
        16: '这个人把空位段切断，`l` 重置',
        11: lambda S, B, r: (f'`l = {S.l}` 不为空：前面有一段空位，现在结算' if S.l is not None else '`l` 为空：前面没有空位段，不用结算'),
        18: lambda S, B, r: (f'`l = {S.l}`：右端还有一段空位，靠右边坐' if S.l is not None else '`l` 为空：末尾是人，没有尾部空位段'),
        'res = max(res, len(seats) - l)': '靠右边的段：距离 = `{len(seats)} - {l}` = {len(seats) - l}，`res = {res}`',
        'return res': '最远能坐到离最近的人 `{res}` 远',
    },
    cards=dict(
        one_liner='每段连续空位：靠边坐边上，否则坐正中间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`seats[i] = 1` 有人，`0` 为空位，至少一个空位和一个人',
                 '选一个空位坐下，使到最近的人的距离最大，返回该距离',
                 '示例：`[1,0,0,0,1,0,0]` → `2`'],
        quote='对于一段连续的空位，若这一段空位位于两侧，就选择最边上的座位，否则就选择这一段空位最中间的座位。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到 0 记下段起点 `l`，遇到 1 结算这一段',
              '段从 0 开始：距离是 `index`；中间段：`(index - l + 1) // 2`',
              '扫完后若 `l` 仍非空，说明右端有空位段：`len - l`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：两端的段不能除以 2；末尾的段要在循环后单独处理',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
