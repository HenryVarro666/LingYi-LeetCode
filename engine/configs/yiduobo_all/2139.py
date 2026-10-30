CONFIG = dict(
    num=2139, title='得到目标值的最少行动次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='倒推 · 偶数就减半',
    tags=['难度分 1417'],
    code='''
class Solution(object):
    def minMoves(self, target, maxDoubles):

        res = 0
        while target > 1 and maxDoubles > 0:
            if target % 2 == 0:
                target //= 2
                maxDoubles -= 1
                res += 1
            else:
                target -= 1
                res += 1
        
        res += target - 1
        return res
''',
    call='Solution().minMoves(19, 2)',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: f'当前要到达的 `target = {S["target"]}`（倒推：从 19 往 1 走）' if 'target' in S else '', size=34, h=120),
        dict(type='text', fn=lambda S: f'剩余加倍次数 `maxDoubles = {S["maxDoubles"]}`，已用操作 `res = {S["res"]}`' if 'res' in S else '', size=30, h=100),
        dict(type='text', fn=lambda S: ('加倍次数用完或到 1：剩下全靠 +1，共 `target − 1 = ' + str(S['target'] - 1) + '` 次') if 'res' in S and (S['target'] <= 1 or S['maxDoubles'] <= 0) else '', size=28, h=100),
    ],
    watch=[('target', 'target', 'blue'), ('maxDoubles', 'maxDoubles', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录已经用掉的操作次数',
        'while target > 1': lambda S, B, r: (f'`target = {S.target} > 1` 且 `maxDoubles = {S.maxDoubles} > 0`，继续倒推' if S.target > 1 and S.maxDoubles > 0
                                             else f'`target = {S.target}`，`maxDoubles = {S.maxDoubles}`：不用再倒推了'),
        'if target % 2 == 0': '`{target} % 2 == 0` → {"偶数：可以由一半加倍得到" if target % 2 == 0 else "奇数：只能由 target − 1 加 1 得到"}',
        'target //= 2': '偶数且有加倍次数：`{B.target}` 是 `{target}` 加倍来的，倒推成 `{target}`，==加倍越晚越赚==，剩 `{maxDoubles}` 次',
        'res += 1': '这一步花掉一次操作，`res = {res}`',
        'target -= 1': '奇数只能由 `{target}` 加 1 得到，倒推成 `{target}`',
        'res += target - 1': '加倍用完（或已到 1）：从 1 加到 `{target}` 需要 `{target} − 1` 次 +1，`res = {res}`',
        'return res': '最少 `{res}` 次行动',
    },
    cards=dict(
        one_liner='加倍留到数大的时候用，倒推：偶数就减半',
        complexity='时间 `O(log target)`，空间 `O(1)`',
        problem=['从 `1` 出发，每次 `+1` 或 `×2`，`×2` 至多 `maxDoubles` 次',
                 '求到达 `target` 的最少操作数',
                 '本视频：`target = 19, maxDoubles = 2` → `7`'],
        quote='使用加倍操作相当于节省了target - 2次操作次数。为了使得总的操作数尽可能少，那么当target越大时使用加倍操作就越赚，因此在这里可以倒推',
        quote_src='—— yiduobo 题解原文',
        idea=['不加倍要 `target − 1` 次，加倍省的次数随 target 变大而变多',
              '倒推：偶数且还能加倍就减半，奇数只能减 1',
              '加倍用完后，剩下全是 +1，直接 `target − 1`'],
        summary=['时间 `O(log target)`，空间 `O(1)`',
                 '易错点：奇数不能加倍得到，必须先 −1',
                 '循环结束后别忘了加上 `target − 1`',
                 '原文为 Python 2 写法，`target /= 2` 已改为 `target //= 2`'],
    ),
)
