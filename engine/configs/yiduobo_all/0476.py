CONFIG = dict(
    num=476, title='数字的补数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='补数 + num = 2^k - 1',
    tags=['位运算', '基础题'],
    code='''
class Solution(object):
    def findComplement(self, num):

        pow2 = 1
        while pow2 <= num:
            pow2 <<= 1
        
        return pow2 - 1 - num
''',
    call='Solution().findComplement(25)',
    expect=6,
    views=[
        dict(type='array', var=lambda S: [1, 2, 4, 8, 16, 32, 64], label='2 的幂：pow2 逐步左移',
             pointers={'pow2 位置': 'blue'} if False else {},
             color=lambda S, i, v: 'blue' if v == S.get('pow2') else None, h=200),
        dict(type='text', fn=lambda S: f"`pow2 = {S['pow2']}`，`num = {S['num']}`：" + ("`pow2 <= num` → 还要左移" if S['pow2'] <= S['num'] else "`pow2 > num` → 停下，pow2 比 num 多一位"), size=30),
    ],
    watch=['num', ('pow2', 'pow2', 'blue')],
    captions={
        'pow2 = 1': '`pow2` 从 1 开始，每次左移一位，找第一个大于 `num` 的 2 的幂',
        'while pow2 <= num': lambda S, B, r: (f'`{S.pow2} <= {S.num}` → 还不够大，继续' if S.pow2 <= S.num else f'`{S.pow2} > {S.num}` → 够了，`pow2 = 2^k`，k 就是 num 的位数'),
        'pow2 <<= 1': '左移一位，乘 2：`pow2` = {pow2}',
        'return': '`num + 补数` = 全 1 = `pow2 - 1` = {pow2 - 1}，所以补数 = `{pow2} - 1 - {num}` = =={ret}==',
    },
    cards=dict(
        one_liner='补数 + num = 全 1 = 2^k - 1',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['把二进制表示逐位取反再转十进制，求补数',
                 '本视频：`num=25 = 11001` → 补数 `00110` = `6`'],
        quote='补数加上num必然是1111..111这种形式，而这里的1111..111 = 2^k - 1，这里的k则可以通过num的长度获取到。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一位 num 和补数恰好一个是 1 → 相加必然全是 1',
              '全 1 的数等于 `2^k - 1`，k 是 num 的位数',
              '循环左移求出第一个大于 num 的 2 的幂，减去 1 再减 num'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '`while pow2 <= num`：用 `<=`，保证 pow2 比 num 多一位',
                 '原文作者提醒：此法在 C 里可能越界，Python 整数无此问题',
                 '原文本身可在 Python 3 运行，没有改动'],
    ),
)
