CONFIG = dict(
    num='LCP 06', title='拿硬币', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='每堆向上取整',
    code='''
class Solution(object):
    def minCount(self, coins):

        res = 0
        for coin in coins:
            res += (coin + 1) // 2
        
        return res
''',
    call='Solution().minCount([4,2,1,5])',
    expect=7,
    views=[
        dict(type='array', var='coins', label='coins（每堆硬币数）', h=240),
        dict(type='text', fn=lambda S: f"这一堆 `{S['coin']}` 枚：两两拿，需要 `({S['coin']} + 1) // 2` = =={(S['coin'] + 1) // 2}== 次" if 'coin' in S else ''),
        dict(type='text', fn=lambda S: f"累计次数 ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=['coin', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计总共拿的次数，先记 0',
        'for coin in coins': '处理下一堆：这堆有 `{coin}` 枚',
        'res += (coin + 1) // 2': '每次最多拿 2 枚，`{coin}` 枚要 `({coin} + 1) // 2 = {(coin + 1) // 2}` 次（向上取整）→ `res` = =={res}==',
        'return res': '所有堆都拿完，最少共 `{res}` 次',
    },
    cards=dict(
        one_liner='每次尽量拿两枚，一堆 k 枚就要 k/2 向上取整次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['桌上有 n 堆硬币，`coins[i]` 是第 i 堆的数量',
                 '每次选一堆，拿走 1 枚或 2 枚，求拿完所有硬币的最少次数',
                 '本视频：`[4,2,1,5]` → `7`'],
        quote='为了使得拿的次数尽量少，就应该尽量两个两个地拿，那么对于一堆k个硬币而言，拿完地次数就是k除以2向上取整。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次拿得越多越好，所以能拿 2 枚就不拿 1 枚',
              '各堆互不影响，把每堆的次数加起来就是答案',
              '向上取整写成 `(coin + 1) // 2`，奇数堆最后多拿一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：奇数堆要向上取整，`1` 枚也要 1 次',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
