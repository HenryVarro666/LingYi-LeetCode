CONFIG = dict(
    num=2264, title='字符串中最大的 3 位相同数字', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='下标 2 起向前看两位',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1309'],
    code='''
class Solution(object):
    def largestGoodInteger(self, num):

        res = -1
        for index in range(2, len(num)):
            if num[index] == num[index - 1] == num[index - 2]:
                res = max(res, int(num[index]))
        
        if res == -1:
            return ''
        
        return str(res) * 3
''',
    call='Solution().largestGoodInteger("6777133339")',
    expect='777',
    views=[
        dict(type='string', var='num', pointers={'index': 'blue'}, h=260,
             color=lambda S, i, v: 'green' if 'index' in S and S['index'] - 2 <= i <= S['index'] and S['num'][S['index']] == S['num'][S['index'] - 1] == S['num'][S['index'] - 2] else None),
        dict(type='text', h=120, fn=lambda S: f"目前最大的优质数字 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'res = -1': '`res` 记录最大的优质数字，-1 表示还没找到（数字都 ≥ 0）',
        'for index': lambda S, B, r: ('从下标 2 开始，这样可以回头看前两个字符：`index = 2`' if 'index' not in B else f'`index = {S.index}`：窗口右端右移一格') if 'index' in S else '遍历结束',
        'if num[index] == num[index - 1]': lambda S, B, r: (f"`{S.num[S.index]}` = `{S.num[S.index-1]}` = `{S.num[S.index-2]}` → 三个相同，能形成优质整数" if S.num[S.index] == S.num[S.index-1] == S.num[S.index-2] else f"`{S.num[S.index-2]}{S.num[S.index-1]}{S.num[S.index]}` 三个字符不全相同"),
        'res = max': '用这个数字更新答案：`res = max({B.res}, {int(num[index])})` = =={res}==',
        'if res == -1': lambda S, B, r: '`res != -1`，找到了优质整数' if S.res != -1 else '`res == -1`，一个也没找到 → 返回空串',
        'return str(res) * 3': '把数字 `{res}` 重复 3 次：=={ret!r}==',
    },
    cards=dict(
        one_liner='从下标 2 往后看，当前字符与前两个都相同就更新答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `num` 表示大整数，找由同一数字重复 3 次的长为 3 子串',
                 '返回最大的，没有则返回空串',
                 '示例：`"6777133339"` → `"777"`'],
        quote='从字符串中下标2开始向后遍历，若当前字符与上一个及上上个字符相同，那么说明这三个字符能形成一个优质整数，使用这个值来更新答案就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举每个长为 3 的窗口的右端 `index`，检查是否三字符全相同',
              '用整数 `res` 保存最大数字，初值 -1 表示没有',
              '最后把数字转成字符串重复 3 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 用 -1 作哨兵，因为 `0` 也是合法的优质数字（`"000"`）',
                 '最后要 `str(res) * 3`，不要只返回单个数字',
                 '原文为 Python 2 风格，本题代码无需改动，仅是类声明写法 `Solution(object)`'],
    ),
)
