CONFIG = dict(
    num=3175, title='找到连续赢 K 场比赛的第一位玩家', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='打擂台 · 维护最大值下标', tags=[],
    code='''
class Solution:
    def findWinningPlayer(self, skills: List[int], k: int) -> int:
        max_i = win = 0
        for i in range(1, len(skills)):
            if skills[i] > skills[max_i]:  # 打擂台，发现新的最大值
                max_i = i
                win = 0
            win += 1  # 获胜回合 +1
            if win == k:  # 连续赢下 k 场比赛
                break
        # 如果 k 很大，那么 max_i 就是 skills 最大值的下标，毕竟最大值会一直赢下去
        return max_i
''',
    call='Solution().findWinningPlayer([4,2,6,3,9], 2)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"擂主 `{S['max_i']}` 号（技能 =={S['skills'][S['max_i']]}==），已连胜 ==`{S['win']}`== / `{S['k']}` 场", size=30),
        dict(type='bars', var='skills', pointers={'max_i': 'pink', 'i': 'blue'}, h=420,
             color=lambda S, i, v: 'pink' if i == S['max_i'] else None),
    ],
    watch=[('max_i', 'max_i', 'pink'), ('i', 'i', 'blue'), ('win', 'win', 'green'), ('k', 'k', 'yellow')],
    captions={
        'max_i = win': '擂主先定为 0 号，连胜数 `win = 0`',
        'for i in range': '下一位挑战者是 `{i}` 号，技能 `{skills[i]}`',
        'if skills[i] >': '挑战者 `{skills[i]}` 对擂主 `{skills[max_i]}`：{"挑战者更强，擂主易位" if skills[i] > skills[max_i] else "擂主更强，守擂成功"}',
        'max_i = i': '新擂主上台：`max_i = {max_i}`',
        'win = 0': '换了擂主，他的连胜重新数：`win = 0`',
        'win += 1': '这一场擂主赢了（新擂主靠击败旧擂主赢下这一场）：`win` → =={win}==',
        'if win == k': '`win = {win}`，要连赢 `k = {k}` 场 → {"达标，结束" if win == k else "还不够，继续"}',
        'break': '已经连赢 k 场，擂主就是赢家，跳出循环',
        'return max_i': '赢家是 `{max_i}` 号。若循环跑完都没达标，说明 k 很大，最大值会一直赢下去，答案也是它',
    },
    cards=dict(
        one_liner='把队列模拟成打擂台：只需记住擂主和连胜数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 位玩家按编号排队，队首两人比技能，高者留队首，败者去队尾',
                 '第一个连续赢下 `k` 场的人是赢家，返回他的编号',
                 '示例：`skills = [4,2,6,3,9], k = 2` → `2`'],
        quote='本题和 5.19 的每日一题 1535 几乎一样，把代码中的 mx 改成最大值的下标即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['败者去队尾，但队尾的人迟早也要面对擂主，所以==只需按下标顺序依次挑战==',
              '挑战者更强：擂主易位，连胜清零再 +1；否则擂主连胜 +1',
              '`win == k` 立刻返回；k 太大就会遍历完，答案是最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`，不必真的模拟队列',
                 '==换擂主时 win 先清零再 +1==：新擂主已经赢了旧擂主一场',
                 '`k` 可达 `10^9`，循环只走一遍 `n`，不会超时',
                 '与 1535 的区别：这里返回最大值的下标而不是值'],
    ),
)
