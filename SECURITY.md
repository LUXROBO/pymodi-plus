# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in pymodi-plus, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email:

- **Email**: module.dev@luxrobo.com
- **Subject**: [SECURITY] Brief description of the vulnerability

### What to Include

Please include the following information in your report:

1. **Description**: A clear description of the vulnerability
2. **Impact**: What can be exploited and the potential impact
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Proof of Concept**: If possible, include code or commands that demonstrate the vulnerability
5. **Suggested Fix**: If you have ideas for how to fix it, please share them
6. **Environment**: Python version, OS, pymodi-plus version

### Example Report

```
Subject: [SECURITY] Command injection in BLE module

Description:
Found a command injection vulnerability in the Bluetooth connection module
that allows execution of arbitrary system commands.

Impact:
An attacker with local access could execute arbitrary commands with sudo
privileges through malicious file paths.

Steps to Reproduce:
1. Create a directory with semicolons in the name
2. Symlink the BLE module directory to this malicious path
3. Import pymodi_plus and initialize BLE connection
4. Arbitrary commands in the path will be executed

Suggested Fix:
Replace os.system() calls with subprocess.run() using argument lists
instead of shell command strings.

Environment:
- Python 3.9
- Raspberry Pi OS
- pymodi-plus 0.3.1
```

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Target**: Within 30 days for critical issues, 90 days for others

### What Happens Next

1. **Acknowledgment**: We'll acknowledge receipt of your report within 48 hours
2. **Investigation**: We'll investigate and validate the issue
3. **Fix Development**: We'll develop and test a fix
4. **Coordinated Disclosure**: We'll work with you on timing of public disclosure
5. **Credit**: With your permission, we'll credit you in the security advisory

## Security Best Practices for Users

### Installation

Always install from the official PyPI repository:

```bash
pip install pymodi-plus
```

Verify the package authenticity:

```bash
pip show pymodi-plus
# Check: Author: LUXROBO
# Check: Home-page: https://github.com/LUXROBO/pymodi-plus
```

### Running Examples

The example scripts in this repository are intended for educational purposes:

- Review example code before running
- Don't run examples from untrusted sources
- Be cautious with examples that require sudo privileges

### Hardware Communication

When using pymodi-plus to control hardware:

- Only connect trusted MODI+ modules
- Keep your system updated
- Use the principle of least privilege (avoid running as root when possible)
- Monitor for unexpected behavior

### Raspberry Pi Users

If using Bluetooth (BLE) functionality on Raspberry Pi:

- The library requires sudo access for Bluetooth configuration
- Ensure your system is up to date: `sudo apt update && sudo apt upgrade`
- Review the BLE task code if you have security concerns
- Consider using USB connection instead of BLE if sudo access is a concern

## Known Security Considerations

### Bluetooth Low Energy (BLE)

The BLE implementation requires elevated privileges (sudo) on Linux systems to:
- Configure Bluetooth adapter intervals
- Reset the Bluetooth adapter
- Scan for and connect to devices

This is a requirement of the underlying Linux Bluetooth stack. We use subprocess with validated arguments to minimize risks.

### Tutorial Mode

The tutorial mode is designed for educational purposes in trusted environments. It validates user input to ensure it matches expected commands.

## Security Updates

Security updates will be released as:
- **Critical**: Immediate patch release (e.g., 0.3.1 → 0.3.2)
- **High**: Patch release within 30 days
- **Medium**: Minor version update
- **Low**: Next minor/major release

Security advisories will be published:
1. GitHub Security Advisories
2. PyPI project page
3. Release notes (HISTORY.md)

## Recognition

We appreciate security researchers who help keep pymodi-plus secure. With your permission, we will:

- Credit you in the security advisory
- Add your name to our CONTRIBUTORS.md file
- Publicly thank you in release notes

## Security Hall of Fame

Contributors who have responsibly disclosed security issues:

<!-- Security researchers will be listed here -->

*Be the first to help secure pymodi-plus!*

## Contact

For security concerns:
- **Email**: module.dev@luxrobo.com
- **GitHub**: https://github.com/LUXROBO/pymodi-plus

For general questions (non-security):
- **Issues**: https://github.com/LUXROBO/pymodi-plus/issues

---

**Last Updated**: 2025-10-27

Thank you for helping keep pymodi-plus and our users safe! 🔒
