CONFIG = dict(
    num=1822, title='数组元素积的符号', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 只记符号',
    code='''
class Solution(object):
    def arraySign(self, nums):

        res = 1
        for num in nums:
            if num == 0:
                return 0
            if num < 0:
                res = -res
        
        return res
''',
    call='Solution().arraySign([2,-3,4,-5,-1])',
    expect=-1,
    views=[
        dict(type='text', fn=lambda S: f"当前符号 res = ==({S['res']})==" if 'res' in S else '', size=40, h=70),
        dict(type='array', var='nums', pointers={'下标': 'blue'} if False else {}, h=200,
             color=lambda S, i, v: ('red' if v < 0 else 'green' if v > 0 else 'yellow')),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'res = 1': '先假设乘积为正：`res = 1`，只记符号，不算真正的乘积',
        'for num in nums': lambda S, B, r: (f'依次取出 `num = {S.num}`' if B.get('num') != S.num else '所有元素取完，循环结束'),
        'if num == 0': lambda S, B, r: ('`num == 0`：乘积一定是 0，直接返回 0' if S.num == 0
                                        else f'`{S.num} == 0`？不是，乘积不会被抹成 0'),
        'if num < 0': lambda S, B, r: (f'`{S.num} < 0` → 负数让符号翻转一次' if S.num < 0
                                       else f'`{S.num} < 0`？不是，正数不改变符号'),
        'res = -res': '符号翻转：`res` 从 {B.res} 变成 =={res}==',
        'return res': '负数共出现奇数次 → 符号为 `{res}`',
    },
    cards=dict(
        one_liner='不算乘积，只跟踪符号：遇负翻转，遇零直接 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`signFunc(x)`：正数返回 1，负数返回 -1，0 返回 0',
                 '求数组所有元素乘积 `product` 的 `signFunc(product)`',
                 '示例：`[2,-3,4,-5,-1]` → `-1`'],
        quote='由于题目并不关心最终结果的大小，而只需要知道最终符号，因此可以直接一趟遍历，在过程中计算最终的符号。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积太大会溢出，也没必要算出来', '只要符号：每遇到一个负数，符号取反一次',
              '遇到 `0` 乘积必为 0，立刻返回'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：0 要在遍历中立刻返回，不能等遍历完再看符号',
                 '本质是数负数个数的奇偶性',
                 '原文代码已是 Python 3 可运行写法，仅保留代码主体'],
    ),
)
