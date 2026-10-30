CONFIG = dict(
    num=553, title='最优除法', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数学：加括号',
    tags=[],
    code='''
class Solution(object):
    def optimalDivision(self, nums):

        if len(nums) == 1:
            return str(nums[0])
        
        if len(nums) == 2:
            return str(nums[0]) + '/' + str(nums[1])
        
        return str(nums[0]) + '/(' + '/'.join([str(x) for x in nums[1:]]) + ')'
''',
    call='Solution().optimalDivision([1000, 100, 10, 2])',
    expect='1000/(100/10/2)',
    views=[
        dict(type='array', var='nums', h=170,
             color=lambda S, i, v: 'green' if i == 0 else ('pink' if i == 1 else 'blue')),
        dict(type='text', size=32,
             fn=lambda S: '分子 ==nums[0]==，分母第一项 ==nums[1]== 固定，其余全部想办法放到分子'),
        dict(type='text', size=32,
             fn=lambda S: ('加括号后：`' + str(S['nums'][0]) + '/(' + '/'.join(str(x) for x in S['nums'][1:]) + ')`'
                           ' = ' + str(S['nums'][0]) + ' ÷ (' + str(S['nums'][1]) + ' ÷ ' + ' ÷ '.join(str(x) for x in S['nums'][2:]) + ')') if len(S['nums']) > 2 else ''),
    ],
    watch=[('n', 'len(nums)', 'blue'), ('首项', 'nums[0]', 'green')],
    captions={
        'if len(nums) == 1': '只有一个数时，没有除法可做：`len(nums) = {len(nums)}`，是 1 吗？→ {len(nums) == 1}',
        'if len(nums) == 2': '只有两个数时，只能 `a/b`，括号加不加结果都一样：`len(nums) = {len(nums)}`，是 2 吗？→ {len(nums) == 2}',
        'return str(nums[0]) + \'/(\'': '三个及以上：把 `nums[1:]` 连起来，整体加括号 → 分母 `{nums[1]}/{nums[2]}/...` 被除后，后面的数全进了分子 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='不用搜索：a/(b/c/...) 让 b 以外的数全进分子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个正整数数组 `nums`，相邻两数做除法：`a/b/c/...`',
                 '可以随意加括号改变运算顺序，要让结果 ==最大==',
                 '返回加了括号的表达式字符串，示例 `[1000,100,10,2]` → `"1000/(100/10/2)"`'],
        quote='对于a/b/c/...这个式子而言，第一项a必然是分子的一个乘数，而第二项b必然是分母的一个乘数。',
        quote_src='—— yiduobo 题解',
        idea=['数都是正整数：==a 一定在分子，b 一定在分母==，这两个位置改不了',
              '从 c 开始的数，想办法全放到分子上，结果才最大',
              '所以写成 `a/(b/c/...)`：括号里 b 做被除数，后面再除再取倒数，c… 都跑到分子'],
        after=[dict(heading='为什么不用回溯', lines=['乍一看像「加括号」的搜索回溯，复杂度很高',
                '但数都是正的，结论是固定的：==只有一种最优写法==',
                '数学上想清楚，代码就是几行字符串拼接'])],
        summary=['时间 `O(n)`，空间 `O(n)`：只是字符串拼接',
                 '易错点：只有 1 个数、只有 2 个数要单独判断',
                 '只有 2 个数时不能加括号，答案是 `a/b`，多余括号不被接受',
                 '关键是看出「正整数」这个前提，才能不搜索'],
    ),
)
