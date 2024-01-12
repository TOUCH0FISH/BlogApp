import 'dart:typed_data';

import 'package:flutter/material.dart';
import '../models/blog.dart';
import '../services/blog_service.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';

class BlogForm extends StatefulWidget {
  final Blog? blog;
  final VoidCallback onBlogUpdated;

  BlogForm({this.blog, required this.onBlogUpdated});

  @override
  _BlogFormState createState() => _BlogFormState();
}

class _BlogFormState extends State<BlogForm> {
  final BlogService _blogService = BlogService();
  final _formKey = GlobalKey<FormState>();
  late String _title;
  late String _content;
  late String _description;
  late int _moduleId;
  late int _tagId;

  Uint8List? _pickedFileBytes;
  String? _pickedFileName;

  Future<void> _selectFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      setState(() {
        _pickedFileBytes = result.files.single.bytes;
        _pickedFileName = result.files.single.name;
      });
    } else {
      print('No file selected');
    }
  }

  @override
  void initState() {
    super.initState();
    _title = widget.blog?.title ?? '';
    _content = widget.blog?.content ?? '';
    _description = widget.blog?.description ?? '';
    _moduleId = widget.blog?.moduleId ?? 1;
    _tagId = widget.blog?.tagId ?? 1;
  }

  Future<void> _saveBlog() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      final Blog newBlog = Blog(
          title: _title,
          content: _content,
          createdAt: DateTime.now().toString(),
          description: _description,
          moduleId: _moduleId,
          tagId: _tagId,
          );

      print(newBlog);
      print("------------------");

      try {
        if (widget.blog == null) {
          print('Attempting to add blog');
          await _blogService.addBlog(newBlog);
          print('Blog added');
        } else {
          print('Attempting to update blog');
          await _blogService.updateBlog(newBlog);
          print('Blog updated');
        }
        widget.onBlogUpdated();
      } catch (e) {
        print('Error saving blog: $e');
      }

      // if (widget.blog == null) {
      //   _blogService.addBlog(newBlog).then((_) => widget.onBlogUpdated());
      // } else {
      //   _blogService.updateBlog(newBlog).then((_) => widget.onBlogUpdated());
      // }
    }
  }

  // 上传文件
  Future<File?> _pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      return File(result.files.single.path!); // 如果有选择文件，则返回文件对象
    } else {
      // 用户取消了文件选择
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.blog == null ? 'Add Blog' : 'Edit Blog'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: <Widget>[
                TextFormField(
                  initialValue: _title,
                  decoration: InputDecoration(labelText: 'Title'),
                  onSaved: (value) => _title = value ?? '',
                  validator: (value) =>
                      value!.isEmpty ? 'Please enter a title' : null,
                ),
                TextFormField(
                  initialValue: _content,
                  decoration: InputDecoration(labelText: 'Content'),
                  onSaved: (value) => _content = value ?? '',
                  validator: (value) =>
                      value!.isEmpty ? 'Please enter content' : null,
                ),
                TextFormField(
                  initialValue: _description,
                  decoration: InputDecoration(labelText: 'Description'),
                  onSaved: (value) => _content = value ?? '',
                  validator: (value) =>
                      value!.isEmpty ? 'Please enter description' : null,
                ),
                TextFormField(
                initialValue: _moduleId.toString(),
                decoration: InputDecoration(labelText: 'Module ID'),
                onSaved: (value) => _moduleId = int.tryParse(value!) ?? _moduleId,
                validator: (value) => value!.isEmpty ? 'Please enter module ID' : null,
                keyboardType: TextInputType.number,
              ),
              TextFormField(
                initialValue: _tagId.toString(),
                decoration: InputDecoration(labelText: 'Tag ID'),
                onSaved: (value) => _tagId = int.tryParse(value!) ?? _tagId,
                validator: (value) => value!.isEmpty ? 'Please enter tag ID' : null,
                keyboardType: TextInputType.number,
              ),
                ElevatedButton(
                  onPressed: _saveBlog,
                  child: Text('Save Blog'),
                ),
                if (_pickedFileName != null)
                  Text('Selected file: $_pickedFileName'),
                ElevatedButton(
                  onPressed: _selectFile,
                  child: Text('Select File'),
                ),
                ElevatedButton(
                  // onPressed: () {
                  //   _blogService.uploadFile(_pickedFileName, _pickedFileBytes);
                  // },
                  onPressed: () {
                    if (_pickedFileName != null && _pickedFileBytes != null) {
                      // 假设以下变量包含必要的信息
                      String title = '示例标题';
                      String description = '示例描述';
                      int moduleId = 2;
                      int tagId = 1;
                      // testing
                      print('Uploading file with module ID: $moduleId');
                      // testing
                      _blogService.uploadFile(_pickedFileName, _pickedFileBytes,
                          title, description, moduleId, tagId);
                    } else {
                      print('No file selected');
                    }
                  },

                  child: Text('Upload File'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
