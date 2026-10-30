CONFIG = dict(
    num=1647, title='字符频次唯一的最小删除次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='频次降序 + 逐个往下压',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def minDeletions(self, s):

        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1

        cnt_list = sorted(char_cnt.values(), reverse=True)
        res = 0
        now = cnt_list[0]
        mul = 1
        p = 1
        while p < len(cnt_list):
            while p < len(cnt_list) and now == cnt_list[p]:
                mul += 1
                p += 1

            if mul > 1:
                res += mul - 1
                now -= 1
                mul -= 1
            else:
                now = cnt_list[p]
                p += 1

        while mul > 1 and now > 0:
            res += mul - 1
            now -= 1
            mul -= 1

        return res
''',
    call="Solution().minDeletions('aaabbbcc')",
    expect=2,
    views=[
        dict(type='map', var='char_cnt', h=170, label='char_cnt（每种字符的频次）'),
        dict(type='array', var=lambda S: S['cnt_list'] if 'cnt_list' in S else [], pointers={'p': 'blue'}, h=200, label='cnt_list（频次降序）'),
        dict(type='text', fn=lambda S: f"当前频次 `now = {S['now']}`，有 `mul = {S['mul']}` 种字符频次相同" if 'mul' in S else ''),
    ],
    watch=['now', 'mul', ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'char_cnt[char] =': '统计 `{char}` 出现次数：`char_cnt[{char!r}] = {char_cnt[char]}`',
        'cnt_list = sorted': '频次从大到小排序：==先处理频次高的==，它们往下压才不会撞上后面的。`{cnt_list}`',
        'res = 0': '`res` 累计删除次数',
        'now = cnt_list[0]': '`now` = 当前考察的频次 = 最高频次 `{now}`',
        'mul = 1': '`mul`：频次为 `now` 的字符种数，目前 1 种',
        'p = 1': '`p` 指向下一个待考察的频次',
        'while p < len(cnt_list):': lambda S, B, r: (f'`p = {S.p} < {len(S.cnt_list)}`：还有频次没处理' if S.p < len(S.cnt_list) else f'`p = {S.p}` 到末尾 → 扫完所有频次'),
        'while p < len(cnt_list) and now': lambda S, B, r: (f'`now = {S.now}` 等于 `cnt_list[{S.p}]` → 又一种字符撞频次' if S.p < len(S.cnt_list) and S.now == S.cnt_list[S.p] else '后面的频次和 `now` 不同了，撞车的种数数完'),
        'mul += 1': '又多一种字符频次是 `now`：`mul` → {mul}',
        'p += 1': '`p` 右移到 {p}',
        'if mul > 1': lambda S, B, r: (f'`mul = {S.mul} > 1`：频次重复，==保留一种，其余各删一个==' if S.mul > 1 else '`mul = 1`：频次唯一，不用删'),
        'res += mul - 1': '保留 1 种，其余 `{mul}-1` 种各删一个字符：`res` → ==`{res}`==',
        'now -= 1': '这些字符删一个后频次变成 `now - 1`：`now` → {now}',
        'mul -= 1': '被降一级的字符有 `{mul}` 种，接着和 `cnt_list[p]` 比',
        'now = cnt_list[0]': '`now` = 最高频次 `{now}`',
        'now = cnt_list[p]': '`mul = 1` 无冲突，转去考察下一个频次：`now = {now}`',
        'while mul > 1 and now': lambda S, B, r: (f'扫完了但 `mul = {S.mul} > 1` 且 `now = {S.now} > 0`：还要继续往下压' if S.mul > 1 and S.now > 0 else '`mul <= 1` 或 `now = 0`：不再有冲突 → 结束'),
        'return res': '最少删除 `{res}` 个字符',
    },
    cards=dict(
        one_liner='频次重复就保留一种，其余各删一个往下压',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`（k 为字符种类）',
        problem=['字符串 `s` 中，若任意两个字符出现次数都不同，称为「优质字符串」',
                 '每次可以删除一个字符，求使 `s` 优质的最少删除次数',
                 '示例：`aaabbbcc` → `2`'],
        quote='对于出现统一频次的字符而言，最好的做法就是保留一种字符不动，其他的字符出现次数全部减一。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计每种字符的频次，按频次从大到小排序',
              '`now` 是当前频次，`mul` 是频次等于 `now` 的字符种数',
              '`mul > 1`：删去 `mul - 1` 个字符，它们的频次降到 `now - 1`，继续比较',
              '扫完后若 `mul` 还大于 1，要继续往下压，直到 `now` 为 0'],
        summary=['时间 `O(n + k log k)`，空间 `O(k)`',
                 '易错：扫完 `cnt_list` 后还要处理剩余的 `mul`，`now` 降到 0 就不能再删了',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '常见更短写法：从高到低遍历，已用频次放进集合，撞了就减一'],
    ),
)
