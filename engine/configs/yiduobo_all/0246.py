CONFIG = dict(
    num=246, title='中心对称数', difficulty='Easy', category='双指针',
    author='yiduobo', technique='左右双指针 · 对称配对',
    tags=[],
    code='''
class Solution(object):
    def isStrobogrammatic(self, num):

        left = 0
        right = len(num) - 1
        single_set = set(['0', '1', '8'])
        pair_set = set(['6', '9'])
        while left <= right:
            if num[left] in single_set:
                if num[right] != num[left]:
                    return False
            elif num[left] in pair_set:
                if num[right] not in pair_set or num[left] == num[right]:
                    return False
            else:
                return False
            
            left += 1
            right -= 1
        
        return True
''',
    call="Solution().isStrobogrammatic('61819')",
    expect=True,
    views=[
        dict(type='string', var='num', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=240, cell=110,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', h=80, fn=lambda S: '自对称：`0 1 8`　　互为一对：`6 ↔ 9`　　`2 5 3 4 7` 都不行'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('num[left]', "num[left] if left < len(num) else ''", 'blue'),
           ('num[right]', "num[right] if right >= 0 else ''", 'pink')],
    captions={
        'left = 0': '`left` 从最左边开始',
        'right = len': '`right = len(num) - 1 = {right}`，从最右边开始',
        'single_set = set': '第一类：旋转后==还是自己==的数字 `0 1 8`',
        'pair_set = set': '第二类：`6` 和 `9` 旋转后互相变成对方',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`，继续配对' if S.left <= S.right
                                                else f'`left = {S.left} > right = {S.right}`：两边都配好了 → 结束'),
        'if num[left] in single_set': lambda S, B, r: (f'左边 `{S.num[S.left]}` 属于 0/1/8，对面必须是它自己' if S.num[S.left] in S.single_set
                                                       else f'左边 `{S.num[S.left]}` 不是 0/1/8'),
        'if num[right] != num[left]': '右边 `{num[right]}` 要等于左边 `{num[left]}`：' + '==不等就失败==',
        'elif num[left] in pair_set': lambda S, B, r: (f'左边 `{S.num[S.left]}` 是 6/9，对面必须是另一个' if S.num[S.left] in S.pair_set
                                                       else f'左边 `{S.num[S.left]}` 不是 6/9'),
        'if num[right] not in pair_set': '右边 `{num[right]}` 必须是 6/9，且和左边 `{num[left]}` ==不能相同==（6 对 6 翻转后变 9 对 6）',
        'else:': '左边是 2/3/4/5/7，旋转后不是数字',
        'left += 1': '这一对配好了，`left` 右移到 {left}',
        'right -= 1': '`right` 左移到 {right}',
        'return False': '这一对不能配成中心对称 → 直接返回 `False`',
        'return True': '所有对都配好了 → `True`',
    },
    cards=dict(
        one_liner='两头向中间配对：0/1/8 配自己，6 配 9',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['中心对称数：旋转 180 度后，看起来和原来==一样==的数',
                 '给字符串 `num`，判断它是不是中心对称数',
                 '示例：`"69"` → `true`；`"962"` → `false`；本视频：`"61819"` → `true`'],
        quote='第一类是自身与自身对称，一共有0、1、8这三种；第二类则是与另一个数对称，只有6和9这一对。需要注意2和5并不是中心对称数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字分两类：自对称（`0 1 8`）和成对（`6 9`）',
              '`left`、`right` 从两端向中间，逐对检查',
              '任何一对不符合就返回 `False`，走完才返回 `True`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while left <= right`：奇数长度时中间那位自己配自己，必须是 0/1/8',
                 '6 与 6、9 与 9 配对要判错：`num[left] == num[right]`',
                 '2 和 5 看起来像，但不是中心对称数',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串'],
    ),
)
