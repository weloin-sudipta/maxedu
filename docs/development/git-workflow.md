# Git Workflow

A consistent Git workflow ensures smooth collaboration and code quality.

## 1. Branching Strategy
- **`main`**: The production-ready branch.
- **`develop`**: The integration branch for new features.
- **`feature/`**: Individual feature branches (e.g., `feature/library-recommendations`).
- **`bugfix/`**: Fixes for existing issues (e.g., `bugfix/issue-renewal-fix`).

## 2. Commit Guidelines
- **Commit Messages**: Use the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat: add book renewal API`).
- **Granular Commits**: Commit small, logical chunks of work to make reviews easier.

## 3. Pull Request Process
1. **Create Branch**: `git checkout -b feature/my-new-feature`.
2. **Commit Changes**: `git commit -m "feat: my change"`.
3. **Push Branch**: `git push origin feature/my-new-feature`.
4. **Open PR**: Submit a pull request to the `develop` branch.
5. **Code Review**: Address feedback and iterate.
6. **Merge**: Merge the PR once approved and tests pass.

A disciplined Git workflow is the foundation of a stable and predictable development process.
