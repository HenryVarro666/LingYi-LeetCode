CONFIG = dict(
    num=2165, title='重排数字的最小值', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='分类讨论 · 负数降序、正数升序并换掉前导零（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1362'],
    code='''
class Solution:
    def smallestNumber(self, num: int) -> int:
        s = list(str(num))
        if num <= 0:
            t = s[1:]
            t.sort(reverse=True)  # 负数，从大到小排序（兼容 num=0）
            s[1:] = t
            ans = int("".join(s))
            return ans
        s.sort()  # 正数，从小到大排序
        i = 0
        while s[i] == '0':  # 如果有前导零就从后面找一个数字
            i += 1
        s[i], s[0] = s[0], s[i]  # 交换，保证没有前导零
        ans = int("".join(s))
        return ans
''',
    call='Solution().smallestNumber(310)',
    expect=103,
    views=[
        dict(type='string', var='s', label='s（蓝 = i 指向的第一个非 0，粉 = 下标 0）', cell=110, h=240, pointers={'i': 'blue'}),
        dict(type='text', size=36, h=140, fn=lambda S: ('正数：从小到大排序 → 前导 0 要和第一个非 0 交换' if 'num' in S and S['num'] > 0 else '负数 / 0：符号不动，数字部分从大到小排')),
    ],
    watch=['num', ('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        's = list': '把 `num` 转成字符列表：`s = {s}`',
        'if num <= 0': lambda S, B, r: ('`num <= 0`：负数，要让绝对值最大 → 走负数分支' if S.num <= 0 else '`num > 0`：正数，要让绝对值最小 → 走正数分支'),
        's.sort()': '正数从小到大排序：`s = {s}`（可能出现前导 0）',
        'while s[i]': lambda S, B, r: (f"`s[{S.i}] = '{S.s[S.i]}'` 还是 0 → 继续往后找" if S.s[S.i] == '0' else f"`s[{S.i}] = '{S.s[S.i]}'`：第一个非 0 数字，停下"),
        'i += 1': '前导零，`i` 后移到 {i}',
        's[i], s[0]': '把第一个非 0 数字换到最前面：`s = {s}`，==没有前导零了==',
        'ans = int': '拼成数字 `ans = {ans}`',
        'return ans': '最小值 =={ans}==',
    },
    cards=dict(
        one_liner='正数升序排好，再把首位的 0 换成第一个非 0',
        complexity='时间 `O(L log L)`，空间 `O(L)`（`L` 为位数）',
        problem=['重排 `num` 的各位数字，使值最小且没有前导零，符号不变',
                 '示例：`310` → `103`；`-7605` → `-7650`',
                 '本视频：`310` → `103`'],
        quote='负数，从大到小排序（兼容 num=0）；正数，从小到大排序；如果有前导零就从后面找一个数字，交换，保证没有前导零。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['负数：绝对值越大越小 → 数字降序排',
              '正数：绝对值越小越小 → 数字升序排',
              '升序后 0 会跑到最前，找第一个非 0 与首位交换'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`sort.Slice` 对应 `list.sort`）',
                 '时间 `O(L log L)`，空间 `O(L)`',
                 '易错点：负数只排符号之后的部分 `s[1:]`；`num = 0` 走第一个分支',
                 '正数的 `while s[i] == \'0\'` 不会越界：num > 0 至少有一个非 0'],
    ),
)
