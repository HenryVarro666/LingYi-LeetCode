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
    call='Solution().numOfPairs(["1", "12", "2"], "12")',
    expect=1,
    views=[
        dict(type='string', var='target', label='target', cell=84, h=140),
        dict(type='array', var='nums', label='nums', cell=100, h=190,
             pointers={'left': 'blue', 'right': 'pink'},
             color=lambda S, i, v: ('blue' if i == S.get('left') else 'pink' if i == S.get('right') else None)
                                   if S.get('_line', 0) >= 28 else ('yellow' if 'num' in S and v == S['num'] and i == len(S.get('num_l', [])) - 1 else None)),
        dict(type='array', var='left_flag', label='left_flag(前缀)', cell=100, h=130,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='right_flag', label='right_flag(后缀)', cell=100, h=130,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='num_l', label='num_l(长度)', cell=100, h=130),
    ],
    watch=[('target_l', 'target_l', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'target_l = len': '`target_l = {target_l}`：两段长度之和必须恰好等于它',
        'for num in nums': '检查第 `{len(num_l)}` 个串 `num = {num!r}`（先看能不能当前缀、当后缀）',
        'num_l.append': '记下长度：`num_l` = `{num_l}`',
        'if num_l[-1] >= target_l': lambda S, B, r: (f'长度 `{S.num_l[-1]}` ≥ `{S.target_l}`：自己就够长了，拼另一段只会更长 → 不可能' if S.num_l[-1] >= S.target_l else f'长度 `{S.num_l[-1]}` < `{S.target_l}`：还有可能，继续检查前后缀'),
        'left_flag.append(False)': '前缀、后缀标记都记 `False`',
        'right_flag.append(False)': '前缀、后缀标记都记 `False`',
        'for index in range': '逐个字符比较：`num` 共 `{num_l[-1]}` 个字符',
        'flag = True': '先假设整串都匹配，逐个字符验证',
        'if num[index] != target[index]': lambda S, B, r: f"前缀比较：`num[{S.index}] = {S.num[S.index]!r}` 对 `target[{S.index}] = {S.target[S.index]!r}` → " + ('不等，不能当前缀' if S.num[S.index] != S.target[S.index] else '相等'),
        'if num[-index - 1] != target[-index - 1]': lambda S, B, r: f"后缀比较（从末尾往前）：`num[-{S.index + 1}] = {S.num[-S.index - 1]!r}` 对 `target[-{S.index + 1}] = {S.target[-S.index - 1]!r}` → " + ('不等，不能当后缀' if S.num[-S.index - 1] != S.target[-S.index - 1] else '相等'),
        'flag = False': '有字符对不上 → `flag = False`',
        'left_flag.append(flag)': '`{num!r}` 能当 target 的前缀吗：=={flag}==',
        'right_flag.append(flag)': '`{num!r}` 能当 target 的后缀吗：=={flag}==',
        'res = 0': '标记都算好了，接下来枚举有序对 `(left, right)`，`res` 计数',
        'for left in range(n)': lambda S, B, r: ('`left` 都枚举完了' if 'left' in B and B['left'] == S.left and S.left == S.n - 1 and False else f'枚举前半部分 `left = {S.left}`（`{S.nums[S.left]!r}`）') if not ('left' in B and B['left'] == S.left) else f'`left = {S.left}` 这一轮的所有 `right` 都试完了，换下一个 `left`' if S.left < S.n - 1 else '`left` 也都枚举完了',
        'for right in range(n)': lambda S, B, r: f'枚举后半部分 `right = {S.right}`（`{S.nums[S.right]!r}`）' if not ('right' in B and B['right'] == S.right) else '`right` 枚举完了，回到外层',
        'if left == right': lambda S, B, r: ('同一个串不能用两次 → 跳过' if S.left == S.right else f'`left != right`，可以组成一对，继续判断'),
        'if num_l[left] + num_l[right] == target_l': lambda S, B, r: f"长度 `{S.num_l[S.left]} + {S.num_l[S.right]} = {S.num_l[S.left] + S.num_l[S.right]}`（目标 `{S.target_l}`），前缀标记 {S.left_flag[S.left]}，后缀标记 {S.right_flag[S.right]} → " + ('==成立==' if S.num_l[S.left] + S.num_l[S.right] == S.target_l and S.left_flag[S.left] and S.right_flag[S.right] else '不成立'),
        'res += 1': '`{nums[left]!r} + {nums[right]!r} = {target!r}`，找到一对：`res = {res}`',
        'return res': '一共 `{res}` 对',
    },
    skip=['continue'],
    max_steps=100,
    cards=dict(
        one_liner='拼接等于 target，就是前半匹配前缀、后半匹配后缀、长度加起来刚好',
        complexity='时间 `O(nl + n^2)`，空间 `O(n)`',
        problem=['`nums` 是数字字符串数组，`target` 是目标数字串',
                 '数出有序下标对 `(i, j)`，`i != j`，使 `nums[i] + nums[j] == target`',
                 '示例：`["1","12","2"]`，`target="12"` → `1`'],
        quote='拼接后字符串是否等于target的判断，可以分成两部分来看，即前半部分的字符串能与target的前缀匹配，以及后半部分的字符串能与target的后缀匹配。……还需要满足这两个部分长度之和恰好等于target的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个串各检查一遍：能否匹配 `target` 的前缀、后缀，结果存进标记数组',
              '长度 ≥ `target` 的串不可能参与，直接标记为假',
              '再枚举有序对：长度和等于 `target_l`，且左边是前缀、右边是后缀就计数',
              '作者说这里偷懒用了朴素枚举；也可统计次数后用双指针优化'],
        summary=['时间 `O(nl + n^2)`，空间 `O(n)`（朴素枚举配对）',
                 '易错：`left == right` 要跳过，同一个串不能用两次',
                 '易错：后缀比较要从末尾往前对齐：`num[-index - 1]` 对 `target[-index - 1]`',
                 '`(i, j)` 是有序对：`(0, 2)` 和 `(2, 0)` 要分别判断',
                 '原文已是 Python 3 可运行写法，仅删去了类型说明文档字符串'],
    ),
)
