CONFIG = dict(
    num=2457, title='美丽整数的最小增量', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='拆位 + 逐位进位', tags=['难度分 1680'],
    code='''
class Solution(object):
    def makeIntegerBeautiful(self, n, target):

        digit_list = []
        now = n
        while now:
            digit_list.append(now % 10)
            now //= 10
        
        s = sum(digit_list)
        p = 0
        inc_flag = False
        while s > target or inc_flag:
            while digit_list[p] == 0:
                p += 1
            
            s -= digit_list[p]
            digit_list[p] = 0
            if p == len(digit_list) - 1:
                digit_list.append(1)
                break
            
            if digit_list[p + 1] != 9:
                s += 1
                digit_list[p + 1] += 1
                inc_flag = False
            else:
                inc_flag = True

        digit_list.reverse()
        now = 0
        for digit in digit_list:
            now = now * 10 + digit
        
        return now - n
''',
    call='Solution().makeIntegerBeautiful(467, 6)',
    expect=33,
    views=[
        dict(type='array', var='digit_list', pointers={'p': 'blue'}, h=260, label='digit_list（低位在前）', cell=120,
             color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None),
        dict(type='text', size=34, fn=lambda S: (f"数位和 `s = {S['s']}`，目标 `≤ {S['target']}`" + (f"，进位位 `p = {S['p']}`" if 'p' in S else '')) if 's' in S else f"`n = {S['n']}`，`target = {S['target']}`"),
    ],
    watch=['s', 'p', 'inc_flag', ('target', 'target', 'green')],
    captions={
        'digit_list.append': '把个位 `{digit_list[-1]}` 放进列表：低位在前，方便从低位开始进位',
        'now //= 10': '去掉个位，`now` → {now}',
        's = sum': '初始数位和 `s = {s}`，比 `target = {target}` 大，需要靠进位把它变小',
        'p = 0': '`p` 指向当前要进位的数位，从最低位开始',
        12: '`inc_flag`：上一次进位时高一位是 9 的标记，初始为假',
        'while s > target': '`s = {s}`，`target = {target}`：=={"还大，或者还有 9 没处理完 → 继续进位" if (s > target or inc_flag) else "达标，停止进位"}==',
        'while digit_list[p] == 0': '跳过已经是 0 的位：它再进位不会让和变小',
        'p += 1': '这一位是 0，`p` → {p}',
        's -= digit_list[p]': '这一位要进位归零：`s` 减去 `{B.digit_list[p]}` → {s}',
        'digit_list[p] = 0': '第 `{p}` 位归零',
        'if p == len': '`p = {p}` 是最高位吗：=={"是，进位超出最高位，补一个 1 并结束" if p == len(digit_list) - 1 else "不是，进位会落到下一位"}==',
        'digit_list.append(1)': '进位超过最高位：新增一位 `1`',
        'if digit_list[p + 1] != 9': '高一位是 `{digit_list[p+1]}`：=={"不是 9，直接加 1" if digit_list[p+1] != 9 else "是 9，加 1 会连锁进位"}==',
        's += 1': '高一位加 1，数位和 `s` + 1 → {s}',
        'digit_list[p + 1] += 1': '高一位变成 `{digit_list[p+1]}`',
        26: '这次进位没遇到 9，标记清除',
        'inc_flag = True': '高一位是 9：先不加 1，打上标记，本轮 `s` 不拿去比较',
        'digit_list.reverse()': '翻转成高位在前，准备还原成数字',
        'now = now * 10': '拼回数字：`now = {now}`',
        'return now - n': '进位后的数 `{now}` 减去原数 `{n}` = =={ret}==',
    },
    cards=dict(
        one_liner='只有进位能让数位和变小，从低位开始逐位进位',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['数位和 `≤ target` 的整数是美丽整数',
                 '求最小非负 `x`，使 `n + x` 美丽',
                 '示例：`467, 6` → `33`'],
        quote='变小的唯一途经是产生了进位，使得某一位上的数变成了0。',
        quote_src='—— yiduobo 题解原文',
        idea=['一开始拆出各位数字并算好 `s`，进位时 `O(1)` 地加减 `s`',
              '为了让 x 最小，从低位的后缀开始进位：该位归零、高一位加 1',
              '特殊情况：进位超过最高位要补 1；高一位是 9 时用 `inc_flag` 推迟比较'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`',
                 '易错：高一位是 9 的连续进位、进位超过最高位',
                 '对比灵神：灵神每轮直接重算进位后的数位和，更短；这里一次拆位后增量维护'],
    ),
)
