NUMS = ['12', '3', '1']
TARGET = '123'


def _nc(S, i, v):
    if 'left' in S and i == S['left']:
        return 'blue'
    if 'right' in S and i == S['right']:
        return 'pink'
    if 'num' in S and 'left_flag' in S and 'res' not in S and i == len(S['left_flag']) - 1 and S.get('_line') not in (7,):
        return 'yellow'
    return None


def _txt(S):
    if 'res' in S and 'left' in S and 'right' in S and S['left'] != S['right']:
        l, r = S['left'], S['right']
        ok = S['num_l'][l] + S['num_l'][r] == len(S['target']) and S['left_flag'][l] and S['right_flag'][r]
        return (f"`nums[{l}] + nums[{r}]`：长度 {S['num_l'][l]} + {S['num_l'][r]} = {S['num_l'][l] + S['num_l'][r]}，"
                f"前缀匹配 {S['left_flag'][l]}，后缀匹配 {S['right_flag'][r]} → " + ('==是一对==' if ok else '不是'))
    return '`left_flag[i]`：nums[i] 是 target 的前缀；`right_flag[i]`：nums[i] 是 target 的后缀'


CONFIG = dict(
    num=2023, title='连接后等于目标字符串的字符串对', difficulty='Medium', category='字符串',
    author='yiduobo', technique='前后缀标记数组 + 枚举字符串对',
    tags=[],
    code='''
class Solution(object):
    def numOfPairs(self, nums, target):

        n = len(nums)
        left_flag = []
        right_flag = []
        num_l = []
        target_l = len(target)

        for num in nums:
            num_l.append(len(num))
            if num_l[-1] >= target_l:
                left_flag.append(False)
                right_flag.append(False)
                continue
            
            flag = True
            for index in range(num_l[-1]):
                if num[index] != target[index]:
                    flag = False
                    break
            left_flag.append(flag)

            flag = True
            for index in range(num_l[-1]):
                if num[-index - 1] != target[-index - 1]:
                    flag = False
                    break
            right_flag.append(flag)
        
        res = 0
        for left in range(n):
            for right in range(n):
                if left == right:
                    continue
                if num_l[left] + num_l[right] == target_l and left_flag[left] and right_flag[right]:
                    res += 1
        
        return res
''',
    call=f'Solution().numOfPairs({NUMS}, {TARGET!r})',
    expect=1,
    max_steps=110,
    skip=['flag = False', 'n = len(nums)', 'left_flag = []', 'right_flag = []', 'num_l = []', 'target_l = len(target)',
          'num_l.append', 'flag = True', 'continue', 'break', 'for index in range', 'res = 0'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = left，粉 = right）', cell=100, h=190, font=26,
             color=lambda S, i, v: ('blue' if 'res' in S and i == S.get('left') else 'pink' if 'res' in S and i == S.get('right') else
                                    'yellow' if 'res' not in S and 'num' in S and v == S['num'] and i == len(S.get('num_l', [])) - 1 else None)),
        dict(type='array', var='left_flag', label='left_flag（是 target 的前缀？）', cell=100, h=150, font=22,
             color=lambda S, i, v: 'green' if v is True else None),
        dict(type='array', var='right_flag', label='right_flag（是 target 的后缀？）', cell=100, h=150, font=22,
             color=lambda S, i, v: 'green' if v is True else None),
        dict(type='text', fn=_txt, size=22, h=60),
    ],
    watch=[('target', 'target'), ('num_l', 'num_l'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'for num in nums': lambda S, B, r: ('每个字符串的前后缀标记都算好了' if len(S.left_flag) == len(S.nums) and len(S.right_flag) == len(S.nums) and len(S.num_l) == len(S.nums)
                                            else f"处理 `nums` 里的下一个字符串（已处理 {len(S.num_l)} 个）"),
        'if num_l[-1] >= target_l': lambda S, B, r: (f'`{S.num_l[-1]} >= {S.target_l}`：它已经和 target 一样长（或更长），拼不出 target → 前后缀都记 False'
                                                    if S.num_l[-1] >= S.target_l else f'`{S.num_l[-1]} < {S.target_l}`：比 target 短，可以当前缀或后缀'),
        'if num[index] != target[index]': lambda S, B, r: (f"`num[{S.index}] = '{S.num[S.index]}'` ≠ `target[{S.index}] = '{S.target[S.index]}'` → 不是前缀，`flag = False`"
                                                          if S.num[S.index] != S.target[S.index] else f"`num[{S.index}] = '{S.num[S.index]}'` = `target[{S.index}]` → 继续比下一位"),
        'left_flag.append(flag)': '`{num}` 是 target 的前缀吗？`{flag}` → left_flag = {left_flag}',
        'if num[-index - 1] != target[-index - 1]': lambda S, B, r: (f"从末尾比：`num[-{S.index + 1}] = '{S.num[-S.index - 1]}'` ≠ `target[-{S.index + 1}] = '{S.target[-S.index - 1]}'` → 不是后缀，`flag = False`"
                                                                    if S.num[-S.index - 1] != S.target[-S.index - 1] else f"从末尾比：`num[-{S.index + 1}] = '{S.num[-S.index - 1]}'` = `target[-{S.index + 1}]` → 继续往前比"),
        'right_flag.append(flag)': '`{num}` 是 target 的后缀吗？`{flag}` → right_flag = {right_flag}',
        'for left in range(n)': lambda S, B, r: ('所有字符串对都枚举完了' if 'left' in B and S.left == B.left and S.left == S.n - 1 and 'right' in B and B.right == S.n - 1
                                                 else f'枚举前半部分：`nums[{S.left}] = {S.nums[S.left]!r}`'),
        'for right in range(n)': lambda S, B, r: ('这个 left 配完了' if 'right' in B and B.right == S.n - 1 and S.right == B.right and 'left' in B and B.left == S.left
                                                  else f'枚举后半部分：`nums[{S.right}] = {S.nums[S.right]!r}`'),
        'if left == right': lambda S, B, r: ('同一个下标，不能自己配自己' if S.left == S.right else '下标不同，可以配对'),
        'if num_l[left] + num_l[right] == target_l': lambda S, B, r: (
            f"长度 `{S.num_l[S.left]} + {S.num_l[S.right]} = {S.num_l[S.left] + S.num_l[S.right]}`（target 长 {S.target_l}），前缀 `{S.left_flag[S.left]}`，后缀 `{S.right_flag[S.right]}` → "
            + ('==是一对==' if S.num_l[S.left] + S.num_l[S.right] == S.target_l and S.left_flag[S.left] and S.right_flag[S.right] else '不满足')),
        'res += 1': '找到一对 `({left}, {right})`：`{nums[left]} + {nums[right]} = {target}`，`res` = =={res}==',
        'return res': '一共 =={res}== 对',
    },
    cards=dict(
        one_liner='先标记谁是 target 的前缀、谁是后缀，再配对',
        complexity='时间 `O(nL + n^2)`，空间 `O(n)`（n 个串，target 长 L）',
        problem=['给你数字字符串数组 `nums` 和 `target`，数满足 `nums[i] + nums[j] == target`（`i ≠ j`）的下标对',
                 '`(i, j)` 与 `(j, i)` 是不同的对',
                 '示例：`["12","3","1"]`，`"123"` → `1`（`"12"+"3"`）；`["1","1","1"]`，`"11"` → `6`'],
        quote='拼接后字符串是否等于target的判断，可以分成两部分来看，即前半部分的字符串能与target的前缀匹配，以及后半部分的字符串能与target的后缀匹配。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍 `nums`：每个串是否是 target 的前缀（`left_flag`）、后缀（`right_flag`），顺便记下长度',
              '再枚举字符串对：长度之和 == target 长，且前者是前缀、后者是后缀',
              '作者说自己偷懒用了朴素的 `O(n^2)` 配对；也可以统计次数 + 双指针优化'],
        summary=['时间 `O(nL + n^2)`，空间 `O(n)`',
                 '长度 `>= target_l` 的串不可能参与拼接，直接标 False',
                 '`left == right` 要跳过：同一个下标不能用两次',
                 '对比灵神：灵神反过来枚举 target 的切点，用哈希表计数，不用枚举字符串对'],
    ),
)
