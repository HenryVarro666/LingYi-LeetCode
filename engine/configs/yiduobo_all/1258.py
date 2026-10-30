CONFIG = dict(
    num=1258, title='近义词句子', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集分组 + 回溯',
    tags=[],
    code='''
class Solution(object):
    def generateSentences(self, synonyms, text):

        word_mapping = {}
        cnt = 0
        for x, y in synonyms:
            if x not in word_mapping:
                word_mapping[x] = cnt
                cnt += 1

            if y not in word_mapping:
                word_mapping[y] = cnt
                cnt += 1

        fa = list(range(cnt))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y in synonyms:
            x_id = word_mapping[x]
            y_id = word_mapping[y]

            fa_x = find(x_id)
            fa_y = find(y_id)

            if fa_x != fa_y:
                fa[fa_x] = fa_y

        syn_dict = {}
        for word in word_mapping:
            fa_word = find(word_mapping[word])
            if fa_word not in syn_dict:
                syn_dict[fa_word] = []
            syn_dict[fa_word].append(word)

        for fa_word in syn_dict:
            syn_dict[fa_word].sort()

        res = []
        word_list = text.split(' ')
        n = len(word_list)

        def dfs(level, now):
            if level == n:
                res.append(' '.join(now))
                return

            if word_list[level] in word_mapping:
                fa_word = find(word_mapping[word_list[level]])
                for syn_word in syn_dict[fa_word]:
                    now.append(syn_word)
                    dfs(level + 1, now)
                    now.pop()
            else:
                now.append(word_list[level])
                dfs(level + 1, now)
                now.pop()

        dfs(0, [])
        return res
''',
    call="Solution().generateSentences([['happy','joy'],['joy','cheerful']], 'I am happy')",
    expect=['I am cheerful', 'I am happy', 'I am joy'],
    views=[
        dict(type='map', var='word_mapping', label='word_mapping（单词 → id）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=24),
        dict(type='array', var='fa', label='fa（并查集父节点）', cell=70, h=150),
        dict(type='map', var='syn_dict', label='syn_dict（根 → 同组单词）', fmt=lambda k, v: f'{k}: {v}', h=150, font=24),
        dict(type='array', var='word_list', label='word_list（level = 当前位置）', cell=110, h=150, color=lambda S, i, v: 'yellow' if i == S.get('level') else None),
        dict(type='calls', h=120, hide=('now',)),
        dict(type='text', h=70, size=26, fn=lambda S: ('now = ' + ' '.join(S['_inner']['now']) if 'now' in S.get('_inner', {}) else '') + ('   |   res = ' + str(S['res']) if 'res' in S and S['res'] else '')),
    ],
    watch=['cnt', 'level', ('now', 'now', 'cyan'), ('n', 'n', 'green')],
    captions={
        'word_mapping = {}': '第一步：给 synonyms 里出现的每个单词编号',
        'for x, y in synonyms:': lambda S, B, r: (f'取下一对近义词 `{S.x}`、`{S.y}`' if 'x' in S else '近义词对读完'),
        'if x not in word_mapping': '`{x}` 没编号？{"没有，要新建" if x not in word_mapping else "已有编号"}',
        'if y not in word_mapping': '`{y}` 没编号？{"没有，要新建" if y not in word_mapping else "已有编号"}',
        'word_mapping[x] = cnt': '`{x}` 的编号是 `{cnt}`',
        'word_mapping[y] = cnt': '`{y}` 的编号是 `{cnt}`',
        'fa = list(range(cnt))': '共 `{cnt}` 个单词，并查集初始：每个都是自己的根',
        'x_id = word_mapping[x]': '`{x}` → id `{x_id}`',
        'y_id = word_mapping[y]': '`{y}` → id `{y_id}`',
        'fa_x = find(x_id)': '`find({x_id})` 找 x 的根',
        'fa_y = find(y_id)': '`find({y_id})` 找 y 的根',
        'if fa_x != fa_y': '根 `{fa_x}` 和 `{fa_y}`：{"不同 → 合并" if fa_x != fa_y else "相同 → 已是一组"}',
        'fa[fa_x] = fa_y': '近义词可传递，把两组合成一组：`fa[{fa_x}] = {fa_y}`',
        'for word in word_mapping': '第二步：把单词按根分组，当前单词 `{word}`',
        'fa_word = find(word_mapping[word])': '`{word}` 所在组的根是 `{fa_word}`',
        'if fa_word not in syn_dict': '这个根还没有组？{"是，先建空列表" if fa_word not in syn_dict else "已有，直接加入"}',
        'syn_dict[fa_word] = []': '为根 `{fa_word}` 建一个空组',
        'syn_dict[fa_word].append(word)': '`{word}` 加入根 `{fa_word}` 的组：`{syn_dict[fa_word]}`',
        'for fa_word in syn_dict': '第三步：每组内部排序（字典序），当前组的根是 `{fa_word}`：`{syn_dict[fa_word]}`',
        'syn_dict[fa_word].sort()': '组内排序：`{syn_dict[fa_word]}`',
        'word_list = text.split': '句子拆成单词：`{word_list}`，共 `{n}` 个',
        'if level == n': '`level = {level}`，{"句子每个位置都选好了 → 收集答案" if level == n else "还没选完，继续往后"}',
        'res.append': '得到一句：==`{res[-1]}`==',
        'if word_list[level] in word_mapping': '`{word_list[level]}` {"有近义词 → 逐个尝试同组的词" if word_list[level] in word_mapping else "没有近义词 → 原样保留"}',
        'fa_word = find(word_mapping[word_list[level]])': '`{word_list[level]}` 所在组的根：`{fa_word}`，组内有 `{syn_dict[fa_word]}`',
        'for syn_word in syn_dict[fa_word]': '同组近义词取下一个：`{syn_word}`',
        'now.append(syn_word)': '选 `{syn_word}`：`now = {now}`',
        'now.append(word_list[level])': '原样放入 `{word_list[level]}`：`now = {now}`',
        'dfs(level + 1, now)': '递归进入下一个位置',
        'now.pop()': '回溯：撤销刚才的选择，`now = {now}`',
        'dfs(0, [])': '从第 0 个位置、空句子开始搜索',
        'return res': '一共 `{len(res)}` 个句子，已按字典序',
    },
    skip=['return fa[x]', 'cnt += 1', 'if fa[x] != x', 'cnt = 0', 'res = []', 'n = len', 'syn_dict = {}', 'x_id = word_mapping', 'y_id = word_mapping', 'if fa_word not in syn_dict', 'syn_dict[fa_word].sort()'],
    max_steps=120,
    cards=dict(
        one_liner='先用并查集圈出近义词组，再回溯枚举每个位置的替换',
        complexity='时间 `O(2^n·n)` 量级（结果数指数级），空间 `O(m)`',
        problem=['给近义词对 `synonyms` 和句子 `text`，近义词可传递',
                 '把句子里的词任意替换成同组近义词，生成所有句子',
                 '结果按字典序排序返回',
                 '本视频：happy–joy–cheerful，`I am happy` → 3 句'],
        quote='近义词是可以传递的，比如说happy <-> joy <-> cheerful，在最终替换时也可以用cheerful来替换happy。',
        quote_src='—— yiduobo 题解原文',
        idea=['近义词可传递，要维护连通性 → ==并查集==，单词先编号再合并',
              '遍历所有单词，按根分组并排序，组内顺序就是字典序',
              '搜索回溯：逐个位置向后，有近义词就依次试组内每个词，否则原样放入'],
        summary=['回溯层数 = 句子单词数 `n`，每层分支数 = 组大小，总数是乘积',
                 '易错点：组要按根分，且必须先 `sort`，否则结果不是字典序',
                 '不在 `word_mapping` 里的词没有近义词，原样保留',
                 '`now.append` 与 `now.pop` 成对出现，回溯后要还原现场',
                 '原文为 Python 2 写法，`fa = range(cnt)` 已改为 `list(range(cnt))`'],
    ),
)
