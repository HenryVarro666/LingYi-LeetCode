def _txt(S):
    line = S.get('_line')
    if 'cnt_list' not in S:
        return '像基数排序：从最低位（最后一名）排到最高位（第一名），每一轮只看这一位的票数'
    cl = S['cnt_list']
    if line in (13, 14):
        return '`cnt_list[名次][队伍]`：每个名次上各队得了几票'
    if 'order' in S and line in (22, 23, 24, 25):
        return '`order[队伍]` = 当前排位（0 最前）；每轮用「这一位的票数多 → 前，同票则保持上一轮顺序」重排'
    return '`cnt_list[名次]` = 该名次上各队的得票'


CONFIG = dict(
    num=1366, title='通过投票对团队排名', difficulty='Medium', category='字符串',
    author='yiduobo', technique='基数排序 · 从低位名次到高位名次',
    tags=[],
    code='''
class Solution(object):
    def rankTeams(self, votes):

        n = len(votes)
        l = len(votes[0])
        char_set = set(list(votes[0]))
        cnt_list = [{} for _ in range(l)]
        for vote in votes:
            for index, char in enumerate(vote):
                if char not in cnt_list[index]:
                    cnt_list[index][char] = 0
                cnt_list[index][char] += 1
        
        order = {}
        cnt = 0
        for asc in range(26):
            char = chr(asc + 65)
            if char in char_set:
                order[char] = cnt
                cnt += 1

        for index in range(l - 1, -1, -1):
            order = {x: index for index, x in enumerate(sorted(order.keys(), key=lambda d:(-cnt_list[index].get(d, 0), order[d])))}

        return ''.join([x[0] for x in sorted(order.items(), key=lambda d:d[1])])
''',
    call="Solution().rankTeams(['ABC', 'ACB', 'ABC', 'ACB', 'ACB'])",
    expect='ACB',
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='cnt_list', label='cnt_list[名次]：该名次上各队的得票（行 = 第 1、2、3 名）', h=150,
             fmt=lambda *a: '', ) if False else dict(type='map', var=lambda S: {f'第{i + 1}名': d for i, d in enumerate(S.get('cnt_list', []))},
                                                    label='cnt_list：每个名次上各队得几票', fmt=lambda k, v: f'{k}: {v}', h=210),
        dict(type='map', var='order', label='order：队伍 → 当前排位（0 = 最前）', fmt=lambda k, v: f'{k} → {v}', h=130),
    ],
    skip=['for asc in range(26)', 'char = chr(', 'if char in char_set', 'cnt += 1'],
    max_steps=80,
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink'), ('cnt', 'cnt', 'yellow')],
    captions={
        'n = len(votes)': '`n = {n}` 张票',
        'l = len(votes[0])': '每张票排 `l = {l}` 位：要处理 `l` 个名次',
        'char_set = ': '参赛队伍集合 `{sorted(char_set)}`',
        'cnt_list = [{}': '每个名次一个字典：`队伍 → 得票数`',
        'for vote in votes': lambda S, B, r: ('所有票统计完' if 'vote' in B and sum(sum(d.values()) for d in S.cnt_list) == len(S.votes) * S.l
                                              else f'读第 {sum(sum(d.values()) for d in S.cnt_list) // S.l + 1} 张票 `{S.vote}`'),
        'if char not in cnt_list[index]': lambda S, B, r: ('`{}` 在第 {} 名还没有记录 → 先记 0'.format(S.char, S.index + 1) if S.char not in S.cnt_list[S.index]
                                                           else '`{}` 在第 {} 名已有记录'.format(S.char, S.index + 1)),
        'cnt_list[index][char] = 0': '初始化 `cnt_list[{index}][{char!r}] = 0`',
        'cnt_list[index][char] += 1': '`{char}` 排第 `{index + 1}` 名多一票 → `{cnt_list[index][char]}`',
        'order = {}': '`order` 记录每支队伍当前的排位',
        'cnt = 0': '`cnt` 从 0 开始给队伍编号',
        'for asc in range(26)': '按 ASCII 顺序枚举 A–Z，保证初始排位是字母序',
        'char = chr(': '字母 `{char}`',
        'if char in char_set': lambda S, B, r: ('`{}` 参赛 → 加入'.format(S.char) if S.char in S.char_set else '`{}` 没参赛，跳过'.format(S.char)),
        'order[char] = cnt': '`order[{char!r}] = {cnt}`：初始排位就是字母序（全平局时按字母排）',
        'cnt += 1': '下一个排位 `cnt` = {cnt}',
        'for index in range(l - 1, -1, -1)': lambda S, B, r: ('所有名次都排完了：最后排的第 1 名票数优先级最高，`order` 就是最终排名' if S.index == 0 and B.get('index') == 0
                                                             else f'从最低位开始：现在按第 `{S.index + 1}` 名的票数重排'),
        'order = {x: index': lambda S, B, r: ('第 {} 名票数 `{}`：==票多的在前==，票数相同的沿用上一轮顺序 → `order = {}`'.format(
            S.index + 1, S.cnt_list[S.index], S.order)),
        'return': '`order` 按排位排序后取队伍名 → =={ret}==',
    },
    cards=dict(
        one_liner='像基数排序：先按最后一名排，最后才按第一名排',
        complexity='时间 `O(n·l + l²·log l)`，空间 `O(l²)`',
        problem=['每张投票把所有队伍从高到低排好；按「第一名票数多者在前」，并列看第二名，以此类推',
                 '完全平局按字母序',
                 '示例：`["ABC","ACB","ABC","ACB","ACB"]` → `"ACB"`'],
        quote='有一种经典的排序方式，名称为基数排序。其做法是先将要排序的数补充到同样的长度，然后从低位开始向高位遍历，逐位进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「各名次票数」看成一个多位数：第一名票数是最高位',
              '先按字母序给初始排位，再从最后一名到第一名逐位重排',
              '每位用 `(-票数, 上一轮排位)` 排序：票多在前，同票沿用上一轮顺序'],
        summary=['时间 `O(n·l + l²·log l)`，空间 `O(l²)`',
                 '易错：必须==从低位到高位==排，最后排的第一名票数才是最高优先级',
                 '同票时用上一轮的 `order[d]` 保持稳定，初始 `order` 是字母序，所以完全平局按字母',
                 '原文偷懒用 `sort` 代替桶排序，代码为 Python 2 风格，但在 Python 3 下无需修改即可运行'],
    ),
)
