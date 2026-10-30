CONFIG = dict(
    num=3191, title='使二进制数组全部等于 1 的最少操作次数 I', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='一趟遍历，当前为 0 就以它为起点翻',
    tags=['灵神题单', '难度分 1312'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        res = 0

        for index in range(0, len(nums) - 2):
            if nums[index] == 0:
                nums[index + 1] ^= 1
                nums[index + 2] ^= 1
                res += 1
        
        if nums[-1] == 0 or nums[-2] == 0:
            return -1
        return res
''',
    call='Solution().minOperations([0,1,1,1,0,0])',
    expect=3,
    skip=['res = 0'],
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 以 index 为起点的 3 个数）', cell=96, h=330,
             pointers={'index': 'blue'},
             window=('index', 'index + 2'),
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] and v == 1 else None),
        dict(type='text', fn=lambda S: ('以 `index` 为起点的操作只能改 `nums[index]`、`nums[index+1]`、`nums[index+2]`' if 'index' in S else ''), size=28),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'for index in range': '依次把每个下标当作操作起点，到倒数第 3 个为止',
        'if nums[index] == 0': lambda S, B, r: (f'`nums[{B.index}] = 0` 需要修改：只剩以 `{B.index}` 为起点的操作能改它 → 执行'
                                                if B.nums[B.index] == 0 else f'`nums[{B.index}] = 1` 不用改，也不会回头操作'),
        'nums[index + 1] ^= 1': '操作 `index` 反转三个数；`nums[index]` 本该变 1，但之后不再访问，代码省略。反转后一位：`nums[{index+1}]` → `{nums[index+1]}`',
        'nums[index + 2] ^= 1': '反转再后一位：`nums[{index+2}]` → `{nums[index+2]}`',
        'res += 1': '这个起点只操作一次（偶数次等于没做）：`res = {res}`',
        'if nums[-1] == 0': lambda S, B, r: (f'最后两个数 `{B.nums[-2]}, {B.nums[-1]}` 只能被动修改，不全是 1 → 无解' if (B.nums[-1] == 0 or B.nums[-2] == 0)
                                             else f'最后两个数 `{B.nums[-2]}, {B.nums[-1]}` 都是 1 → 成立'),
        'return -1': '返回 `-1`',
        'return res': '全部为 1，返回最少操作次数 `{res}`',
    },
    cards=dict(
        one_liner='一趟遍历：当前位置是 0，就以它为起点翻转',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `nums`，每次可选==连续三个==元素全部反转',
                 '问最少几次能让数组全为 1，做不到返回 `-1`',
                 '示例：`[0,1,1,1,0,0]` → `3`'],
        quote='对于下标0而言，只有在选择以0为起点的操作时才能修改其数值，在处理完下标0之后，……想要修改下标1的值就不应该回过头去再以0为起点执行操作，而是只能执行以1为起点的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一起点要么不做、要么做一次，做偶数次等于没做',
              '下标 0 只能靠以 0 为起点的操作修改，下标 1 之后同理',
              '所以一趟遍历：当前为 0 就操作，最后两个数被动修改，要检查'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环到 `len-3` 为止；最后两个数不全是 1 就返回 `-1`',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
