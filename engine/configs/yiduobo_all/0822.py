CONFIG = dict(
    num=822, title='翻转卡片游戏', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排除正反相同 · 找最小',
    code='''
class Solution(object):
    def flipgame(self, fronts, backs):

        ban_set = set()
        for index in range(len(fronts)):
            if fronts[index] == backs[index]:
                ban_set.add(fronts[index])
        
        res = 0
        for num in fronts:
            if num not in ban_set and (res == 0 or res > num):
                res = num
        for num in backs:
            if num not in ban_set and (res == 0 or res > num):
                res = num
                
        return res
''',
    call='Solution().flipgame([1,2,4,4,7], [1,3,4,1,3])',
    expect=2,
    views=[
        dict(type='array', var='fronts', pointers={'index': 'blue'}, h=170, label='fronts（正面）'),
        dict(type='array', var='backs', pointers={'index': 'blue'}, h=170, label='backs（背面）'),
        dict(type='set', var='ban_set', h=130, label='ban_set（正反相同的数）'),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ban_set = set': '`ban_set` 存「同一张卡两面都有」的数',
        'for index in range(len': '逐张卡片检查正反面是否相同',
        'if fronts[index] == backs[index]': '第 `{index}` 张：`{fronts[index]}` 和 `{backs[index]}` {"相同 → 这个数不可能是答案" if fronts[index] == backs[index] else "不同 → 跳过"}',
        'ban_set.add': '`{fronts[index]}` 进入 `ban_set`：{ban_set}',
        'res = 0': '`res = 0` 表示还没找到答案（也是无解时的返回值）',
        'for num in fronts': '先扫所有正面的数',
        'for num in backs': '再扫所有背面的数',
        'if num not in ban_set': lambda S, B, r: (f'`{S.num}` 在 ban_set 里 → 不能要' if S.num in S.ban_set else (f'`{S.num}` 可用；`res = {S.res}`，' + ('还没有答案 → 采用它' if S.res == 0 else (f'`{S.num}` < `{S.res}` → 更小，采用' if S.res > S.num else f'`{S.num}` 不比 `{S.res}` 小 → 不换')))),
        'res = num': '最小候选更新为 `res = {res}`',
        'return res': '没被排除的最小数字：`{res}`',
    },
    cards=dict(
        one_liner='正反相同的数必须排除，剩下的数里取最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 张卡片，每张正面 `fronts[i]`、背面 `backs[i]`，可以任意翻转',
                 '选一张卡，若它背面的数不与任何卡的正面相同，这个数就是想要的',
                 '求其中最小的，没有返回 `0`；示例：`[1,2,4,4,7]`、`[1,3,4,1,3]` → `2`'],
        quote='如果一张卡片的正反两面都是同一个数字的话，那么这个数字必然不能成为答案。而对于除开这类数字之外其他数字，由于其不会同时出现在同一张卡片的两边，因此只需要将该数字翻到卡片的背面就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍卡片，把两面相同的数放进 `ban_set`',
              '其他数字总能翻到背面，所以只剩「取不在 ban_set 的最小数」',
              '正面、背面各扫一遍，用 `res == 0` 表示还没有候选'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`res = 0` 既是「未找到」也是「无解」的返回值，更新时要写 `res == 0 or res > num`',
                 '正面和背面都要扫，答案可能来自任何一面',
                 '对比灵神：灵神用生成器 + `min(default=0)` 一行完成，这里是两个显式循环'],
    ),
)
