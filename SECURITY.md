# 🔒 Security Policy

## 📋 Supported Versions

We actively maintain and provide security updates for the following:

| Component | Version | Status |
|-----------|---------|--------|
| ASUSTOR Package | 4.x.x (latest) | ✅ Supported |
| ASUSTOR Package | < 4.0 | ❌ Not supported |
| Build System | Current | ✅ Supported |
| Scripts & Utilities | Current | ✅ Supported |

---

## 🚨 Reporting Security Vulnerabilities

### For ASUSTOR Package Issues

If you discover a security vulnerability in this package (scripts, configurations, or build system), please report it responsibly:

#### 🔐 Private Disclosure (Preferred)

- Use [GitHub Security Advisory](https://github.com/JigSawFr/asustor-runtipi/security/advisories/new)
- Use GitHub's private vulnerability reporting feature
- Include detailed information about the vulnerability

#### 📧 Direct Contact

- Create a private issue or contact maintainers directly
- **Do NOT create public issues for security vulnerabilities**

### For Runtipi Core Issues

If you find a security issue in Runtipi itself (not the ASUSTOR package):

1. **Report to Upstream**: Contact the [Runtipi security team](https://github.com/runtipi/runtipi/security)
2. **Notify Us**: Let us know so we can coordinate updates
3. **Follow Responsible Disclosure**: Allow time for fixes before public disclosure

---

## 🛡️ Security Measures

### Repository Security

- 🔒 **Automated Dependency Updates**: Dependabot monitors and updates dependencies
- ✅ **CI/CD Validation**: All changes undergo automated checks
- 🔍 **Code Scanning**: CodeQL scans for vulnerabilities in Python code
- 📝 **Audit Trail**: All changes are tracked and reviewed

### Package Security

- 🐚 **POSIX Compliance**: Scripts use `/bin/sh` for maximum compatibility and security
- 📊 **Unified Logging**: All operations are logged for audit purposes
- 💾 **Automatic Backups**: Pre-upgrade backups prevent data loss
- 🔐 **Permission Checks**: Scripts validate permissions before operations

### Infrastructure Security

- 🤖 **Automated Workflows**: GitHub Actions with restricted permissions
- 🔑 **Secret Management**: Proper handling of sensitive information
- 🔄 **Regular Updates**: Frequent security updates via automation

---

## 🚀 Security Best Practices

### For Users

When using this package:

- 🔄 **Keep Updated**: Update to the latest package version regularly
- 🔒 **Use Strong Passwords**: Set secure passwords for Runtipi dashboard
- 🌐 **Network Security**: Use HTTPS with valid certificates (Cloudflare DNS recommended)
- 💾 **Regular Backups**: Use the backup scripts regularly
- 🔍 **Monitor Logs**: Check `/share/Docker/RunTipi/logs/` for suspicious activity

### For Contributors

When contributing to this repository:

- ✅ **Test Scripts**: Test all shell scripts on ADM before submitting
- 🐚 **POSIX Compliance**: Use `/bin/sh` syntax, not bash-specific features
- 🔍 **Review Dependencies**: Check for known vulnerabilities
- 📝 **Document Changes**: Clearly document security-relevant changes

---

## 🎯 Security Scope

### What We Secure

- ✅ **Package Scripts**: Installation, uninstallation, and management scripts
- ✅ **Build System**: Python build tools and configuration
- ✅ **Utility Scripts**: Backup, restore, status, and helper scripts
- ✅ **CI/CD Pipelines**: GitHub Actions workflows

### What We Don't Control

- ❌ **Runtipi Application**: Security of Runtipi itself (report to upstream)
- ❌ **Docker Images**: Security of pulled container images
- ❌ **Third-party Apps**: Apps installed via Runtipi app stores
- ❌ **User Configurations**: Custom configurations and modifications
- ❌ **Network Infrastructure**: User's network and NAS security

---

## 🔧 Vulnerability Response Process

### 1. Initial Response (24-48 hours)

- Acknowledge receipt of vulnerability report
- Assign severity level and priority
- Begin initial assessment

### 2. Investigation (1-7 days)

- Reproduce and validate the vulnerability
- Assess impact and affected components
- Develop remediation plan

### 3. Resolution (Varies by severity)

| Severity | Timeline |
|----------|----------|
| 🔴 Critical | Immediate fix and release |
| 🟠 High | Fix within 7 days |
| 🟡 Medium | Fix within 30 days |
| 🟢 Low | Fix in next regular release |

### 4. Disclosure

- Coordinate with reporter on disclosure timeline
- Publish security advisory if applicable
- Update documentation and guidance

---

## 🔗 Security Resources

### External Resources

- [Runtipi Security](https://github.com/runtipi/runtipi/security): Platform security
- [ASUSTOR Security](https://www.asustor.com/security): NAS security advisories
- [Docker Security](https://docs.docker.com/engine/security/): Container security best practices

### Internal Documentation

- [Contributing Guidelines](CONTRIBUTING.md): Security considerations for contributors
- [Developer Guide](DEVELOPER.md): Build and development security

---

## 📞 Contact Information

### Security Team

- 🔐 **GitHub Security Advisories**: [Create Advisory](https://github.com/JigSawFr/asustor-runtipi/security/advisories/new)
- 💬 **Discord**: [#asustor Channel](https://discord.gg/xPtEFWEcjT)
- 🐛 **Issues**: [GitHub Issues](https://github.com/JigSawFr/asustor-runtipi/issues) (for non-sensitive matters)

### Response Time Expectations

| Type | Response Time |
|------|---------------|
| 🔴 Critical Vulnerabilities | Within 24 hours |
| 🟠 High Severity | Within 48 hours |
| 🟡 Medium/Low Severity | Within 7 days |
| ❓ General Security Questions | Within 14 days |

---

## 🙏 Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who help improve our security posture. Your contributions help keep the self-hosting community safe.

Thank you for helping keep asustor-runtipi secure! 🛡️

---

*Last updated: November 2025*
