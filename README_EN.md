# 🕒 GitHub Commit Time Stats

[한국어](README.md) | [English](README_EN.md)

A tool that analyzes your GitHub commit patterns and beautifully displays them in your profile README.

![Example](./스크린샷.png)

> 🤖 This project was created with the help of Claude AI.

## 🚀 Installation

1. **Fork this repository**
   - Click the `Fork` button in the top-right corner
   - The repository will be copied to your account

2. **Create GitHub Personal Access Token**
   - Go to [GitHub Settings](https://github.com/settings/tokens)
   - Select `Generate new token (classic)`
   - Note: `GT_TOKEN` (or any name you prefer)
   - Expiration: Choose your preferred duration
   - Scopes:
     - ✓ `repo` (select all)
   - Click `Generate token` and copy the generated token

3. **Repository Setup**
   - Go to `Settings` → `Secrets and variables` → `Actions` in your forked repository
   - Click `New repository secret`
   - Name: `GT_TOKEN`
   - Value: Paste your token
   - Click `Add secret`

4. **Prepare GitHub Profile README**
   - Create your GitHub profile README repository if you don't have one
     - Create a new repository with the same name as your GitHub username
     - Example: `username/username`
     (Replace `{username}` with your GitHub username)

## ⚙️ How It Works

- Statistics are automatically updated daily at midnight
- Stats are displayed below the hits badge in your GitHub profile README
- To update manually:
  1. Go to the `Actions` tab in your forked repository
  2. Select the `Update Stats` workflow
  3. Click `Run workflow`

## ❓ Troubleshooting

- **If stats are not updating**
  - Check if GitHub Actions is running properly
  - Verify that your Personal Access Token hasn't expired
  
- **If the image is not displaying**
  - Check if the username in the image URL is correct
  - Verify the repository name

## 📝 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Bug reports, feature suggestions, and pull requests are welcome!

## 👏 Acknowledgments

This project uses GitHub API and GitHub Actions. 