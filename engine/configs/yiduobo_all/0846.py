CONFIG = dict(
    num=846, title='一手顺子', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='计数 + 未完结顺子数 now',
    code='''
class Solution(object):
    def isNStraightHand(self, hand, W):

        n = len(hand)
        if n % W != 0:
            return False
        
        cnt_dict = {}
        stop_dict = {}
        num_list = []
        for num in sorted(hand):
            if num not in cnt_dict:
                cnt_dict[num] = 1
                num_list.append(num)
            else:
                cnt_dict[num] += 1
        
        now = 0
        for num in num_list:
            if cnt_dict[num] < now:
                return False
            else:
                if cnt_dict[num] > now:
                    stop_num = num + W - 1
                    if cnt_dict.get(stop_num, 0) < cnt_dict[num] - now:
                        return False
                    stop_dict[stop_num] = cnt_dict[num] - now
                now = cnt_dict[num] - stop_dict.get(num, 0)
        
        return now == 0
''',
    call='Solution().isNStraightHand([1,2,2,3,3,4], 3)',
    expect=True,
    views=[
        dict(type='array', var='hand', label='hand（W = 3，每组 3 张连续的牌）', cell=90, h=150),
        dict(type='array', var='num_list', label='num_list（去重后从小到大的点数）', cell=90, h=170,
             color=lambda S, i, v: 'blue' if S.get('num') == v else None),
        dict(type='map', var='cnt_dict', label='cnt_dict：点数 → 张数', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='map', var='stop_dict', label='stop_dict：在该点数结束的顺子数', fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', size=30, h=90,
             fn=lambda S: f"未完结的顺子 now = =={S['now']}==" if 'now' in S else ''),
    ],
    watch=['n', 'num', 'now', ('stop_num', 'stop_num', 'orange')],
    captions={
        'n % W != 0': '`{n} % {W} = {n % W}`：{"不是 W 的倍数，没法分组 → False" if n % W else "张数是 W 的倍数，继续"}',
        'cnt_dict[num] = 1': '第一次见到 `{num}`：计数 1，并记入 `num_list`',
        'cnt_dict[num] += 1': '`{num}` 又出现一次 → 共 `{cnt_dict[num]}` 张',
        'now = 0': '`now` = 当前还没结束、需要继续接牌的顺子数，从 0 开始',
        'if cnt_dict[num] < now': lambda S, B, r: (f'`{S.cnt_dict[S.num]} < now = {S.now}`：'
            + ('这点数的牌不够接 now 个顺子 → False' if S.cnt_dict[S.num] < S.now else '牌够接，继续')),
        'if cnt_dict[num] > now': lambda S, B, r: (f'`{S.cnt_dict[S.num]} > now = {S.now}`：'
            + ('多出来的牌要作为新顺子的起点' if S.cnt_dict[S.num] > S.now else '刚好够，没有新起点')),
        'stop_num = num + W - 1': '多出的牌当起点，顺子终点必然是 `{num} + {W} - 1` = =={stop_num}==',
        'if cnt_dict.get(stop_num, 0)': '终点 `{stop_num}` 有 `{cnt_dict.get(stop_num, 0)}` 张，要新开 `{cnt_dict[num] - now}` 个顺子：{"不足 → False" if cnt_dict.get(stop_num, 0) < cnt_dict[num] - now else "足够"}',
        'stop_dict[stop_num] =': '有 `{stop_dict[stop_num]}` 个顺子将在 `{stop_num}` 处结束',
        'now = cnt_dict[num]': '`now = {cnt_dict[num]} - {stop_dict.get(num, 0)} = =={now}==`：共 cnt 个顺子，扣掉在此结束的',
        'return now == 0': '最后 `now = {now}`：{"没有未完结的顺子 → True" if now == 0 else "还有顺子没结束 → False"}',
    },
    cards=dict(
        one_liner='用 now 记录还没结束的顺子数，一趟扫完点数',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['`hand` 是手里的牌，能否重新排成若干组，每组 `W` 张且点数连续',
                 '能返回 `true`，否则 `false`',
                 '示例：`[1,2,2,3,3,4]`，`W = 3` → `true`（1,2,3 和 2,3,4）'],
        quote='可以使用一个变量now来表示当前有多少个尚未完结的顺子。我们同样是将卡片按点数从小到大进行排序，但是这里我们将同样点数的卡片归在一起，并记录起数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点数有 `cnt` 张：先接上 `now` 个未完结顺子，多出的当新起点',
              '新起点的终点是 `num + W - 1`，那里要有足够的牌，记入 `stop_dict`',
              '`now = cnt - stop_dict[num]`：在这里结束的顺子不再往后接'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '先判断 `n % W`，不整除直接 False',
                 '易错：`cnt < now` 说明牌不够接；终点牌数也要检查',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
