# Unified Versioning Strategy

Data Contracts Studio uses a **unified versioning approach** where both frontend and backend share the same version number. This simplifies release management and avoids version mismatches.

## Version Format

We follow [Semantic Versioning (SemVer)](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Current Version

**v0.0.3** (Latest Release)

## Version Sources

The version is maintained in several files but synchronized through our release process:

1. **`VERSION`** - Master version file (source of truth)
2. **`package.json`** - Root package version
3. **`frontend/package.json`** - Frontend package version
4. **`frontend/src/version.ts`** - Runtime frontend version
5. **`backend/app/__version__.py`** - Backend module version
6. **`backend/app/core/config.py`** - Backend API version

## Commands

### Check Version Consistency
```bash
make version-check
# or directly:
./scripts/check-version-sync.sh
```

### View Current Versions
```bash
make version
```

### Create New Release
```bash
make release VERSION=0.0.4
# or directly:
./scripts/release.sh 0.0.4
```

## Release Process

The release script (`scripts/release.sh`) automatically:

1. ✅ Validates version format (semantic versioning)
2. ✅ Checks version consistency across all files
3. ✅ Runs tests and linting
4. ✅ Updates all version files synchronously
5. ✅ Creates git commit and tag
6. ✅ Provides next steps for deployment

## Best Practices

- **Always use the release script** - Never manually update version files
- **Check version sync** - Run `make version-check` before releases
- **Follow semantic versioning** - Use MAJOR.MINOR.PATCH format
- **Test before release** - The script runs tests automatically

## Version Mismatch Prevention

The system now includes:
- Pre-release version consistency checks
- Automated synchronization of all version files
- Clear error messages when versions are out of sync
- Easy-to-use commands for version management

This approach ensures that frontend and backend versions are always aligned, eliminating the "Frontend/Backend version mismatch" warning.
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
