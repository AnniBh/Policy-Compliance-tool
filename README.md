# Policy Compliance Tool

A comprehensive Windows-based policy compliance assessment and reporting tool designed to help organizations evaluate and maintain compliance with various security policies and standards.

## �� **About**

The Policy Compliance Tool is a Python-based application that automates the process of checking Windows systems for compliance with security policies, industry standards, and organizational requirements. It provides detailed reports and recommendations for achieving and maintaining compliance.

## ✨ **Features**

- **Automated Policy Scanning**: Comprehensive scanning of Windows system configurations
- **Multiple Compliance Frameworks**: Support for various industry standards and regulations
- **Detailed Reporting**: Generate comprehensive compliance reports in multiple formats
- **Real-time Monitoring**: Continuous compliance monitoring capabilities
- **Custom Policy Support**: Ability to define and implement custom compliance policies
- **User-friendly Interface**: Intuitive command-line and GUI options

## 🚀 **Quick Start**

### Prerequisites

- Windows 10/11 or Windows Server 2016+
- Python 3.8 or higher
- Administrative privileges (for system-level policy checks)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AnniBh/Policy-Compliance-tool.git
   cd Policy-Compliance-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the tool**:
   ```bash
   python policy_compliance_tool_windows.py
   ```

## 📋 **Usage**

### Basic Usage

```bash
# Run with default settings
python policy_compliance_tool_windows.py

# Run with specific compliance framework
python policy_compliance_tool_windows.py --framework NIST

# Generate detailed report
python policy_compliance_tool_windows.py --report detailed

# Export results to specific format
python policy_compliance_tool_windows.py --export csv
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--framework` | Specify compliance framework | Auto-detect |
| `--report` | Report detail level (basic/detailed) | basic |
| `--export` | Export format (txt/csv/json/html) | txt |
| `--output` | Output file path | compliance_report.txt |
| `--verbose` | Enable verbose logging | False |
| `--help` | Show help information | - |

## 🔧 **Configuration**

### Policy Frameworks Supported

- **NIST Cybersecurity Framework**
- **ISO 27001**
- **PCI DSS**
- **HIPAA**
- **SOX Compliance**
- **Custom Organizational Policies**

### Configuration Files

The tool uses configuration files to define policy requirements:

```yaml
# config/policies.yaml
frameworks:
  NIST:
    - id: "AC-1"
      title: "Access Control Policy and Procedures"
      description: "Establish, document, and disseminate access control policy"
      checks:
        - type: "registry"
          path: "HKLM\\Software\\Policies\\Microsoft\\Windows\\System"
          value: "EnableSmartScreen"
          expected: 1
```

## 📊 **Output Examples**

### Compliance Summary Report

```
POLICY COMPLIANCE TOOL - COMPLIANCE REPORT
==========================================

Scan Date: 2025-01-24 14:30:00
System: DESKTOP-ABC123
Framework: NIST Cybersecurity Framework

OVERALL COMPLIANCE: 78%

COMPLIANT POLICIES (23/30):
✓ AC-1: Access Control Policy and Procedures
✓ AC-2: Account Management
✓ AC-3: Access Enforcement
...

NON-COMPLIANT POLICIES (7/30):
✗ AC-4: Information Flow Enforcement
✗ AC-5: Separation of Duties
✗ AC-6: Least Privilege
...

RECOMMENDATIONS:
1. Enable Windows Defender SmartScreen
2. Configure password complexity requirements
3. Enable audit logging for security events
```

## 🛠️ **Development**

### Project Structure

```
Policy-Compliance-tool/
├── policy_compliance_tool_windows.py  # Main application
├── config/                            # Configuration files
│   ├── policies.yaml                 # Policy definitions
│   └── settings.yaml                 # Tool settings
├── modules/                          # Core modules
│   ├── scanner.py                   # Policy scanner
│   ├── reporter.py                  # Report generator
│   └── validator.py                 # Policy validator
├── tests/                           # Test suite
├── docs/                            # Documentation
└── requirements.txt                 # Python dependencies
```

### Adding New Policies

1. **Define policy in config/policies.yaml**:
   ```yaml
   - id: "NEW-001"
     title: "New Policy Title"
     description: "Policy description"
     checks:
       - type: "registry"
         path: "HKLM\\Path\\To\\Key"
         value: "ValueName"
         expected: "ExpectedValue"
   ```

2. **Implement custom check logic** in modules/scanner.py
3. **Add tests** in tests/
4. **Update documentation**

## 🧪 **Testing**

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=modules tests/

# Run specific test
python -m pytest tests/test_scanner.py::test_registry_check
```

## 📈 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature/new-feature`
6. Submit a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 **Support**

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/AnniBh/Policy-Compliance-tool/issues)
- **Discussions**: Join community discussions in [GitHub Discussions](https://github.com/AnniBh/Policy-Compliance-tool/discussions)
- **Documentation**: Check our [Wiki](https://github.com/AnniBh/Policy-Compliance-tool/wiki) for detailed guides

## 🙏 **Acknowledgments**

- Windows Security Team for policy guidance
- NIST for cybersecurity framework
- Open source community for tools and libraries
- Contributors and users of this project

---

**Made with ❤️ for better security compliance**

*Last updated: January 2025*
