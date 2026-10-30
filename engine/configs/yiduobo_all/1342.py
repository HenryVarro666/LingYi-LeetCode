def _b(x):
    return list(format(x, 'b'))

CONFIG = dict(
    num=1342, title='将数字变成 0 的操作次数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='按位拆解：1 的个数 + 位数 - 1',
    tags=['位运算', '基础题'],
    code='''
class Solution(object):
    def numberOfSteps(self, num):

        res = 0
        while num:
            if num & 1:
                res += 1
                if num == 1:
                    break
            
            num //= 2
            res += 1
        
        return res
''',
    call='Solution().numberOfSteps(14)',
    expect=6,
    views=[
        dict(type='string', var=lambda S: _b(S['num']) if S.get('num') else ['0'], label='num 的二进制', h=200,
             color=lambda S, i, v: 'yellow' if v == '1' else None),
        dict(type='text', fn=lambda S: f"`num = {S['num']}`，已操作 =={S['res']}== 次", size=34),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计步数',
        'while num': lambda S, B, r: (f'`num = {S.num}`，继续' if S.num else '`num = 0`，结束'),
        'if num & 1': '`num & 1` = {num & 1}：最低位是 {num & 1} → {"奇数，要减 1" if num & 1 else "偶数，直接右移"}',
        7: '减 1 算一步：`res` → {res}',
        12: '除以 2 算一步：`res` → {res}',
        'if num == 1': lambda S, B, r: ('`num == 1`：只剩最高位，减 1 就变成 0，不用再除以 2 → ==break==' if S.num == 1 else f'`num = {S.num} ≠ 1`，还要继续除以 2'),
        'num //= 2': '除以 2 = 二进制右移一位：`num` = {num}',
        'return': '一共 =={ret}== 步',
    },
    cards=dict(
        one_liner='答案 = 1 的个数 + 二进制位数 - 1',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['偶数除以 2，奇数减 1，求变成 0 的步数',
                 '示例：`num=14` → `6`'],
        quote='答案就等于num二进制表示中1的数目，加上num二进制表示的位数，然后再减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数减 1：只是把最低位的 1 去掉，对应一个 1',
              '除以 2：把二进制右移一位，要移到只剩一位',
              '最高位的 1 不用减（直接 break），所以总数再减 1'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '`num == 1` 时减 1 后就是 0，要立刻 `break`',
                 '原文为 Python 2 写法，`num /= 2` 已改为 `num //= 2`'],
    ),
)
