param()

if ($env:SKIP_AISDLC_SKILLS_ADD -eq '1') { exit 0 }

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  exit 0
}

npx skills add https://github.com/zixun-github/aisdlc --skill "*" --agent claude-code cursor --yes --copy --global
