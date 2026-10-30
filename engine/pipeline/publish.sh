#!/usr/bin/env bash
# 把 LC_Video 分批推到 GitHub 仓库 LingYi-LeetCode。可以重复运行：已经推过的批次会自动跳过，
# 以后新生成的视频，再运行一次就会作为新的批次推上去。
#
#   bash ~/Documents/LC_Video/engine/pipeline/publish.sh
#   REPO=别的名字 bash ~/Documents/LC_Video/engine/pipeline/publish.sh
#
# 需要：git，并且这台电脑已经能 push 到 GitHub（装了 gh 并 gh auth login，或 git 已保存 GitHub 凭据）。
# 没装 gh 时，先在 https://github.com/new 新建同名的空仓库（Public，不要勾选 README），脚本会提示怎么关联。
# 分批：① 文字和代码（不含视频，约 300 MB）② 分类概念视频 ③ 每个题号区间一批视频（每批约 300 MB），
# 每批单独 push，避开 GitHub 单次 push 2 GB 的上限。
set -euo pipefail
cd "$(cd "$(dirname "$0")/../.." && pwd)"
REPO="${REPO:-LingYi-LeetCode}"
DESC="灵茶山艾府 + yiduobo 两位大神的 LeetCode 题解，配 6000+ 个逐行执行代码的动画讲解视频，按刷题路径串起来"
BUDGET="${BUDGET:-0}"   # >0：运行这么多秒后不再开始新批次（给有时间限制的 shell 用）
START=$(date +%s)

[ -d .git ] || git init -q -b main
git config core.quotepath false
git config core.precomposeunicode true
git config http.postBuffer 524288000

# 用 gh 登录过的话，让 git push 也用这份登录凭据
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then gh auth setup-git >/dev/null 2>&1 || true; fi
if ! git config user.name >/dev/null; then
  echo "请先设置提交者名字和邮箱：git config --global user.name \"你的名字\"; git config --global user.email \"你的邮箱\""; exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    OWNER=$(gh api user -q .login)
    gh repo view "$OWNER/$REPO" >/dev/null 2>&1 || gh repo create "$REPO" --public --description "$DESC"
    git remote add origin "https://github.com/$OWNER/$REPO.git"
  else
    echo "还没关联 GitHub 仓库。请先在 https://github.com/new 新建空仓库 $REPO（Public，不要勾选 README），然后运行："
    echo "  git -C \"$PWD\" remote add origin https://github.com/<你的用户名>/$REPO.git"
    echo "再重新运行本脚本。"
    exit 1
  fi
fi

ahead() {  # 本地比远端多几个提交
  if git rev-parse -q --verify refs/remotes/origin/main >/dev/null; then
    git rev-list --count origin/main..main
  else
    git rev-list --count main 2>/dev/null || echo 0
  fi
}
push() { git push -u origin main 2>&1 | tail -1; }
batch() {  # batch "提交说明" pathspec...
  local msg="$1"; shift
  git add -A -- "$@"
  if ! git diff --cached --quiet; then
    git commit -q -m "$msg"
    echo "提交：$msg（$(git show --stat --format= HEAD | tail -1)）"
  fi
  if [ "$(ahead)" != "0" ]; then push; fi
}
timeup() { [ "$BUDGET" -gt 0 ] && [ $(( $(date +%s) - START )) -gt "$BUDGET" ]; }

# ① 文字和代码（不含视频）
batch "题解、刷题路径、学习笔记、引擎与配置（不含视频）" . ':(exclude)*.mp4'
# ② 分类概念视频
batch "分类概念视频" 分类概念视频
# ③ 每个题号区间一批视频
for d in 题解/*/; do
  if timeup; then echo "到时间了，剩下的下次再推（再运行一次本脚本即可）"; exit 0; fi
  b="${d%/}"
  [ "$b" = "题解/_assets" ] && continue
  batch "视频：${b#题解/}" "$b"
done
# 收尾：README、索引等后来又更新过的文字
batch "更新索引与 README" . ':(exclude)*.mp4'
echo "全部推送完成：$(git remote get-url origin)"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh repo edit --add-topic leetcode,algorithms,python,visualization,animation,leetcode-solutions >/dev/null 2>&1 || true
fi
