CONFIG = dict(
    num=1256, title='加密数字', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='num+1 的二进制去掉最高位',
    tags=[],
    code='''
class Solution(object):
    def encode(self, num):

        num += 1
        digit_list = []
        while num:
            digit_list.append(num % 2)
            num //= 2
        
        digit_list.pop()
        digit_list.reverse()
        
        return ''.join([str(x) for x in digit_list])
''',
    call='Solution().encode(23)',
    expect='1000',
    views=[
        dict(type='text', size=34, h=70, fn=lambda S: f"当前 `num` = =={S['num']}==" if 'num' in S else ''),
        dict(type='array', var='digit_list', label='digit_list（先存低位，后面再反转）', h=200, cell=96),
    ],
    watch=[('num', 'num', 'blue'), ('digit_list', 'digit_list', 'green')],
    captions={
        'num += 1': '规律：编码 = `num + 1` 的二进制去掉最高位 1。先加一：`num` = =={num}==',
        'while num': lambda S, B, r: (f'`num = {S.num}` 不为 0，继续取最低位' if S.num else '`num` 变成 0：所有二进制位都取完了'),
        'digit_list.append': '`num % 2` = {num % 2}：取出最低位，存入 digit_list → {digit_list}',
        'num //= 2': '`num` 除以 2（右移一位）：{B.num} → =={num}==',
        'digit_list.pop': '最后存进去的是==最高位==，它一定是 1，按规律要去掉 → {digit_list}',
        'digit_list.reverse': '低位在前，反转成高位在前：{digit_list}',
        'return': '拼成字符串，返回 `{ret!r}`',
    },
    cards=dict(
        one_liner='编码就是 num+1 的二进制去掉最高位的 1',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['把非负整数 `num` 按规则编码成字符串：0→""，1→"0"，2→"1"，3→"00"，4→"01"，5→"10"，6→"11"，7→"000"',
                 '示例：`23` → `"1000"`'],
        quote='找规律的题目，具体的规律是num + 1的二进制表示然后去掉最高位的1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`23 + 1 = 24 = 11000`（二进制），去掉最高位的 1 得 `1000`',
              '代码里不断模 2、除 2 取出每一位，得到的是低位在前',
              '最后弹出末尾的最高位，再反转成正常顺序'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错：先 `+1` 再取位；`num=0` 时 `num+1=1`，去掉最高位后得到空串',
                 '原文为 Python 2 写法，整数除法 `num /= 2` 已改为 `num //= 2`'],
    ),
)
