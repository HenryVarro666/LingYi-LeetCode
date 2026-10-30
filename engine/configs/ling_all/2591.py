CONFIG = dict(
    num=2591, title='将钱分给最多的儿童', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='先分 1 美元 + 分类讨论', tags=['灵神题单', '难度分 1531'],
    code='''
class Solution:
    def distMoney(self, money: int, children: int) -> int:
        money -= children  # 每人至少 1 美元
        if money < 0: return -1
        ans = min(money // 7, children)  # 初步分配，让尽量多的人分到 8 美元
        money -= ans * 7
        children -= ans
        # children == 0 and money：必须找一个前面分了 8 美元的人，分配完剩余的钱
        # children == 1 and money == 3：不能有人恰好分到 4 美元
        if children == 0 and money or \\
           children == 1 and money == 3:
            ans -= 1
        return ans
''',
    call='Solution().distMoney(20, 3)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: f"剩余 `money = {S['money']}`，未满 8 美元的人数 `children = {S['children']}`" + (f"，已有 `ans = {S['ans']}` 人分到 8 美元" if 'ans' in S else '')),
        dict(type='array', var=lambda S: [8] * S['ans'] + [1] * S['children'] if 'ans' in S else [1] * S['children'], label='每个孩子当前的钱（先各 1 美元）', h=240, cell=70,
             color=lambda S, i, v: 'green' if v == 8 else None),
    ],
    skip=['children == 1 and money == 3:'],
    watch=['money', 'children', ('ans', 'ans', 'green')],
    captions={
        'money -= children': '每人先发 1 美元：`money = {B.money} - {B.children} = {money}`',
        'if money < 0': '`money < 0`？不够每人 1 美元 → 无解返回 -1',
        'ans = min': '剩余的钱每 7 美元可让 1 人变成 8 美元：`min({money} // 7, {children})` = =={ans}==',
        'money -= ans': '这 `{ans}` 人各用掉 7 美元，剩 `money = {money}`',
        'children -= ans': '还没到 8 美元的人剩 `{children}` 个',
        'if children == 0': '特判：`children == {children}`、`money == {money}`。没人可分但钱有剩，或只剩 1 人且恰好 3 美元（会变成 4）→ 都要让一个 8 美元的人少一个',
        'ans -= 1': '`ans` 减一 → {ans}',
        'return ans': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='先保证每人 1 美元，再尽量多地凑 8 美元',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `money` 美元分给 `children` 个孩子：钱要全分完，每人至少 1 美元，没人恰好 4 美元',
                 '求最多有几个孩子恰好得到 8 美元，无解返回 `-1`',
                 '示例：`money=20, children=3` → `1`'],
        quote='首先，每人至少分配 1 美元，把 money 减少 children。如果 money<0，返回 -1。然后不断给每个人 7 美元（前面分配了 1 美元）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每人先 1 美元，剩下的钱每 7 美元让一个人变成 8',
              '两种坏情形：全都 8 美元了还有剩钱；或只剩 1 人且恰好 3 美元（= 4）',
              '这两种情形都让答案减 1，其余情形剩余的钱给同一个人即可'],
        summary=['`ans = min(money // 7, children)`',
                 '`children == 0 and money`：剩余的钱只能加到某个 8 美元的人身上',
                 '`children == 1 and money == 3`：那人会得到 4 美元，不合法',
                 '注意 `children >= 2` 保证了其他情况可以拆开分'],
    ),
)
