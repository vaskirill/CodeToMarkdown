# Security Policy

## Supported Versions

We provide security updates for the following versions of Code to Markdown:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **DO NOT** create a public issue

Security vulnerabilities should be reported privately to prevent exploitation.

### 2. Contact Information

Please report security vulnerabilities to:

- **Email**: [security@example.com](mailto:security@example.com)
- **GitHub Security Advisories**: Use the "Report a vulnerability" button on the repository's Security tab

### 3. Information to Include

When reporting a vulnerability, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** assessment
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### 4. Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Resolution**: As quickly as possible (typically within 30 days)

### 5. What to Expect

- We will acknowledge receipt of your report
- We will investigate the vulnerability
- We will provide regular updates on our progress
- We will coordinate the disclosure timeline with you
- We will credit you in our security advisories (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

- Keep the application updated to the latest version
- Only download from official sources
- Verify file integrity when possible
- Be cautious when processing untrusted code repositories
- Review generated markdown files before sharing

### For Developers

- Follow secure coding practices
- Validate all user inputs
- Use secure file handling methods
- Implement proper error handling
- Keep dependencies updated
- Use static analysis tools

## Security Considerations

### File Processing

- The application processes various file types
- Binary files are detected and excluded by default
- File size limits help prevent memory exhaustion
- Path traversal attacks are prevented through proper path validation

### Data Privacy

- No data is sent to external servers
- All processing is done locally
- Generated files remain on your system
- No telemetry or usage data is collected

### Dependencies

- We regularly update dependencies
- Security vulnerabilities in dependencies are addressed promptly
- We use Dependabot for automated dependency updates

## Security Updates

Security updates will be released as:

- **Patch releases** (e.g., 1.2.1) for critical security fixes
- **Minor releases** (e.g., 1.3.0) for security improvements
- **Security advisories** for detailed information about vulnerabilities

## Disclosure Policy

We follow responsible disclosure practices:

1. **Private reporting** of vulnerabilities
2. **Coordinated disclosure** with the reporter
3. **Timely patching** of confirmed vulnerabilities
4. **Public disclosure** after patches are available
5. **Credit attribution** to security researchers

## Security Tools

We use the following tools to maintain security:

- **Static Analysis**: Ruff, mypy
- **Dependency Scanning**: Dependabot
- **Code Review**: All changes require review
- **Automated Testing**: Comprehensive test suite
- **Security Headers**: When applicable

## Contact

For security-related questions or concerns:

- **Email**: [security@example.com](mailto:security@example.com)
- **GitHub**: [Security Advisories](https://github.com/kirill-vasilev/code-to-markdown/security/advisories)

## Acknowledgments

We thank the security researchers who help keep Code to Markdown secure through responsible disclosure.

---

**Note**: This security policy is subject to change. Please check back regularly for updates.
