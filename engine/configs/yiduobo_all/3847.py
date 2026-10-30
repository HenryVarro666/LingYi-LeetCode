CONFIG = dict(
    num=3847, title='计算比赛分数差', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 符号变量 sign',
    tags=[],
    code='''
class Solution(object):
    def scoreDifference(self, nums):
        
        res = 0
        sign = 1
        for index, v in enumerate(nums):
            if v % 2 == 1:
                sign *= -1
            if index % 6 == 5:
                sign *= -1
            
            res += v * sign
        
        return res
''',
    call='Solution().scoreDifference([2,4,2,1,2,1,3,4])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（第 index 场的得分）', pointers={'index': 'blue'}, cell=90, h=200),
        dict(type='text', h=110, size=32, fn=lambda S: (('sign = ==+1==：第一位玩家主动，得分加到 res' if S['sign'] == 1 else 'sign = ==−1==：第二位玩家主动，得分从 res 扣掉') if 'sign' in S else '')),
        dict(type='text', h=90, size=30, fn=lambda S: f"第一位 − 第二位 = `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['index', 'v', ('sign', 'sign', 'pink'), ('res', 'res', 'green')],
    captions={
        'sign = 1': '`sign = 1`：==+1 表示第一位玩家主动==，−1 表示第二位主动',
        'if v % 2 == 1': '`v = {v}` {"是奇数 → 换人" if v % 2 == 1 else "是偶数 → 不换"}',
        'sign *= -1': '换人：`sign` 乘 −1 → ==`{sign}`==',
        'if index % 6 == 5': '`index % 6 = {index % 6}` → {"第 6 场，要再换人" if index % 6 == 5 else "不是第 6 场"}',
        'res += v * sign': '`res += {v} × ({sign})` → ==`{res}`==（正的算第一位，负的算第二位）',
        'return res': '第一位总分 − 第二位总分 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='sign 记谁主动，得分乘 sign 直接累加成分数差',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两位玩家，第一位一开始是主动玩家；主动玩家拿到当场得分',
                 '得分为奇数换人；每第 6 场（`index = 5, 11, ...`）也换人',
                 '求第一位总分减第二位总分'],
        quote='可以使用一个标记变量sign来表示目前是谁在进行比赛。当sign为1时，表示第一位玩家是主动玩家，当sign为-1时，则表示第二位玩家是主动玩家。',
        quote_src='—— yiduobo 题解原文',
        idea=['只要分数差，不必分别记两人总分',
              '`sign = ±1`，`v * sign` 恰好是这场对分数差的贡献',
              '先按奇偶、再按第 6 场修正 `sign`，最后累加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：先换人再加分',
                 '奇数且恰好第 6 场时换两次，`sign` 不变',
                 '对比灵神：灵神用 0/1 下标和异或分别记两人，yiduobo 用 ±1 直接记差'],
    ),
)
