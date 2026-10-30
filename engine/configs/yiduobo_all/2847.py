CONFIG = dict(
    num=2847, title='给定数字乘积的最小数字', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='从 9 到 2 倒序分离因子',
    tags=[],
    code='''
class Solution(object):
    def smallestNumber(self, n):

        if n == 1:
            return "1"

        cnt = [0] * 10
        for i in range(9, 1, -1):
            while n % i == 0:
                cnt[i] += 1
                n //= i
        
        if n > 1:
            return "-1"
        
        return "".join([str(i) * cnt[i] for i in range(2, 10)])
''',
    call='Solution().smallestNumber(288)',
    expect='489',
    views=[
        dict(type='text', fn=lambda S: f"剩余 `n` = =={S['n']}==" if 'cnt' in S else ''),
        dict(type='array', var='cnt', pointers={'i': 'blue'}, label='cnt[d] = 数字 d 要用几个（下标 = 数字）', h=300),
    ],
    watch=[('n', 'n', 'yellow'), ('i', 'i', 'blue')],
    captions={
        'cnt = [0]': '`cnt[d]` 记录数字 `d`（2~9）要用几个',
        'for i in range(9, 1, -1)': '`i` = {i}：从 9 往 2 倒序，每次尽量多分出当前因子',
        'while n % i': lambda S, B, r: (f'`{S.n} % {S.i} == 0`：还能再分出一个 {S.i}' if S.n % S.i == 0
                                       else f'`{S.n} % {S.i} != 0`：分不出 {S.i} 了，换更小的'),
        'cnt[i] += 1': '`cnt[{i}]` = {cnt[i]}',
        'n //= i': '`n` 除掉 {i}，剩 =={n}==',
        'if n > 1': lambda S, B, r: (f'`n = {S.n}` 还大于 1：含大于 7 的质因子 → 返回 "-1"' if S.n > 1 else '`n = 1`：全部分干净了，有解'),
        'return "".join': '按 2→9 升序把每个数字重复 `cnt` 次拼起来 → =={ret}==（小数字在高位）',
    },
    cards=dict(
        one_liner='n 只能由 2、3、5、7 组成，先凑大数字，再升序拼接',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给正整数 `n`，求最小的正整数，使其各位数字之积等于 `n`',
                 '答案可能很大，用字符串返回；不存在返回 `"-1"`',
                 '示例：`105` → `"357"`；本视频：`288` → `"489"`'],
        quote='应该尽量组合出较大的数。更具体的，就是应该优先组合9和8，然后是6，最后是4。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字之积是 n，质因子只能有 2、3、5、7；5 和 7 只能单独成位',
              '2 和 3 可以合并成 4、6、8、9，合并越大位数越少、数越小',
              '从 9 到 2 倒序分离，最后升序拼接：小数字放高位'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`n == 1` 单独返回 `"1"`',
                 '分完 `n > 1` 说明有大于 7 的质因子，返回 `"-1"`',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`'],
    ),
)
