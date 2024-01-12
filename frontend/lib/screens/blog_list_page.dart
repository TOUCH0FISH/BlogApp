import 'package:flutter/material.dart';
import '../models/blog.dart';
import '../services/blog_service.dart';
import '../widgets/blog_form.dart';

class BlogListPage extends StatefulWidget {
  @override
  _BlogListPageState createState() => _BlogListPageState();
}

class _BlogListPageState extends State<BlogListPage> {
  final BlogService _blogService = BlogService();
  List<Blog> _blogs = [];

  @override
  void initState() {
    super.initState();
    _loadBlogs();
  }

  _loadBlogs() async {
    _blogs = await _blogService.getBlogs();
    setState(() {});
  }

  _addOrUpdateBlog(Blog? blog) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => BlogForm(blog: blog, onBlogUpdated: _loadBlogs)),
    );
    if (result != null) {
      _loadBlogs();
    }
  }

  _deleteBlog(int blogId) async {
    await _blogService.deleteBlog(blogId);
    _loadBlogs();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Blogs')),
      body: ListView.builder(
        itemCount: _blogs.length,
        itemBuilder: (context, index) {
          final blog = _blogs[index];
          return ListTile(
            title: Text(blog.title),
            subtitle: Text(blog.content),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: <Widget>[
                IconButton(
                  icon: Icon(Icons.edit),
                  onPressed: () => _addOrUpdateBlog(blog),
                ),
                IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => _deleteBlog(blog.blogId!),
                ),
              ],
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () => _addOrUpdateBlog(null),
      ),
    );
  }
}
