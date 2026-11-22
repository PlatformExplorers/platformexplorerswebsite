import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_blog', ROOT / 'tools/build_blog.py')
blog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blog)


class BlogBuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        shutil.copy2(ROOT / 'contribution.md', self.site / 'contribution.md')
        shutil.copytree(ROOT / '_blog/templates', self.site / '_blog/templates')
        (self.site / '_blog/posts').mkdir()
        (self.site / '_blog/authors').mkdir()
        (self.site / 'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://platformexplorers.com/</loc></url></urlset>')
        self.profile = self.site / '_blog/authors/test-author.yml'
        self.profile.write_text('name: Test Author\nbio: A contributor biography.\n')
        self.post = self.site / '_blog/posts/test-post.md'
        template = (ROOT / '_blog/templates/post-template.md').read_text(encoding='utf-8')
        self.content = template.split('\n---\n', 1)[0] + '\n---\n\n## A useful example\n\nHello community.\n'
        self.content = self.content.replace('Your full name','Test Author').replace('your-name','test-author').replace('your-article-title','test-post').replace('draft: true','draft: false')
        self.post.write_text(self.content, encoding='utf-8')

    def test_generated_pages_and_author_and_idempotence(self):
        self.assertEqual(blog.build(self.site), 1)
        page = self.site / 'blog/test-post/index.html'
        output = page.read_text(encoding='utf-8')
        self.assertIn('Written by', output)
        self.assertIn('About the author', output)
        self.assertIn('A contributor biography.', output)
        self.assertIn('BlogPosting', output)
        self.assertIn('/blog/test-post/', (self.site / 'blog.html').read_text(encoding='utf-8'))
        self.assertIn('/blog/test-post/', (self.site / 'sitemap.xml').read_text())
        stamp = page.stat().st_mtime_ns
        blog.build(self.site)
        self.assertEqual(stamp, page.stat().st_mtime_ns)

    def test_draft_and_deleted_post_cleanup(self):
        blog.build(self.site)
        self.post.write_text(self.content.replace('draft: false','draft: true'))
        self.assertEqual(blog.build(self.site), 0)
        self.assertFalse((self.site / 'blog/test-post/index.html').exists())
        self.post.unlink()
        blog.build(self.site)
        self.assertNotIn('/blog/test-post/', (self.site / 'sitemap.xml').read_text())

    def test_missing_author_blocks_build(self):
        self.profile.unlink()
        with self.assertRaisesRegex(ValueError, 'add author profile'):
            blog.build(self.site)

    def test_invalid_metadata(self):
        for before, after, error in [('slug: "test-post"','slug: "../bad"','slug'), ('lastModified: "2026-11-22"','lastModified: "2020-01-01"','before date'), ('draft: false','draft: "false"','true or false')]:
            with self.subTest(error=error):
                self.post.write_text(self.content.replace(before, after))
                with self.assertRaisesRegex(ValueError, error):
                    blog.build(self.site)

    def test_duplicate_slug_and_metadata(self):
        other = self.post.with_name('another.md')
        other.write_text(self.content)
        with self.assertRaisesRegex(ValueError, 'Duplicate slug'):
            blog.build(self.site)
        other.unlink()
        self.post.write_text(self.content.replace('featured: false','featured: false\nfeatured: true'))
        with self.assertRaisesRegex(ValueError, 'Duplicate metadata'):
            blog.build(self.site)

    def test_escape_html_and_unsafe_links(self):
        self.post.write_text(self.content+'\n<script>alert(1)</script>\n\n[bad](javascript:alert(1))\n')
        blog.build(self.site)
        output = (self.site / 'blog/test-post/index.html').read_text(encoding='utf-8')
        self.assertNotIn('<script>alert', output)
        self.assertNotIn('href="javascript:', output)

    def test_missing_image_blocks_build(self):
        self.post.write_text(self.content.replace('image: ""', 'image: "/assets/blog/missing.webp"'))
        with self.assertRaisesRegex(ValueError, 'Image not found'):
            blog.build(self.site)


    def make_folder_post(self):
        folder = self.site / 'blog/test-post'
        folder.mkdir(parents=True)
        self.post = self.post.rename(folder / 'index.md')
        (folder / 'images').mkdir()
        (folder / 'images/cover.webp').write_bytes(b'image fixture')
        return folder

    def test_article_folder_relative_cover_and_inline_images(self):
        self.make_folder_post()
        content = self.content.replace('image: ""', 'image: "./images/cover.webp"').replace('imageAlt: ""', 'imageAlt: "A useful cover"')
        self.post.write_text(content + '\n![An inline example](./images/cover.webp)\n')
        self.assertEqual(blog.build(self.site), 1)
        article = (self.post.parent / 'index.html').read_text(encoding='utf-8')
        listing = (self.site / 'blog.html').read_text(encoding='utf-8')
        self.assertIn('src="/blog/test-post/images/cover.webp"', article)
        self.assertIn('alt="An inline example"', article)
        self.assertNotIn('src="./images/', article)
        self.assertIn('src="/blog/test-post/images/cover.webp"', listing)

    def test_folder_name_must_match_slug(self):
        folder = self.make_folder_post()
        folder.rename(folder.with_name('wrong-folder'))
        with self.assertRaisesRegex(ValueError, 'folder and slug match'):
            blog.build(self.site)

    def test_folder_image_traversal_rejected(self):
        folder = self.make_folder_post()
        (folder / 'outside.webp').write_bytes(b'outside images')
        self.post.write_text(self.content + '\n![Example](./images/../outside.webp)\n')
        with self.assertRaisesRegex(ValueError, 'outside its images folder'):
            blog.build(self.site)

    def test_draft_preserves_markdown_and_images(self):
        folder = self.make_folder_post()
        blog.build(self.site)
        self.post.write_text(self.content.replace('draft: false', 'draft: true'))
        blog.build(self.site)
        self.assertFalse((folder / 'index.html').exists())
        self.assertTrue(self.post.is_file())
        self.assertTrue((folder / 'images/cover.webp').is_file())


    def test_contribution_page_and_blog_links(self):
        blog.build(self.site)
        guide = (self.site / 'contribute.html').read_text(encoding='utf-8')
        self.assertIn('id="option-a-contribute-using-vs-code"', guide)
        self.assertIn('id="option-b-contribute-directly-on-github"', guide)
        self.assertIn('/blob/main/_blog/templates/post-template.md', guide)
        self.assertNotIn('Maintainer notes', guide)
        self.assertIn('<pre><code class="language-shell">git clone ', guide)
        self.assertIn('<pre><code class="language-shell">git switch -c ', guide)
        self.assertIn('<ol start="5">', guide)
        for name in ('blog.html', 'blog/test-post/index.html'):
            self.assertIn('href="/contribute.html">Contribute a blog', (self.site / name).read_text(encoding='utf-8'))
        sitemap = (self.site / 'sitemap.xml').read_text()
        self.assertEqual(sitemap.count('https://platformexplorers.com/contribute.html'), 1)
        blog.build(self.site)
        self.assertEqual((self.site / 'sitemap.xml').read_text().count('https://platformexplorers.com/contribute.html'), 1)


if __name__ == '__main__':
    unittest.main()
