CONFIG = dict(
    num=2729, title='判断一个数是否迷人', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='数位放进集合检查', tags=[],
    code='''
class Solution(object):
    def isFascinating(self, n):

        if n * 3 >= 1000:
            return False

        num_set = set()
        for char in str(n):
            num_set.add(char)
        for char in str(n + n):
            num_set.add(char)
        for char in str(n + n + n):
            num_set.add(char)
        
        return len(num_set) == 9 and '0' not in num_set
''',
    call='Solution().isFascinating(192)',
    expect=True,
    views=[
        dict(type='set', var='num_set', h=260, fmt=lambda x: str(x)),
        dict(type='text', h=110, fn=lambda S: (f"集合里已有 =={len(S['num_set'])}== 个不同数位" + ('，含 `0`' if '0' in S['num_set'] else '') if 'num_set' in S else f"`3n = {S['n'] * 3}`")),
    ],
    watch=[('n', 'n', 'blue'), ('char', 'char', 'yellow')],
    captions={
        'if n * 3': '`3n = {n * 3}`，`>= 1000` 吗？{"是，拼起来会超过 9 位，返回 False" if n * 3 >= 1000 else "否，三个数都是三位，共 9 位"}',
        'num_set = set()': '准备一个集合，装所有出现过的数位',
        'num_set.add': '`{char}` 放进集合，现在有 {len(num_set)} 个不同数位',
        'return len': '集合大小 `{len(num_set)}` 是 9 吗？{len(num_set) == 9}；含 `0` 吗？{"含" if "0" in num_set else "不含"} → =={ret}==',
    },
    cards=dict(
        one_liner='把 n、2n、3n 的每个数位丢进集合，看是不是 1~9',
        complexity='时间 `O(1)`（位数固定），空间 `O(1)`',
        problem=['三位数 `n`，把 `n`、`2n`、`3n` 首尾相接',
                 '恰好含 1 到 9 各一次、且没有 0，就是迷人的',
                 '示例：`192` → `192384576` → `true`'],
        quote='按照题目要求计算出2n和3n，首先要保证3n不超过1000，接下来将这三个数的数位分离出来，最后检测这些数位是否包含1到9各一次。',
        quote_src='—— yiduobo 题解',
        idea=['先判断 `3n >= 1000` 就不行，否则三个数共 9 位',
              '逐个拆出 `n`、`n+n`、`n+n+n` 的数位放进集合',
              '集合恰好 9 个元素且没有 `0`，说明 1~9 各出现一次'],
        summary=['时间、空间都是常数',
                 '==9 位里只有 9 种不同字符，必然每种恰好一次==',
                 '易错：集合大小为 9 但含 `0` 的情况要排除',
                 '`n + n` 即 `2n`，作者用加法代替乘法'],
    ),
)
