CONFIG = dict(
    num=2591, title='将钱分给最多的儿童', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按 p 与 children 的大小关系分类', tags=['灵神题单', '贪心与思维', '难度分 1531'],
    code='''
class Solution(object):
    def distMoney(self, money, children):

        if money < children:
            return -1
        
        money -= children
        p = money // 7
        if p > children:
            return children - 1
        elif p == children:
            if p * 7 == money:
                return p
            else:
                return p - 1
        else:
            if money - p * 7 == 3 and p == children - 1:
                return p - 1
            else:
                return p
''',
    call='Solution().distMoney(20, 3)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: f"`money = {S['money']}`，`children = {S['children']}`" + (f"，`p = {S['p']}`（最多 p 份 7 美元）" if 'p' in S else '')),
        dict(type='array', var=lambda S: [1] * S['children'], label='每个孩子先分到 1 美元', h=240, cell=70),
    ],
    watch=['money', 'children', ('p', 'p', 'green')],
    captions={
        'if money < children': '钱不够每人 1 美元？`{money} < {children}` → 不成立，继续',
        'money -= children': '每人先发 1 美元，剩 `money = {money}`',
        'p = money': '剩下的钱最多可分出 `p = {money} // 7 = {p}` 份 7 美元',
        'if p > children': '`p > children`？`{p} > {children}` → {"成立：钱太多，多出的给最后一人，答案 `children - 1`" if p > children else "不成立"}',
        'elif p == children': '`p == children`？`{p} == {children}` → {"成立：每人 7 美元，要看钱是否恰好用完" if p == children else "不成立，说明 p < children"}',
        'if p * 7 == money': '`p*7 = {p*7}`，`money = {money}`：恰好分完才算 p 个人都是 8 美元',
        'if money - p * 7 == 3': '`p < children`：剩 `{money - p*7}` 美元；若恰为 3 且只剩一人，那人会拿到 4 美元，不合法',
        'return p - 1': '答案要少一个：返回 =={ret}==',
        'return p': '最多 `p` 人拿到 8 美元：返回 =={ret}==',
        'return children - 1': '返回 =={ret}==',
        'return -1': '无法保证每人 1 美元，返回 -1',
    },
    cards=dict(
        one_liner='令 p = 剩余钱 // 7，对 p 与 children 做三种比较',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `money` 美元分给 `children` 个孩子：钱要全分完，每人至少 1 美元，没人恰好 4 美元',
                 '求最多有几个孩子恰好得到 8 美元',
                 '示例：`money=20, children=3` → `1`'],
        quote='若这里的p大于children，说明剩余的钱太多了，最多分出p - 1个7美元，而多出来的部分则可以分给最后这个人。',
        quote_src='—— yiduobo 题解',
        idea=['`money < children` 直接 -1；否则每人先 1 美元，令 `p = money // 7`',
              '`p > children`：答案 `children - 1`；`p == children`：恰好分完才是 `p`，否则 `p - 1`',
              '`p < children`：剩 3 美元且只剩一人时，只能让 `p - 1`'],
        summary=['原文为 Python 2 写法，其中整数除法 `/` 已改为 `//`',
                 '`p == children` 时别忘了检查 `p * 7 == money`',
                 '`p < children` 的特例：剩 3 美元且恰好只剩 1 个人',
                 '三种情形共用同一个 `p`，逻辑比先扣再判更直白'],
    ),
)
