# Contributing to AWS Projects Repository

Thank you for your interest in contributing to this AWS projects repository! We welcome contributions from developers of all skill levels who want to share practical AWS implementations and real-world scenarios.

## 🚀 Getting Started

### 1. Fork & Clone
- Fork this repository to your GitHub account
- Clone your fork locally:
  ```bash
  git clone https://github.com/YOUR_USERNAME/AWS.git
  cd AWS
  ```

### 2. Set Up Upstream Remote
Configure the original repository as upstream to keep your fork synchronized:
```bash
# Add the original repository as upstream
git remote add upstream https://github.com/ldpacl/AWS.git

# Verify remotes
git remote -v
# Should show:
# origin    https://github.com/YOUR_USERNAME/AWS.git (fetch)
# origin    https://github.com/YOUR_USERNAME/AWS.git (push)
# upstream  https://github.com/ldpacl/AWS.git (fetch)
# upstream  https://github.com/ldpacl/AWS.git (push)

# Keep your fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 3. Find an Issue
Look for issues that match your skill level and interests:

- 🟢 **`good first issue`** - Perfect for newcomers
- 🐛 **`bug`** - Bug fixes needed
- ✨ **`enhancement`** - New features or improvements
- 📚 **`documentation`** - Documentation improvements

### 4. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Contribution Requirements

### **Documentation Standards**
Every implementation **MUST** include a comprehensive README with:

- **Prerequisites**: Required tools, permissions, versions
- **Step-by-step setup instructions**: Clear, numbered steps
- **Configuration details**: Parameter explanations
- **Usage examples**: How to run/deploy the solution
- **Cleanup instructions**: How to remove resources
- **Troubleshooting section**: Common issues and solutions

### **Implementation Standards**

#### **Terraform Code**
- **MUST** be formatted using `terraform fmt`
- Run before committing:
  ```bash
  terraform fmt -recursive
  ```
- Include `variables.tf`, `main.tf`, and `terraform.tfvars.example`
- Add meaningful variable descriptions and default values

#### **Python Code**
- Follow PEP8 standards
- Include requirements or dependencies clearly
- Add error handling and meaningful comments
- Use boto3 best practices

#### **AWS CLI Scripts**
- Include all necessary commands in sequence
- Add comments explaining each step
- Handle common error scenarios
- Provide verification commands

#### **CloudFormation Templates**
- Use clear parameter descriptions
- Include template validation steps
- Provide parameter examples
- Add outputs for key resources

### 📸 **Proof of Implementation**
**REQUIRED**: Provide evidence of successful implementation and attach to your PR or issue

- **Screenshots**: Key AWS console views showing resources created
- **Terminal output**: Command execution results  
- **Video walkthrough**: For complex implementations (optional but encouraged)
- **Testing results**: Evidence that the solution works as intended

**Important**: All screenshots and videos must be **attached directly to your Pull Request or GitHub issue**. Do not store them in the repository to keep the repo size manageable.

## Content Guidelines

### **Real-World Scenarios**
- Create practical, business-relevant use cases
- Explain the problem being solved
- Describe the benefits and outcomes
- Any industry or use case is welcome (e-commerce, healthcare, fintech, etc.)

### **Project Structure**
When adding a new AWS service, follow this structure:
```
aws_[service_name]/
├── README.md                    # Service overview
├── awscli/
│   ├── README.md               # CLI implementation guide
│   └── [scripts/configs]
├── python/
│   ├── README.md               # Python implementation guide
│   ├── requirements.txt
│   └── [python files]
├── cloudformation/
│   ├── README.md               # CloudFormation guide
│   └── [template files]
├── terraform/
│   ├── README.md               # Terraform guide
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars.example
└── diagrams/
    └── [architecture diagrams]
```

## Submission Process

### 1. **Before Submitting**
- [ ] All code is properly formatted (especially `terraform fmt`)
- [ ] README files are complete with step-by-step instructions
- [ ] Screenshots/videos of successful implementation included
- [ ] All files follow the project structure
- [ ] Test your implementation on a clean AWS account if possible

### 2. **Create Pull Request**
- Write a clear title and description
- Reference the issue you're addressing: `Fixes #123`
- Include:
  - What you implemented
  - How to test it
  - Any special considerations
  - Screenshots in the PR description

### 3. **PR Review Process**
- Reviews typically completed within **1-2 days**
- Address any feedback promptly
- Maintainers may request changes or additional documentation

## Reporting Issues

### Bug Reports
Include:
- AWS service and implementation type
- Steps to reproduce
- Expected vs actual behavior
- Environment details (AWS region, tool versions)
- Error messages and logs

### Feature Requests
Include:
- AWS service or improvement idea
- Real-world use case
- Proposed implementation approach
- Any relevant examples or references

## Contribution Ideas

### **High Priority**
- New AWS services (EC2, RDS, Lambda, API Gateway, etc.)
- Enhanced security implementations
- Multi-service integrated scenarios
- Cost optimization examples

### **Always Welcome**
- Bug fixes and improvements
- Documentation enhancements
- Additional implementation approaches
- Architecture diagram improvements
- Testing and validation scripts

## Communication

- **Questions and discussions**: Use GitHub Issues only
- **Report bugs**: Create a new issue with the `bug` label
- **Suggest features**: Create an issue with the `enhancement` label

## 🏆 Recognition

Contributors will be:
- Listed in repository acknowledgments
- Credited in relevant documentation
- Welcomed to join as collaborators for significant contributions

---

## Quick Checklist for Contributors

- [ ] Forked and cloned the repository
- [ ] Created a feature branch
- [ ] Found and referenced an existing issue
- [ ] Implemented solution with proper documentation
- [ ] Formatted code (especially Terraform)
- [ ] Included screenshots/videos of working implementation
- [ ] Tested on clean environment
- [ ] Created clear, descriptive pull request

**Thank you for contributing to the AWS community! 🌟**

Every contribution helps developers worldwide learn and implement AWS solutions more effectively.

Please also review our **[Code of Conduct](CODE_OF_CONDUCT.md)** to ensure a positive experience for all contributors.
