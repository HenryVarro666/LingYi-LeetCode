CONFIG = dict(
    num=2160, title='拆分数位后四位数字的最小和', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='数位排序 · 小的放十位',
    tags=['灵神题单', '难度分 1314'],
    code='''
class Solution(object):
    def minimumSum(self, num):

        num_list = sorted([num // 1000, num // 100 % 10, num // 10 % 10, num % 10])
        return num_list[0] * 10 + num_list[1] * 10 + num_list[2] + num_list[3]
''',
    call='Solution().minimumSum(2932)',
    expect=52,
    views=[
        dict(type='array', var='num_list', label='排序后的四个数位（前两个放十位，后两个放个位）', cell=110,
             color=lambda S, i, v: 'green' if i < 2 else 'blue'),
        dict(type='text', fn=lambda S: (f"两个两位数：`{S['num_list'][0]}{S['num_list'][2]}` + `{S['num_list'][1]}{S['num_list'][3]}`"
                                        f" = ==`{S['num_list'][0]*10+S['num_list'][1]*10+S['num_list'][2]+S['num_list'][3]}`==")
                                       if 'num_list' in S else '', size=30),
    ],
    watch=['num', 'num_list'],
    captions={
        'num_list = sorted': '拆出四个数位 `num // 1000`、`num // 100 % 10`、`num // 10 % 10`、`num % 10`，排序得 `{num_list}`',
        'return': '较小的两个放十位：`{num_list[0]}×10 + {num_list[1]}×10 + {num_list[2]} + {num_list[3]}` = =={ret}==',
    },
    cards=dict(
        one_liner='拆成两个两位数，最小的两个数字放十位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['四位正整数 `num`，把四个数位全部用上，拆成两个整数（可有前导 0）',
                 '求两个整数之和的==最小值==',
                 '示例：`2932` → `52`（`23 + 29`）'],
        quote='为了使得和最小，显然应该构造出两个两位数，同时将数字中较小的两个放在十位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['位数越多，高位权重越大，所以拆成两个两位数最划算',
              '十位权重是 10，个位是 1：==小数字放十位==',
              '排序后答案 = 前两个 ×10 + 后两个'],
        after=[dict(heading='为什么不是三位数 + 一位数', lines=[
            '`2932`：`223 + 9 = 232`，远大于 `23 + 29 = 52`',
            '三位数的百位权重是 100，一个高位数字就吃亏',
            '两个两位数时只有十位权重 10，把最小的两个放上去最划算',
            '`4009` 排序得 `0,0,4,9` → `0 + 0 + 4 + 9 = 13`'])],
        summary=['时间、空间都是 `O(1)`（只有四个数字）',
                 '易错：`/` 在 Python 3 是浮点除法，必须用 `//`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '同类题：2578 最小和分割（位数不固定时交替分配）'],
    ),
)
