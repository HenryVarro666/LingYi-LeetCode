CONFIG = dict(
    num=1470, title='重新排列数组', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='一趟遍历 · 依次追加 x_i 和 y_i',
    tags=['List.md', '字节30天'],
    code='''
class Solution(object):
    def shuffle(self, nums, n):
        res = []
        for index in range(n):
            res.append(nums[index])
            res.append(nums[index + n])

        return res
''',
    call='Solution().shuffle([2, 5, 1, 3, 4, 7], 3)',
    expect=[2, 3, 5, 4, 1, 7],
    views=[
        dict(type='text', fn=lambda S: ('前半是 `x1..xn`，后半是 `y1..yn`：第 `index` 轮取 ==nums[index]== 和 ==nums[index + n]=='
                                        if 'index' not in S else
                                        f"`index = {S['index']}`：`x{S['index'] + 1} = nums[{S['index']}]`，"
                                        f"`y{S['index'] + 1} = nums[{S['index'] + S['n']}]`"), size=26),
        dict(type='array', var='nums', label='nums（蓝 = 前半 x，粉 = 后半 y）', cell=96, h=230,
             pointers={'index': 'blue', 'index + n': 'pink'},
             pointer_labels={'index + n': 'index+n'},
             color=lambda S, i, v: ('blue' if i == S.get('index') else 'pink' if 'index' in S and i == S['index'] + S['n'] else None),
             dim=lambda S, i, v: 'index' in S and i not in (S['index'], S['index'] + S['n']) and (i < S['index'] or S['n'] <= i < S['index'] + S['n'])),
        dict(type='array', var='res', label='res（答案，依次追加；蓝 = x，粉 = y）', cell=96, h=180, min_slots=6,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
    ],
    watch=[('index', 'index', 'blue'), 'n'],
    captions={
        'res = []': '`res` 存放答案，从空开始依次追加',
        'for index in range(n)': lambda S, B, ret: (f'`index = {S.index}`：处理第 {S.index + 1} 对 `(x, y)`'
                                                   if S.get('index') is not None and S.index != B.get('index')
                                                   else f'`index` 已经遍历完 `0..{S.n - 1}`'),
        'res.append(nums[index])': '先追加 `x{index + 1} = nums[{index}] = {nums[index]}` → `res = {res}`',
        'res.append(nums[index + n])': '再追加 `y{index + 1} = nums[{index} + {n}] = {nums[index + n]}` → `res = {res}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='第 index 轮把 nums[index] 和 nums[index + n] 加到答案末尾',
        complexity='时间 `O(n)`，空间 `O(n)`（答案数组）',
        problem=['数组 `nums` 有 `2n` 个元素：`[x1,x2,...,xn,y1,y2,...,yn]`',
                 '把它重新排列成 `[x1,y1,x2,y2,...,xn,yn]` 并返回',
                 '示例：`nums = [2,5,1,3,4,7]`，`n = 3` → `[2,3,5,4,1,7]`'],
        quote='比较基础的题目。从0到n - 1进行遍历，对于当前位置index，==将nums[index]以及nums[index + n]加入到答案的末尾==即可。',
        quote_src='—— yiduobo 题解',
        idea=['`x_i` 在下标 `i-1`，`y_i` 在下标 `i-1+n`：两者相差 `n`',
              '按 `index = 0..n-1` 遍历，每轮先放 x 再放 y',
              '追加的顺序就是答案的顺序，不用算目标下标'],
        result='运行结束：返回 `[2,3,5,4,1,7]` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（返回的新数组）',
                 '下标对应：`x` 是 `nums[index]`，`y` 是 `nums[index + n]`，别写成 `index + 1`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改',
                 '对比灵神：灵神还给了 `O(1)` 额外空间的原地写法（沿置换环交换 + 负数标记）'],
    ),
)
