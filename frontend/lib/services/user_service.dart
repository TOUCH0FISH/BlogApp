import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/user.dart';
import '../services/secure_storage_service.dart';

class UserService {
  final SecureStorageService _secureStorageService = SecureStorageService();
  static const String baseUrl = 'http://127.0.0.1:5000/users';

  Future<List<User>> getUsers() async {
    final token = await _secureStorageService.getToken();
    final response = await http.get(
      Uri.parse(baseUrl),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data is List) {
        return data.map<User>((json) => User.fromJson(json)).toList();
      } else if (data is Map && data.containsKey('users')) {
        final usersList = data['users'] as List;
        return usersList.map<User>((json) => User.fromJson(json)).toList();
      } else {
        throw Exception('Unexpected JSON format');
      }
    } else {
      throw Exception('Failed to load users');
    }
  }

  Future<User> getUser(int userId) async {
    final token = await _secureStorageService.getToken();
    final response = await http.get(
      Uri.parse('$baseUrl/$userId'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data != null && data is Map<String, dynamic>) {
        final userData = data['user'];
        if (userData != null && userData is Map<String, dynamic>) {
          return User.fromJson(userData);
        } else {
          throw Exception('Invalid user data');
        }
      } else {
        throw Exception('Invalid response data');
      }
    } else {
      throw Exception('Failed to load user');
    }
  }

  Future<void> createUser(User user) async {
    final token = await _secureStorageService.getToken();
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to create user');
    }
  }

  Future<void> updateUser(User user) async {
    final token = await _secureStorageService.getToken();
    final response = await http.put(
      Uri.parse('$baseUrl/${user.userId}'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update user');
    }
  }

  Future<void> deleteUser(int userId) async {
    final token = await _secureStorageService.getToken();
    final response = await http.delete(
      Uri.parse('$baseUrl/$userId'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to delete user');
    }
  }
}
