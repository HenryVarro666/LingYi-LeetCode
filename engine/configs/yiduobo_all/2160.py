CONFIG = dict(
    num=2160, title='拆分数位后四位数字的最小和', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='拆数位、排序后分配十位个位',
    tags=['贪心与思维', '难度分 1314'],
    code='''
class Solution(object):
    def minimumSum(self, num):
        num_list = sorted([num // 1000, num // 100 % 10, num // 10 % 10, num % 10])
        return num_list[0] * 10 + num_list[1] * 10 + num_list[2] + num_list[3]
''',
    call='Solution().minimumSum(4009)',
    expect=13,
    views=[
        dict(type='text', fn=lambda S: f"num = `{S['num']}`：千、百、十、个位依次取出", size=30),
        dict(type='array', var='num_list', label='num_list（升序：前两个放十位，后两个放个位）', cell=110,
             color=lambda S, k, v: 'blue' if k < 2 else 'pink'),
        dict(type='text', fn=lambda S: (f"`{S['num_list'][0]}×10 + {S['num_list'][1]}×10 + {S['num_list'][2]} + {S['num_list'][3]}` = =={S['num_list'][0]*10 + S['num_list'][1]*10 + S['num_list'][2] + S['num_list'][3]}==" if 'num_list' in S else ''), size=28),
    ],
    watch=[('num', 'num')],
    captions={
        'num_list = sorted': '`num // 1000`、`num // 100 % 10`、`num // 10 % 10`、`num % 10` 取出四个数位并排序 → `{num_list}`',
        'return': '较小的两个放十位：`{num_list[0]}×10 + {num_list[1]}×10`；较大的两个放个位：`{num_list[2]} + {num_list[3]}` → =={ret}==',
    },
    cards=dict(
        one_liner='和要小，就拿两个两位数，小的数字放十位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['四位数 `num` 拆成 `new1`、`new2`，每个数位都要用，允许前导 0',
                 '求两数之和最小',
                 '本视频：`4009` → `13`（`4 + 9`）'],
        quote='为了使得和最小，显然应该构造出两个两位数，同时将数字中较小的两个放在十位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['位数越多的数越大，所以两个数都取两位',
              '十位的权重是个位的 10 倍，较小的两个数字放十位',
              '分离数位并排序得 `num_list`，套公式即可'],
        after=[dict(heading='验证示例 2932', lines=['数位排序：`[2, 2, 3, 9]`', '十位放 `2, 2`，个位放 `3, 9`：`29 + 23`', '`2×10 + 2×10 + 3 + 9 = 52`，和示例一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '排序后最小的两个下标 0、1 对应十位，所以乘 10',
                 '公式：`num_list[0]*10 + num_list[1]*10 + num_list[2] + num_list[3]`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去了类型说明文档字符串'],
    ),
)
