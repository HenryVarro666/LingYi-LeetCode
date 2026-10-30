def _color(S, i, v):
    if 'pos' not in S:
        return None
    if 'index' in S and i == S['index'] and S['index'] > S['pos']:
        return 'blue'
    if i <= S['pos']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'index' in S and S['pos'] + 1 < i < S['index']


def _flag_text(S):
    if 'pos' not in S:
        return ''
    nums, pos = S['nums'], S['pos']
    ans = nums[:pos + 1]
    s = f'ans = `nums[0:{pos + 1}]` = `{ans}`'
    if S.get('second_flag'):
        s += f'；`second_flag` ==为真==：末尾已有两个 `{nums[pos]}`'
    return s


def _eq_cap(S, B, ret):
    i, pos, nums = S.index, S.pos, S.nums
    if nums[i] == nums[pos]:
        return f'`nums[{i}] = {nums[i]}` 等于 ans 末尾 `nums[{pos}] = {nums[pos]}` → 要看 ans 里已经有几个'
    return f'`nums[{i}] = {nums[i]}` ≠ ans 末尾 `{nums[pos]}` → 新的数，一定可以加入'


CONFIG = dict(
    num=80, title='删除有序数组中的重复项 II', difficulty='Medium', category='双指针',
    author='yiduobo', technique='写指针 pos + second_flag 标记',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def removeDuplicates(self, nums):
        second_flag = False
        pos = 0
        for index in range(1, len(nums)):
            if nums[index] == nums[pos]:
                if second_flag:
                    continue
                second_flag = True
            else:
                second_flag = False

            pos += 1
            nums[pos] = nums[index]

        return pos + 1
''',
    call='''nums = [1, 1, 1, 2, 2, 3]
k = Solution().removeDuplicates(nums)
(k, nums[:k])''',
    expect=(5, [1, 1, 2, 2, 3]),
    views=[
        dict(type='array', var='nums', label='nums（绿 = 答案数组 ans，蓝 = 当前 index）', cell=110, h=290,
             pointers={'index': 'blue', 'pos': 'pink'}, window=('0', 'pos'), window_color='green',
             color=_color, dim=_dim),
        dict(type='text', fn=_flag_text, size=27, h=100, lines=2),
        dict(type='text', fn=lambda S: '原地覆盖：答案长度 ≤ 原数组长度，`pos` 永远不会超过 `index`', size=24, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'pink'), ('second_flag', 'second_flag', 'orange')],
    captions={
        3: '`second_flag`：ans 末尾是否==已经有两个==相同的数',
        'pos = 0': '`pos` 是 ans 最后一个元素的下标（ans 先放入 `nums[0]`）',
        'for index in range': lambda S, B, ret: (f'看 `nums[{S.index}] = {S.nums[S.index]}`' if S.get('index') != B.get('index')
                                                 else '扫描结束'),
        'if nums[index] == nums[pos]': _eq_cap,
        'if second_flag': lambda S, B, ret: (f'`second_flag` 为真：ans 里已经有两个 `{S.nums[S.pos]}` → 跳过 `nums[{S.index}]`'
                                             if S.second_flag else f'`second_flag` 为假：ans 里只有一个 `{S.nums[S.pos]}`，还能再放一个'),
        'continue': '`continue`：这个数不要了',
        'second_flag = True': '放入后末尾就有两个了 → `second_flag = True`，之后相同的都不能再加',
        11: '遇到新数 → 重置 `second_flag = False`',
        'pos += 1': '`pos` 后移到 {pos}',
        'nums[pos] = nums[index]': '把 `nums[{index}] = {nums[index]}` 覆盖写到 `nums[{pos}]`',
        'return pos + 1': 'ans 的长度 = `pos + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='从左往右扫，和答案末尾比较；用 second_flag 记住末尾是否已有两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有序数组 `nums`，==原地==删除重复项，使每个元素==最多出现两次==',
                 '返回新长度 `k`，`nums` 的前 `k` 个元素就是结果；额外空间 `O(1)`',
                 '示例：`[1,1,1,2,2,3]` → `5`，`nums = [1,1,2,2,3]`'],
        quote='当遇到nums[k] == ans[-1]时，判断ans中是否已经有两个nums[k]了。如果有，那么就跳过nums[k]……我在这里==设置了一个second_flag标记来表示这个状态==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想成往新数组 ans 里放：和 `ans[-1]` 相同时，看是否已经放了两个',
              '答案不会比原数组长 → 直接把 ans ==从头覆盖到 nums 上==',
              '这时要维护 `pos` 表示 ans 的末尾，用 `nums[pos]` 代替 `ans[-1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`second_flag` 在遇到新数时要==重置为 False==',
                 '返回的是长度 `pos + 1`，不是 `pos`',
                 '对比灵神：灵神比较 `nums[stack_size-2]`，不需要额外标记',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
