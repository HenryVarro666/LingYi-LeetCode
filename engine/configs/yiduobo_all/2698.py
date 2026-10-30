CONFIG = dict(
    num=2698, title='求一个整数的惩罚数', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='暴力搜索回溯拆分',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1679'],
    code='''
class Solution(object):
    def punishmentNumber(self, n):

        def check(level, now, pre, digits, target):
            if level == len(digits):
                return now + pre == target

            num = pre * 10 + int(digits[level])
            if check(level + 1, now, num, digits, target):
                return True

            return check(level + 1, now + num, 0, digits, target)

        res = 0
        for i in range(1, n + 1):
            p = i * i
            if check(0, 0, 0, list(str(p)), i):
                res += p

        return res
''',
    call='Solution().punishmentNumber(9)',
    expect=82,
    views=[
        dict(type='text', fn=lambda S: (f"目标：把 `{S['p']}` 拆成若干段，和等于 =={S['i']}==" if 'p' in S and 'i' in S else ''), size=26, h=70),
        dict(type='array', var='digits', label='digits（蓝 = 正在处理的数字）', cell=70, h=230,
             pointers={'level': 'blue'}),
        dict(type='text', fn=lambda S: (f"已拆好的和 `now = {S['_inner']['now']}`，正在拼的数 `pre = {S['_inner']['pre']}`" if 'now' in S['_inner'] else ''), size=26, h=70),
        dict(type='calls', h=250, hide=('digits',)),
    ],
    watch=[('i', 'i', 'blue'), ('now', lambda S: S['_inner'].get('now'), 'cyan'), ('pre', lambda S: S['_inner'].get('pre'), 'pink'),
           ('res', 'res', 'green')],
    skip=['res = 0', 'p = i * i'],
    captions={
        'for i in range': lambda S, B, ret: (f'枚举 `i = {S.i}`' if 'i' in S else '枚举结束'),
        'if check(0, 0, 0': '`i = {i}`，`i*i = {p}`：从第 0 位开始搜，看能不能拆出和 `{i}`',
        'if level == len(digits)': lambda S, B, ret: (f'`level == {S.level}` = 数字个数：拆完了' if S.level == len(S.digits)
                                                       else f'`level = {S.level}`：还剩数字 `{"".join(S.digits[S.level:])}` 没处理'),
        'return now + pre == target': '`now + pre = {now} + {pre} = {now + pre}`，目标 `{target}` → ==返回 {ret}==',
        'num = pre * 10 + int(digits[level])': '把数字 `{digits[level]}` ==接在当前这一段后面==：`num = {num}`',
        'if check(level + 1, now, num': '分支一：这一段还没完，继续往后接（`pre = {num}`）',
        'return True': '某种拆法成功了 → 一路返回 `True`',
        'return check(level + 1, now + num, 0': '分支二：这一段到此为止，`now + num = {B.now + B.num}`，下一段重新从 0 拼',
        'res += p': '`{p}` 满足 → `res` = =={res}==',
        'return res': '所有 `i` 都判断完了，`res = {res}`',
    },
    max_steps=66,
    cards=dict(
        one_liner='对 i*i 的每一位二选一：接在当前段后面，或者在这里切一刀',
        complexity='时间 `O(n·2^m)`（`m` 为 `i*i` 的位数），空间 `O(m)`',
        problem=['`i*i` 的十进制字符串能拆成若干段，整数值之和等于 `i`，`i` 就算数',
                 '惩罚数 = 所有满足条件的 `i`（`1 <= i <= n`）的 `i*i` 之和',
                 '示例：`n = 10` → `182`；本视频：`n = 9` → `82`'],
        quote='最大的i * i也不过是10^6，因此我在这里使用的是直接搜索回溯暴力拆解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`check(level, now, pre, ...)`：`now` 是已拆好的段之和，`pre` 是正在拼的那一段',
              '每一位有两种选择：并入 `pre`，或者先把 `pre` 并入 `now` 再开新的一段',
              '走到末尾判断 `now + pre == target`；`n <= 1000`，逐个 `i` 暴力即可'],
        summary=['`n <= 1000`，`i*i <= 10^6`，最多 7 位，每个 `i` 至多 `2^6` 种拆法',
                 '末尾要判断 `now + pre`：最后一段还没并入 `now`',
                 '题解提到也可用 DP 拆分，但数据小，直接回溯就够',
                 '对比灵神：灵神枚举切割位置并预处理前缀和；yiduobo 逐位二选一，对每个 `i` 单独算',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行'],
    ),
)
