CONFIG = dict(
    num=1104, title='二叉树寻路', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='按层计数 + 倒推父节点',
    tags=['灵神题单', '链表树与回溯', '难度分 1545'],
    code='''
class Solution(object):
    def pathInZigZagTree(self, label):

        cnt_list = [1]
        while cnt_list[-1] < label:
            cnt_list.append(cnt_list[-1] + cnt_list[-1] + 1)
        
        res = []
        level = len(cnt_list) - 1
        if level % 2 == 0:
            if level == 0:
                pos = 1
            else:
                pos = label - cnt_list[-2] - 1
        else:
            pos = cnt_list[-1] - label

        while level > 0:
            if level % 2 == 0:
                res.append(cnt_list[level - 1] + 1 + pos)
            else:
                res.append(cnt_list[level] - pos)
            level -= 1
            pos //= 2
        
        res.append(1)
        res.reverse()
        return res
''',
    call='Solution().pathInZigZagTree(26)',
    expect=[1, 2, 6, 10, 26],
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (
            ('`cnt_list[k]` = 前 k+1 层的节点总数 = 第 k 层的最大标号（普通编号下）' if 'res' not in S else
             (f"第 {S['level']} 层（{'偶数层：从右往左标号' if S['level'] % 2 == 0 else '奇数层：从左往右标号'}），"
              f"从该层「编号从左数」第 `{S['pos']}` 个往上走" if S.get('level', 0) > 0 else '回到根，反转路径')))),
        dict(type='array', var='cnt_list', label='cnt_list（前 k+1 层节点总数；蓝 = level）', cell=84, h=190,
             pointers={'level': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('level') else None),
        dict(type='array', var='res', label='res（从 label 倒推到根，最后反转）', cell=84, h=190),
    ],
    watch=[('label', 'label', 'yellow'), ('level', 'level', 'blue'), ('pos', 'pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt_list = [1]': '`cnt_list[k]` 记录前 `k+1` 层的节点总数：1、3、7、15……（满二叉树）',
        'while cnt_list[-1] < label': lambda S, B, r: (
            f'`cnt_list[-1] = {S.cnt_list[-1]} < label = {S.label}`：前面这些层还装不下 `label` → 再加一层'
            if S.cnt_list[-1] < S.label else f'`cnt_list[-1] = {S.cnt_list[-1]} >= label = {S.label}`：`label` 就在最后一层'),
        'cnt_list.append': '新一层：总数 = 前总数 × 2 + 1 → `{cnt_list}`',
        'level = len': '`label` 位于最后一层：`level = {level}`（根是第 0 层）',
        10: lambda S, B, r: (
            f'`level = {S.level}` 是偶数层 → 这层标号==从右往左==，要换算成从左数的位置' if S.level % 2 == 0
            else f'`level = {S.level}` 是奇数层 → 这层标号==从左往右==，位置就是 `cnt_list[level] - label`'),
        'pos = label - cnt_list[-2] - 1': '偶数层：本层最小标号是 `cnt_list[-2] + 1`，`pos = label - cnt_list[-2] - 1 = =={pos}==`',
        'pos = cnt_list[-1] - label': '奇数层：`pos = cnt_list[-1] - label = {cnt_list[-1]} - {label} = =={pos}==`',
        'while level > 0': lambda S, B, r: (f'`level = {S.level} > 0`：还没到根，继续往上' if S.level > 0 else '`level = 0`：到根了，结束循环'),
        19: lambda S, B, r: (f'`level = {S.level}` 是偶数层 → 用「前一层总数 + 1 + pos」算标号（偶数层从右往左）' if S.level % 2 == 0
                             else f'`level = {S.level}` 是奇数层 → 用「本层总数 − pos」算标号（奇数层从左往右）'),
        'res.append(cnt_list[level - 1] + 1 + pos)': '偶数层第 `{B.pos}` 个：标号 `cnt_list[{B.level - 1}] + 1 + {B.pos}` = =={res[-1]}== 加入路径',
        'res.append(cnt_list[level] - pos)': '奇数层第 `{B.pos}` 个：标号 `cnt_list[{B.level}] - {B.pos}` = =={res[-1]}== 加入路径',
        'level -= 1': '上一层：`level = {level}`',
        'pos //= 2': '父亲是上一层的第 `pos // 2` 个：`pos = {B.pos} // 2 = =={pos}==`',
        'res.append(1)': '根节点的标号是 `1`',
        'res.reverse()': '路径是从下往上收集的 → 反转成从根到 `label`：`{res}`',
        'return res': '返回路径 `{res}`',
    },
    cards=dict(
        one_liner='先找 label 所在层和位置，再一层层往上找父亲',
        complexity='时间 `O(log label)`，空间 `O(log label)`',
        problem=['无限满二叉树，节点逐行按“之”字形标号：奇数行从左到右，偶数行从右到左',
                 '给出节点标号 `label`，返回从根到它的路径上所有标号',
                 '示例：`label = 14` → `[1,3,4,14]`；本视频：`label = 26` → `[1,2,6,10,26]`'],
        quote='对于第l层第p个节点而言，其父亲节点为第l - 1层的第p / 2个节点，根据这一点我们就可以从label对应的节点开始倒推回root。',
        quote_src='—— yiduobo 题解原文',
        idea=['满二叉树第 k 层有 `2^(k-1)` 个节点，前缀和 1、3、7、15… 就能定位 label 在第几层',
              '算出它是该层“从左数”的第 `pos` 个，父亲就是上一层的第 `pos // 2` 个',
              '偶数层标号反向，换算标号时要分奇偶层处理'],
        summary=['时间、空间都是 `O(log label)`',
                 '易错：偶数层 `pos = label - cnt_list[-2] - 1` 与奇数层公式不同；根要单独处理',
                 '路径是倒推出来的，最后要 `reverse`',
                 '原文为 Python 2 写法，`pos /= 2` 已改为 `pos //= 2`'],
    ),
)
