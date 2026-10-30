CONFIG = dict(
    num=3270, title='求出数字答案', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从高到低逐位分离',
    code='''
class Solution(object):
    def generateKey(self, num1, num2, num3):

        res = 0
        for d in [1000, 100, 10, 1]:
            res += d * min(num1 // d, num2 // d, num3 // d)
            num1 %= d
            num2 %= d
            num3 %= d
        
        return res
''',
    call='Solution().generateKey(987, 879, 798)',
    expect=777,
    views=[
        dict(type='text', h=70, fn=lambda S: (f"当前位权 `d = {S['d']}`：三数该位 `{S['num1']//S['d']}, {S['num2']//S['d']}, {S['num3']//S['d']}`" if 'd' in S and S['d'] else '')),
        dict(type='array', var=lambda S: [S['num1'], S['num2'], S['num3']], pointers={}, h=200, label='num1, num2, num3（取模去掉已处理的高位）'),
        dict(type='array', var=lambda S: [1000, 100, 10, 1], pointers={}, h=200, label='位权 d 依次为 1000, 100, 10, 1',
             color=lambda S, i, v: 'yellow' if S.get('d') == v else None),
    ],
    watch=[('d', 'd', 'yellow'), ('num1', 'num1', 'blue'), ('num2', 'num2', 'pink'), ('num3', 'num3', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累加答案',
        'for d in': '按 `1000, 100, 10, 1` 的顺序处理：这次 `d = {d}`',
        'res += d *': '`num // d` 分离出这一位：`min({num1 // d}, {num2 // d}, {num3 // d})` = {min(num1 // d, num2 // d, num3 // d)}，乘 `{d}` 累加 → `res` = =={res}==',
        'num1 %= d': '`num1 %= {d}` 去掉已处理的高位：`num1` → {num1}',
        'num2 %= d': '`num2 %= {d}`：`num2` → {num2}',
        'num3 %= d': '`num3 %= {d}`：`num3` → {num3}',
        'return res': '拼出的数字答案 `{res}`',
    },
    cards=dict(
        one_liner='固定四位，从高到低先除后取模，逐位取最小',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['三个正整数，视为补了前导 0 的四位数',
                 'key 每一位是三数对应位的最小值',
                 '示例：`987, 879, 798` → `777`'],
        quote='可以按1000、100、10、1的顺序遍历，对于当前遍历到的数值d，通过先除以d后对d取模的操作可以分离出nums1、nums2、nums3对应的数位以及剩余的数',
        quote_src='—— yiduobo 题解原文',
        idea=['数最多四位，位权固定 `1000, 100, 10, 1`，不用管前导 0',
              '`num // d` 得到最高位，`num %= d` 留下低位给下一轮',
              '最小位乘位权累加，就是答案'],
        summary=['时间、空间都是常数（固定四位）',
                 '补 0 是隐式的：短的数 `// 1000` 自然得 0',
                 '先除再取模，顺序反了会丢位'],
    ),
)
