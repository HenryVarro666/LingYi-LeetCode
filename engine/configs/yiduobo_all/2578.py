CONFIG = dict(
    num=2578, title='最小和分割', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='排序后交替分配',
    tags=['灵神题单', '难度分 1351'],
    code='''
class Solution(object):
    def splitNum(self, num):

        first = second = 0
        for index, digit in enumerate(sorted(list(str(num)))):
            if index % 2 == 0:
                first = first * 10 + int(digit)
            else:
                second = second * 10 + int(digit)
        
        return first + second
''',
    call='Solution().splitNum(4325)',
    expect=59,
    views=[
        dict(type='text', fn=lambda S: f"排序后的数字依次发给 `first` 和 `second`（偶数下标给 first）" if 'digit' in S else '', size=26),
        dict(type='text', fn=lambda S: f"`first = {S.get('first', 0)}`　`second = {S.get('second', 0)}`", size=36),
        dict(type='text', fn=lambda S: f"当前数字：`{S['digit']}`（下标 {S['index']}）→ 给 =={'first' if S['index'] % 2 == 0 else 'second'}==" if 'digit' in S and 'index' in S else '', size=30),
    ],
    watch=['index', 'digit', ('first', 'first', 'blue'), ('second', 'second', 'pink')],
    captions={
        'first = second = 0': '两个数都从 0 开始，一位一位往后拼',
        'for index': lambda S, B, r: f"按从小到大取数字：`digit = {S.digit}`，下标 `{S.index}`",
        'if index % 2 == 0': lambda S, B, r: f"`index = {S.index}` 是{'偶' if S.index % 2 == 0 else '奇'}数 → 给 =={'first' if S.index % 2 == 0 else 'second'}==",
        'first = first * 10': '`first` 末尾接上 `{digit}` → ==`{first}`==：先来的小数字留在高位',
        'second = second * 10': '`second` 末尾接上 `{digit}` → ==`{second}`==：先来的小数字留在高位',
        'return': '`{first} + {second}` = =={ret}==',
    },
    cards=dict(
        one_liner='两个数位数尽量接近，小数字放高位，排序后交替分配',
        complexity='时间 `O(m log m)`，空间 `O(m)`，`m` 为位数',
        problem=['把 `num` 的所有数位分给 `num1`、`num2`（可有前导 0），求两数之和的==最小值==',
                 '示例：`4325` → `59`（`24 + 35`）',
                 '`687` → `75`（`68 + 7`）'],
        quote='为了使得最终的和最小，就应该让参与加法的两个数位数尽量少，也就是这两个数的位数应该尽量接近。',
        quote_src='—— yiduobo 题解原文',
        idea=['位数接近：两个数各取一半数字，高位权重不会堆在同一个数上',
              '每个数里，==较小的数字放高位，较大的放低位==',
              '排序后遍历，偶数下标发给 `first`，奇数下标发给 `second`'],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '数位个数为奇数时，`first` 会多一位，仍然是最优',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '灵神等价写法：排序后 `s[::2]` 与 `s[1::2]` 相加'],
    ),
)
