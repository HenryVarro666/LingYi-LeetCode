CONFIG = dict(
    num=3028, title='边界上的蚂蚁', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 累计位置',
    code='''
class Solution(object):
    def returnToBoundaryCount(self, nums):

        s = 0
        res = 0
        for v in nums:
            s += v
            if s == 0:
                res += 1
        
        return res
''',
    call='Solution().returnToBoundaryCount([2,3,-5,4,-4,1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=230,
             color=lambda S, i, v: 'pink' if v < 0 else 'blue',
             ),
        dict(type='text', fn=lambda S: (f"蚂蚁位置 `s = {S['s']}`" + ('  ==在边界上，计数 +1==' if S['s'] == 0 and S['_line'] >= 8 else '')) if 's' in S else '', size=34),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        's = 0': '`s` 记录蚂蚁当前位置，从边界 0 出发',
        'res = 0': '`res` 统计回到边界的次数',
        's += v': '蚂蚁走 `{v}`：位置 `{B.s}` → =={s}==',
        'if s == 0': lambda S, B, r: (f'`s = {S.s}` ≠ 0，不在边界上' if S.s != 0 else '`s == 0`：==刚好停在边界上==，要计数'),
        'res += 1': '`res` → {res}',
        'return res': '一共回到边界 `{res}` 次',
    },
    cards=dict(
        one_liner='走完每一步后看位置是不是 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['蚂蚁在数轴原点，按 `nums` 依次左右移动，求返回原点的次数',
                 '中途穿过原点不算，只看每一步走完后的位置',
                 '示例：`[2,3,-5]` → `1`'],
        quote='由于只需要计算刚好停留在边界上的次数，那么只需一趟遍历，计算当前蚂蚁所处的位置并判断是否处于边界上就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['用变量 `s` 模拟蚂蚁的位置，每读一个数就加上去',
              '加完后 `s == 0` 就让 `res` 加一',
              '不用记录路径，一趟遍历即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '检查放在移动之后，穿过边界的中间位置不会被统计',
                 '原文为 Python 2 风格，在 Python 3 下无需修改，逐字使用'],
    ),
)
