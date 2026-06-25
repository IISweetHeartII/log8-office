# 보안 정책 / Security Policy

## 지원 버전 / Supported Versions

현재 `main` 브랜치 최신 커밋만 보안 패치를 지원합니다.  
Only the latest commit on the `main` branch receives security fixes.

| Version | Supported |
|---------|-----------|
| main (latest) | ✓ |
| older tags | ✗ |

---

## 취약점 신고 / Reporting a Vulnerability

**공개 이슈로 보안 취약점을 보고하지 마세요.**  
**Do not file security vulnerabilities as public issues.**

GitHub의 비공개 취약점 신고 기능을 사용해주세요:  
Please use GitHub's private vulnerability reporting:

**Security tab → "Report a vulnerability"**  
→ https://github.com/IISweetHeartII/log8-office/security/advisories/new

신고를 검토하는 즉시 개인적으로 연락드립니다.  
We will respond privately as soon as the report is reviewed.

---

## 알려진 보안 설정 / Known Security Settings

이 앱은 두 가지 내장 보안 레이어를 포함합니다:

- **에셋 드로어 비밀번호**: 에셋 관리 패널은 `ASSET_DRAWER_PASS`로 보호됩니다.
- **약한 비밀번호 차단**: 프로덕션 환경에서 기본/단순 비밀번호는 서버 시작 시 거부됩니다.

This app includes two built-in security layers:

- **Asset drawer password**: The asset management panel is protected by `ASSET_DRAWER_PASS`.
- **Weak password blocking**: Default or trivial passwords are rejected at server startup in production.

### 프로덕션 배포 전 필수 설정 / Required before production

`.env.example`을 복사해 `.env`를 만들고 반드시 설정하세요:  
Copy `.env.example` to `.env` and set these before deploying:

```bash
FLASK_SECRET_KEY=<강력한-랜덤-문자열 / strong-random-string>
ASSET_DRAWER_PASS=<강력한-비밀번호 / strong-password>
```

기본값 그대로 프로덕션에서 실행하면 서버가 시작되지 않거나 보호가 무력화됩니다.  
Running production with default values will either prevent server startup or leave the drawer unprotected.
