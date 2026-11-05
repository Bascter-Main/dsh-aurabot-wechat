# dsh-aurabot-wechat

Native Agent WeChat bridge for DSH Aurabot.

This public repository is being initialized to compile and evaluate an **experimental** upstream Agent WeChat v1.5.1 sticker-source hotfix. The current validated DSH bridge remains deployed separately; this repository does **not** contain WeChat login data, account tokens, chat databases, or VPS configuration.

## Sticker hotfix build

The `build/sticker-hotfix-v1.5.1` branch contains:

- `native-hotfix/sticker-hosts-v1.5.1.patch` — targeted Rust allowlist change for candidate Tencent sticker CDN hostnames and opt-in hostname-only diagnostics.
- `.github/workflows/build-agent-wechat-sticker-hotfix.yml` — checks out the exact upstream `v1.5.1` tag, applies the patch, runs Rust tests, builds a Linux x86_64 GNU `wx` executable, and uploads the binary and SHA-256 digest as a workflow artifact.

**Live diagnostic:** a failing dynamic store sticker identified the exact source host `snsvideo.hk.wechat.com` on 2026-11-06. The patch now allowlists this exact hostname. The NEW binary and real animated sticker download have not yet passed acceptance. Never replace a working native binary without backing up the existing daemon configuration and checking account/server identity after restart. The patch does not disable DNS/public-IP checks, redirect restrictions or source-length/MD5 integrity checks.

**Build compatibility:** Debian 12 with GLIBC 2.36; the workflow runs `wx --json version`, checks GLIBC symbols, runs sticker URL tests, and uploads an artifact with an `-hk-UNVERIFIED` suffix. The previous artifact without the `-hk` suffix must not be mistaken for the updated build.

Agent WeChat upstream: https://github.com/thisnick/agent-wechat

## Acknowledgments

The DSH bridge integrates independent native WeChat functionality with an Aurabot personality system. Refer to upstream projects for their respective licenses.
