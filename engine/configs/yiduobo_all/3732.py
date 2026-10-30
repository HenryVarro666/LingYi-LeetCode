CONFIG = dict(
    num=3732, title='一次替换后的三元素最大乘积', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='绝对值最大的两个数 × 10^5',
    tags=['贪心与思维', '乘积贪心', '难度分 1529'],
    code='''
class Solution(object):
    def maxProduct(self, nums):
        
        first, second = None, None
        for v in nums:
            v = abs(v)
            if first is None or v > first:
                first, second = v, first
            elif second is None or v > second:
                second = v
        
        return first * second * 100000
''',
    call='Solution().maxProduct([6, -2, 8, -9, 1, 4])',
    expect=7200000,
    views=[
        dict(type='text', fn=lambda S: (f"first = =={S['first']}==，second = =={S['second']}==（都是绝对值）；`first × second × 10^5` = =={S['first']*S['second']*100000 if S['second'] is not None else '待定'}==" if 'first' in S and S['first'] is not None else '先找出绝对值最大的两个元素'), h=90),
        dict(type='array', var='nums', h=260, label='nums（绿 = 绝对值最大，青 = 第二大）',
             color=lambda S, i, v: ('green' if S.get('first') is not None and abs(v) == S['first'] else
                                    'cyan' if S.get('second') is not None and abs(v) == S['second'] else None)),
    ],
    watch=[('v', 'v', 'yellow'), ('first', 'first', 'green'), ('second', 'second', 'cyan')],
    captions={
        'first, second = None': '两个位置先空着（`None`）',
        'for v in nums': '取下一个元素',
        'v = abs(v)': '取绝对值 `v = {v}`：符号交给被替换的那个数处理',
        'if first is None': lambda S, B, r: (f'`first` 还是空 → v 是新的最大' if B.first is None else f'`{S.v} > first = {B.first}` → ' + ('成立，v 是新的最大' if S.v > B.first else '不成立')),
        'elif second is None': lambda S, B, r: (f'`second` 还是空 → v 是新的第二大' if B.second is None else f'`{S.v} > second = {B.second}` → ' + ('成立，v 是新的第二大' if S.v > B.second else '不成立，丢弃')),
        'first, second = v': '`first, second` = `{first}, {second}`：新最大，旧最大降为第二',
        'second = v': '`second = {second}`',
        'return': lambda S, B, ret: f'`{S.first} × {S.second} × 100000` = =={ret}==',
    },
    cards=dict(
        one_liner='答案 = 绝对值最大的两个数 × 10^5',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 里恰好一个元素换成 `[-10^5, 10^5]` 内的整数',
                 '再选三个下标不同的元素，求最大乘积',
                 '本视频：`[6,-2,8,-9,1,4]` → `7200000`'],
        quote='若选出的这两个元素之积小于0，就替换另一个元素为-10^5，否则替换另一个元素为10^5。更进一步的，对于nums中选出的两个元素，应该让它们乘积的绝对值最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素绝对值都不超过 `10^5`，被替换的数取 `±10^5` 最划算',
              '积为负就换成 `-10^5`，积为正就换成 `10^5`，总能得到正数',
              '所以一趟遍历找绝对值最大的两个：`first`、`second`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`first, second = v, first` 先整体求值，旧的 first 才能传给 second',
                 '`None` 要先判断，再比较大小',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
