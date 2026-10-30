def _cur(S):
    if 'num' not in S:
        return ''
    n = S['num']
    parts = [f"百位 {n // 100}", f"十位 {n // 10 % 10}", f"个位 {n % 10}"]
    return f'正在检查三位偶数 `{n}`：' + '，'.join(parts)


CONFIG = dict(
    num=2094, title='找出 3 位偶数', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='枚举每个三位偶数 + 哈希表计数',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findEvenNumbers(self, digits):

        digit_dict = {}
        for digit in digits:
            digit_dict[digit] = digit_dict.get(digit, 0) + 1
        
        res = []
        for num in range(100, 1000, 2):
            first = num // 100
            if digit_dict.get(first, 0) > 0:
                digit_dict[first] -= 1
            else:
                continue

            second = num // 10 % 10
            if digit_dict.get(second, 0) > 0:
                digit_dict[second] -= 1
            else:
                digit_dict[first] += 1
                continue

            third = num % 10
            if digit_dict.get(third, 0) > 0:
                res.append(num)
            digit_dict[first] += 1
            digit_dict[second] += 1
        
        return res
''',
    call='Solution().findEvenNumbers([2, 1, 0])',
    expect=[102, 120, 210],
    views=[
        dict(type='map', var='digit_dict', label='digit_dict：数字 → 还剩几个', h=200),
        dict(type='text', fn=_cur, size=32),
        dict(type='stack', var='res', label='res', h=110),
    ],
    watch=[('num', 'num', 'blue'), ('first', 'first', 'pink'), ('second', 'second', 'cyan'),
           ('third', 'third', 'orange'), ('res', 'res', 'green')],
    skip=['res = []', 'for digit in digits'],
    max_steps=66,
    captions={
        'digit_dict[digit] =': '统计库存：数字 `{digit}` 一共有 `{digit_dict[digit]}` 个',
        'for num in range': '枚举每个三位偶数：`num = {num}`（步长 2，只看偶数）',
        'first = num': '分离百位：`{num} // 100 = {first}`',
        'if digit_dict.get(first': lambda S, B, ret: (
            f'百位数字 `{S.first}` 库存 `{S.digit_dict.get(S.first, 0)}` 个 → ==够用==，先占一个' if S.digit_dict.get(S.first, 0) > 0
            else f'百位数字 `{S.first}` 库存为 0 → 凑不出 `{S.num}`'),
        'digit_dict[first] -= 1': '占用百位：`digit_dict[{first}]` → {digit_dict[first]}',
        14: '百位不够，凑不出 → `continue` 换下一个 `num`',
        21: '十位也不够 → 百位已还回，`continue` 换下一个 `num`',
        'second = num': '分离十位：`{num} // 10 % 10 = {second}`',
        'if digit_dict.get(second': lambda S, B, ret: (
            f'十位数字 `{S.second}` 库存 `{S.digit_dict.get(S.second, 0)}` 个 → ==够用==，再占一个' if S.digit_dict.get(S.second, 0) > 0
            else f'十位数字 `{S.second}` 已经没有了 → 凑不出，要先把百位的库存==还回去=='),
        'digit_dict[second] -= 1': '占用十位：`digit_dict[{second}]` → {digit_dict[second]}',
        20: '`continue` 会跳过末尾的还原，所以先把百位还回去：`digit_dict[{first}]` → {digit_dict[first]}',
        26: '还原百位：`digit_dict[{first}]` → {digit_dict[first]}',
        'third = num': '分离个位：`{num} % 10 = {third}`',
        'if digit_dict.get(third': lambda S, B, ret: (
            f'个位数字 `{S.third}` 库存 `{S.digit_dict.get(S.third, 0)}` 个 → 三位都够，==`{S.num}` 可以凑出==' if S.digit_dict.get(S.third, 0) > 0
            else f'个位数字 `{S.third}` 库存为 0 → 凑不出 `{S.num}`'),
        'res.append': '记录答案 `{num}`',
        27: '还原十位：`digit_dict[{second}]` → {digit_dict[second]}，库存恢复成 {digit_dict}，给下一个 `num` 用',
        'return res': '全部检查完，一共 `{len(ret)}` 个。`num` 递增枚举，所以==结果天然有序==',
    },
    cards=dict(
        one_liner='三位偶数只有 450 个，直接逐个枚举，用哈希表判断数字够不够',
        complexity='时间 `O(n + 450)`，空间 `O(1)`',
        problem=['给一堆 0~9 的数字，挑 3 个拼成==不含前导零的三位偶数==',
                 '互不相同，从小到大返回',
                 '本视频：`[2,1,0]` → `[102,120,210]`'],
        quote='由于三位偶数的数量非常少，那么完全可以直接枚举每个三位偶数，然后将每一位分离出来，并借助哈希表来判断是否有足够的数字可以用来构成当前枚举到的这个三位偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`range(100, 1000, 2)`：从 100 起步长 2，天然没有前导零、一定是偶数',
              '`digit_dict` 记库存；依次占百位、十位，个位只查不占',
              '中途凑不出就要把已占的库存==还回去==，再试下一个数'],
        result='找到 102、120、210 ✓',
        summary=['时间 `O(n + 450)`，空间 `O(1)`',
                 '易错：第二位失败时要先 `digit_dict[first] += 1` 再 `continue`',
                 '个位只判断不占用，所以末尾只还原百位和十位',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '步数很多，视频中间一段会快进'],
    ),
)
