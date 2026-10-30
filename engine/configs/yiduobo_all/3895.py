def _digits(S):
    x = S.get('v', 0)
    return list(str(x)) if x > 0 else ['0']


def _col(S, i, v):
    if 'v' not in S or S['v'] <= 0:
        return None
    if i == len(str(S['v'])) - 1:
        return 'green' if int(v) == S['digit'] else 'pink'
    return None


def _text(S):
    if 'v' not in S:
        return '遍历 `nums`，对每个 `v` 模 10 取个位、除以 10 去个位'
    if S['v'] <= 0:
        return f"`v` 已经变成 0：这个数拆完了，目前 `res = {S['res']}`"
    return f"`v = {S['v']}`：`v % 10 = {S['v'] % 10}`，要找的 `digit = {S['digit']}`"


CONFIG = dict(
    num=3895, title='统计数字出现总次数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='遍历 + 模 10 分离数位', tags=[],
    code='''
class Solution(object):
    def countDigitOccurrences(self, nums, digit):
        
        res = 0
        for v in nums:
            while v:
                if v % 10 == digit:
                    res += 1
                v //= 10
        
        return res
''',
    call='Solution().countDigitOccurrences([101, 20, 5, 30], 0)',
    expect=3,
    views=[
        dict(type='text', fn=_text, size=30, h=80),
        dict(type='array', var='nums', label='nums（这次找数字 0）', cell=110, h=190),
        dict(type='array', var=_digits, label='当前 v 的各数位（最后一格 = v % 10：绿 = 命中，粉 = 没命中）', cell=110,
             color=_col, h=200),
    ],
    watch=[('v', 'v', 'blue'), ('digit', 'digit', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录 `digit` 出现的总次数',
        'for v in nums': lambda S, B, r: (f'一趟遍历：取出 `v = {S.v}`' if S.v else '`nums` 遍历完毕，退出循环'),
        'while v': lambda S, B, r: (f'`v = {S.v}` 非零，还有数位要看' if S.v else '`v = 0`：数位分离完，回到 for 取下一个数'),
        'if v % 10 == digit': '模 10 得到个位 `{v % 10}`，和 `digit = {digit}` {"相同，命中" if v % 10 == digit else "不同"}',
        'res += 1': '命中一次，`res` = =={res}==',
        'v //= 10': '除以 10 丢掉个位，`v` 变成 {v}',
        'return res': '遍历完毕，`digit` 共出现 =={ret}== 次',
    },
    cards=dict(
        one_liner='一趟遍历，模 10 取个位、除 10 去个位，数一数',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['数组 `nums` 和数字 `digit`',
                 '求 `digit` 在全部元素的十进制表示中出现的总次数',
                 '本视频：`[101,20,5,30]`，`digit = 0` → `3`'],
        quote='对nums进行一趟遍历，对于当前遍历到的元素v，通过模10除以10的方法分离出其中的数位，然后统计digit在其中出现的次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `while v:` 当 `v` 变成 0 就停止',
              '每轮 `v % 10` 是当前最低位，等于 `digit` 就计一次',
              '`101` 里的中间 0 也会被模出来：`101 → 10 → 1 → 0`'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`nums[i] >= 1`，所以 `while v` 不会漏掉数字本身为 0 的情况',
                 '`digit = 0` 时中间的 0 也要算，上面示例正好演示',
                 '原文为 Python 2 风格（继承 object、无类型标注），无需改动，代码原样运行'],
    ),
)
