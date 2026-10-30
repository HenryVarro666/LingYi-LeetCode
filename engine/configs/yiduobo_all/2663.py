def _chars(S):
    a = S.get('asc_list')
    return [chr(x) for x in a] if a else []


def _bad(S, i):
    a = S.get('asc_list')
    if not a or i is None or i < 0 or i >= len(a):
        return False
    return (i > 0 and a[i] == a[i - 1]) or (i > 1 and a[i] == a[i - 2])


def _txt(S):
    if 'asc_list' not in S:
        return '先找必须修改的最高位，再把它右边填成最小的合法字母'
    if 'index' in S and S['_line'] >= 31:
        return f"填第 `{S['index']}` 位：从 `a` 起选第一个与左边两个字母都不同的字母"
    if 'p' in S:
        return f"尝试修改第 `{S['p']}` 位：新字母要比原来大、不超过第 k 个字母，且不与左边两位相同"
    return ''


CONFIG = dict(
    num=2663, title='字典序最小的美丽字符串', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='找最高修改位 · 再逐位填最小',
    tags=['灵神题单', '贪心与思维', '难度分 2416'],
    code='''
class Solution(object):
    def smallestBeautifulString(self, s, k):

        asc_list = []
        for char in s:
            asc_list.append(ord(char))
        
        max_asc = 97 + k - 1

        n = len(asc_list)
        flag = False
        p = n
        while p > 0 and not flag:
            p -= 1
            for asc in range(asc_list[p] + 1, max_asc + 1):
                if p > 0 and asc_list[p - 1] == asc:
                    continue
                if p > 1 and asc_list[p - 2] == asc:
                    continue
                
                flag = True
                asc_list[p] = asc
                break

        if p == 0 and not flag:
            return ""

        for index in range(p + 1, n):
            for asc in range(97, max_asc + 1):
                if index > 0 and asc_list[index - 1] == asc:
                    continue
                if index > 1 and asc_list[index - 2] == asc:
                    continue
                
                asc_list[index] = asc
                break
        
        return ''.join([chr(x) for x in asc_list])
''',
    call='Solution().smallestBeautifulString("dacd", 4)',
    expect='dbac',
    skip=['for char in s', 'asc_list.append(ord(char))'],
    views=[
        dict(type='text', fn=_txt, size=26, h=100),
        dict(type='array', var=_chars, label='asc_list 对应的字母（蓝 = 当前位 p / index）', cell=110, h=300,
             pointers={'p': 'blue', 'index': 'pink'},
             color=lambda S, k, v: ('blue' if k == S.get('p') and 'index' not in S else 'pink' if k == S.get('index') else None)),
        dict(type='text', fn=lambda S: (f"候选字母 `asc = {S['asc']}` 即 `'{chr(S['asc'])}'`" if 'asc' in S and 'asc_list' in S else ''), size=26, h=70),
    ],
    watch=[('p', 'p', 'blue'), ('flag', 'flag', 'green'), ('index', 'index', 'pink'), ('asc', 'asc', 'orange')],
    captions={
        'asc_list = []': '`asc_list` 存每个字母的 ASCII 码',
        'max_asc =': '前 k 个字母的最大编码 `max_asc = {max_asc}`（即 `{chr(max_asc)}`）',
        'n = len': '`n = {n}`',
        'flag = False': '`flag` 表示“已找到可修改的位置”',
        'p = n': '`p` 从末尾往前枚举修改的最高位',
        'while p > 0 and not flag': lambda S, B, r: (f"还没找到修改位（`flag = False`），继续往前" if not S.flag else '已找到修改位，退出'),
        'p -= 1': '尝试修改第 `p = {p}` 位（原字母 `{chr(asc_list[p])}`）',
        'for asc in range(asc_list[p] + 1': lambda S, B, r: (f"第 {S.p} 位的候选都试完了，没有合法的 → 再往前一位" if 'asc' in B and B.asc == S.asc else f"候选 `{chr(S.asc)}`：必须比原字母大" if 'asc' in S and S.asc <= S.max_asc else f"第 {S.p} 位没有更大且不超过第 k 个字母的候选了"),
        'if p > 0 and asc_list[p - 1] == asc': lambda S, B, r: (f"`{chr(S.asc)}` 与左边第 1 位相同 → 长 2 回文，跳过" if S.p > 0 and S.asc_list[S.p - 1] == S.asc
                                                                else f"`{chr(S.asc)}` 与左边第 1 位不同"),
        'if p > 1 and asc_list[p - 2] == asc': lambda S, B, r: (f"`{chr(S.asc)}` 与左边第 2 位相同 → 长 3 回文，跳过" if S.p > 1 and S.asc_list[S.p - 2] == S.asc
                                                                else f"`{chr(S.asc)}` 与左边第 2 位也不同"),
        'continue': '这个候选不行，换下一个字母',
        'flag = True': '找到了！这一位就是必须修改的最高位',
        'asc_list[p] = asc': '第 `{p}` 位改成 `{chr(asc)}`',
        'break': '确定这一位，退出候选循环',
        'if p == 0 and not flag': lambda S, B, r: ('枚举到最高位仍然没找到 → 无解' if S.p == 0 and not S.flag else '找到了修改位，继续填右边'),
        'for index in range(p + 1, n)': lambda S, B, r: ('右边都填好了' if 'index' in B and B.index == S.index else f"右边第 `{S.index}` 位：要填最小的合法字母"),
        'for asc in range(97, max_asc + 1)': '从 `a` 开始试，找第一个合法的',
        'if index > 0 and asc_list[index - 1] == asc': lambda S, B, r: (f"`{chr(S.asc)}` 与左边第 1 位相同，跳过" if S.asc_list[S.index - 1] == S.asc else f"`{chr(S.asc)}` 与左边第 1 位不同"),
        'if index > 1 and asc_list[index - 2] == asc': lambda S, B, r: (f"`{chr(S.asc)}` 与左边第 2 位相同，跳过" if S.index > 1 and S.asc_list[S.index - 2] == S.asc else f"`{chr(S.asc)}` 与左边第 2 位也不同"),
        'asc_list[index] = asc': '第 `{index}` 位填最小的合法字母 `{chr(asc)}`',
        'return \'\'.join': '答案 `{ret!r}`',
        'return ""': '无解，返回空串',
    },
    max_steps=80,
    cards=dict(
        one_liner='先找必须改的最高位，右边再逐位填最小',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['==美丽字符串==：只含前 `k` 个字母，且没有长度 `>= 2` 的回文子串',
                 '给定美丽字符串 `s`，求字典序比它大的最小美丽字符串，没有返回 `""`',
                 '示例：`s = "dacd"`，`k = 4` → `"dbac"`'],
        quote='于是可以从字符串尾部开始向前遍历，枚举必须进行修改的最高位。对于这个最高位上修改后的字符，需要满足以下三个条件：……',
        quote_src='—— yiduobo 题解原文',
        idea=['只需避开长 2、长 3 的回文：新字母不能等于左边第 1、第 2 位',
              '从尾部往前枚举“最高修改位” `p`：新字母要大于原字母、不超过第 k 个字母、不与左边两位相同',
              '`p` 右边要字典序最小：每一位从 `a` 起选第一个合法字母，`k >= 4` 保证总有解'],
        result='末两位改不动，`p = 1` 把 `a` 改成 `b`，右边依次填 `a`、`c`：`dbac` ✓',
        summary=['时间 `O(nk)`，空间 `O(n)`',
                 '`p` 一路枚举到 0 仍失败才无解',
                 '右边填字母时同样只看左边两位；`k >= 4` 保证一定有字母可选',
                 '与灵神对比：灵神用 k 进制加一 + 进位一趟走完；yiduobo 分成“找最高位”和“填右边”两段',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
