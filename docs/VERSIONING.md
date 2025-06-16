# Versioning and Release Management

This document explains the versioning and release management system for Data Contracts Studio.

## Version Format

We follow [Semantic Versioning (SemVer)](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Current Version

**v0.0.1** (Initial Release)

## Version Files

The following files contain version information and are automatically synchronized:

1. `VERSION` - Single source of truth for the version number
2. `package.json` - Root package version
3. `frontend/package.json` - Frontend application version
4. `backend/app/core/config.py` - Backend API version
5. `backend/app/__version__.py` - Backend Python package version
6. `frontend/src/version.ts` - Frontend version module

## Release Workflow

### 1. Manual Release (Recommended)

```bash
# Create a new release with version bump
make release VERSION=0.0.2

# This will:
# - Run tests and linting
# - Update all version files
# - Create git commit and tag
# - Provide next steps
```

### 2. Quick Version Check

```bash
# Check current version and consistency
make version

# Check version consistency only
./scripts/check-version.sh
```

### 3. Publishing the Release

After running `make release`, follow these steps:

```bash
# Push changes and tags to remote
git push && git push --tags

# The GitHub Actions workflow will automatically:
# - Run tests
# - Build applications
# - Create GitHub release
# - Build Docker images
```

## Release Checklist

Before creating a release:

- [ ] All tests pass (`make test`)
- [ ] Code is properly linted (`make lint`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated with changes
- [ ] Version bump is appropriate (major/minor/patch)
- [ ] Git working directory is clean
- [ ] On main/master branch (recommended)

## Automated Workflows

### GitHub Actions

- **Release Workflow** (`.github/workflows/release.yml`):
  - Triggered on version tags (v*)
  - Runs tests and builds
  - Creates GitHub release
  - Builds Docker images

### Pre-commit Hooks

- Version consistency checking
- Automated testing
- Code formatting

## Version History

### v0.0.1 (2025-06-16)
- Initial release
- Core functionality implemented
- React frontend with TypeScript
- FastAPI backend
- Docker containerization
- Auto-generation features
- Complete development setup

## File Structure

```
├── VERSION                          # Single source of truth
├── package.json                     # Root package version
├── CHANGELOG.md                     # Release notes and history
├── frontend/
│   ├── package.json                 # Frontend version
│   └── src/version.ts               # Frontend version module
├── backend/
│   ├── app/
│   │   ├── __version__.py          # Backend Python version
│   │   └── core/config.py          # Backend API version
├── scripts/
│   ├── release.sh                  # Release automation
│   └── check-version.sh            # Version consistency check
└── .github/workflows/
    └── release.yml                 # Automated release workflow
```

## Best Practices

1. **Always use the release workflow** instead of manually updating versions
2. **Test thoroughly** before releasing
3. **Update CHANGELOG.md** with meaningful release notes
4. **Use descriptive commit messages** following conventional commits
5. **Tag releases** for easy version tracking
6. **Keep versions synchronized** across all components

## Troubleshooting

### Version Inconsistency

If you see version inconsistency errors:

```bash
# Fix by running the release script with the correct version
make release VERSION=<correct-version>
```

### Failed Release

If a release fails:

1. Check git status: `git status`
2. Ensure all tests pass: `make test`
3. Fix any issues and retry
4. Contact maintainers if problems persist

## Future Improvements

- [ ] Automated changelog generation
- [ ] Release notes templates
- [ ] Beta/RC release support
- [ ] Container registry publishing
- [ ] Deployment automation
