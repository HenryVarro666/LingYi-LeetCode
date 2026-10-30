import itertools as _it


def _runs(s):
    out, i = [], 0
    for ch, g in _it.groupby(s):
        k = len(list(g))
        out.append((i, i + k - 1, k))
        i += k
    return out


def _color(S, i, v):
    for a, b, k in _runs(S['s']):
        if a <= i <= b and k >= 3:
            return 'orange' if k % 3 == 0 else 'pink' if k % 3 == 1 else 'purple'
    return None


def _flags(S):
    if 'lower_flag' not in S:
        return ''
    lack = [n for n, f in (('小写', S['lower_flag']), ('大写', S['upper_flag']), ('数字', S['digit_flag'])) if f]
    cur = f'，正在看字符 `{S["char"]}`' if 'char' in S and 'cate_loss' not in S else ''
    return f'还缺的种类：=={"、".join(lack) if lack else "无"}=={cur}'


def _calc(S):
    if 'cate_loss' not in S:
        return ''
    s = S['s']
    parts = [f'`len = {len(s)}`', f'`cate_loss = {S["cate_loss"]}`']
    if 'deal3' in S:
        parts.append(f'`deal3 = {S["deal3"]}`')
    if 'del_cnt' in S:
        parts.append(f'`del_cnt = {S["del_cnt"]}`')
    return '，'.join(parts)


