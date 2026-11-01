CONFIG = dict(
    num=2139, title='得到目标值的最少行动次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='倒推 · 大数才值得加倍',
    tags=['灵神题单', '贪心与思维', '难度分 1417'],
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
        dict(type='text', size=44, h=120, fn=lambda S: f"`target = {S['target']}`，剩余加倍 `{S['maxDoubles']}` 次，已用 `{S['res']}` 步" if 'res' in S else ''),
        dict(type='text', size=34, h=120, fn=lambda S: (f"一次加倍省下约 `target − 2 = {S['target']-2}` 步：target 越大越赚" if 'res' in S and S['target'] > 2 else '')),
    ],
    watch=[('target', 'target', 'blue'), ('maxDoubles', 'maxDoubles', 'pink'), ('res', 'res', 'green')],
    captions={
        'while target > 1': lambda S, B, r: (f'`target = {S.target}`，加倍还剩 `{S.maxDoubles}` 次 → 继续倒推'
                                              if S.target > 1 and S.maxDoubles > 0 else
                                              (f'没有加倍次数了' if S.maxDoubles == 0 else '`target = 1`，已回到起点') + '，退出循环'),
        'if target % 2 == 0': lambda S, B, r: (f'`{S.target}` 是偶数：它可以由 `{S.target // 2}` 加倍而来，==绝佳时机=='
                                                if S.target % 2 == 0 else f'`{S.target}` 是奇数：只可能由 `{S.target - 1}` 加 1 得到'),
        'target //= 2': '从 `target / 2` 加倍得到：`target` → =={target}==（原文的 `/=` 在 Python 3 要写 `//=`）',
        'maxDoubles -= 1': '用掉一次加倍，还剩 `{maxDoubles}` 次',
        'target -= 1': '奇数只能靠加 1：`target` → =={target}==',
        'res += 1': '这一步算 1 次行动：`res = {res}`',
        'res += target - 1': '加倍用完（或到 1）：剩下全靠加 1，需要 `{B.target} - 1` 步 → `res = {res}`',
        'return res': '最少行动次数 =={res}==',
    },
    cards=dict(
        one_liner='一次加倍省 `target - 2` 步，所以留给最大的数',
        complexity='时间 `O(min(maxDoubles, log target))`，空间 `O(1)`',
        problem=['从 `1` 出发，每步 `+1` 或 `×2`，`×2` 至多用 `maxDoubles` 次',
                 '求得到 `target` 的最少步数',
                 '示例：`target = 19, maxDoubles = 2` → `7`'],
        quote='使用加倍操作相当于节省了target - 2次操作次数。为了使得总的操作数尽可能少，那么当target越大时使用加倍操作就越赚，因此在这里可以倒推。',
        quote_src='—— yiduobo 题解原文',
        idea=['不加倍要 `target - 1` 步；加倍一次省 `target - 2` 步',
              '倒推分三种：无加倍次数 → 直接加 `target - 1`；偶数 → 折半；奇数 → 减 1',
              '循环条件同时检查 `target > 1` 和 `maxDoubles > 0`'],
        summary=['时间 `O(min(maxDoubles, log target))`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `target /= 2` 已改为 `target //= 2`',
                 '易错点：循环结束后别忘了 `res += target - 1`',
                 '对比灵神：灵神循环里直接 return；yiduobo 退出循环后统一补'],
    ),
)
