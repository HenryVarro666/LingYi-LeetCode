CONFIG = dict(
    num=3514, title='不同 XOR 三元组的数目 II', difficulty='Medium', category='位运算',
    author='yiduobo', technique='三个集合 one/two/three 逐步累积',
    tags=['灵神题单·位运算', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def uniqueXorTriplets(self, nums):
        
        one = set()
        two = set()
        three = set()
        for v in list(set(nums)):
            one.add(v)
            
            for pre in one:
                two.add(pre ^ v)
            
            for pre in two:
                three.add(pre ^ v)
        
        return len(three)
''',
    call='Solution().uniqueXorTriplets([6,7,8,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={}, label='nums', h=120),
        dict(type='set', var='one', fmt=lambda x: str(x), label='one：取 1 个元素的异或结果', h=150),
        dict(type='set', var='two', fmt=lambda x: str(x), label='two：取 2 个元素的异或结果', h=150),
        dict(type='set', var='three', fmt=lambda x: str(x), label='three：取 3 个元素的异或结果', h=150),
    ],
    watch=[('v', 'v', 'blue'), ('pre', 'pre', 'pink'), ('|three|', 'len(three)', 'green')],
    captions={
        'for v in list(set(nums))': '取下一个新元素 `v = {v}`：它只能作为当前前缀里的元素参与异或',
        'one.add(v)': '`v` 单独一个元素，加入 `one` → `{sorted(one)}`',
        'two.add(pre ^ v)': '`one` 里的 `pre = {pre}` 再和 `v` 异或：`{pre} ^ {v} = {pre ^ v}`，加入 `two`',
        'three.add(pre ^ v)': '`two` 里的 `pre = {pre}` 再和 `v` 异或：`{pre} ^ {v} = {pre ^ v}`，加入 `three`',
        'return len(three)': '`three` 里是所有取 3 个元素的异或结果，个数 ==`{ret}`==',
    },
    max_steps=90,
    cards=dict(
        one_liner='三个集合记录取 1、2、3 个元素的所有异或结果',
        complexity='时间 `O(n·U)`，空间 `O(U)`',
        problem=['整数数组 `nums`，`i<=j<=k` 的三元组，值为三数异或',
                 '求不同异或值的个数',
                 '示例：`[6,7,8,9]` → `4`'],
        quote='使用三个集合one、two、three记录从当前前缀中取出1、2、3个元素异或后可以得到的所有结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历到 `v`：先放进 `one`，再用 `one` 里的数异或 `v` 填 `two`',
              '再用 `two` 里的数异或 `v` 填 `three`，顺序保证 `v` 可重复选',
              '异或结果都在 0~2047 之间，遍历集合不会超时'],
        summary=['时间 `O(n·U)`，`U` 约 2048；空间 `O(U)`',
                 '顺序不能反：先 `one` 再 `two` 再 `three`，这样同一个 `v` 可选多次',
                 '前提是元素值 ≤ 1500，异或结果才不超过 2047',
                 '先 `set(nums)` 去重省循环；原文无需改动即可在 Python 3 运行',
                 '对比灵神：灵神先算两数异或集合再异或 nums；这里边遍历边累积'],
    ),
)
