def _chars(S):
    return ''.join(S['char_list']) if 'char_list' in S else ''


def _info(S):
    if 'digits' not in S:
        return ''
    s = S.get('s')
    ps = [f'{n}={S[n]}' for n in ('p1_1', 'p1_2', 'p2_1', 'p2_2') if S.get(n) is not None]
    t = f'数字和 `s = {s}`，`s % 3 = {s % 3}`' if s is not None else ''
    if S.get('_line', 0) >= 20 and S.get('res') is not None:
        t += f'；当前结果 ==`{S["res"]}`=='
    return t


CONFIG = dict(
    num=1363, title='形成三的最大倍数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数字和判整除 · 贪心删最小数字',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def largestMultipleOfThree(self, digits):

        digits = sorted(digits, reverse=True)
        s = 0
        p1_1 = None
        p1_2 = None
        p2_1 = None
        p2_2 = None
        char_list = [chr(x + 48) for x in digits]
        for index in range(len(digits) - 1, -1, -1):
            s += digits[index]
            if digits[index] % 3 == 1:
                if p1_1 is None:
                    p1_1 = index
                elif p1_2 is None:
                    p1_2 = index
            
            if digits[index] % 3 == 2:
                if p2_1 is None:
                    p2_1 = index
                elif p2_2 is None:
                    p2_2 = index

        if s % 3 == 0:
            res = ''.join(char_list)
        
        elif s % 3 == 1:
            if p1_1 is not None:
                res = ''.join(char_list[:p1_1]) + ''.join(char_list[p1_1 + 1:])
                s -= digits[p1_1]
            elif p2_1 is not None and p2_2 is not None:
                res = ''.join(char_list[:p2_2]) + ''.join(char_list[p2_2 + 1 : p2_1]) + ''.join(char_list[p2_1 + 1:])
                s -= digits[p2_1] + digits[p2_2]
            else:
                res = ''

        else:
            if p2_1 is not None:
                res = ''.join(char_list[:p2_1]) + ''.join(char_list[p2_1 + 1:])
                s -= digits[p2_1]
            elif p1_1 is not None and p1_2 is not None:
                res = ''.join(char_list[:p1_2]) + ''.join(char_list[p1_2 + 1 : p1_1]) + ''.join(char_list[p1_1 + 1:])
                s -= digits[p1_1] + digits[p1_2]
            else:
                res = ''
        
        if len(res) > 1 and s == 0:
            return '0'
        
        return res
''',
    call='Solution().largestMultipleOfThree([8, 1, 9, 5, 2])',
    expect='9852',
    skip=['p1_1 = None', 'p1_2 = None', 'p2_1 = None', 'p2_2 = None'],
    views=[
        dict(type='array', var='digits', label='digits（从大到小排好）', h=190, cell=84,
             pointers={'index': 'blue', 'p1_1': 'pink', 'p1_2': 'purple', 'p2_1': 'orange', 'p2_2': 'cyan'},
             color=lambda S, i, v: ('pink' if i == S.get('p1_1') or i == S.get('p1_2') else 'orange' if i == S.get('p2_1') or i == S.get('p2_2') else None) if 'p1_1' in S else None),
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='string', var='res', label='res（拼出的答案）', h=140, cell=70) if False else dict(type='text', fn=lambda S: f'结果 `res` = =={S["res"]!r}==' if S.get('res') is not None else '', size=30, h=70),
    ],
    watch=[('s', 's', 'green'), ('p1_1', 'p1_1', 'pink'), ('p1_2', 'p1_2', 'purple'), ('p2_1', 'p2_1', 'orange'), ('p2_2', 'p2_2', 'cyan')],
    captions={
        'digits = sorted': '先从大到小排序：数字越大越要排在高位 → `{digits}`',
        'char_list = ': '把每个数字转成字符，最后拼答案用',
        'for index in range': lambda S, B, r: (f'从小的一端往大的扫：`index = {S.index}`（数字 {S.digits[S.index]}），顺便累加和、记录模 3 余 1 / 余 2 的最小数字' if S.get('index') is not None and 'index' in S and S.get('index') != B.get('index') else '扫描结束'),
        's += digits[index]': '累加数字和：`s = {s}`',
        'digits[index] % 3 == 1': '`{digits[index]} % 3 = {digits[index] % 3}`：{"余 1，登记到余 1 的候选里" if digits[index] % 3 == 1 else "不是余 1，跳过"}',
        'digits[index] % 3 == 2': '`{digits[index]} % 3 = {digits[index] % 3}`：{"余 2，登记到余 2 的候选里" if digits[index] % 3 == 2 else "不是余 2，跳过"}',
        'p1_1 = index': '第一个遇到的余 1 数字就是==最小的==：`p1_1 = {p1_1}`',
        'p1_2 = index': '第二小的余 1 数字：`p1_2 = {p1_2}`',
        'p2_1 = index': '第一个遇到的余 2 数字就是==最小的==：`p2_1 = {p2_1}`',
        'p2_2 = index': '第二小的余 2 数字：`p2_2 = {p2_2}`',
        'if s % 3 == 0': '和 `{s}` 模 3 = `{s % 3}`：{"能被 3 整除 → 全部数字都用" if s % 3 == 0 else "不能整除，要删掉一些数字"}',
        'elif s % 3 == 1': '和模 3 余 1：删==一个余 1==，或删==两个余 2==',
        'res = \'\'.join(char_list)': '全部保留，已是从大到小 → `res = {res!r}`',
        'if p1_1 is not None': '有余 1 的数字吗？{"有 → 只删最小的那个" if p1_1 is not None else "没有"}',
        'elif p2_1 is not None and p2_2': '没有余 1 → 删两个最小的余 2（和余 1 时必然存在）',
        'if p2_1 is not None': '和模 3 余 2：有余 2 的数字吗？{"有 → 只删最小的那个" if p2_1 is not None else "没有"}',
        'elif p1_1 is not None and p1_2': '没有余 2 → 删两个最小的余 1',
        'res = \'\'.join(char_list[:p1_1])': '删掉下标 `{p1_1}` 的数字，其余保持从大到小 → `res = {res!r}`',
        'res = \'\'.join(char_list[:p2_1])': '删掉下标 `{p2_1}` 的数字，其余保持从大到小 → `res = {res!r}`',
        'res = \'\'.join(char_list[:p2_2])': '删掉下标 `{p2_2}`、`{p2_1}` 两个余 2 数字 → `res = {res!r}`',
        'res = \'\'.join(char_list[:p1_2])': '删掉下标 `{p1_2}`、`{p1_1}` 两个余 1 数字 → `res = {res!r}`',
        's -= ': '同步更新数字和 `s = {s}`（现在应是 3 的倍数）',
        'res = \'\'': '没办法凑出 3 的倍数 → 空串',
        'if len(res) > 1 and s == 0': '前导 0 检查：`{res!r}` 若长度 > 1 且数字和为 0 → 全是 0，只返回 `\'0\'`；这里{"需要" if len(res) > 1 and s == 0 else "不需要"}',
        'return res': '返回 `{ret!r}`',
    },
    cards=dict(
        one_liner='数字和决定删谁：从最小的余数数字里删，剩下从大到小排',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['给你一个整数数组 `digits`，用其中若干数字按任意顺序拼成==最大的 3 的倍数==',
                 '以字符串形式返回；凑不出就返回空串；结果不要有多余前导 0',
                 '示例：`[8,1,9]` → `"981"`；本视频：`[8,1,9,5,2]` → `"9852"`'],
        quote='3的倍数都满足各个位上数字加起来也是3的倍数……我们首先应该保证使用的数字尽量多，然后对于使用的数字，我们应该让较大的数字尽量排在高位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字和 `s` 模 3 为 0：全用；余 1：删最小的一个余 1，没有就删最小的两个余 2',
              '余 2 同理：删一个余 2，或两个余 1；删的数字越少、越小越好',
              '排序后从后往前扫，第一、二次遇到的就是最小的两个',
              '结果全是 0 时只返回 `"0"`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：删数字后要==同步更新 `s`==，最后靠 `s == 0` 判断结果是否全是 0',
                 '余 1 与余 2 都没有、且 `s` 不整除是不可能的，所以分支里的 `else` 只是兜底',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
