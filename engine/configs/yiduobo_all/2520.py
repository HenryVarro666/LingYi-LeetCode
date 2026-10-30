def _txt(S):
    if 'tmp' not in S:
        return ''
    if 'v' not in S or S['tmp'] == 0 and S.get('_line') is None:
        return ''
    return f"`num = {S['num']}`，当前位 `v = {S['v']}`，`{S['num']} % {S['v']}` = =={S['num'] % S['v']}=="


CONFIG = dict(
    num=2520, title='统计能整除数字的位数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='摸 10 分离每一位', tags=[],
    code='''
class Solution(object):
    def countDigits(self, num):

        tmp = num
        res = 0
        while tmp:
            v = tmp % 10
            tmp //= 10
            if num % v == 0:
                res += 1
        
        return res
''',
    call='Solution().countDigits(1245)',
    expect=2,
    views=[
        dict(type='string', var=lambda S: str(S['tmp']) if 'tmp' in S and S['tmp'] else '', label='tmp 还剩的数位', cell=110, h=220),
        dict(type='text', fn=lambda S: (f"`num = {S['num']}`，刚分离出 `v = {S['v']}`，`{S['num']} % {S['v']}` = =={S['num'] % S['v']}==" if 'v' in S else ''), size=30, h=120),
    ],
    watch=['num', ('tmp', 'tmp', 'blue'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'tmp = num': '`tmp` 是 `num` 的副本，用来逐位拆；`num` 本身保留不变',
        'res = 0': '`res` 累计满足条件的位数',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}`，还没拆完，继续' if S.tmp else '`tmp = 0`：每一位都分离完了 → 结束'),
        'v = tmp % 10': '摸 10：分离出最低位 `v = {v}`',
        'tmp //= 10': '把已处理的最低位丢掉：`tmp` → {tmp}',
        'if num % v': '`num % v` = `{num} % {v}` = {num % v} → =={"能整除" if num % v == 0 else "不能整除"}==',
        'res += 1': '这一位能整除 `num`：`res` → {res}',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='摸 10 分离每一位，再看 num 能不能整除它',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['统计 `num` 的数位里，能整除 `num` 本身的有几位',
                 '数位里没有 0；重复出现的数位各算一次',
                 '示例：`121` → `2`；本视频：`1245` → `2`'],
        quote='通过摸10不断分离出num的每一位，然后根据num能否整除该位来更新最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`tmp % 10` 取出最低位 `v`，`tmp //= 10` 丢掉它',
              '拿原数 `num` 对 `v` 取余：余 0 就计数',
              '1245：`5`、`1` 整除，`4`、`2` 不整除'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `tmp /= 10` 已改为 `tmp //= 10`',
                 '要用 `num` 而不是 `tmp` 做被除数',
                 '对比灵神：灵神把判断写成 `ans += num % (x % 10) == 0`，这里先存 `v` 再 `if`'],
    ),
)
