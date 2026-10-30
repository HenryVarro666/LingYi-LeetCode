def _b(x, w=3):
    return list(format(x, '0%db' % w))

CONFIG = dict(
    num=476, title='数字的补数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='用全 1 掩码做异或',
    tags=['位运算', '基础题'],
    code='''
class Solution:
    def findComplement(self, num: int) -> int:
        w = num.bit_length()
        return ((1 << w) - 1) ^ num
''',
    call='Solution().findComplement(25)',
    expect=6,
    views=[
        dict(type='string', var=lambda S: _b(S['num'], 5), label='num = 25', h=150),
        dict(type='string', var=lambda S: _b((1 << S['w']) - 1, 5) if 'w' in S else _b(0, 5), label='掩码 (1 << w) - 1',
             color=lambda S, i, v: 'blue' if v == '1' else None, h=150),
        dict(type='string', var=lambda S: _b(((1 << S['w']) - 1) ^ S['num'], 5) if 'w' in S else _b(0, 5), label='掩码 ^ num = 补数',
             color=lambda S, i, v: 'green' if v == '1' else None, h=150),
    ],
    watch=['num', ('w', 'w', 'blue')],
    captions={
        'w = num.bit_length()': '`num = {num}` 二进制是 `{num:b}`，长度 `w = {w}`：只需要取反低 {w} 位',
        'return': '`1 << {w}` = {1 << w}，减 1 得全 1 掩码 `{(1 << w) - 1:b}`；和 `num` 异或，==1 变 0、0 变 1== → =={ret}==（若直接 `~num` 会把高位的 0 也变成 1）',
    },
    cards=dict(
        one_liner='只取反低 w 位：和 w 个 1 做异或',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把整数的二进制表示（无前导零）按位取反，再转十进制',
                 '示例：`5 = 101` → `010` = `2`',
                 '本视频：`25 = 11001` → `00110` = `6`'],
        quote='所以对于这个例子，要只把 num 的低 5 位取反，也就是计算 num 和 11111 的异或。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直接 `~num` 不行：高位的 0 也会被取反',
              '先求二进制长度 `w`，`(1 << w) - 1` 就是 w 个 1',
              '异或 1 等于取反，所以只翻转了低 w 位'],
        after=[dict(heading='为什么不能直接取反', lines=['`num=25` 在 32 位里是 `00…011001`', '`~num` 会把前面 27 个 0 全变成 1', 'Python 里 `~25 = -26`，是负数', '所以用 `w` 位的全 1 掩码，只翻转有效位']), dict(heading='与 1009 的关系', lines=['第 1009 题和本题完全相同', '区别只是 1009 允许输入 `0`', '`0` 的反码按题意是 `1`，要特判', '其余代码一字不差'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：不能直接用 `~num`，Python 的 `~` 会得到负数',
                 '同类题：1009 十进制整数的反码（多一个 0 的特判）'],
    ),
)
