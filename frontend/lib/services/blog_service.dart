import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../models/blog.dart';
import '../services/secure_storage_service.dart';
import 'dart:io';
import 'package:http_parser/http_parser.dart';

class BlogService {
  final SecureStorageService _secureStorageService = SecureStorageService();
  final String baseUrl = 'http://127.0.0.1:5000/materials';

  Future<List<Blog>> getBlogs() async {
    final token = await _secureStorageService.getToken();
    final response = await http.get(
      Uri.parse(baseUrl),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );
    if (response.statusCode == 200) {
      List<dynamic> blogsJson = json.decode(response.body);
      return blogsJson.map((json) => Blog.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load blogs');
    }
  }

  Future<Blog> addBlog(Blog blog) async {
    final token = await _secureStorageService.getToken();
    print("token:");
    print(token);
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/form-data',
        'Authorization': 'Bearer $token',
      },
      body: json.encode(blog.toJson()),
    );
    print(json.encode(blog.toJson()));
    if (response.statusCode == 201) {
      return Blog.fromJson(json.decode(response.body));
    } else {
      print(json.decode(response.body));
      throw Exception('Failed to add blog');
    }
  }

  Future<Blog> updateBlog(Blog blog) async {
    final token = await _secureStorageService.getToken();
    final response = await http.put(
      Uri.parse('$baseUrl/${blog.blogId}'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode(blog.toJson()),
    );
    if (response.statusCode == 200) {
      return Blog.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to update blog');
    }
  }

  Future<void> deleteBlog(int id) async {
    final token = await _secureStorageService.getToken();
    final response = await http.delete(
      Uri.parse(
        '$baseUrl/$id',
      ),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete blog');
    }
  }

  // 上传文件 -------------------------------------------------------------------------

  // Future<void> uploadFile(String? fileName, Uint8List? fileBytes) async {
  //   final token = await _secureStorageService.getToken();
  //   if (fileName == null || fileBytes == null) {
  //     print('No file selected');
  //     return;
  //   }

  //   var request = http.MultipartRequest('POST', Uri.parse(baseUrl))
  //     ..files.add(http.MultipartFile.fromBytes(
  //       'file',
  //       fileBytes,
  //       filename: fileName,
  //     ));

  //   final response = await http.post(
  //     Uri.parse(baseUrl),
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Authorization': 'Bearer $token',
  //     },
  //     // body: json.encode(.toJson()),
  //   );
  //   var response = await request.send();

  //   if (response.statusCode == 200) {
  //     print('File uploaded successfully');
  //   } else {
  //     print('File upload failed: ${response.statusCode}');
  //   }
  // }

  // Future<void> uploadFile(String? fileName, Uint8List? fileBytes) async {
  //   final token = await _secureStorageService.getToken();
  //   if (fileName == null || fileBytes == null) {
  //     print('No file selected');
  //     return;
  //   }

  //   var uri = Uri.parse(baseUrl);
  //   var request = http.MultipartRequest('POST', uri)
  //     ..headers['Authorization'] = 'Bearer $token'
  //     ..files.add(http.MultipartFile.fromBytes(
  //       'file',
  //       fileBytes,
  //       filename: fileName,
  //     ));

  //   // 如果有其他表单数据需要添加，可以使用 request.fields 来添加
  //   // 例如：request.fields['title'] = 'Your Title';

  //   var multipartResponse = await request.send();

  //   if (multipartResponse.statusCode == 200) {
  //     print('File uploaded successfully');
  //   } else {
  //     print('File upload failed: ${multipartResponse.statusCode}');
  //   }
  // }

  // Future<void> uploadFile(String? fileName, Uint8List? fileBytes, String title,
  //     String description, int moduleId, int tagId) async {
  //   final token = await _secureStorageService.getToken();
  //   if (fileName == null || fileBytes == null) {
  //     print('No file selected');
  //     return;
  //   }

  //   var uri = Uri.parse(baseUrl);
  //   var request = http.MultipartRequest('POST', uri)
  //     ..headers['Authorization'] = 'Bearer $token'
  //     ..fields['title'] = title
  //     ..fields['description'] = description
  //     ..fields['module_id'] = moduleId.toString()
  //     ..fields['tag_id'] = tagId.toString()
  //     ..files.add(http.MultipartFile.fromBytes(
  //       'file',
  //       fileBytes,
  //       filename: fileName,
  //     ));

  //   var multipartResponse = await request.send();

  //   if (multipartResponse.statusCode == 200) {
  //     print('File uploaded successfully');
  //   } else {
  //     print('File upload failed: ${multipartResponse.statusCode}');
  //   }
  // }

  Future<void> uploadFile(String? fileName, Uint8List? fileBytes, String title,
      String description, int moduleId, int tagId) async {
    final token = await _secureStorageService.getToken();
    if (fileName == null || fileBytes == null) {
      print('No file selected');
      return;
    }

    var request = http.MultipartRequest('POST', Uri.parse(baseUrl))
      ..headers['Authorization'] = 'Bearer $token'
      ..fields['title'] = title
      ..fields['description'] = description
      ..fields['module_id'] = moduleId.toString()
      ..fields['tag_id'] = tagId.toString()
      ..files.add(http.MultipartFile.fromBytes(
        'file',
        fileBytes,
        filename: fileName,
      ));

    // var response = await request.send();

    // if (response.statusCode == 200) {
    //   print('File uploaded successfully');
    // } else {
    //   response.stream.transform(utf8.decoder).listen((value) {
    //     print(value); // 打印出错误详情
    //   });
    //   print('File upload failed: ${response.statusCode}');
    // }

    try {
      var response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        // 处理成功响应
      } else {
        // 处理错误响应，不尝试解析 JSON
        print('Error from server: $responseBody');
      }
    } catch (e) {
      print('Error processing request: $e');
    }
  }



}
