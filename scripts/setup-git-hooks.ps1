param(
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-GitRepo {
  $inside = (git rev-parse --is-inside-work-tree 2>$null)
  if ($LASTEXITCODE -ne 0 -or $inside.Trim() -ne 'true') {
    throw '当前目录不是 Git 仓库根目录（请在仓库根目录运行）。'
  }
}

Assert-GitRepo

$hooksDir = '.githooks'
if (-not (Test-Path -LiteralPath $hooksDir -PathType Container)) {
  throw "未找到 $hooksDir 目录。"
}

$current = (git config --get core.hooksPath 2>$null)
if (-not $Force -and $current -and $current.Trim() -ne $hooksDir) {
  throw "core.hooksPath 已设置为 '$($current.Trim())'。如需覆盖请重新运行并加 -Force。"
}

git config core.hooksPath $hooksDir
Write-Host "已启用 Git hooks：core.hooksPath=$hooksDir"
