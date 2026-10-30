CONFIG = dict(
    num=1487, title='保证文件名唯一', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表记录已用序号', tags=[],
    code='''
class Solution(object):
    def getFolderNames(self, names):

        name_dict = {}
        res = []
        for name in names:
            tmp = name
            while tmp in name_dict:
                tmp = name + '(' + str(name_dict[name]) + ')'
                name_dict[name] += 1
                
            name = tmp
            name_dict[name] = 1
            res.append(name)
        
        return res
''',
    call="Solution().getFolderNames(['kaido', 'kaido(1)', 'kaido', 'kaido(1)'])",
    expect=['kaido', 'kaido(1)', 'kaido(2)', 'kaido(1)(1)'],
    views=[
        dict(type='array', var='names', label='names（蓝 = 正在处理的这个）', cell=150, h=200, font=26,
             color=lambda S, i, v: 'blue' if 'res' in S and i == len(S['res']) - (1 if S['_line'] == 14 else 0) and S['_line'] != 16 else None),
        dict(type='map', var='name_dict', label='name_dict（名字 → 下一个可用序号）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
        dict(type='array', var='res', label='res（最终文件名）', cell=150, h=200, font=26),
    ],
    watch=['name', 'tmp'],
    captions={
        'name_dict = {}': '`name_dict` 记录每个名字已经用到了哪个序号',
        'res = []': '`res` 保存最终分配的名字',
        'for name in names': lambda S, B, r: ('名字都处理完了' if B.get('name') == S.get('name') and 'name' in B and len(S.res) == len(S.names)
                                              else '取下一个名字 `{}`'.format(S.name)),
        7: '先试试原名 `tmp = {tmp}`',
        'while tmp in name_dict': lambda S, B, r: (f'`{S.tmp}` ==已经用过==（在字典里）→ 要加序号' if S.tmp in S.name_dict
                                                    else f'`{S.tmp}` 没出现过 → 可以用，退出循环'),
        9: '把序号接在 ==整个原名== 后面：`{tmp}`（名字当整体字符串，不拆分）',
        'name_dict[name] += 1': '`{name}` 的序号用掉了，下次从 `{name_dict[name]}` 试起；回去检查 `{tmp}` 是否也被占用',
        'name = tmp': '最终名字确定：`{name}`',
        'name_dict[name] = 1': '新名字 `{name}` 登记进字典，序号从 1 开始',
        'res.append': '`{name}` 加入答案 → `{res}`',
        'return res': '全部分配完毕，返回 `res`',
    },
    cards=dict(
        one_liner='字典记住每个名字用到几号，重名就不断加后缀试',
        complexity='时间 `O(n·k)`（k 为重名次数），空间 `O(n)`',
        problem=['给定文件名列表 `names`，按顺序创建文件夹',
                 '名字已被占用时，加后缀 `(k)`，`k` 是最小的正整数使名字唯一',
                 '本视频：`[kaido, kaido(1), kaido, kaido(1)]`'],
        quote='最后一个样例中的kaido(1)最终被变成了kaido(1)(1)，也就是说这里不能将kaido(1)拆分成kaido和序号1，而是应该直接将kaido(1)视为一个字符串，在后面添加上额外的1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`name_dict[x]` = 字符串 `x` 下一个要试的序号',
              '没出现过：直接用，登记序号 1',
              '出现过：接上 `(序号)`，序号加一，再检查新名字有没有被占，直到不冲突'],
        summary=['均摊时间接近 `O(n)`，空间 `O(n)`',
                 '后缀名本身也要登记进字典，否则后面的 `kaido(1)` 会撞名',
                 '`kaido(1)` 当作整体字符串处理，不能拆分',
                 '循环里最后用 `name = tmp` 改写变量，所以 `name_dict[name] = 1` 登记的是新名字'],
    ),
)
