CONFIG = dict(
    num=249, title='移动字符串分组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='相邻差值数组作哈希 key',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def groupStrings(self, strings):

        single_list = []
        h = {}
        for s in strings:
            if len(s) == 1:
                single_list.append(s)
            else:
                diff_list = [(ord(s[index]) - ord(s[index - 1]) + 26) % 26 for index in range(1, len(s))]
                key = tuple(diff_list)
                if key not in h:
                    h[key] = []
                h[key].append(s)
        
        res = list(h.values())
        if single_list:
            res.append(single_list)
        return res
''',
    call='Solution().groupStrings(["abc","bcd","az","ba","a","z"])',
    expect=[['abc', 'bcd'], ['az', 'ba'], ['a', 'z']],
    views=[
        dict(type='string', var='s', h=130, cell=60, label='当前字符串 s'),
        dict(type='text', h=60, fn=lambda S: ('差值 `' + str(S['diff_list']) + '`：相邻字母“差几位”（循环，+26 再取模）') if S.get('diff_list') is not None and S.get('_line') in (10, 11, 12, 13, 14) else ''),
        dict(type='map', var='h', fmt=lambda k, v: f'{list(k)} → {v}', font=24, h=300, label='h：差值数组 → 同组字符串'),
        dict(type='array', var='single_list', h=150, cell=60, label='single_list：长度为 1 的串，全部归为一组'),
    ],
    watch=['s', 'diff_list', 'key'],
    captions={
        'single_list = []': '长度为 1 的字符串彼此都能移成对方，统一放进 `single_list`',
        'h = {}': '`h`：差值数组 → 该组的字符串',
        'for s in strings': lambda S, B, r: ('所有字符串都分好了' if B.get('s') == S.get('s') and S.get('s') == S.strings[-1] and B.get('key') is not None and 'a' in S.strings else f'取下一个字符串 `{S.s}`'),
        'if len(s) == 1': '`len({s}) == 1`：{"长度为 1，放进 single_list" if len(s) == 1 else "长度 >= 2，要算差值数组"}',
        'single_list.append': '`{s}` 加入 `single_list` → `{single_list}`',
        'diff_list =': '同组的串整体平移 k 位，相邻字母之差不变 → 算相邻差 `(s[i]-s[i-1]+26)%26`：`{s}` → ==`{diff_list}`==',
        'key = tuple': '列表不能当字典的 key，转成元组：`key = {key}`',
        'if key not in h': '`{key}` 在 `h` 里吗？{"不在，是新的一组" if key not in B.h else "在，说明和前面某个串同组"}',
        'h[key] = []': '为这个差值新建一组：`h[{key}] = []`',
        'h[key].append(s)': '把 `{s}` 放进这一组：`h[{key}] = {h[key]}`',
        'res = list(h.values())': '`h` 里每一组就是一个答案：`{res}`',
        'if single_list': '`single_list` {"非空，也算一组" if single_list else "为空，不用加"}',
        'res.append(single_list)': '把长度为 1 的那组也加进去：`{res}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='整体平移不改变相邻字母之差：差值数组就是组的“指纹”',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['字符串每个字母都可以==整体循环右移==（`z` 之后回到 `a`）',
                 '能互相移成对方的字符串算一组，把 `strings` 按组分开',
                 '本视频：`["abc","bcd","az","ba","a","z"]` → `[["abc","bcd"],["az","ba"],["a","z"]]`'],
        quote='t[i] - t[i - 1] = (s[i] + k) - (s[i - 1] + k) = s[i] - s[i - 1]，也就是说如果两个字符串可以分到同一组，那么相邻位置相减得到的差值数组必然是完全相同的。',
        quote_src='—— yiduobo 题解原文',
        idea=['同组 ⇔ 每个字母移动了同一个 `k`',
              '相邻两个字母相减，`k` 被抵消，只剩原始的相邻差',
              '差值数组做哈希 key，一趟遍历分组；长度为 1 的串单独归成一组'],
        summary=['时间、空间都是 `O(总字符数)`，只遍历一次',
                 '差值要 `+ 26` 再 `% 26`，处理 `z → a` 的循环（如 `az` 与 `ba`）',
                 '长度为 1 的字符串差值数组为空，题解选择把它们统一放在最后一组',
                 '原文为 Python 2 写法，`h.values()` 在 Python 3 返回的不是列表、没有 `append`，已改为 `list(h.values())`'],
    ),
)
