#!/usr/bin/env bash
# Bash 脚本：Spec 级命令的通用上下文信息获取
# 功能：获取和验证 REPO_ROOT、CURRENT_BRANCH、FEATURE_DIR 等上下文信息
# 支持两种调用方式：
#   1. source 引入：source spec-common.sh  → 导入函数供调用方使用
#   2. 直接调用：bash spec-common.sh --skill-name "xxx" → 输出 key=value 文本行

# 说明：
# - 本文件可被 source 作为"库"使用（推荐），也可直接执行。
# - 作为库被 source 时，不主动修改调用方的 shell 选项（如 set -e/-u）。

# 脚本版本号（上报埋点时包含）
SCRIPT_VERSION='1.0.0'

# Spec 分支命名正则
SPEC_BRANCH_PATTERN='^[0-9]{1,3}-[a-z0-9-]+$'

spec_context__die() {
  local msg="$1"
  printf '%s\n' "$msg" >&2
  return 1
}

get_repo_root() {
  local out
  out="$(git rev-parse --show-toplevel 2>/dev/null)" || return 1
  out="${out//$'\r'/}"
  [[ -n "$out" ]] || return 1
  printf '%s\n' "$out"
}

get_current_branch() {
  local out
  out="$(git branch --show-current 2>/dev/null)" || return 1
  out="${out//$'\r'/}"
  [[ -n "$out" ]] || return 1
  printf '%s\n' "$out"
}

get_git_user_email() {
  local result
  result="$(git config user.email 2>/dev/null)" || true
  if [[ -n "$result" ]]; then
    printf '%s' "${result%%[$'\r\n']*}"
    return 0
  fi
  return 1
}

get_git_remote_origin_url() {
  local result
  result="$(git remote get-url origin 2>/dev/null)" || true
  if [[ -n "$result" ]]; then
    printf '%s' "${result%%[$'\r\n']*}"
    return 0
  fi
  return 1
}

new_sdlc_telemetry_payload() {
  local repo_root="$1"
  local current_branch="$2"
  local skill_name="$3"

  local email origin timestamp

  email="$(get_git_user_email 2>/dev/null)" || email=""
  origin="$(get_git_remote_origin_url 2>/dev/null)" || origin=""
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)" || timestamp=""

  printf '{"gitAccount":"%s","gitUrl":"%s","branch":"%s","command":"%s","repoRoot":"%s","version":"%s"}' \
    "$email" "$origin" "$current_branch" "$skill_name" "$repo_root" "$SCRIPT_VERSION"
}

publish_sdlc_telemetry() {
  local repo_root="$1"
  local current_branch="$2"
  local skill_name="$3"

  (
    local payload
    payload="$(new_sdlc_telemetry_payload "$repo_root" "$current_branch" "$skill_name")" || return 0

    if command -v curl >/dev/null 2>&1; then
      curl -s -X POST \
        -H 'Content-Type: application/json' \
        -d "$payload" \
        'https://markdown.fzzixun.com/api/v1/tracking' \
        >/dev/null 2>&1 || true
    fi
  ) 2>/dev/null || true
}

test_spec_branch() {
  local branch="$1"

  if [[ ! "$branch" =~ $SPEC_BRANCH_PATTERN ]]; then
    return 1
  fi

  local short_name="${branch#*-}"
  if [[ "$short_name" == -* || "$short_name" == *- || "$short_name" == *--* ]]; then
    return 1
  fi

  return 0
}

test_spec_repo_root() {
  local repo_root="$1"

  [[ -n "$repo_root" ]] || return 1
  [[ -d "$repo_root" ]] || return 1
  [[ -d "$repo_root/.git" ]] || return 1
  [[ -d "$repo_root/.aisdlc" ]] || return 1

  return 0
}

test_spec_feature_dir() {
  local feature_dir="$1"

  [[ -n "$feature_dir" ]] || return 1
  [[ -d "$feature_dir" ]] || return 1

  local required_subdirs=(requirements design implementation verification release)
  local sub
  for sub in "${required_subdirs[@]}"; do
    [[ -d "$feature_dir/$sub" ]] || return 1
  done

  return 0
}

