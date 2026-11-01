CONFIG = dict(
    num=2075, title='解码斜向换位密码', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='沿斜线扫描二维矩阵（Go 原文转写）', tags=[],
    code='''
class Solution:
    def decodeCiphertext(self, encodedText: str, rows: int) -> str:
        ans = []
        i = j = k = 0
        cols = len(encodedText) // rows
        while k < cols:
            ans.append(encodedText[i * cols + j])  # 转换成在 encodedText 上的下标
            i += 1
            j += 1
            if i == rows or j == cols:  # 触及边界
                k += 1
                i, j = 0, k  # 移至下一条斜向
        return ''.join(ans).rstrip(' ')  # 移除末尾多余空格
''',
    call="Solution().decodeCiphertext('ch   ie   pr', 3)",
    expect='cipher',
    views=[
        dict(type='grid', label='二维矩阵（rows × cols，黄 = 当前读取的格子 (i, j)）', cell=96, h=330,
             var=lambda S: [list(S['encodedText'][r * S['cols']:(r + 1) * S['cols']]) for r in range(S['rows'])] if 'cols' in S else None,
             cursors=[('i if i < rows and j < cols else None', 'j', 'yellow')]),
        dict(type='array', var=lambda S: S.get('ans'), label='ans（已读出的字符）', cell=60, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), 'cols'],
    captions={
        'cols = len': '总长 {len(encodedText)}，`cols = len / rows = {cols}`，位置 `(i, j)` 对应 `encodedText[i*cols+j]`',
        'ans.append': '读斜线上的 `(i, j) = ({i}, {j})` → 下标 `{i}*{cols}+{j} = {i*cols+j}`，字符 `{ans[-1]!r}`',
        'i += 1': '向右下走一格：`i` → {i}',
        'j += 1': '`j` → {j}',
        'if i == rows': lambda S, B, r: f"`i = {S.i}`，`j = {S.j}` → " + ('==触及下边界或右边界，这条斜线读完==' if (S.i == S.rows or S.j == S.cols) else '没到边界，继续沿斜线走'),
        'k += 1': '斜线起点右移一列：`k` → {k}',
        'i, j = 0, k': '下一条斜线从第 0 行第 `{k}` 列开始：`i, j = 0, {k}`',
        'while k < cols': lambda S, B, r: (f"`k = {S.k} < cols = {S.cols}`，还有斜线没读" if S.k < S.cols else f"`k = {S.k}` == cols，所有斜线读完"),
        'return': '去掉末尾多余的空格，得到 ==`{ret!r}`==',
    },
    cards=dict(
        one_liner='把一维串还原成矩阵，沿每条斜线从上往下读',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`encodedText` 是矩阵按行拼接的字符串，`originalText` 是沿斜线读出来的',
                 '给定 `encodedText` 和 `rows`，还原 `originalText`（末尾无空格）',
                 '示例：`"ch   ie   pr"`，`rows = 3` → `"cipher"`'],
        quote='题目描述很长，实际上就是传入了一个二维矩阵，让你斜着扫描，返回去掉末尾空格的扫描结果。',
        quote_src='—— 灵茶山艾府题解',
        idea=['列数 `cols = len / rows`，位置 `(i, j)` 就是 `encodedText[i*cols+j]`',
              '`k` 是当前斜线的起点列，`(i, j)` 每次同时 +1',
              '触及下边界或右边界就换到下一条斜线，`i, j = 0, k`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`bytes.TrimRight` → `rstrip(\' \')`）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：`cols` 用整除；只能去掉末尾空格，开头的空格要保留',
                 '`rows = 1` 时每条斜线只有一个字符，结果等于原串'],
    ),
)
