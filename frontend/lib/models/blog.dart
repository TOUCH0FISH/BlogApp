import 'crud_model.dart';

class Blog implements CrudModel {
  final int? blogId;
  final String title;
  final String content;
  final String createdAt;
  final String description;
  final int moduleId;
  final int tagId;

  Blog({
    this.blogId,
    required this.title,
    required this.content,
    required this.createdAt,
    required this.description,
    required this.moduleId,
    required this.tagId,
  });

  factory Blog.fromJson(Map<String, dynamic> json) {
    return Blog(
      blogId: json['blog_id'],
      title: json['title'],
      content: json['content'],
      createdAt: json['created_at'],
      description: json['description'],
      moduleId: json['module_id'],
      tagId: json['tag_id'],
    );
  }

  @override
  String getId() {
    return blogId.toString();
  }

  @override
  Map<String, dynamic> toJson() {
    return {
      'blog_id': blogId,
      'title': title,
      'content': content,
      'created_at': createdAt,
      'description': description,
      'module_id': moduleId,
      'tag_id': tagId,
    };
  }
}
