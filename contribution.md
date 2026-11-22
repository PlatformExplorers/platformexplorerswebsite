# Contribute a blog to Platform Explorers

We welcome practical guides, project stories and experiences from our community.
You can contribute using **VS Code on your computer** or **GitHub in your browser**.
Both methods use a fork, a separate branch and a pull request for team review.

A **fork** is your copy of this repository. A **branch** keeps your article's edits
together. A **pull request (PR)** asks the Platform Explorers team to review those
edits and add them to the website.

## What you need

For either method:

- A free [GitHub account](https://github.com/signup).
- Your article, a title, a short summary and your author bio for your first post.
- Any images you want to use, with permission to publish them and descriptive alt text.

For the VS Code method, install these if you don’t already have them:

- [Git](https://git-scm.com/downloads).
- [Visual Studio Code](https://code.visualstudio.com/).

After installing Git, close and reopen VS Code so its terminal can find Git.
The GitHub-only method needs no local software installation.

## Where your files go

Start from the main repository folder. Replace `your-article-title` and
`your-name` with your own names.

| What you are adding | Where to save it |
| --- | --- |
| Your article | `blog/your-article-title/index.md` |
| Cover image, if used | `blog/your-article-title/images/cover.webp` |
| Screenshots or other article images | `blog/your-article-title/images/` |
| Your author profile (first contribution only) | `_blog/authors/your-name.yml` |

Copy the article template from
[`_blog/templates/post-template.md`](_blog/templates/post-template.md).
For your first contribution, also copy the
[author template](_blog/templates/author-template.yml).

The build updates `blog.html` automatically when articles are published.

Create one folder in `blog/` for your article. Its name must match the post's
`slug`, using lowercase words separated by hyphens. For example,
`blog/my-first-automation/index.md` uses `slug: "my-first-automation"`.
The public URL will be `https://platformexplorers.com/blog/my-first-automation/`.

Put your article text in `index.md` and its images in that article's `images/`
folder. You do not need an images folder if the article has no images. Do not edit
`blog.html` or the generated `index.html` inside an article folder.

## Option A: contribute using VS Code

### 1. Fork the repository

1. Sign in to GitHub and open
   [PlatformExplorers/platformexplorerswebsite](https://github.com/PlatformExplorers/platformexplorerswebsite).
2. Select **Fork**, choose your own account and select **Create fork**.
3. Your fork should have an address like
   `https://github.com/YOUR-USERNAME/platformexplorerswebsite`.

If you already have a fork, open it, select **Sync fork**, then **Update branch**
before starting a new contribution.

### 2. Copy your fork to your computer

1. In **your fork** on GitHub, select **Code**, then **HTTPS**, and copy the URL.
2. Open **Visual Studio Code**.
3. In the top menu, select **Terminal > New Terminal**. A terminal opens at the
   bottom of VS Code.
4. Type `git clone`, add a space, paste the URL you copied, then press **Enter**.
   Your command should look like this, with your own GitHub username:

   ```shell
   git clone https://github.com/YOUR-USERNAME/platformexplorerswebsite.git
   ```

5. Wait for the download to finish. Git creates a folder called
   `platformexplorerswebsite` in the location shown in your terminal. If you need
   the full location, type `pwd` and press **Enter**. Your new folder is inside
   the location it prints.
6. Select **File > Open Folder**. Find and open that new `platformexplorerswebsite`
   folder. You should now see the website files in VS Code's Explorer on the left.

### 3. Create a branch for your article

1. Select **Terminal > New Terminal** in the project you just opened.
2. Type the command below and press **Enter**:

   ```shell
   git switch -c blog/my-first-automation
   ```

3. This creates a separate branch for your article and switches you to it.
   Use your own article name in place of `my-first-automation`. Use that same
   name in the folder and commands below.

### 4. Create your article folder and Markdown file

1. In VS Code's Explorer, right-click `blog` and select **New Folder**.
2. Name it `my-first-automation` (replace this with your own slug).
3. Inside it, create an `images` folder if you have images. Drag your images into it.
4. Open `_blog/templates/post-template.md` in the Explorer and copy its contents.
5. Right-click your article folder, select **New File**, name it `index.md` and
   paste the template into it.
6. Replace the template's metadata and example content with your own article.
   See **Article metadata and images** below.

### 5. Add your author profile

1. Open `_blog/templates/author-template.yml` in the Explorer and copy its contents.
2. Right-click `_blog/authors`, select **New File**, and name it `your-name.yml`.
   Replace `your-name` with your name in lowercase, with hyphens instead of spaces.
3. Paste the template and fill in your full name and a short bio.
4. In your article, set `authorId` to that filename without `.yml`. Set `author`
   to the exact name in your profile.

Do this for your first contribution only. For later articles, reuse your existing
profile. See **Your author profile** below for an example.

### 6. Check your article

1. Save your files using **File > Save All**.
2. Open your article's `index.md` file.
3. Select the **Open Preview to the Side** icon at the top-right of the editor.
   It opens a formatted preview beside your Markdown.
4. Read through your article. Check the headings, links, spelling and images.
5. Set `draft: false` in the metadata when your article is ready for review.
   Keep `draft: true` if you are still working on it.

This preview shows your Markdown formatting. The website adds its own design,
the title, the byline and your author bio when the article is built.

### 7. Save your changes to GitHub

In the VS Code terminal, run each command below separately. Press **Enter** after
each command and wait for it to finish. Replace the example article and author
names with your own.

First, select your article folder and its images:

```shell
git add blog/my-first-automation/
```

Select your author profile too, if you created or changed it:

```shell
git add _blog/authors/your-name.yml
```

Save these changes with a short message:

```shell
git commit -m "Blog: add my first automation article"
```

Upload your branch to your fork on GitHub:

```shell
git push -u origin blog/my-first-automation
```

Sign in to GitHub if asked. Wait for the upload to finish, then open your fork
in your browser. Your article branch and files should now be there.

If Git asks for your name and email before it can commit, run these commands with
your own details, then retry the `git commit` command:

```shell
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
```

Use an email connected to your GitHub account, or the no-reply email shown in
your GitHub email settings. These details are attached to your commits.

### 8. Create your pull request

Follow **Open a pull request** below. Pushing to your fork alone does not submit
the article to Platform Explorers.

## Option B: contribute directly on GitHub

### 1. Fork and create a branch

1. Sign in and [fork the repository](https://github.com/PlatformExplorers/platformexplorerswebsite/fork).
   If you already have a fork, sync its `main` branch first.
2. In **your fork**, open the branch dropdown that currently says `main`.
3. Enter `blog/my-first-automation`, then choose the option to create that branch
   from `main`. Use your own article name.
4. Check that this branch is selected before adding files. Stay on it throughout
   your contribution.

### 2. Create the article folder and Markdown file

1. Open [`_blog/templates/post-template.md`](_blog/templates/post-template.md)
   in another tab and copy its contents.
2. Return to the root of **your fork**, on your new branch.
3. Select **Add file → Create new file**.
4. In the filename field, enter `blog/my-first-automation/index.md`.
   GitHub creates the folders when you type the `/` characters.
5. Paste the template, replace the metadata and write your article.
6. Use **Preview** to check the Markdown formatting.
7. Select **Commit changes**, enter a clear message and commit to your article
   branch. Do not create a different branch for each file.

### 3. Upload your images

Skip this step if your article has no images.

1. Open your new `blog/my-first-automation/` folder in your fork.
2. To create its images folder, use **Add file → Create new file**, enter
   `images/.gitkeep` and commit this empty placeholder to the same branch.
3. Open `images/`, select **Add file → Upload files**, then drag in your images.
4. Commit the upload to the same branch. You can leave `.gitkeep` in the folder;
   it does not appear in your article.
5. Back in `index.md`, use `./images/filename.webp` for both the cover and inline
   images. See the examples below.

### 4. Add your author profile (first contribution only)

1. Copy [`_blog/templates/author-template.yml`](_blog/templates/author-template.yml).
2. At your fork's root, use **Add file → Create new file** and enter
   `_blog/authors/your-name.yml`.
3. Paste the template, fill in your name and bio, and commit to the same article branch.
4. Check `author` in `index.md` matches your profile's `name`, and `authorId`
   matches the profile filename without `.yml`.

You can edit any file again using its pencil/edit button, then commit the changes
to this same branch. No terminal, local clone or Python installation is needed.

## Your author profile

Complete this once, on your first contribution:

```yaml
name: "Your full name"
bio: "Two or three sentences about your work, interests and experience with your topic."
image: ""
website: ""
```

Save it as `_blog/authors/your-name.yml`. In the article, use:

```yaml
author: "Your full name"
authorId: "your-name"
```

The website adds **Written by** near the top of your article and **About the author**
with your bio at the end. Reuse the same `authorId` for future posts. You may update
your profile in a later PR. A public HTTPS profile link and portrait are optional.
For a reusable portrait, upload it to `assets/blog/` and use, for example,
`image: "/assets/blog/your-name.webp"`. Leave optional fields empty to omit them.
Only include information you want to appear publicly.

## Article metadata and images

Keep the metadata between the two `---` lines at the start of `index.md`.
Set `slug` to the article folder name. These must match. For a local image:

```yaml
slug: "my-first-automation"
image: "./images/cover.webp"
imageAlt: "Describe what the cover image shows"
```

To insert an image in the article body:

```markdown
![Describe what the reader needs to know](./images/example-screenshot.png)
```

Use lowercase, hyphenated filenames. Supported image formats are JPG, JPEG, PNG,
WebP and GIF; aim for under 500 KB per image. Keep image paths inside your article's
`images/` folder. Do not use paths from your computer such as `C:\Users\...`.
If you do not need a cover, keep `image: ""` and `imageAlt: ""`.

| Field | What to enter |
| --- | --- |
| `title` | The visible article headline. |
| `slug` | Unique lowercase words separated by hyphens. Becomes `/blog/your-slug/`. Keep it unchanged after publication so existing links keep working. |
| `author` | Your full name, exactly as it appears in your author profile. |
| `authorId` | Your profile filename without `.yml`, for example `rachel-irabor`. |
| `date` | Original publication date in quoted `YYYY-MM-DD` format. |
| `lastModified` | Date of the latest edit, on or after `date`. |
| `description` | Short introduction displayed at the top of the article. |
| `excerpt` | Summary displayed on the blog listing. |
| `category` | One clear topic, such as Automation, Career or Community. |
| `tags` | A list such as `["Power Automate", "SharePoint"]`. |
| `featured` | `true` to show a Featured label; otherwise `false`. |
| `draft` | `true` hides the post from the public site. Set `false` when ready for review and publication. |
| `image` | Optional cover image, e.g. `./images/cover.webp`. Leave `""` to omit. |
| `imageAlt` | Describe the cover image for readers who cannot see it. Required when an image is supplied. |
| `seoTitle` | Search and browser title, usually your headline plus Platform Explorers. |
| `seoDescription` | A concise, accurate summary for search engines and shared links. |

Write sections with `## Heading` and subsections with `### Heading`. Do not repeat
the article title, byline or author bio in the body; the website adds them.
Use descriptive links, readable paragraphs, lists and fenced code blocks where
helpful. Use Markdown rather than raw HTML. Scripts, iframes, forms and unsafe
links are removed during the build.

Credit sources and any images that require attribution. Check facts and links,
and remove credentials or private information from examples and screenshots.

## Open a pull request (both methods)

1. Open **your fork** on GitHub and choose your article branch.
2. Select **Contribute → Open pull request** or **Compare & pull request**.
   If neither appears, use **Pull requests → New pull request → compare across forks**.
3. Confirm these settings:

    | Setting | Value |
    | --- | --- |
    | Base repository | `PlatformExplorers/platformexplorerswebsite` |
    | Base branch | `main` |
    | Head repository | Your fork |
    | Compare branch | `blog/my-first-automation` (your article branch) |

4. Review the files shown in the comparison. Include your article, its images
   and your author profile if new or changed. Do not include unrelated changes.
5. Add a title such as `Blog: My first automation` and a short description.
6. Complete the PR checklist. Confirm `draft: false` for a ready article, or keep
   `draft: true` and create a draft PR if you still want feedback.
7. Select **Create pull request**. A Platform Explorers maintainer will review it.

Watch the PR's checks and comments. If a check fails, open its build log and find
the filename and error. Fix the file on **the same branch** in VS Code or GitHub,
commit and push/save. The existing PR updates automatically; do not open another.
If this is your first contribution, a maintainer may need to approve the automated
checks before they run.

Opening a PR does not publish your article. After a maintainer approves and merges
a ready post, the build creates its HTML page, updates `blog.html` and the sitemap,
and deploys the website. A draft remains hidden. Keep an existing post's slug
unchanged so its published links continue working.

## Before you submit

- [ ] My article is `blog/my-article/index.md` and the folder matches its `slug`.
- [ ] I used the post template and filled in every required metadata field.
- [ ] I added or reused an author profile with a publication-ready bio.
- [ ] My images are in my article's `images/` folder, with working paths and alt text.
- [ ] I have permission to publish the content and images, and credited sources.
- [ ] I checked formatting, links and private information.
- [ ] I set `draft` correctly and included only the intended files in my PR.

## Further help

- [VS Code: cloning repositories](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes)
- [VS Code: branches and publishing a branch](https://code.visualstudio.com/docs/sourcecontrol/branches-worktrees)
- [GitHub: opening a pull request from a fork](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork)

## Maintainer notes

- On the owner's local project, this repository content lives in `dist/`; run
  `python -m pip install -r dist/requirements-blog.txt` once, then `python dev.py --open`.
  The live preview automatically rebuilds Markdown and refreshes the browser.
- The root of the GitHub repository corresponds to the **contents** of `dist/`.
  Publish the source folders, templates, requirements, tests and `.github/` too.
- At the first approved publication, set repository **Settings → Pages → Build
  and deployment → Source → GitHub Actions**. Keep the custom domain
  `platformexplorers.com` and HTTPS. The workflow preserves `CNAME` and `.nojekyll`.
- Make the `build` job a required PR check in branch protection if desired.
  Keep reviews required before merging. Fork PR builds have read-only permission
  and do not receive deployment credentials.
- The workflow builds a clean public artifact excluding Markdown sources,
  tools and tests. Generated pages do not need a bot commit back to the repository.
- Shared blog HTML is in `_blog/templates/page.html` and `article.html`.
  `blog.css` controls the blog design. Apply shared header/footer changes in the
  page template too. `tools/build_blog.py` rebuilds the listing, posts and sitemap.
- Removing a post or returning it to draft removes only its previously generated
  page on the next build. `date` is metadata, **not** a publishing schedule;
  use `draft: true` to keep a post unpublished.
- Never merge a ready post until its author bio, rights, links and content have
  been reviewed. No application data or private information belongs in this repo.