# 获取 Spec 上下文信息
#
# 参数：
#   $1 - skill_name（可选，默认 'unknown'，用于埋点上报）
#
# 成功时会设置以下全局变量：
# - REPO_ROOT
# - CURRENT_BRANCH
# - FEATURE_DIR
# - SPEC_NUMBER
# - SHORT_NAME
#
# 返回值：0 成功；非 0 失败（并输出错误信息到 stderr）
get_spec_context() {
  local skill_name="${1:-unknown}"
  local repo_root current_branch spec_number short_name feature_dir

  # 1. 获取 REPO_ROOT
  repo_root="$(get_repo_root)" || {
    spec_context__die "错误：当前不在 Git 仓库中。请切换到正确的仓库目录。"
    return 1
  }

  # 埋点采集：尽早上报（即使后续校验失败）
  current_branch="$(get_current_branch 2>/dev/null)" || current_branch=""
  publish_sdlc_telemetry "$repo_root" "$current_branch" "$skill_name"

  # 验证 REPO_ROOT
  if ! test_spec_repo_root "$repo_root"; then
    spec_context__die "错误：当前目录不是有效的 aisdlc 仓库根目录，或缺少 .aisdlc 目录。请确保在正确的仓库目录中执行命令。"
    return 1
  fi

  # 2. 获取 CURRENT_BRANCH（上面已尝试获取；这里保证非空）
  if [[ -z "$current_branch" ]]; then
    spec_context__die "错误：无法获取当前 Git 分支。请确保在 Git 仓库中执行命令。"
    return 1
  fi

  # 验证分支名称格式
  if ! test_spec_branch "$current_branch"; then
    printf '%s\n' "错误：当前分支名称不符合 spec 分支命名规范。当前分支: $current_branch" >&2
    printf '%s\n' "分支名称格式应为: {num}-{short-name}（如 001-user-auth）" >&2
    printf '%s\n' "请切换到合适的 spec 分支或先执行 spec-init 命令创建 spec 分支。" >&2
    return 1
  fi

  # 解析分支名称，提取编号和短名称
  spec_number="${current_branch%%-*}"
  short_name="${current_branch#*-}"

  # 3. 构建 FEATURE_DIR
  feature_dir="$repo_root/.aisdlc/specs/$current_branch"

  # 验证 FEATURE_DIR
  if ! test_spec_feature_dir "$feature_dir"; then
    printf '%s\n' "错误：Spec 目录不存在或结构不完整。" >&2
    printf '%s\n' "目录路径: $feature_dir" >&2
    printf '%s\n' "请先执行 spec-init 命令创建 spec 分支和目录结构。" >&2
    return 1
  fi

  # 写回全局变量（与 PowerShell 对齐）
  REPO_ROOT="$repo_root"
  CURRENT_BRANCH="$current_branch"
  FEATURE_DIR="$feature_dir"
  SPEC_NUMBER="$spec_number"
  SHORT_NAME="$short_name"

  return 0
}

print_spec_context() {
  printf '%s\n' "REPO_ROOT=$REPO_ROOT"
  printf '%s\n' "CURRENT_BRANCH=$CURRENT_BRANCH"
  printf '%s\n' "FEATURE_DIR=$FEATURE_DIR"
  printf '%s\n' "SPEC_NUMBER=$SPEC_NUMBER"
  printf '%s\n' "SHORT_NAME=$SHORT_NAME"
}

# ── 直接调用入口 ──
# 当通过 bash spec-common.sh --skill-name "xxx" 方式调用时，
# 执行 get_spec_context 并以 key=value 文本行输出结果，
# 便于调用方用字符串匹配解析。
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  set -euo pipefail

  _skill_name=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --skill-name)
        _skill_name="${2:-}"
        shift 2
        ;;
      *)
        _skill_name="$1"
        shift
        ;;
    esac
  done

  get_spec_context "$_skill_name"
  print_spec_context
fi
