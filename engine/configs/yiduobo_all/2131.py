def _nm(k):
    return chr(k // 26 + 97) + chr(k % 26 + 97)


def _top(S):
    if 'word' not in S or 'res' not in S:
        return ''
    return f"答案 `res = {S['res']}`" + (f"，中心候选 `mid_cnt = {S['mid_cnt']}`" if S.get('mid_cnt') is not None else '')


CONFIG = dict(
    num=2131, title='连接两字母单词得到的最长回文串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='哈希表配对 · 中心单词',
    tags=['灵神题单', '难度分 1557'],
    code='''
class Solution(object):
    def longestPalindrome(self, words):

        def get_num(first, second):
            return (ord(first) - 97) * 26 + ord(second) - 97

        mid_cnt = 0
        res = 0
        num_dict = {}
        for word in words:
            if word[0] == word[1]:
                mid_flag = True
            else:
                mid_flag = False

            reverse_num = get_num(word[1], word[0])
            if num_dict.get(reverse_num, 0) > 0:
                res += 4
                num_dict[reverse_num] -= 1
                if mid_flag:
                    mid_cnt -= 1
            else:
                num = get_num(word[0], word[1])
                num_dict[num] = num_dict.get(num, 0) + 1
                if mid_flag:
                    mid_cnt += 1
        
        if mid_cnt > 0:
            res += 2
        
        return res
''',
    call='Solution().longestPalindrome(["ab","ty","yt","gg","gg","gg"])',
    expect=10,
    views=[
        dict(type='array', var='words', label='words（黄 = 当前处理的单词）', cell=96,
             color=lambda S, i, v: 'yellow' if S.get('word') == v and S.get('_line', 0) >= 11 else None),
        dict(type='map', var='num_dict', label='num_dict（编号 → 还没配对的个数；括号里是对应单词）',
             fmt=lambda k, v: f'{k}（{_nm(k)}）: {v}', h=220),
        dict(type='text', fn=_top, size=26),
    ],
    skip=['mid_flag = False', 'return (ord'],
    max_steps=80,
    watch=['word', ('reverse', 'reverse_num', 'cyan'), ('mid_flag', 'mid_flag', 'orange'), ('mid_cnt', 'mid_cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'def get_num': '约定：单词 `xy` 编号 `x×26 + y`，哈希表用编号当键',
        'mid_cnt = 0': '`mid_cnt`：还没配对的==回文单词==（如 `gg`）有几个，用来决定中心',
        'res = 0': '`res` 累计回文串长度，每配成一对加 4',
        'num_dict = {}': '`num_dict`：记录==还没找到搭档==的单词个数',
        'for word in words': '处理单词 `"{word}"`',
        'if word[0] == word[1]': lambda S, B, r: (f'`"{S.word}"` 两字母相同 → 它是回文单词，可能当中心' if S.word[0] == S.word[1]
                                                  else f'`"{S.word}"` 两字母不同 → 只能找 `"{S.word[::-1]}"` 配对'),
        'mid_flag = True': '`mid_flag = True`：记下==当前是回文单词==',
        'reverse_num = get_num': '算反向单词 `"{word[::-1]}"` 的编号：`get_num({word[1]!r}, {word[0]!r})` = ==26×{ord(word[1]) - 97} + {ord(word[0]) - 97}==',
        'if mid_flag': lambda S, B, r: ('是回文单词，配对 / 入表都会影响 `mid_cnt`' if S.mid_flag else '不是回文单词，不影响中心'),
        'if num_dict.get': lambda S, B, r: (f'表里有 `{S.num_dict.get(S.reverse_num, 0)}` 个未配对的 `"{S.word[::-1]}"` → ==配对成功=='
                                            if S.num_dict.get(S.reverse_num, 0) > 0
                                            else f'表里没有未配对的 `"{S.word[::-1]}"` → 先存起来等搭档'),
        'res += 4': '一对单词放两侧，长度 +4 → `res = {res}`',
        'num_dict[reverse_num] -= 1': '搭档被用掉 1 个 → `num_dict[{reverse_num}] = {num_dict[reverse_num]}`',
        'mid_cnt -= 1': '这个回文单词配成了对，不再落单 → `mid_cnt = {mid_cnt}`',
        'num = get_num': '单词自己 `"{word}"` 的编号：`get_num({word[0]!r}, {word[1]!r})` = ==26×{ord(word[0]) - 97} + {ord(word[1]) - 97}==',
        'num_dict[num] =': '`"{word}"` 入表，等后面的搭档 → `num_dict[{num}] = {num_dict[num]}`',
        'mid_cnt += 1': '回文单词入表后暂时落单 → `mid_cnt = {mid_cnt}`',
        'if mid_cnt > 0': lambda S, B, r: (f'`mid_cnt = {S.mid_cnt} > 0`：还有落单的回文单词 → ==放中心==' if S.mid_cnt > 0
                                           else '`mid_cnt = 0`：没有落单的回文单词，中心空着'),
        'res += 2': '中心放 1 个两字母单词，长度 +2 → `res = {res}`',
        'return res': '最长回文串长度 `{res}`',
    },
    cards=dict(
        one_liner='一个单词只有它的反向单词能配对，配成对就两侧各放一个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`words` 中每个元素是 ==两个小写字母== 的单词，每个至多用一次',
                 '任意顺序连接，求能得到的==最长回文串的长度==，没有返回 0',
                 '示例：`["lc","cl","gg"]` → `6`',
                 '本视频：`["ab","ty","yt","gg","gg","gg"]` → `10`'],
        quote='对于每个两字母单词，只有唯一的两字母单词，也就是其两个字符调换过的反向单词能与之配对。……对于寻找配对的问题，在这里可以使用哈希表统计每种两字母单词出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：当前单词的反向单词在表里还有剩 → ==配成一对，答案 +4==',
              '没有 → 把自己存进表，等后面来的搭档',
              '最后若还有落单的 `aa` 类单词，放==中心，+2=='],
        result='`ab` 没等到 `ba`；`ty/yt` 配 1 对 +4，`gg` 配 1 对 +4，剩 1 个 `gg` 放中心 +2 → 10',
        summary=['时间 `O(n)`，空间 `O(n)`，一趟遍历 + 哈希表',
                 '`mid_cnt` 跟踪落单的回文单词：入表 +1，配对成功 −1',
                 '回文单词 `gg` 的反向单词就是自己，所以第 2 个 `gg` 能和第 1 个配对',
                 '对比灵神：灵神先统计全部次数再取 min；yiduobo 边扫边配对，不用二次遍历'],
    ),
)
