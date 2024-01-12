import 'crud_model.dart';

class User implements CrudModel {
  final int? userId;
  final String username;
  final String role;
  final String? password;

  User(
      {this.userId, required this.username, required this.role, this.password});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      userId: json['user_id'],
      username: json['username'],
      role: json['role'],
    );
  }

  @override
  String getId() {
    return userId.toString();
  }

  @override
  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = {
      'username': username,
      'role': role,
    };

    if (userId != null) {
      data['user_id'] = userId;
    }

    if (password != null) {
      data['password'] = password;
    }

    return data;
  }
}