CONFIG = dict(
    num=420, title='强密码检验器', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='分三种长度讨论 · 贪心删除',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def strongPasswordChecker(self, s):

        lower_flag = upper_flag = digit_flag = 1
        same_list = []
        now = None
        cnt = 0

        for char in s:
            if char >= 'a' and char <= 'z':
                lower_flag = 0
            elif char >= 'A' and char <= 'Z':
                upper_flag = 0
            elif char >= '0' and char <= '9':
                digit_flag = 0
            
            if now is None or now != char:
                now = char
                if cnt >= 3:
                    same_list.append(cnt)
                cnt = 1
            else:
                cnt += 1

        if cnt >= 3:
            same_list.append(cnt)

        cate_loss = lower_flag + upper_flag + digit_flag
        if len(s) < 6:
            return max(6 - len(s), cate_loss)

        else:
            deal3 = 0
            mod3_cnt = [0, 0, 0]
            for same in same_list:
                deal3 += same // 3
                mod3_cnt[same % 3] += 1
            
            if len(s) <= 20:
                return max(deal3, cate_loss)
            else:
                del_cnt = len(s) - 20
                if del_cnt <= mod3_cnt[0]:
                    return max(deal3 - del_cnt, cate_loss) + len(s) - 20

                del_cnt -= mod3_cnt[0]
                deal3 -= mod3_cnt[0]
                if del_cnt <= mod3_cnt[1] * 2:
                    return max(deal3 - del_cnt // 2, cate_loss) + len(s) - 20

                del_cnt -= mod3_cnt[1] * 2
                deal3 -= mod3_cnt[1]
                return max(deal3 - del_cnt // 3, cate_loss) + len(s) - 20
''',
    call="Solution().strongPasswordChecker('aaaaabbbbbbccccccc12AB')",
    expect=6,
    views=[
        dict(type='text', fn=_flags, size=26),
        dict(type='string', var='s', label='s（橙 = 长度 3m 的连续段，粉 = 3m+1，紫 = 3m+2）', cell=40, color=_color, h=220),
        dict(type='array', var='same_list', label='same_list：长度 ≥ 3 的连续段长度', h=150),
        dict(type='array', var='mod3_cnt', label='mod3_cnt[r]：长度 % 3 = r 的段有几个', h=150,
             color=lambda S, i, v: ('green' if v else None)),
        dict(type='text', fn=_calc, size=26),
    ],
    watch=['cnt', ('cate_loss', 'cate_loss', 'orange'), ('deal3', 'deal3', 'cyan'), ('del_cnt', 'del_cnt', 'pink')],
    skip=['lower_flag = 0', 'upper_flag = 0', 'digit_flag = 0', "if char >= 'a'", 'elif char >=', 'if now is None', 'for char in s'],
    max_steps=80,
    captions={
        'lower_flag = upper_flag': '三个 flag：1 表示==还缺==这一类（小写、大写、数字）',
        'same_list = []': '`same_list` 收集每段长度 ≥ 3 的连续相同字符',
        'now = None': '`now` 是当前这一段的字符，`cnt` 是它连续出现的次数',
        'now = char': '`{char}` 与上一段字符不同 → 开启新的一段：`now = {char}`',
        'if cnt >= 3': lambda S, B, r: (f'上一段长度 `{S.cnt} >= 3` → 记进 `same_list`' if S.cnt >= 3 else f'上一段长度 `{S.cnt} < 3`，没有重复问题，不记'),
        'same_list.append(cnt)': '`same_list = {same_list}`',
        'cnt = 1': '新段计数从 `1` 开始',
        'cnt += 1': '`{char}` 和 `now` 相同 → 连续出现 `{cnt}` 次',
        'cate_loss = ': '缺的种类数 `cate_loss = {lower_flag} + {upper_flag} + {digit_flag} = =={cate_loss}==`：每缺一类至少要一次操作',
        'if len(s) < 6': lambda S, B, r: (f'`len = {len(S.s)} < 6`：太短，补字符就行（补字符时顺便补缺的种类）' if len(S.s) < 6 else f'`len = {len(S.s)} >= 6`：不用补字符，要看重复段和长度上限'),
        'deal3 = 0': '`deal3`：把所有重复段拆开需要替换的次数',
        'mod3_cnt = [0': '`mod3_cnt[r]`：长度除以 3 余 r 的重复段有几个，后面删字符时要按余数分优先级',
        'for same in same_list': lambda S, B, r: (f'处理长度为 `{S.same}` 的重复段' if sum(S.mod3_cnt) < len(S.same_list) else '所有重复段都统计完了'),
        'deal3 += same // 3': '长度 `{same}` 的段每 3 个换 1 个字符 → 需要 `{same} // 3` 次替换，`deal3 = {deal3}`',
        'mod3_cnt[same % 3] += 1': '`{same} % 3 = {same % 3}` → `mod3_cnt = {mod3_cnt}`',
        'if len(s) <= 20': lambda S, B, r: (f'`len = {len(S.s)} <= 20`：长度合格，只要处理重复和缺失种类' if len(S.s) <= 20 else f'`len = {len(S.s)} > 20`：必须删掉 `{len(S.s) - 20}` 个字符，删的时候争取顺带消掉重复'),
        'return max(deal3, cate_loss)': '替换既能拆重复又能补种类 → 取 `max({deal3}, {cate_loss})` = {ret}',
        'del_cnt = len(s) - 20': '至少要删 `del_cnt = {len(s)} - 20 = =={del_cnt}==` 个字符',
        'if del_cnt <= mod3_cnt[0]': lambda S, B, r: (f'`del_cnt = {S.del_cnt} <= mod3_cnt[0] = {S.mod3_cnt[0]}`：长度 3m 的段删 1 个就能少 1 次替换，删得过来' if S.del_cnt <= S.mod3_cnt[0] else f'`del_cnt = {S.del_cnt} > mod3_cnt[0] = {S.mod3_cnt[0]}`：3m 的段不够删，先全用掉，剩下的看 3m+1 的段'),
        'del_cnt -= mod3_cnt[0]': '先把长度 3m 的段各删 1 个 → 剩下 `del_cnt = {del_cnt}`',
        'deal3 -= mod3_cnt[0]': '这些段各省 1 次替换 → `deal3 = {deal3}`',
        'if del_cnt <= mod3_cnt[1] * 2': lambda S, B, r: (f'3m+1 的段删 2 个才省 1 次替换：`del_cnt = {S.del_cnt} <= {S.mod3_cnt[1]} × 2` → 够用' if S.del_cnt <= S.mod3_cnt[1] * 2 else f'`del_cnt = {S.del_cnt} > {S.mod3_cnt[1]} × 2`：3m+1 的段也不够，剩下的只能每 3 个删除省 1 次替换'),
        'return max(deal3 - del_cnt // 2': '删 `{del_cnt}` 个字符省 `{del_cnt} // 2` 次替换：`max({deal3} - {del_cnt // 2}, {cate_loss}) + {len(s) - 20}` = =={ret}==',
        'return max(deal3 - del_cnt // 3': '剩下按每 3 个删除省 1 次替换：`max({deal3} - {del_cnt // 3}, {cate_loss}) + {len(s) - 20}` = =={ret}==',
        'return max(deal3 - del_cnt,': '`max({deal3} - {del_cnt}, {cate_loss}) + {len(s) - 20}` = =={ret}==：删除次数必须算上',
    },
    cards=dict(
        one_liner='先看长度：太短补、合格换、太长先删，删的时候顺带拆掉重复段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['强密码：长度 6~20，含小写、大写、数字各至少 1 个，且不能有连续 3 个相同字符',
                 '每步可以插入、删除或替换一个字符，求把 `s` 变成强密码的最少步数',
                 '本视频：`s = "aaaaabbbbbbccccccc12AB"`（长 22，有 3 段重复）'],
        quote='题目难度其实不大，就是细节需要想清楚。首先，可以通过一趟扫描确定s中是否有大写字母、小写字母以及数字，同时可以统计出连续出现相同字符3次或以上的子串的长度与数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描得到：缺哪几类（`cate_loss`）和每段重复的长度（`same_list`）',
              '长度 < 6：补字符，答案 `max(6 - l, cate_loss)`；6~20：只用替换，`max(deal3, cate_loss)`',
              '长度 > 20：必须删 `l - 20` 个；==余 0 的段删 1 个、余 1 的删 2 个、余 2 的删 3 个==各省一次替换，按这个顺序删'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：删除的次数一定要加到答案里：`+ l - 20`',
                 '易错：`max(…, cate_loss)`，替换既拆重复又补种类，不能相加',
                 '原文为 Python 2 写法，其中的 `/` 是整数除法，已改为 `//`（`same / 3`、`del_cnt / 2`、`del_cnt / 3`），并删去了 `:type` 文档字符串'],
    ),
)
