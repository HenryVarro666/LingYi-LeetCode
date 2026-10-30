CONFIG = dict(
    num=1518, title='换水问题', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='模拟：每换一次少 numExchange-1 瓶', tags=[],
    code='''
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        ans = 0
        while numBottles >= numExchange:
            ans += numExchange  # 吨吨吨~
            numBottles -= numExchange - 1
        return ans + numBottles
''',
    call='Solution().numWaterBottles(9, 3)',
    expect=13,
    views=[
        dict(type='text', h=120, size=34,
             fn=lambda S: (f"手上 `numBottles` = =={S['numBottles']}==　兑换需要 `{S['numExchange']}`" if 'ans' in S else '')),
        dict(type='text', h=120, size=34,
             fn=lambda S: (f"已喝 `ans` = =={S['ans']}==" if 'ans' in S else '')),
    ],
    watch=['numBottles', 'numExchange', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录喝掉的瓶数，从 0 开始',
        'while numBottles': lambda S, B, r: (f'`{S.numBottles} >= {S.numExchange}`：还能换 → 继续' if S.numBottles >= S.numExchange
                                             else f'`{S.numBottles} < {S.numExchange}`：不够换了 → 退出循环'),
        'ans += numExchange': '吨吨吨：喝掉 `{numExchange}` 瓶，`ans = {ans}`',
        'numBottles -= ': '空瓶换 1 瓶新水：手上少 `{numExchange}` 再多 1，==净减 `{numExchange-1}`== → `numBottles = {numBottles}`',
        'return ans': '剩下的 `{numBottles}` 瓶也喝掉：`{ans} + {numBottles}` = `{ret}`',
    },
    cards=dict(
        one_liner='每兑换一次，喝掉 numExchange 瓶，手上净减 numExchange-1',
        complexity='时间 `O(numBottles / numExchange)`，空间 `O(1)`',
        problem=['`numExchange` 个空瓶可换一瓶水，起初有 `numBottles` 瓶',
                 '喝完变空瓶，求最多能喝几瓶',
                 '示例：`numBottles = 9, numExchange = 3` → `13`'],
        quote='如果 numBottles ≥ numExchange，那么我们可以用 numExchange 瓶水换 1 瓶水……相当于把 numBottles 减少了 numExchange−1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['够换就换：先喝掉 `numExchange` 瓶，答案加上它',
              '换回 1 瓶，手上瓶数净减 `numExchange - 1`',
              '循环到不够换，把剩下的全喝掉'],
        summary=['时间 `O(numBottles / numExchange)`，空间 `O(1)`',
                 '易错点：循环条件是 ==`>=`==，恰好等于 numExchange 也能换',
                 '方法二公式：`numBottles + (numBottles - 1) // (numExchange - 1)`，`O(1)`',
                 '循环了多少次，就是额外多得到多少瓶'],
    ),
)
