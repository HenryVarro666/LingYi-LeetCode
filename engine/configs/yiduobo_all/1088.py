def _stage(S):
    ln = S['_line']
    if ln <= 26:
        return '第一部分：数出 1..n 中全由 ==0,1,6,8,9== 组成的数'
    if ln <= 38:
        return '第二部分：减去位数 < length 的、翻转后相同的数'
    return '第三部分：减去位数 == length 且 <= n 的、翻转后相同的数'


CONFIG = dict(
    num=1088, title='易混淆数 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='数位枚举 · 可翻转数 − 翻转后相同的数',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def confusingNumberII(self, n):

        num_list = [int(x) for x in str(n)]
        length = len(num_list)
        res = 0
        
        flag = True
        valid_digit = [0, 1, 6, 8, 9]
        pow5 = [1]
        for index in range(1, length):
            pow5.append(pow5[-1] * 5)

        for index in range(length):
            p = len(valid_digit) - 1
            while valid_digit[p] > num_list[index]:
                p -= 1
            
            res += p * pow5[length - index - 1]
            if num_list[index] > valid_digit[p]:
                res += pow5[length - index - 1]
                flag = False
                break

        if flag:
            res += 1

        for k in range(1, length):
            if k == 1:
                res -= 3
            elif k == 2:
                x = 4
                res -= x
            elif k % 2 == 1:
                res -= x * 3
            else:
                x *= 5
                res -= x

        reverse_digit = {0: 0, 1: 1, 6: 9, 8: 8, 9: 6}
        middle_digit = [0, 1, 8]

        left = 0
        right = length - 1
        bound_list = [None] * length
        if length % 2 == 1:
            middle_choice = 3
        else:
            middle_choice = 1

        flag = True
        while left <= right:
            if left == right:
                candidate_digit = middle_digit
            else:
                candidate_digit = valid_digit

            p = len(candidate_digit) - 1
            while candidate_digit[p] > num_list[left]:
                p -= 1
            
            if left < right - 1:
                delta = middle_choice * pow5[(right - left - 1) // 2]
            else:
                delta = 1

            if left == 0:
                res -= (p - 1) * delta
            else:
                res -= p * delta

            if num_list[left] > candidate_digit[p]:
                res -= delta
                flag = False
                break
            else:
                bound_list[left] = candidate_digit[p]
                bound_list[right] = reverse_digit[candidate_digit[p]]

            left += 1
            right -= 1

        if flag and int(''.join([str(x) for x in bound_list])) <= n:
            res -= 1

        return res
''',
    call='Solution().confusingNumberII(20)',
    expect=6,
    views=[
        dict(type='array', var='num_list', label='num_list（n 的各位数字，蓝 = 当前 index）', cell=96, h=190,
             pointers={'left': 'cyan', 'right': 'pink'},
             color=lambda S, i, v: 'blue' if S['_line'] <= 26 and i == S.get('index') else None),
        dict(type='array', var='valid_digit', label='valid_digit（可翻转的数字）', cell=70, h=150),
        dict(type='array', var='bound_list', label='bound_list（左右对称填出的边界数）', cell=70, h=150),
        dict(type='text', h=90, size=28, fn=_stage),
    ],
    watch=[('length', 'length', 'blue'), ('res', 'res', 'green'), ('p', 'p', 'orange'), ('flag', 'flag', 'pink')],
    captions={
        'for index in range(1, length)': '先算出 `5^0 .. 5^(length-1)`',
        'for index in range(length)': '从 n 的最高位开始，逐位卡住上界',
        'while candidate_digit[p] > num_list[left]': lambda S, B, r: (
            f'`candidate_digit[{S.p}] = {S.candidate_digit[S.p]} > num_list[{S.left}] = {S.num_list[S.left]}`：太大 → `p` 左移'
            if S.candidate_digit[S.p] > S.num_list[S.left] else
            f'`candidate_digit[{S.p}] = {S.candidate_digit[S.p]} <= {S.num_list[S.left]}`：`p = {S.p}`'),
        'if left < right - 1': lambda S, B, r: ('`left` 和 `right` 之间还夹着别的位 → 中间的填法有 `middle_choice × 5^(…)` 种' if S.left < S.right - 1
                                                else '`left` 与 `right` 相邻或相同 → 中间没有空位'),
        'if left == 0': lambda S, B, r: ('`left = 0`：这是最高位，不能填 0' if S.left == 0 else '不是最高位，`0` 也可以填'),
        'num_list = [int': '把 `n` 拆成各位数字：`num_list = {num_list}`',
        'length = len': '`length = {length}` 位',
        'res = 0': '`res` 累计答案，先算“可翻转数”再减去“翻转后相同的数”',
        'flag = True': '`flag` 记录 n 自己是不是由可翻转数字组成',
        'valid_digit = [': '可翻转数字只有 `0, 1, 6, 8, 9` 五个',
        'pow5 = [1]': '`pow5[k] = 5^k`：k 位可自由填的数共 `5^k` 种（允许前导 0）',
        'pow5.append': '`pow5 = {pow5}`',
        'p = len(valid_digit) - 1': '从 `valid_digit` 最大的数字往前找',
        'while valid_digit[p] > num_list[index]': lambda S, B, r: (
            f'`valid_digit[{S.p}] = {S.valid_digit[S.p]} > num_list[{S.index}] = {S.num_list[S.index]}`：太大 → `p` 左移'
            if S.valid_digit[S.p] > S.num_list[S.index] else
            f'`valid_digit[{S.p}] = {S.valid_digit[S.p]} <= {S.num_list[S.index]}`：`p = {S.p}` 是最大的不超过当前位的下标'),
        'p -= 1': '`p` 左移 → {p}',
        'res += p * pow5': '这一位填比 `valid_digit[p]` 小的 `{p}` 种数字，后面 `{length - index - 1}` 位随便填：`res += {p} × {pow5[length - index - 1]}` → ==`{res}`==',
        'if num_list[index] > valid_digit[p]': lambda S, B, r: (
            f'`{S.num_list[S.index]} > valid_digit[{S.p}] = {S.valid_digit[S.p]}`：当前位 `{S.num_list[S.index]}` 不是可翻转数字 → 填 `valid_digit[p]` 的数都小于 n，也一并数上，后面不用再看'
            if S.num_list[S.index] > S.valid_digit[S.p] else
            f'`num_list[{S.index}] = valid_digit[{S.p}]`：当前位本身可翻转 → 继续看下一位'),
        'res += pow5[length - index - 1]': '填 `valid_digit[p]` 本身，后面随便填：`res += {pow5[length - index - 1]}` → ==`{res}`==',
        'flag = False': '`flag = False`：n 本身不是可翻转数，结束这一部分',
        'if flag:': lambda S, B, r: ('每一位都可翻转 → n 自己也算一个：`res += 1`' if S.flag else '`flag = False`，n 自己不算'),
        'for k in range(1, length)': '按位数 `k` 统计翻转后相同的数（位数小于 `length` 的全部要减掉）',
        'res -= 3': '1 位的对称数：`0, 1, 8` 共 3 个（`0` 也被问题 1 算进去了）→ `res -= 3`',
        'x = 4': '2 位的只有 `11, 69, 88, 96` 共 4 个，`x = 4`',
        'res -= x * 3': '奇数位：在偶数位的中间插入 `0/1/8`，共 `x × 3`',
        'x *= 5': '偶数位：在中间插入 `00/11/69/88/96`，`x × 5` → `x = {x}`',
        'res -= x': '`res -= {x}` → {res}',
        'reverse_digit = {': '每个可翻转数字翻转后是谁：`6 ↔ 9`，其余不变',
        'middle_digit = [': '奇数位的正中间只能是 `0, 1, 8`',
        'left = 0': '`left`、`right` 从两端往中间填：先定左边，右边自动成为它的翻转',
        'right = length - 1': '`right = {right}`',
        'bound_list = [None]': '`bound_list` 记录“紧贴 n 的上界”那个对称数',
        'middle_choice = 3': '长度为奇数：最中间有 3 种选择',
        'middle_choice = 1': '长度为偶数：没有中间位，系数为 1',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`，继续' if S.left <= S.right
                                                else f'`left = {S.left} > right = {S.right}`：全部处理完'),
        'candidate_digit = middle_digit': '`left == right`：正中间只能用 `[0, 1, 8]`',
        'candidate_digit = valid_digit': '不是中间位：五个可翻转数字都能用',
        'delta = middle_choice': '中间还剩若干位，合法的对称填法共 `delta = {delta}` 种',
        'delta = 1': '`delta = 1`：中间没有空位了',
        'res -= (p - 1) * delta': '最高位不能是 0，所以只有 `p - 1` 种更小的选择：`res -= {p - 1} × {delta}` → ==`{res}`==',
        'res -= p * delta': '更小的选择有 `p` 种：`res -= {p} × {delta}` → ==`{res}`==',
        'if num_list[left] > candidate_digit[p]': lambda S, B, r: (
            f'`{S.num_list[S.left]} > {S.candidate_digit[S.p]}`：当前位不是可翻转数字 → 填 `candidate_digit[p]` 的对称数也都小于 n，不用再往里看'
            if S.num_list[S.left] > S.candidate_digit[S.p] else
            f'`{S.num_list[S.left]} = {S.candidate_digit[S.p]}`：先把它填到两端，继续往里'),
        'res -= delta': '这些对称数都 `< n`：`res -= {delta}` → ==`{res}`==',
        'bound_list[left] = candidate_digit[p]': '左端填 `{candidate_digit[p]}`',
        'bound_list[right] = reverse': '右端填它的翻转 `{reverse_digit[candidate_digit[p]]}`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'if flag and int': lambda S, B, r: ('每一层都紧贴 n：看边界数是否 `<= n`，成立则再减 1' if S.flag
                                            else '`flag = False`：前面已经算过，不用再减'),
        'return res': '易混淆数一共 ==`{res}`== 个',
    },
    skip=['pow5.append', 'left += 1', 'right -= 1'],
    max_steps=90,
    cards=dict(
        one_liner='答案 = 由可翻转数字组成的数 − 翻转后不变的数',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['数字旋转 180 度：`0 1 8` 不变，`6 ↔ 9`，其余无效',
                 '翻转后是有效且与原数不同的数称为易混淆数',
                 '统计 `[1, n]` 内的易混淆数个数；本视频 `n = 20` → `6`'],
        quote='那么最终结果就是问题1的答案减去问题2的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题 1：数出 `<= n` 且各位都在 `0,1,6,8,9` 的数，按位卡上界，每位可填 `5^k` 种',
              '问题 2：数出翻转后==与原数相同==的数：左右对称填，中间位只能是 `0,1,8`',
              '前导 0 在问题 1 无害，在问题 2 不合法，因此要拆成“位数小于 length”和“位数等于 length”'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '问题 1 可以顺便算上位数不足的数，因为前导 0 不影响可翻转性',
                 '问题 2 最高位不能为 0，所以用 `p - 1`；奇数位正中间只有 3 种',
                 '这份代码对 1 位的 n 不适用（会漏算），本视频用 n=20，不涉及这种情况',
                 '原文为 Python 2 写法，`(right - left - 1) / 2` 整数除法已改为 `//`'],
    ),
)
