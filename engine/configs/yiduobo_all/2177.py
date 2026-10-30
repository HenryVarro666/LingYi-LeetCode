CONFIG = dict(
    num=2177, title='找到和为给定整数的三个连续整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='设中间数为 x', tags=[],
    code='''
class Solution(object):
    def sumOfThree(self, num):

        if num % 3 == 0:
            return [num // 3 - 1, num // 3, num // 3 + 1]
        
        return []
''',
    call='[Solution().sumOfThree(33), Solution().sumOfThree(4)]',
    expect=[[10, 11, 12], []],
    views=[
        dict(type='text', size=34, h=130, fn=lambda S: (
            f"`{S['num']} % 3` = =={S['num'] % 3}==" + ('，是 3 的倍数' if S['num'] % 3 == 0 else '，不是 3 的倍数'))),
        dict(type='array', var=lambda S: [S['num'] // 3 - 1, S['num'] // 3, S['num'] // 3 + 1] if S['num'] % 3 == 0 else [],
             label='三个连续整数（中间那个是 num // 3）', cell=120, h=200, color=lambda S, i, v: 'green' if i == 1 else None),
    ],
    watch=[('num', 'num'), ('num % 3', lambda S: S['num'] % 3, 'orange')],
    captions={
        'if num % 3 == 0': '三个数的和是 `3x`，所以先看 `num % 3`：`{num} % 3 = {num % 3}` → {"==是 3 的倍数==，有解" if num % 3 == 0 else "==不是 3 的倍数==，无解"}',
        'return [num': '中间数 `x = {num} // 3 = {num // 3}`，另外两个是 `x - 1 = {num // 3 - 1}` 和 `x + 1 = {num // 3 + 1}`',
        'return []': '不是 3 的倍数，凑不出 → 返回空数组 `[]`',
    },
    cards=dict(
        one_liner='设中间数为 x，三数之和就是 3x',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['返回三个连续整数，使它们的和为 `num`；不行就返回空数组',
                 '示例：`33` → `[10,11,12]`；`4` → `[]`'],
        quote='设三个连续整数正中间那个为x，那么三个整数的和就是3x。只需判断num是否为3的倍数',
        quote_src='—— yiduobo 题解原文',
        idea=['中间数 `x`，另外两个是 `x-1` 和 `x+1`，和为 `3x`',
              '`num` 是 3 的倍数：`x = num / 3`，直接返回三个数',
              '不是 3 的倍数：返回空数组'],
        summary=['时间、空间都是 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（Python 3 的 `/` 会得到小数）',
                 '作者吐槽这题标成中等偏高，其实只是一步小学数学',
                 '对比灵神：灵神先算 `x = num // 3`，再用 `num % 3` 一行返回'],
    ),
)
